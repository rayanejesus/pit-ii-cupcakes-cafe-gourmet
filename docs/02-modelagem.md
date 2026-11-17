# 2. Modelagem conceitual, lógica e física

## Diagrama de classes

```mermaid
classDiagram
  Category "1" --> "N" Product
  Order "1" *-- "N" OrderItem
  Product "1" --> "N" OrderItem
  class Category { +id: int +name: string }
  class Product { +id: int +name: string +price: decimal +stock: int +available: boolean }
  class Order { +id: int +customerName: string +total: decimal +status: OrderStatus }
  class OrderItem { +quantity: int +unitPrice: decimal }
```

## DER

```mermaid
erDiagram
  CATEGORIES ||--o{ PRODUCTS : contains
  ORDERS ||--|{ ORDER_ITEMS : has
  PRODUCTS ||--o{ ORDER_ITEMS : referenced_by
  CATEGORIES { INTEGER id PK TEXT name UK }
  PRODUCTS { INTEGER id PK INTEGER category_id FK TEXT name NUMERIC price INTEGER stock }
  ORDERS { INTEGER id PK TEXT customer_email NUMERIC total TEXT status }
  ORDER_ITEMS { INTEGER id PK INTEGER order_id FK INTEGER product_id FK INTEGER quantity }
```

O modelo está normalizado até a terceira forma normal: dados de categoria não são repetidos nos produtos, e itens de pedido preservam o nome/preço histórico para manter a integridade comercial mesmo se o catálogo mudar. O projeto físico está em [`database/schema.sql`](../database/schema.sql) e é materializado via SQLAlchemy com SQLite e foreign keys habilitadas.
