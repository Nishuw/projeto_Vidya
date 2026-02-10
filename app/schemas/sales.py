"""
Schemas Pydantic para validação de dados de vendas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class SaleBase(BaseModel):
    """Schema base para vendas"""
    product_name: str = Field(..., min_length=1, max_length=255, description="Nome do produto")
    category: str = Field(..., min_length=1, max_length=100, description="Categoria do produto")
    quantity: int = Field(..., gt=0, description="Quantidade vendida")
    unit_price: float = Field(..., gt=0, description="Preço unitário")
    
    @validator('product_name', 'category')
    def validate_strings(cls, v):
        """Valida strings removendo espaços extras"""
        return v.strip()


class SaleCreate(SaleBase):
    """Schema para criação de vendas"""
    sale_date: Optional[datetime] = Field(None, description="Data da venda (opcional)")


class SaleUpdate(BaseModel):
    """Schema para atualização de vendas"""
    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[float] = Field(None, gt=0)


class SaleResponse(SaleBase):
    """Schema de resposta para vendas"""
    id: int
    sale_date: datetime
    total_price: float
    
    class Config:
        from_attributes = True


class SaleTextCreate(BaseModel):
    """Schema para criação de texto relacionado à venda"""
    sale_id: int = Field(..., gt=0, description="ID da venda")
    text: str = Field(..., min_length=1, description="Texto/observação sobre a venda")


class SaleTextResponse(BaseModel):
    """Schema de resposta para texto de venda"""
    sale_id: int
    text: str