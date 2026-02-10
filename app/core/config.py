"""
Configurações centrais da aplicação
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do ambiente"""
    
    # Configurações da aplicação
    PROJECT_NAME: str = "Vidya Sales API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Configurações do banco SQLite
    DATABASE_URL: str = "sqlite:///./sales.db"
    
    # Configurações do MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "vidya_sales"
    
    # Configurações de ambiente
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"


# Instância global das configurações
settings = Settings()