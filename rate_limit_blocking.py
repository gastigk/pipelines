import os
import time
from typing import List, Optional
from pydantic import BaseModel

class Pipeline:
    class Valves(BaseModel):
        pipelines: List[str] = []
        max_requests_per_5_seconds: int = 2
        min_interval_seconds: int = 2
        block_time_seconds: int = 10  # Bloqueo de 10 segundos si se excede el límite

    def __init__(self):
        self.type = "filter"
        self.name = "Rate Limit Filter with Temporary Ban"
        
        self.valves = self.Valves(
            pipelines=os.getenv("RATE_LIMIT_PIPELINES", "*").split(","),
            max_requests_per_5_seconds=2,
            min_interval_seconds=2,
            block_time_seconds=10,
        )
        
        self.user_requests = {}
        self.blocked_users = {}  # Diccionario para almacenar usuarios bloqueados
    
    def prune_requests(self, user_id: str):
        """Elimina registros fuera de la ventana de tiempo."""
        now = time.time()
        if user_id in self.user_requests:
            self.user_requests[user_id] = [req for req in self.user_requests[user_id] if now - req < 5]
    
    def log_request(self, user_id: str):
        """Registra una nueva solicitud de un usuario."""
        now = time.time()
        if user_id not in self.user_requests:
            self.user_requests[user_id] = []
        self.user_requests[user_id].append(now)
    
    def is_rate_limited(self, user_id: str, role: str) -> bool:
        """Verifica si un usuario ha excedido los límites."""
        now = time.time()
        
        # Los administradores no tienen restricciones
        if role == "admin":
            return False
        
        # Verificar si el usuario está bloqueado
        if user_id in self.blocked_users and now < self.blocked_users[user_id]:
            return True
        
        # Eliminar solicitudes viejas
        self.prune_requests(user_id)
        
        # Obtener las solicitudes recientes
        user_reqs = self.user_requests.get(user_id, [])
        
        # Revisar si se enviaron más de 2 solicitudes en 5 segundos
        if len(user_reqs) >= self.valves.max_requests_per_5_seconds:
            self.blocked_users[user_id] = now + self.valves.block_time_seconds  # Bloqueo temporal
            return True
        
        # Revisar si la última solicitud fue hace menos de 2 segundos
        if len(user_reqs) > 1 and (now - user_reqs[-1]) < self.valves.min_interval_seconds:
            return True
        
        return False
    
    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        user_id = user.get("id", "default_user")
        role = user.get("role", "user")
        
        if self.is_rate_limited(user_id, role):
            error_message = "Demasiadas solicitudes. Espera unos segundos antes de intentarlo nuevamente."
            print(f"[Rate Limit] {user_id} bloqueado: {error_message}")  # Mensaje en consola
            return {"error": error_message}
        
        self.log_request(user_id)
        return body