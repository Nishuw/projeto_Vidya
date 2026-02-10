"""
Modelos de dados SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Sale(Base):
    """
    Modelo para tabela de vendas no banco relacional
    """
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, nullable=False, server_default=func.now())
    
    @property
    def total_price(self) -> float:
        """Calcula o preço total da venda"""
        return self.quantity * self.unit_price