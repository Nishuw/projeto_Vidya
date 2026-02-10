"""
Configuração alternativa do MongoDB com fallback para SQLite
"""
import os
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.core.config import settings


class MongoDBEmulator:
    """
    Emulador simples do MongoDB usando SQLite como fallback
    quando MongoDB não estiver disponível
    """
    
    def __init__(self, db_path: str = "texts.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Inicializar tabela SQLite para textos"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sales_texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                text_type TEXT DEFAULT 'observation',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def insert_one(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Inserir documento (simula MongoDB insert_one)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sales_texts (sale_id, text, text_type, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            document.get('sale_id'),
            document.get('text'),
            document.get('text_type', 'observation'),
            document.get('created_at', datetime.now())
        ))
        
        inserted_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Retornar objeto que simula o resultado do MongoDB
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = str(inserted_id)
        
        return InsertResult(inserted_id)
    
    def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Buscar documentos (simula MongoDB find)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if 'sale_id' in query:
            cursor.execute(
                "SELECT * FROM sales_texts WHERE sale_id = ?", 
                (query['sale_id'],)
            )
        elif 'text' in query and '$regex' in query['text']:
            # Busca textual básica
            search_term = query['text']['$regex']
            cursor.execute(
                "SELECT * FROM sales_texts WHERE text LIKE ?", 
                (f"%{search_term}%",)
            )
        else:
            cursor.execute("SELECT * FROM sales_texts")
        
        results = []
        for row in cursor.fetchall():
            results.append({
                '_id': str(row['id']),
                'sale_id': row['sale_id'],
                'text': row['text'],
                'text_type': row['text_type'],
                'created_at': row['created_at']
            })
        
        conn.close()
        return results
    
    def count_documents(self, query: Dict[str, Any] = {}) -> int:
        """Contar documentos (simula MongoDB count_documents)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if query:
            # Implementar contagem com filtro se necessário
            cursor.execute("SELECT COUNT(*) FROM sales_texts")
        else:
            cursor.execute("SELECT COUNT(*) FROM sales_texts")
        
        count = cursor.fetchone()[0]
        conn.close()
        return count


# Factory para decidir qual implementação usar
def get_sales_texts_collection():
    """
    Factory que retorna MongoDB real ou emulador SQLite
    """
    try:
        # Tentar conexão MongoDB real primeiro
        from pymongo import MongoClient
        client = MongoClient(
            settings.MONGODB_URL, 
            serverSelectionTimeoutMS=2000  # Timeout rápido
        )
        # Teste rápido de conexão
        client.server_info()
        
        db = client[settings.MONGODB_DB_NAME]
        print("✅ MongoDB conectado com sucesso!")
        return db.sales_texts
    
    except Exception as e:
        print(f"⚠️ MongoDB indisponível, usando SQLite como fallback: {e}")
        return MongoDBEmulator()


def get_mongodb():
    """
    Dependency para obter instância do MongoDB (real ou emulado)
    """
    return get_sales_texts_collection()