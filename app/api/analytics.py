"""
Endpoints analíticos para dados de vendas
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.sales_service import SalesService

# Criar router para analytics
router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/sales-summary")
async def get_sales_summary(db: Session = Depends(get_db)):
    """
    Retorna resumo analítico das vendas:
    - Faturamento total
    - Ticket médio
    - Quantidade total vendida
    - Vendas por categoria
    - Top produtos por faturamento
    """
    try:
        analytics = SalesService.get_sales_analytics(db)
        return {
            "message": "Dados analíticos das vendas",
            "data": analytics
        }
    except Exception as e:
        return {
            "message": "Erro ao gerar analytics",
            "error": str(e)
        }