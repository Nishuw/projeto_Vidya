"""
Modelos de dados SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class SaleStatusEnum(enum.Enum):
    """Enum para status de vendas"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


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
    customer_email = Column(String(255), nullable=True)
    observations = Column(Text, nullable=True)
    status = Column(
        SQLEnum(SaleStatusEnum), 
        nullable=False, 
        default=SaleStatusEnum.COMPLETED
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, 
        nullable=False, 
        server_default=func.now(),
        onupdate=func.now()
    )
    
    @property
    def total_price(self) -> float:
        """Calcula o preço total da venda"""
        return round(self.quantity * self.unit_price, 2)
    
    def __repr__(self):
        return f"<Sale(id={self.id}, product='{self.product_name}', total={self.total_price})>"