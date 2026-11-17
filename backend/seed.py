from decimal import Decimal

from sqlalchemy import select

from app.database.connection import Base, SessionLocal, engine
from app.models.catalog import Category, Product
from app.models.orders import Order, OrderItem

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

IMAGE_URLS = {
    "Red Velvet": "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd",
    "Chocolate Trufado": "https://images.unsplash.com/photo-1486427944299-d1955d23e34d",
    "Baunilha com Morango": "https://images.unsplash.com/photo-1587668178277-295251f900ce",
    "Cenoura com Brigadeiro": "https://images.unsplash.com/photo-1519869325930-281384150729",
    "Doce de Leite": "https://images.unsplash.com/photo-1558301211-0d8c8ddee6ec",
    "Limão Siciliano": "https://images.unsplash.com/photo-1603532648955-039310d9ed75",
    "Espresso Gourmet": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",
    "Cappuccino Cremoso": "https://images.unsplash.com/photo-1509042239860-f550ce710b93",
    "Latte de Baunilha": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd",
    "Café Especial Coado": "https://images.unsplash.com/photo-1447933601403-0c6688de566e",
}


def seed():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        for category_name, products in PRODUCTS.items():
            category = db.scalar(select(Category).where(Category.name == category_name))
            if category is None:
                category = Category(name=category_name)
                db.add(category)
                db.flush()
            for name, description, ingredients, allergens, price in products:
                product = db.scalar(
                    select(Product).where(
                        Product.category_id == category.id,
                        Product.name == name,
                    )
                )
                if product is None:
                    db.add(Product(
                        name=name, description=description, price=Decimal(price), stock=20,
                        image_url=f"{IMAGE_URLS[name]}?auto=format&fit=crop&w=800&q=80",
                        ingredients=ingredients, allergens=allergens, available=True, category_id=category.id,
                    ))
                else:
                    product.image_url = f"{IMAGE_URLS[name]}?auto=format&fit=crop&w=800&q=80"
        db.commit()


if __name__ == "__main__":
    seed()
