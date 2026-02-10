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

### 1. Clone o repositório
```bash
git clone https://github.com/Nishuw/projeto_Vidya.git
cd projeto_Vidya
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

### 4. Execute a aplicação
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: http://localhost:8000
Documentação interativa: http://localhost:8000/docs

## Status do Desenvolvimento

- [x] Estrutura inicial do projeto
- [x] Configuração dos bancos de dados
- [x] Modelos de dados
- [ ] Endpoints CRUD de vendas
- [ ] Endpoint analítico
- [ ] Busca textual no MongoDB
- [ ] Testes unitários
- [ ] Documentação completa
