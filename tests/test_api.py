"""
Testes básicos para a API de vendas
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Bem-vindo" in data["message"]


def test_health_check():
    """Testa o health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_list_sales():
    """Testa listagem de vendas"""
    response = client.get("/api/sales/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_analytics():
    """Testa endpoint de analytics"""
    response = client.get("/api/analytics/sales-summary")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_revenue" in data["data"]


def test_search_texts():
    """Testa busca textual"""
    response = client.get("/api/search/texts?q=cliente")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data


def test_create_sale():
    """Testa criação de venda"""
    sale_data = {
        "product_name": "Produto Teste",
        "category": "Categoria Teste",
        "quantity": 1,
        "unit_price": 100.00
    }
    response = client.post("/api/sales/", json=sale_data)
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == sale_data["product_name"]