"""
Configuração do MongoDB
"""
from pymongo import MongoClient
from app.core.config import settings

# Cliente MongoDB
mongo_client = MongoClient(settings.MONGODB_URL)

# Database
mongodb = mongo_client[settings.MONGODB_DB_NAME]

# Collections
sales_texts_collection = mongodb.sales_texts


def get_mongodb():
    """
    Dependency para obter instância do MongoDB
    """
    return mongodb


def get_sales_texts_collection():
    """
    Dependency para obter collection de textos de vendas
    """
    return sales_texts_collection