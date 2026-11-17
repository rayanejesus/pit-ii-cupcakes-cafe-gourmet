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
