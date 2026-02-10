"""
Serviços de negócio para vendas
"""
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.sales import Sale
from app.schemas.sales import SaleCreate, SaleUpdate
from app.db.mongodb import get_sales_texts_collection


class SalesService:
    """
    Serviço para operações de vendas
    """
    
    @staticmethod
    def create_sale(db: Session, sale_data: SaleCreate) -> Sale:
        """
        Cria uma nova venda no banco de dados
        """
        db_sale = Sale(
            product_name=sale_data.product_name,
            category=sale_data.category,
            quantity=sale_data.quantity,
            unit_price=sale_data.unit_price,
            sale_date=sale_data.sale_date or datetime.now()
        )
        db.add(db_sale)
        db.commit()
        db.refresh(db_sale)
        return db_sale
    
    @staticmethod
    def get_sale(db: Session, sale_id: int) -> Optional[Sale]:
        """
        Busca uma venda por ID
        """
        return db.query(Sale).filter(Sale.id == sale_id).first()
    
    @staticmethod
    def get_sales(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Sale]:
        """
        Lista vendas com filtros opcionais
        """
        query = db.query(Sale)
        
        # Filtro por categoria
        if category:
            query = query.filter(Sale.category == category)
        
        # Filtro por período
        if start_date:
            query = query.filter(func.date(Sale.sale_date) >= start_date)
        if end_date:
            query = query.filter(func.date(Sale.sale_date) <= end_date)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_sale(db: Session, sale_id: int, sale_data: SaleUpdate) -> Optional[Sale]:
        """
        Atualiza uma venda existente
        """
        db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not db_sale:
            return None
        
        # Atualizar apenas campos fornecidos
        update_data = sale_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sale, field, value)
        
        db.commit()
        db.refresh(db_sale)
        return db_sale
    
    @staticmethod
    def delete_sale(db: Session, sale_id: int) -> bool:
        """
        Remove uma venda
        """
        db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not db_sale:
            return False
        
        db.delete(db_sale)
        db.commit()
        return True
    
    @staticmethod
    def get_sales_analytics(db: Session) -> dict:
        """
        Retorna dados analíticos das vendas
        """
        # Faturamento total
        total_revenue = db.query(
            func.sum(Sale.quantity * Sale.unit_price)
        ).scalar() or 0
        
        # Número total de vendas
        total_sales = db.query(Sale).count()
        
        # Ticket médio
        avg_ticket = total_revenue / total_sales if total_sales > 0 else 0
        
        # Quantidade total vendida
        total_quantity = db.query(func.sum(Sale.quantity)).scalar() or 0
        
        # Vendas por categoria
        sales_by_category = db.query(
            Sale.category,
            func.count(Sale.id).label('count'),
            func.sum(Sale.quantity * Sale.unit_price).label('revenue')
        ).group_by(Sale.category).all()
        
        # Top produtos
        top_products = db.query(
            Sale.product_name,
            func.sum(Sale.quantity).label('total_quantity'),
            func.sum(Sale.quantity * Sale.unit_price).label('revenue')
        ).group_by(Sale.product_name).order_by(
            func.sum(Sale.quantity * Sale.unit_price).desc()
        ).limit(10).all()
        
        return {
            "total_revenue": round(float(total_revenue), 2),
            "total_sales": total_sales,
            "avg_ticket": round(float(avg_ticket), 2),
            "total_quantity": total_quantity,
            "sales_by_category": [
                {
                    "category": category,
                    "count": count,
                    "revenue": round(float(revenue), 2)
                }
                for category, count, revenue in sales_by_category
            ],
            "top_products": [
                {
                    "product_name": product_name,
                    "total_quantity": total_quantity,
                    "revenue": round(float(revenue), 2)
                }
                for product_name, total_quantity, revenue in top_products
            ]
        }


class SalesTextService:
    """
    Serviço para operações com textos de vendas no MongoDB
    """
    
    @staticmethod
    def create_sale_text(sale_id: int, text: str) -> dict:
        """
        Cria um novo texto relacionado a uma venda
        """
        collection = get_sales_texts_collection()
        document = {
            "sale_id": sale_id,
            "text": text,
            "created_at": datetime.now()
        }
        result = collection.insert_one(document)
        document["_id"] = str(result.inserted_id)
        return document
    
    @staticmethod
    def get_sale_texts(sale_id: int) -> List[dict]:
        """
        Busca textos relacionados a uma venda específica
        """
        collection = get_sales_texts_collection()
        texts = list(collection.find({"sale_id": sale_id}))
        
        # Converter ObjectId para string
        for text in texts:
            text["_id"] = str(text["_id"])
        
        return texts
    
    @staticmethod
    def search_texts(search_term: str) -> List[dict]:
        """
        Busca textos que contenham o termo especificado
        """
        collection = get_sales_texts_collection()
        
        # Busca usando regex (case-insensitive)
        regex_pattern = {"$regex": search_term, "$options": "i"}
        texts = list(collection.find({"text": regex_pattern}))
        
        # Converter ObjectId para string
        for text in texts:
            text["_id"] = str(text["_id"])
        
        return texts