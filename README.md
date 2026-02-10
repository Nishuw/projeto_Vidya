# Projeto Vidya - Backend API

Sistema de gestão de vendas desenvolvido com Python e FastAPI.

## Descrição

API REST para ingestão, armazenamento e consulta de dados de vendas, utilizando banco de dados relacional (SQLite) para dados estruturados e MongoDB para dados textuais.

## Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados relacional
- **SQLite** - Banco de dados relacional para dados estruturados
- **MongoDB** - Banco NoSQL para dados textuais
- **Pydantic** - Validação de dados e serialização
- **Uvicorn** - Servidor ASGI

## Estrutura do Projeto

```
app/
├── api/           # Endpoints da API
├── core/          # Configurações centrais
├── db/            # Configuração dos bancos de dados
├── models/        # Modelos SQLAlchemy
├── schemas/       # Schemas Pydantic
└── services/      # Lógica de negócio
```

## Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior
- MongoDB (local ou Docker)

### Opção 1: Execução com Docker (Recomendado)

1. Clone o repositório:
```bash
git clone https://github.com/Nishuw/projeto_Vidya.git
cd projeto_Vidya
```

2. Execute com Docker Compose:
```bash
docker-compose up --build
```

A API estará disponível em: http://localhost:8000

### Opção 2: Execução Local

1. Clone o repositório:
```bash
git clone https://github.com/Nishuw/projeto_Vidya.git
cd projeto_Vidya
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env se necessário
```

5. Certifique-se de que o MongoDB está rodando localmente

6. Execute a aplicação:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Populando Dados de Teste

Para facilitar os testes, execute o script de dados de exemplo:
```bash
python populate_sample_data.py
```

## Documentação da API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints Principais

### Vendas (CRUD)
- `POST /api/sales/` - Criar venda
- `GET /api/sales/` - Listar vendas (com filtros)
- `GET /api/sales/{id}` - Buscar venda específica
- `PUT /api/sales/{id}` - Atualizar venda
- `DELETE /api/sales/{id}` - Deletar venda

### Textos de Vendas
- `POST /api/sales/{id}/texts` - Adicionar texto/observação
- `GET /api/sales/{id}/texts` - Buscar textos da venda

### Analytics
- `GET /api/analytics/sales-summary` - Relatório analítico

### Busca Textual
- `GET /api/search/texts?q={termo}` - Buscar em textos

## Exemplos de Uso

### Criar uma venda:
```bash
curl -X POST "http://localhost:8000/api/sales/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "iPhone 15",
    "category": "Eletrônicos",
    "quantity": 1,
    "unit_price": 4999.99
  }'
```

### Buscar vendas por categoria:
```bash
curl "http://localhost:8000/api/sales/?category=Eletrônicos"
```

### Obter analytics:
```bash
curl "http://localhost:8000/api/analytics/sales-summary"
```

### Buscar textos:
```bash
curl "http://localhost:8000/api/search/texts?q=cliente"
```

## Status do Desenvolvimento

- [x] Estrutura inicial do projeto
- [x] Configuração dos bancos de dados
- [x] Modelos de dados
- [x] Endpoints CRUD de vendas
- [x] Endpoint analítico
- [x] Busca textual no MongoDB
- [x] Testes básicos
- [x] Documentação completa
- [x] Dados de exemplo funcionando
- [x] API executando corretamente

## Executando Testes

```bash
# No ambiente virtual ativo
pytest tests/ -v
```

## Estrutura dos Dados

### Modelo de Venda (SQLite)
```json
{
  "id": 1,
  "product_name": "Smartphone Samsung Galaxy S23",
  "category": "Eletrônicos",
  "quantity": 2,
  "unit_price": 2499.99,
  "sale_date": "2026-02-05T10:28:38",
  "total_price": 4999.98
}
```

### Texto de Venda (MongoDB)
```json
{
  "_id": "ObjectId",
  "sale_id": 1,
  "text": "Cliente elogiou a entrega rápida e a qualidade",
  "created_at": "2026-02-10T10:28:38"
}
```
