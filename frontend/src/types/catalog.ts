export type Category = { id: number; name: string };
export type Product = Category & {
  id: number; description: string; price: string; stock: number; image_url: string;
  ingredients: string; allergens: string; available: boolean; category_id: number; category: Category;
};
export type CartItem = { product: Product; quantity: number };
export type Order = {
  id: number;
  subtotal: string;
  shipping: string;
  total: string;
  status: string;
  items: Array<{ product_name: string; quantity: number }>;
};
