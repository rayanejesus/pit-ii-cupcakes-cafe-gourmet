from decimal import Decimal

from sqlalchemy import select

from app.database.connection import Base, SessionLocal, engine
from app.models.catalog import Category, Product

PRODUCTS = {
    "Cupcakes": [
        ("Red Velvet", "Massa red velvet com cobertura cremosa.", "cacau, farinha, cream cheese", "glúten, leite", "18.90"),
        ("Chocolate Trufado", "Chocolate intenso com ganache.", "cacau, chocolate, farinha", "glúten, leite, ovos", "19.90"),
        ("Baunilha com Morango", "Baunilha, morangos e creme leve.", "baunilha, morango, farinha", "glúten, leite", "17.90"),
        ("Cenoura com Brigadeiro", "Massa de cenoura e brigadeiro artesanal.", "cenoura, chocolate, leite condensado", "glúten, leite", "18.50"),
        ("Doce de Leite", "Cupcake de baunilha com doce de leite.", "baunilha, doce de leite", "glúten, leite", "18.50"),
        ("Limão Siciliano", "Massa cítrica com cobertura de limão.", "limão, farinha, açúcar", "glúten, ovos", "17.50"),
    ],
    "Cafés": [
        ("Espresso Gourmet", "Extraído na hora, encorpado e aromático.", "café especial 100% arábica", "não contém", "8.90"),
        ("Cappuccino Cremoso", "Espresso, leite vaporizado e espuma.", "café, leite, canela", "leite", "12.90"),
        ("Latte de Baunilha", "Café suave com leite e baunilha.", "café, leite, baunilha", "leite", "13.90"),
        ("Café Especial Coado", "Método filtrado com notas frutadas.", "café especial 100% arábica", "não contém", "10.90"),
    ],
}


def seed():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.scalar(select(Category)):
            return
        for category_name, products in PRODUCTS.items():
            category = Category(name=category_name)
            db.add(category)
            db.flush()
            for name, description, ingredients, allergens, price in products:
                db.add(Product(
                    name=name, description=description, price=Decimal(price), stock=20,
                    image_url=f"https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=800&q=80",
                    ingredients=ingredients, allergens=allergens, available=True, category_id=category.id,
                ))
        db.commit()


if __name__ == "__main__":
    seed()
