from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.connection import get_db
from app.models.orders import Order, OrderStatus
from app.schemas.orders import OrderCreate, OrderResponse
from app.services.order_service import create_order, update_status

router = APIRouter(prefix="/api/orders", tags=["Pedidos"])


@router.post("", response_model=OrderResponse, status_code=201)
def place_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, payload)


@router.get("", response_model=list[OrderResponse])
def list_orders(email: str | None = None, db: Session = Depends(get_db)):
    query = select(Order).options(selectinload(Order.items)).order_by(Order.created_at.desc())
    if email:
        query = query.where(Order.customer_email == email)
    return db.scalars(query).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id == order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return order


@router.post("/{order_id}/pay", response_model=OrderResponse)
def pay_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return update_status(db, order, OrderStatus.PAGO)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def change_status(order_id: int, status: OrderStatus, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return update_status(db, order, status)
