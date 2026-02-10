"""
Schemas Pydantic para validação de dados de vendas
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, validator, EmailStr
from enum import Enum


class SaleStatus(str, Enum):
    """Status possíveis de uma venda"""
    PENDING = "pending"
    COMPLETED = "completed" 
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class ProductCategory(str, Enum):
    """Categorias de produtos disponíveis"""
    ELETRONICOS = "Eletrônicos"
    ROUPAS = "Roupas"
    CALCADOS = "Calçados"
    LIVROS = "Livros"
    CASA_JARDIM = "Casa e Jardim"
    ESPORTE_LAZER = "Esporte e Lazer"
    BELEZA_CUIDADOS = "Beleza e Cuidados"
    OUTROS = "Outros"


class SaleBase(BaseModel):
    """Schema base para vendas"""
    product_name: str = Field(
        ..., 
        min_length=1, 
        max_length=255, 
        description="Nome do produto",
        example="Smartphone Samsung Galaxy S23"
    )
    category: ProductCategory = Field(
        ..., 
        description="Categoria do produto"
    )
    quantity: int = Field(
        ..., 
        gt=0, 
        le=10000,
        description="Quantidade vendida",
        example=2
    )
    unit_price: Decimal = Field(
        ..., 
        gt=0,
        max_digits=10,
        decimal_places=2,
        description="Preço unitário",
        example=2499.99
    )
    
    @validator('product_name')
    def validate_product_name(cls, v):
        """Valida e normaliza o nome do produto"""
        if not v or v.isspace():
            raise ValueError('Nome do produto não pode estar vazio')
        return v.strip().title()
    
    @validator('unit_price')
    def validate_unit_price(cls, v):
        """Valida o preço unitário"""
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        if v > 999999.99:
            raise ValueError('Preço muito alto')
        return round(float(v), 2)


class SaleCreate(SaleBase):
    """Schema para criação de vendas"""
    sale_date: Optional[datetime] = Field(
        None, 
        description="Data da venda (opcional, padrão: agora)"
    )
    customer_email: Optional[str] = Field(
        None,
        max_length=255,
        description="Email do cliente (opcional)",
        example="cliente@email.com"
    )
    observations: Optional[str] = Field(
        None,
        max_length=1000,
        description="Observações sobre a venda"
    )


class SaleUpdate(BaseModel):
    """Schema para atualização de vendas"""
    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[ProductCategory] = Field(None)
    quantity: Optional[int] = Field(None, gt=0, le=10000)
    unit_price: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    customer_email: Optional[str] = Field(None, max_length=255)
    observations: Optional[str] = Field(None, max_length=1000)
    status: Optional[SaleStatus] = Field(None, description="Status da venda")


class SaleResponse(SaleBase):
    """Schema de resposta para vendas"""
    id: int
    sale_date: datetime
    total_price: float
    status: str = "completed"
    customer_email: Optional[str] = None
    observations: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SaleListResponse(BaseModel):
    """Schema para resposta de lista paginada"""
    items: List[SaleResponse]
    total: int
    page: int
    size: int
    pages: int


class SaleTextCreate(BaseModel):
    """Schema para criação de texto relacionado à venda"""
    sale_id: int = Field(..., gt=0, description="ID da venda")
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=2000,
        description="Texto/observação sobre a venda"
    )
    text_type: Optional[str] = Field(
        "observation",
        description="Tipo do texto: observation, review, complaint, etc."
    )


class SaleTextResponse(BaseModel):
    """Schema de resposta para texto de venda"""
    sale_id: int
    text: str
    text_type: str
    created_at: datetime


class SalesSummaryResponse(BaseModel):
    """Schema para resposta do resumo de vendas"""
    total_revenue: float
    total_sales: int
    avg_ticket: float
    total_quantity: int
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None


class CategorySalesResponse(BaseModel):
    """Schema para vendas por categoria"""
    category: str
    count: int
    revenue: float
    avg_price: float