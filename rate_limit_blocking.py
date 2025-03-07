"""
title: Control de Frecuencia de Mensajes
description: Pipeline para controlar la frecuencia de mensajes por usuario, previniendo spam y uso excesivo del sistema.
            Implementa límites de velocidad configurables y mensajes de advertencia en español.
author: Gastón Guevara
date: 07-03-2025
version: 1.1
license: MIT
"""

from typing import Dict, Optional, Union
from pydantic import BaseModel
import time
import logging

# Configuración del logger
logger = logging.getLogger("rate_limit_blocking")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class RateLimitConfig(BaseModel):
    messages_per_minute: int = 5
    burst_limit: int = 2
    cooldown_minutes: int = 1

class UserState(BaseModel):
    message_count: int = 0
    last_reset: float = 0
    is_blocked: bool = False
    block_until: float = 0
    pending_requests: int = 0  # Nuevo: contador de solicitudes pendientes

class Valves(BaseModel):
    pipelines: list[str] = ["*"]
    priority: int = 0

class Pipeline:
    def __init__(self):
        self.type = "filter"
        self.name = "Rate Limit Blocking"
        self.valves = Valves()
        self.config = RateLimitConfig()
        self.user_states: Dict[str, UserState] = {}

    def create_response_dict(self, message: str, error: bool = False) -> dict:
        """Crea un diccionario de respuesta con la estructura correcta."""
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": message
                    },
                    "finish_reason": "stop" if not error else "error",
                    "index": 0
                }
            ],
            "error": error
        }

    def get_user_state(self, user_id: str) -> UserState:
        """Obtiene o crea el estado de un usuario."""
        if user_id not in self.user_states:
            self.user_states[user_id] = UserState()
        return self.user_states[user_id]

    def get_user_info(self, user: Optional[dict]) -> tuple[str, str]:
        """Obtiene el ID y nombre del usuario."""
        if not user:
            return "unknown", "Usuario Desconocido"
        
        user_id = user.get("id", "unknown")
        user_name = user.get("display_name", user.get("username", user.get("name", "Usuario " + user_id)))
        return user_id, user_name

    def check_and_update_rate_limit(self, user: Optional[dict], message_content: str = "") -> tuple[bool, str]:
        """Verifica y actualiza el límite de velocidad para un usuario."""
        current_time = time.time()
        user_id, user_name = self.get_user_info(user)
        state = self.get_user_state(user_id)
        
        logger.debug(f"Usuario {user_name} - Estado actual: mensajes={state.message_count}, pendientes={state.pending_requests}")
        logger.debug(f"Contenido del mensaje: {message_content[:50]}...")

        # Verificar si el usuario está bloqueado
        if state.is_blocked:
            if current_time < state.block_until:
                remaining = int(state.block_until - current_time)
                logger.warning(f"Usuario {user_name} bloqueado por {remaining} segundos más")
                return False, f"Por favor, espere {remaining} segundos antes de enviar más mensajes."
            logger.info(f"Usuario {user_name} desbloqueado")
            state.is_blocked = False

        # Resetear contador si ha pasado el tiempo
        if current_time - state.last_reset >= 60:
            logger.info(f"Reseteando contador para usuario {user_name}")
            state.message_count = 0
            state.last_reset = current_time

        # Verificar límites
        state.message_count += 1
        state.pending_requests += 1
        
        logger.debug(f"Usuario {user_name} - Nuevo estado: mensajes={state.message_count}, pendientes={state.pending_requests}")

        if state.message_count > self.config.messages_per_minute:
            state.is_blocked = True
            state.block_until = current_time + (self.config.cooldown_minutes * 60)
            logger.warning(f"Usuario {user_name} excedió límite de mensajes por minuto")
            return False, f"Ha excedido el límite de {self.config.messages_per_minute} mensajes por minuto. Por favor, espere {self.config.cooldown_minutes} minutos."

        if state.pending_requests > 4:  # Límite de solicitudes pendientes
            logger.warning(f"Usuario {user_name} tiene demasiadas solicitudes pendientes ({state.pending_requests})")
            return False, "Demasiadas solicitudes pendientes. Por favor, espere a que se procesen las anteriores."

        if state.message_count > self.config.burst_limit:
            logger.warning(f"Usuario {user_name} alcanzó límite de ráfaga")
            return True, "Por favor, reduzca la frecuencia de sus mensajes para evitar ser bloqueado."

        logger.debug(f"Solicitud aceptada para usuario {user_name}")
        return True, ""

    async def inlet(self, body: dict, user: Optional[dict] = None) -> Union[dict, str]:
        """Procesa los mensajes entrantes verificando límites de velocidad."""
        try:
            if not user or "id" not in user:
                logger.warning("Usuario no identificado")
                return body

            message_content = body.get("messages", [{}])[-1].get("content", "") if isinstance(body, dict) else ""
            allowed, message = self.check_and_update_rate_limit(user, message_content)
            
            if not allowed:
                return self.create_response_dict(message, error=True)
            
            if message:  # Advertencia de burst
                if isinstance(body, dict) and "messages" in body:
                    messages = body["messages"]
                    if messages:
                        messages[-1]["content"] = f"{messages[-1]['content']}\n\n[Sistema: {message}]"
                        body["messages"] = messages

            return body

        except Exception as e:
            logger.error(f"Error en inlet: {str(e)}")
            return self.create_response_dict(
                "Lo siento, hubo un error al procesar su mensaje. Por favor, inténtelo de nuevo en unos momentos.",
                error=True
            )

    async def outlet(self, response: Union[dict, str], user: Optional[dict] = None) -> Union[dict, str]:
        """Procesa las respuestas del modelo."""
        try:
            if user and "id" in user:
                user_id, user_name = self.get_user_info(user)
                state = self.get_user_state(user_id)
                state.pending_requests = max(0, state.pending_requests - 1)
                logger.debug(f"Usuario {user_name} - Solicitud completada. Pendientes restantes: {state.pending_requests}")
        except Exception as e:
            logger.error(f"Error en outlet: {str(e)}")
        
        return response

    async def on_startup(self):
        """Inicialización del pipeline."""
        logger.info("Rate Limit Blocking Pipeline iniciado")