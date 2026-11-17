from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.catalog import Product
from app.models.orders import Order, OrderItem, OrderRequest, OrderStatus
from app.schemas.orders import OrderCreate

SHIPPING_FEE = Decimal("8.50")


def create_order(db: Session, payload: OrderCreate, idempotency_key: str) -> Order:
    request = OrderRequest(idempotency_key=idempotency_key)
    db.add(request)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        existing_request = db.scalar(
            select(OrderRequest).where(OrderRequest.idempotency_key == idempotency_key)
        )
        if existing_request is None:
            raise
        if existing_request.order_id is None:
            raise HTTPException(status_code=409, detail="Pedido idempotente ainda está sendo processado.")
        return db.get(Order, existing_request.order_id)

    product_ids = [item.product_id for item in payload.items]
    products = {p.id: p for p in db.scalars(select(Product).where(Product.id.in_(product_ids))).all()}
    if len(products) != len(set(product_ids)):
        db.rollback()
        raise HTTPException(status_code=404, detail="Um ou mais produtos não foram encontrados.")

    subtotal = Decimal("0")
    order_items: list[OrderItem] = []
    for requested in payload.items:
        product = products[requested.product_id]
        if not product.available or product.stock < requested.quantity:
            db.rollback()
            raise HTTPException(status_code=409, detail=f"Estoque insuficiente para {product.name}.")
        subtotal += product.price * requested.quantity
        product.stock -= requested.quantity
        order_items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=requested.quantity,
            )
        )

    order = Order(
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        address=payload.address,
        subtotal=subtotal,
        shipping=SHIPPING_FEE,
        total=subtotal + SHIPPING_FEE,
        payment_method=payload.payment_method.value,
        status=OrderStatus.AGUARDANDO_PAGAMENTO.value,
        items=order_items,
    )
    db.add(order)
    db.flush()
    request.order_id = order.id
    db.commit()
    db.refresh(order)
    return order


def update_status(db: Session, order: Order, status: OrderStatus) -> Order:
    allowed = {
        OrderStatus.AGUARDANDO_PAGAMENTO: {OrderStatus.PAGO, OrderStatus.CANCELADO},
        OrderStatus.PAGO: {OrderStatus.EM_PREPARO, OrderStatus.CANCELADO},
        OrderStatus.EM_PREPARO: {OrderStatus.EM_ROTA},
        OrderStatus.EM_ROTA: {OrderStatus.ENTREGUE},
        OrderStatus.ENTREGUE: set(),
        OrderStatus.CANCELADO: set(),
    }
    current = OrderStatus(order.status)
    if status not in allowed[current]:
        raise HTTPException(status_code=409, detail=f"Transição inválida: {current} -> {status}.")
    order.status = status.value
    db.commit()
    db.refresh(order)
    return order
