"""
Aplicação principal FastAPI para sistema de vendas
"""
from fastapi import FastAPI
from app.core.config import settings

# Criar instância da aplicação
app = FastAPI(
    title="Vidya Sales API",
    description="API para gestão de dados de vendas com banco relacional e NoSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "Bem-vindo à API de Vendas Vidya",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Endpoint para verificação de saúde da API"""
    return {"status": "ok", "message": "API funcionando corretamente"}