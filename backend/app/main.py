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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(catalog.router)
app.include_router(orders.router)


@app.get("/api/health", tags=["Sistema"])
def health():
    return {"status": "ok"}
