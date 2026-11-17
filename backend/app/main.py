import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import catalog, orders
from app.database.connection import Base, engine
from app.models import catalog as catalog_models
from app.models import orders as order_models


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Loja Virtual de Cupcakes e Cafés Gourmet",
    version="1.0.0",
    description="API acadêmica do Projeto Integrador Transdisciplinar II.",
    lifespan=lifespan,
)
configured_origins = os.environ.get("FRONTEND_ORIGINS")
if configured_origins is None:
    allowed_origins = ["http://localhost:5173"]
else:
    allowed_origins = [origin.strip().rstrip("/") for origin in configured_origins.split(",") if origin.strip()]
    if not allowed_origins:
        raise RuntimeError("FRONTEND_ORIGINS está definida, mas vazia.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "X-Order-Management-Token"],
)
app.include_router(catalog.router)
app.include_router(orders.router)


@app.get("/api/health", tags=["Sistema"])
def health():
    return {"status": "ok"}
