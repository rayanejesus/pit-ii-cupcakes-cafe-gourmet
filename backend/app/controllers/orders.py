import hmac
import os

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.connection import get_db
from app.models.orders import Order, OrderStatus
from app.schemas.orders import OrderCreate, OrderResponse
from app.services.order_service import create_order, update_status

router = APIRouter(prefix="/api/orders", tags=["Pedidos"])
management_token_header = APIKeyHeader(name="X-Order-Management-Token", auto_error=False)


def require_order_management_token(token: str | None = Depends(management_token_header)) -> None:
    expected_token = os.environ.get("ORDER_MANAGEMENT_TOKEN")
    if not expected_token:
        raise HTTPException(status_code=503, detail="Gestão de pedidos não configurada.")
    if token is None or not hmac.compare_digest(token, expected_token):
        raise HTTPException(status_code=401, detail="Não autorizado.")


@router.post("", response_model=OrderResponse, status_code=201)
def place_order(
    payload: OrderCreate,
    idempotency_key: str = Header(..., alias="Idempotency-Key", min_length=16, max_length=120),
    db: Session = Depends(get_db),
):
    return create_order(db, payload, idempotency_key)


@router.get("", response_model=list[OrderResponse], dependencies=[Depends(require_order_management_token)])
def list_orders(email: str | None = None, db: Session = Depends(get_db)):
    query = select(Order).options(selectinload(Order.items)).order_by(Order.created_at.desc())
    if email:
        query = query.where(Order.customer_email == email)
    return db.scalars(query).all()


@router.get("/{order_id}", response_model=OrderResponse, dependencies=[Depends(require_order_management_token)])
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id == order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return order


@router.post("/{order_id}/pay", response_model=OrderResponse, dependencies=[Depends(require_order_management_token)])
def pay_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return update_status(db, order, OrderStatus.PAGO)


@router.patch("/{order_id}/status", response_model=OrderResponse, dependencies=[Depends(require_order_management_token)])
def change_status(order_id: int, status: OrderStatus, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return update_status(db, order, status)
