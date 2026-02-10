"""
Endpoints para busca textual no MongoDB
"""
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.sales_service import SalesService, SalesTextService

# Criar router para busca
router = APIRouter(prefix="/search", tags=["busca"])


@router.get("/texts")
async def search_texts(
    q: str = Query(..., min_length=1, description="Termo de busca"),
    db: Session = Depends(get_db)
):
    """
    Busca textos relacionados às vendas no MongoDB
    Retorna os textos encontrados junto com os dados da venda relacionada
    """
    try:
        # Buscar textos no MongoDB
        texts = SalesTextService.search_texts(q)
        
        if not texts:
            return {
                "message": f"Nenhum texto encontrado para o termo '{q}'",
                "results": []
            }
        
        # Buscar dados das vendas relacionadas
        results = []
        for text in texts:
            sale_id = text["sale_id"]
            sale = SalesService.get_sale(db, sale_id)
            
            if sale:
                results.append({
                    "text_id": text["_id"],
                    "text": text["text"],
                    "sale": {
                        "id": sale.id,
                        "product_name": sale.product_name,
                        "category": sale.category,
                        "quantity": sale.quantity,
                        "unit_price": sale.unit_price,
                        "total_price": sale.total_price,
                        "sale_date": sale.sale_date
                    }
                })
        
        return {
            "message": f"Encontrados {len(results)} resultado(s) para '{q}'",
            "search_term": q,
            "total_results": len(results),
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro na busca textual: {str(e)}"
        )