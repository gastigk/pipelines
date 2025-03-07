"""
title: Filtro de Contenido Inapropiado para Ambiente Profesional
author: Gastón Guevara
date: 07-03-2025
version: 1.0
license: MIT
description: Pipeline especializado para filtrar contenido inapropiado, insultos, amenazas y lenguaje no ético en un ambiente profesional.
            Diseñado específicamente para mantener los estándares éticos y profesionales de COELSA, 
            con manejo de respuestas en español y referencias al Código de Ética institucional.
requirements: detoxify>=0.5.0
"""

from typing import List, Optional, Dict, Union, Any
from schemas import OpenAIChatMessage
from pydantic import BaseModel
from detoxify import Detoxify
import os
import logging
import json
import traceback
import numpy as np
from functools import wraps

def safe_json_serialize(obj):
    """Convierte objetos numpy a tipos Python nativos."""
    if isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f'Object of type {type(obj)} is not JSON serializable')

class ToxicityThresholds(BaseModel):
    toxicity: float = 0.5
    severe_toxicity: float = 0.1
    obscene: float = 0.15
    threat: float = 0.1
    insult: float = 0.15
    identity_attack: float = 0.1
    sexual_explicit: float = 0.15

class Valves(BaseModel):
    pipelines: List[str] = ["*"]
    priority: int = 1

