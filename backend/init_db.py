from app.database.connection import Base, engine
from app.models.catalog import Category, Product
from app.models.orders import Order, OrderItem


def create_missing_tables() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_missing_tables()
