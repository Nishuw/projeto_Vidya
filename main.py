"""
Aplicação principal FastAPI para sistema de vendas
"""
from fastapi import FastAPI
from app.core.config import settings
from app.api import sales, analytics, search
from app.db.init_db import create_tables

# Inicializar banco de dados
create_tables()

# Criar instância da aplicação
app = FastAPI(
    title="Vidya Sales API",
    description="API para gestão de dados de vendas com banco relacional e NoSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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