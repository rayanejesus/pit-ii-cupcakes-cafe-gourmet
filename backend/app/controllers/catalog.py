from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_db
from app.models.catalog import Category, Product
from app.schemas.catalog import CategoryResponse, ProductCreate, ProductResponse

router = APIRouter(prefix="/api", tags=["Catálogo"])


@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.scalars(select(Category).order_by(Category.name)).all()


@router.get("/products", response_model=list[ProductResponse])
def list_products(
    category_id: int | None = Query(default=None),
    search: str | None = Query(default=None, max_length=80),
    db: Session = Depends(get_db),
):
    query = select(Product).options(joinedload(Product.category)).where(Product.available.is_(True))
    if category_id:
        query = query.where(Product.category_id == category_id)
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    return db.scalars(query.order_by(Product.name)).unique().all()


@router.post("/admin/products", response_model=ProductResponse, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    if not db.get(Category, payload.category_id):
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return db.scalar(select(Product).options(joinedload(Product.category)).where(Product.id == product.id))
