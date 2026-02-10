"""
Aplicação principal FastAPI para sistema de vendas
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import logger
from app.core.middleware import LoggingMiddleware, SecurityHeadersMiddleware
from app.api import sales, analytics, search
from app.db.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida da aplicação
    """
    # Inicialização
    logger.info("🚀 Inicializando Vidya Sales API...")
    
    # Verificar se banco precisa ser criado
    if not os.path.exists("sales.db"):
        logger.info("📊 Criando estrutura do banco de dados...")
        create_tables()
        logger.info("✅ Banco de dados criado com sucesso!")
    else:
        logger.info("📊 Banco de dados já existe")
    
    logger.info("✅ API inicializada com sucesso!")
    
    yield
    
    # Finalização
    logger.info("🔴 Finalizando aplicação...")


# Criar instância da aplicação
app = FastAPI(
    title="Vidya Sales API",
    description="API para gestão de dados de vendas com banco relacional e NoSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar middlewares personalizados
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Handler global para exceções
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Handler global para capturar exceções não tratadas
    """
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "message": "Erro interno do servidor",
            "detail": "Entre em contato com o suporte se o problema persistir"
        }
    )

# Registrar routers
app.include_router(sales.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(search.router, prefix="/api")


@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "Bem-vindo à API de Vendas Vidya",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "vendas": "/api/sales",
            "analytics": "/api/analytics", 
            "busca": "/api/search"
        }
    }


@app.get("/health")
async def health_check():
    """Endpoint para verificação de saúde da API"""
    return {"status": "ok", "message": "API funcionando corretamente"}