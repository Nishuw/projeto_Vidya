"""
Endpoints para busca textual no MongoDB/SQLite
"""
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.sales_service import SalesService, SalesTextService

# Criar router para busca
router = APIRouter(prefix="/search", tags=["busca-textual"])


@router.get("/texts",
            summary="Busca textual em observações e comentários",
            description="""
            Realiza busca textual nos comentários, observações e textos relacionados às vendas.
            
            **Funcionalidades:**
            - Busca case-insensitive (não diferencia maiúscula/minúscula)
            - Busca por palavras parciais (ex: "client" encontra "cliente")  
            - Retorna dados completos da venda relacionada
            - Suporta MongoDB ou SQLite como fallback
            
            **Exemplos de busca:**
            - `q=cliente` - encontra textos contendo "cliente"
            - `q=elogiou` - encontra elogios de clientes
            - `q=entrega` - encontra comentários sobre entrega
            - `q=qualidade` - encontra menções à qualidade
            
            **Casos de uso:**
            - Análise de feedback dos clientes
            - Busca por reclamações específicas
            - Identificação de pontos de melhoria
            - Relatórios de satisfação
            """)
async def search_texts(
    q: str = Query(
        ..., 
        min_length=1, 
        description="Termo de busca (mínimo 1 caractere)",
        example="cliente"
    ),
    db: Session = Depends(get_db)
):
    """
    Busca textos relacionados às vendas no MongoDB/SQLite
    Retorna os textos encontrados junto com os dados da venda relacionada
    """
    try:
        # Buscar textos no MongoDB/SQLite
        texts = SalesTextService.search_texts(q)
        
        if not texts:
            return {
                "message": f"Nenhum texto encontrado para o termo '{q}'",
                "search_term": q,
                "total_results": 0,
                "results": [],
                "suggestions": [
                    "Tente termos como: cliente, produto, entrega, qualidade",
                    "Verifique se há textos cadastrados no sistema"
                ]
            }
        
        # Buscar dados das vendas relacionadas
        results = []
        for text in texts:
            sale_id = text["sale_id"]
            sale = SalesService.get_sale(db, sale_id)
            
            if sale:
                results.append({
                    "text_id": text.get("_id", "N/A"),
                    "text": text["text"],
                    "text_type": text.get("text_type", "observation"),
                    "created_at": text.get("created_at"),
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erro na busca textual: {str(e)}"
        )