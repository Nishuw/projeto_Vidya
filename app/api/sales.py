"""
Endpoints da API para vendas
"""
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.sales import (
    SaleCreate, SaleUpdate, SaleResponse, 
    SaleTextCreate, SaleTextResponse
)
from app.services.sales_service import SalesService, SalesTextService

# Criar router para vendas
router = APIRouter(prefix="/sales", tags=["vendas"])


@router.post("/", response_model=SaleResponse, status_code=201)
async def create_sale(sale_data: SaleCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova venda
    """
    try:
        sale = SalesService.create_sale(db, sale_data)
        return sale
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar venda: {str(e)}")


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(sale_id: int, db: Session = Depends(get_db)):
    """
    Busca uma venda por ID
    """
    sale = SalesService.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale


@router.get("/", response_model=List[SaleResponse])
async def list_sales(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    start_date: Optional[date] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Lista vendas com filtros opcionais
    """
    sales = SalesService.get_sales(
        db, skip=skip, limit=limit, 
        category=category, start_date=start_date, end_date=end_date
    )
    return sales


@router.put("/{sale_id}", response_model=SaleResponse)
async def update_sale(
    sale_id: int, 
    sale_data: SaleUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza uma venda existente
    """
    sale = SalesService.update_sale(db, sale_id, sale_data)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale


@router.delete("/{sale_id}")
async def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    """
    Remove uma venda
    """
    success = SalesService.delete_sale(db, sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return {"message": "Venda removida com sucesso"}


@router.post("/{sale_id}/texts", response_model=SaleTextResponse, status_code=201)
async def create_sale_text(
    sale_id: int,
    text_data: dict,
    db: Session = Depends(get_db)
):
    """
    Adiciona um texto/observação a uma venda
    """
    # Verificar se a venda existe
    sale = SalesService.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    try:
        text = text_data.get("text", "").strip()
        if not text:
            raise HTTPException(status_code=400, detail="Texto não pode estar vazio")
        
        result = SalesTextService.create_sale_text(sale_id, text)
        return {"sale_id": sale_id, "text": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar texto: {str(e)}")


@router.get("/{sale_id}/texts")
async def get_sale_texts(sale_id: int, db: Session = Depends(get_db)):
    """
    Busca todos os textos relacionados a uma venda
    """
    # Verificar se a venda existe
    sale = SalesService.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    texts = SalesTextService.get_sale_texts(sale_id)
    return {"sale_id": sale_id, "texts": texts}