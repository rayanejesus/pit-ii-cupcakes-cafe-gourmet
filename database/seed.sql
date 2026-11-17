PRAGMA foreign_keys = ON;
INSERT OR IGNORE INTO categories (name) VALUES ('Cupcakes'), ('Cafés');
INSERT OR IGNORE INTO products (category_id,name,description,price,stock,image_url,ingredients,allergens) VALUES
(1,'Red Velvet','Massa red velvet com cobertura cremosa.',18.90,20,'https://images.unsplash.com/photo-1551024601-bec78aea704b','cacau, farinha, cream cheese','glúten, leite'),
(1,'Chocolate Trufado','Chocolate intenso com ganache.',19.90,20,'https://images.unsplash.com/photo-1551024506-0bccd828d307','cacau, chocolate, farinha','glúten, leite, ovos'),
(2,'Espresso Gourmet','Extraído na hora, encorpado e aromático.',8.90,20,'https://images.unsplash.com/photo-1510707577719-ae7c14805e3a','café especial 100% arábica','não contém');
