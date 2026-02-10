"""
Middleware personalizado para logging e tratamento de erros
"""
import time
import uuid
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para log automatico de todas as requisições
    """
    
    async def dispatch(self, request: Request, call_next):
        # Gerar ID único para a requisição
        request_id = str(uuid.uuid4())[:8]
        
        # Log da requisição de entrada
        start_time = time.time()
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - "
            f"Cliente: {request.client.host}"
        )
        
        # Processar requisição
        try:
            response: Response = await call_next(request)
        except Exception as e:
            logger.error(f"[{request_id}] Erro interno: {str(e)}")
            raise
        
        # Log da resposta
        process_time = time.time() - start_time
        logger.info(
            f"[{request_id}] Resposta: {response.status_code} - "
            f"Tempo: {process_time:.3f}s"
        )
        
        # Adicionar headers de resposta
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(round(process_time, 3))
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar headers de segurança
    """
    
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        
        # Headers de segurança básicos
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response