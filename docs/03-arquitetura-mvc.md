# 3. Arquitetura MVC

O back-end separa Model (entidades SQLAlchemy em `backend/app/models`), View (schemas Pydantic que definem as respostas) e Controller (routers FastAPI em `backend/app/controllers`). Regras de negócio que envolvem estoque, preço e transição de status ficam em `backend/app/services`. O front-end React constitui a View e consome os controllers por HTTP. Essa adaptação mantém responsabilidades claras entre cliente web, API e persistência.