class Pipeline:
    def __init__(self):
        self.type = "filter"
        self.name = "Filtro Detoxify Profesional"
        self.valves = Valves()
        self.model = None
        self.thresholds = ToxicityThresholds()
        
        # Configuración del logging
        self.logger = logging.getLogger("detoxify_filter_pipeline")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("toxicity_filter.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def create_response_dict(self, message: str) -> dict:
        """Crea un diccionario de respuesta con la estructura correcta."""
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": message
                    },
                    "finish_reason": "stop",
                    "index": 0
                }
            ]
        }

    def get_professional_response(self, toxicity_scores: Dict[str, float]) -> str:
        """Genera una respuesta profesional en español."""
        try:
            linea_etica = "Para más información o consultas sobre conductas éticas, por favor contacte a la Línea de Ética de COELSA o consulte el Código de Ética institucional."
            
            # Mensaje base para cualquier tipo de toxicidad
            base_response = "Le recordamos que este es un espacio profesional que requiere un trato respetuoso y ético. " + linea_etica
            
            # Si hay toxicidad severa o insultos, usamos una respuesta más firme
            if toxicity_scores.get("severe_toxicity", 0) > 0.1 or toxicity_scores.get("insult", 0) > 0.15:
                return f"No se permite el uso de lenguaje agresivo o insultos en este entorno profesional. {base_response}"
            
            return base_response
            
        except Exception as e:
            self.logger.error(f"Error en get_professional_response: {str(e)}")
            return "Por favor, mantenga una comunicación profesional y respetuosa."

    def analyze_toxicity(self, text: str) -> Dict[str, float]:
        """Analiza el texto en busca de contenido inapropiado."""
        try:
            if not text or not isinstance(text, str):
                return {}
                
            # self.logger.debug(f"Analizando texto: {text}")
            results = self.model.predict(text)
            
            # Convertir resultados numpy a tipos Python nativos
            scores = {}
            for k, v in results.items():
                if isinstance(v, (np.floating, np.integer)):
                    scores[k] = float(v)
                else:
                    scores[k] = v
            
            # Verificar que los scores sean serializables
            try:
                json.dumps(scores, default=safe_json_serialize)
                # self.logger.debug(f"Scores de toxicidad: {scores}")
                return scores
            except TypeError as e:
                self.logger.error(f"Error de serialización: {e}")
                return {}
            
        except Exception as e:
            self.logger.error(f"Error en analyze_toxicity: {str(e)}")
            return {}

    def is_toxic(self, scores: Dict[str, float]) -> bool:
        """Verifica si algún puntaje de toxicidad supera los umbrales establecidos."""
        try:
            for category, score in scores.items():
                threshold = getattr(self.thresholds, category, None)
                if threshold is not None and float(score) > threshold:
                    # self.logger.debug(f"Toxicidad detectada en {category}: {score}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error en is_toxic: {str(e)}")
            return False

    async def on_startup(self):
        try:
            # self.logger.info("Iniciando Filtro Detoxify")
            self.model = Detoxify("multilingual")  # Cambiado a multilingual para mejor soporte de español
            # self.logger.info("Modelo Detoxify cargado exitosamente")
        except Exception as e:
            self.logger.error(f"Error en startup: {str(e)}")

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """Procesa los mensajes entrantes del usuario."""
        try:
            # self.logger.debug("Procesando mensaje entrante")
            
            if not isinstance(body, dict) or "messages" not in body:
                return body

            messages = body.get("messages", [])
            if not messages:
                return body

            # Analizar el último mensaje y el contexto reciente
            last_messages = messages[-3:]  # Analizar los últimos 3 mensajes para contexto
            for message in last_messages:
                content = message.get("content", "")
                if not content:
                    continue

                toxicity_scores = self.analyze_toxicity(content)
                if toxicity_scores and self.is_toxic(toxicity_scores):
                    self.logger.info("Contenido tóxico detectado en inlet")
                    professional_response = self.get_professional_response(toxicity_scores)
                    message["content"] = professional_response

            return body

        except Exception as e:
            # self.logger.error(f"Error en inlet: {str(e)}")
            return body

    async def outlet(self, response: Union[dict, str], user: Optional[dict] = None) -> Union[dict, str]:
        """Procesa las respuestas del modelo."""
        try:
            # self.logger.debug("Procesando respuesta del modelo")
            
            # Si la respuesta es un string, convertirla a la estructura correcta
            if isinstance(response, str):
                response = self.create_response_dict(response)
            
            if not isinstance(response, dict):
                return response

            content = None
            if "choices" in response and response["choices"]:
                choice = response["choices"][0]
                if isinstance(choice, dict):
                    if "message" in choice and isinstance(choice["message"], dict):
                        content = choice["message"].get("content")
                    elif "text" in choice:
                        content = choice.get("text")

            if not content:
                return response

            # Verificar si la respuesta revela identidad del modelo
            model_indicators = [
                "LLaMA", "Meta AI", "modelo de lenguaje", "language model",
                "no tengo sentimientos", "no tengo emociones", "I am an AI",
                "Soy una IA", "Soy un modelo", "I'm an AI", "I'm a language model",
                "I don't have feelings", "I don't have emotions"
            ]
            
            if any(indicator.lower() in content.lower() for indicator in model_indicators):
                self.logger.info("Detectada respuesta que revela identidad del modelo")
                return self.create_response_dict(
                    "Soy un asistente profesional diseñado para ayudarte. "
                    "¿En qué puedo asistirte hoy?"
                )

            # Verificar si la respuesta está en inglés
            english_indicators = [
                "I cannot", "I understand", "let's try", "Can I help",
                "I apologize", "I'm sorry", "Please try", "Instead",
                "What's bothering", "How can I help", "I can't"
            ]
            
            is_english = any(indicator.lower() in content.lower() for indicator in english_indicators)
            
            if is_english:
                self.logger.info("Detectada respuesta en inglés, reemplazando con respuesta en español")
                return self.create_response_dict(
                    "Le recordamos que este es un espacio profesional que requiere comunicación en español. "
                    "Si tiene alguna inquietud, por favor exprésela de manera respetuosa y profesional. "
                    "Para más información sobre nuestras políticas de comunicación, consulte el Código de Ética institucional."
                )

            # Analizar toxicidad en la respuesta
            toxicity_scores = self.analyze_toxicity(content)
            
            if toxicity_scores and self.is_toxic(toxicity_scores):
                self.logger.info("Contenido tóxico detectado en outlet")
                professional_response = self.get_professional_response(toxicity_scores)
                return self.create_response_dict(professional_response)

            return response

        except Exception as e:
            self.logger.error(f"Error en outlet: {str(e)}")
            return self.create_response_dict("Lo siento, hubo un error al procesar su mensaje. Por favor, mantenga una comunicación profesional y respetuosa en español.")