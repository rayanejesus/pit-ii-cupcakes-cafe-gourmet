# Loja Virtual de Cupcakes e Cafés Gourmet

Projeto acadêmico PIT-II independente do FitLife. O sistema usa React/TypeScript/Vite/Tailwind no front-end e FastAPI/SQLAlchemy/SQLite no back-end.

## Execução local no Windows

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload
```

Por padrão, a API usa o SQLite local. Para PostgreSQL, configure `DATABASE_URL`
antes de iniciar a API. URLs `postgres://` e `postgresql://` são convertidas
automaticamente para o driver `psycopg`. Para o Supabase, use a URL do
Transaction Pooler com SSL, mantendo o valor somente nas variáveis do ambiente.
Consulte [.env.example](.env.example), que não contém credenciais.

Em produção, defina `FRONTEND_ORIGINS` com a URL pública do frontend e
`ORDER_MANAGEMENT_TOKEN` com um segredo longo para proteger leitura, pagamento
e atualização de status dos pedidos. O checkout público continua usando apenas
`POST /api/orders`; o navegador não recebe a credencial de gestão.

O comando `python seed.py` cria tabelas ausentes e insere categorias e produtos
somente quando ainda não existem. Ele é idempotente e não é executado em cada
requisição.

Para criar somente tabelas ausentes, sem apagar dados, execute:

```powershell
cd backend
python init_db.py
```

O script importa todos os modelos (`categories`, `products`, `orders` e
`order_items`) antes de chamar `create_all`. A estratégia de permissões do
Supabase está documentada em
[`docs/supabase-access-control.md`](docs/supabase-access-control.md) e não é
aplicada automaticamente.

Em outro terminal:

```powershell
cd frontend
npm install
npm run dev
```

API/Swagger: `http://localhost:8000/docs`. Front-end: `http://localhost:5173`.

## Testes

```powershell
cd backend; pytest
cd ..\frontend; npm test; npm run build
```

O checkout usa Pix e cartão apenas como simulação; não coleta dados financeiros reais.
