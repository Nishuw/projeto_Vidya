"""
Script para popular o banco com dados de exemplo
"""
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.services.sales_service import SalesService, SalesTextService
from app.schemas.sales import SaleCreate


def create_sample_data():
    """
    Cria dados de exemplo para demonstração
    """
    db = SessionLocal()
    
    try:
        print("Criando dados de exemplo...")
        
        # Dados de exemplo
        sample_sales = [
            {
                "product_name": "Smartphone Samsung Galaxy S23",
                "category": "Eletrônicos",
                "quantity": 2,
                "unit_price": 2499.99,
                "sale_date": datetime.now() - timedelta(days=5)
            },
            {
                "product_name": "Notebook Dell Inspiron",
                "category": "Eletrônicos", 
                "quantity": 1,
                "unit_price": 3299.90,
                "sale_date": datetime.now() - timedelta(days=3)
            },
            {
                "product_name": "Tênis Nike Air Max",
                "category": "Calçados",
                "quantity": 1,
                "unit_price": 449.99,
                "sale_date": datetime.now() - timedelta(days=2)
            },
            {
                "product_name": "Camisa Polo Lacoste",
                "category": "Roupas",
                "quantity": 3,
                "unit_price": 189.90,
                "sale_date": datetime.now() - timedelta(days=1)
            },
            {
                "product_name": "Fone de Ouvido Sony WH-1000XM4",
                "category": "Eletrônicos",
                "quantity": 1,
                "unit_price": 1299.00,
                "sale_date": datetime.now()
            }
        ]
        
        # Criar vendas
        created_sales = []
        for sale_data in sample_sales:
            sale_create = SaleCreate(**sale_data)
            sale = SalesService.create_sale(db, sale_create)
            created_sales.append(sale)
            print(f"Venda criada: {sale.product_name} - R$ {sale.total_price}")
        
        # Criar textos de exemplo
        text_examples = [
            (created_sales[0].id, "Cliente elogiou a entrega rápida e a qualidade do smartphone. Compra recomendada por um amigo."),
            (created_sales[1].id, "Notebook para uso profissional. Cliente trabalha com design gráfico e estava satisfeito com a performance."),
            (created_sales[2].id, "Tênis para corrida diária. Cliente mencionou que é a segunda compra da mesma marca."),
            (created_sales[3].id, "Camisas para uso corporativo. Cliente é empresário e compra regularmente."),
            (created_sales[4].id, "Fone com cancelamento de ruído. Cliente viaja muito a trabalho e precisava de qualidade de áudio.")
        ]
        
        for sale_id, text in text_examples:
            SalesTextService.create_sale_text(sale_id, text)
            print(f"Texto criado para venda {sale_id}")
        
        print(f"\n✅ Criados {len(created_sales)} vendas e {len(text_examples)} textos de exemplo!")
        print("Dados prontos para teste da API.")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()