"""
Endpoints da API para vendas
"""
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.sales import (
    SaleCreate, SaleUpdate, SaleResponse, 
    SaleTextCreate, SaleTextResponse
)
from app.services.sales_service import SalesService, SalesTextService

# Criar router para vendas
router = APIRouter(prefix="/sales", tags=["vendas"])


@router.post("/", 
             response_model=SaleResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Criar nova venda",
             description="""
             Cria uma nova venda no sistema.
             
             **Parâmetros:**
             - **product_name**: Nome do produto (obrigatório, 1-255 caracteres)
             - **category**: Categoria do produto (obrigatório, 1-100 caracteres)  
             - **quantity**: Quantidade vendida (obrigatório, > 0)
             - **unit_price**: Preço unitário (obrigatório, > 0)
             - **sale_date**: Data da venda (opcional, padrão: agora)
             
             **Retorna:**
             - Dados completos da venda criada incluindo ID gerado e preço total calculado
             """)
async def create_sale(
    sale_data: SaleCreate = ..., 
    db: Session = Depends(get_db)
):
    """
    Cria uma nova venda no sistema
    """
    try:
        sale = SalesService.create_sale(db, sale_data)
        return sale
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Erro ao criar venda: {str(e)}"
        )


@router.get("/{sale_id}", 
            response_model=SaleResponse,
            summary="Buscar venda por ID",
            description="Retorna os dados de uma venda específica pelo seu ID único.")
async def get_sale(
    sale_id: int = ..., 
    db: Session = Depends(get_db)
):
    """
    Busca uma venda específica por ID
    """
    sale = SalesService.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Venda com ID {sale_id} não encontrada"
        )
    return sale


@router.get("/", 
            response_model=List[SaleResponse],
            summary="Listar vendas",
            description="""
            Lista vendas com filtros opcionais e paginação.
            
            **Filtros disponíveis:**
            - **category**: Filtrar por categoria específica
            - **start_date**: Data inicial (formato: YYYY-MM-DD)
            - **end_date**: Data final (formato: YYYY-MM-DD)
            
            **Paginação:**
            - **skip**: Número de registros a pular (padrão: 0)
            - **limit**: Máximo de registros (padrão: 100, máximo: 1000)
            """)
async def list_sales(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros por página"),
    category: Optional[str] = Query(None, description="Filtrar por categoria específica"),
    start_date: Optional[date] = Query(None, description="Data inicial do período (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Data final do período (YYYY-MM-DD)"),
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


@router.put("/{sale_id}", 
            response_model=SaleResponse,
            summary="Atualizar venda",
            description="Atualiza parcialmente os dados de uma venda existente. Apenas campos fornecidos serão atualizados.")
async def update_sale(
    sale_id: int = ..., 
    sale_data: SaleUpdate = ..., 
    db: Session = Depends(get_db)
):
    """
    Atualiza uma venda existente
    """
    sale = SalesService.update_sale(db, sale_id, sale_data)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Venda com ID {sale_id} não encontrada"
        )
    return sale


@router.delete("/{sale_id}",
               status_code=status.HTTP_200_OK,
               summary="Deletar venda",
               description="Remove uma venda do sistema permanentemente. Esta ação não pode ser desfeita.")
async def delete_sale(
    sale_id: int = ..., 
    db: Session = Depends(get_db)
):
    """
    Remove uma venda do sistema
    """
    success = SalesService.delete_sale(db, sale_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Venda com ID {sale_id} não encontrada"
        )
    return {"message": f"Venda {sale_id} removida com sucesso"}


# ===============================================
# ENDPOINTS PARA TEXTOS/OBSERVAÇÕES DAS VENDAS  
# ===============================================

@router.post("/{sale_id}/texts", 
             response_model=SaleTextResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Adicionar texto/observação à venda",
             description="""
             Adiciona uma observação, comentário ou texto relacionado à uma venda específica.
             
             **Casos de uso:**
             - Comentários do cliente sobre o produto
             - Observações do vendedor
             - Feedback pós-venda
             - Reclamações ou elogios
             
             O texto é armazenado no sistema NoSQL (MongoDB/SQLite) para permitir busca textual.
             """)
async def create_sale_text(
    sale_id: int = ...,
    text_data: dict = ...,
    db: Session = Depends(get_db)
):
    """
    Adiciona um texto/observação a uma venda específica
    """
    # Verificar se a venda existe
    sale = SalesService.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Venda com ID {sale_id} não encontrada"
        )
    
    try:
        text = text_data.get("text", "").strip()
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Texto não pode estar vazio"
            )
        
        result = SalesTextService.create_sale_text(sale_id, text)
        return {"sale_id": sale_id, "text": text}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Erro ao criar texto: {str(e)}"
        )


@router.get("/{sale_id}/texts",
            summary="Buscar textos de uma venda",
            description="Retorna todos os textos, observações e comentários relacionados à uma venda específica.")
async def get_sale_texts(
    sale_id: int = ..., 
    db: Session = Depends(get_db)
):
    """
    Busca todos os textos relacionados a uma venda específica
    """
    # Verificar se a venda existe
    sale = SalesService.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Venda com ID {sale_id} não encontrada"
        )
    
    texts = SalesTextService.get_sale_texts(sale_id)
    return {
        "sale_id": sale_id,
        "sale_info": {
            "product_name": sale.product_name,
            "category": sale.category,
            "total_price": sale.total_price
        },
        "texts": texts,
        "total_texts": len(texts)
    }