import type { Category, Order, Product } from "../types/catalog";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";
async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { headers: { "Content-Type": "application/json" }, ...options });
  if (!response.ok) throw new Error((await response.json()).detail ?? "Não foi possível concluir a operação.");
  return response.json();
}
export const api = {
  products: (search = "", categoryId = "") => request<Product[]>(`/products?search=${encodeURIComponent(search)}${categoryId ? `&category_id=${categoryId}` : ""}`),
  categories: () => request<Category[]>("/categories"),
  createOrder: (payload: unknown) => request<Order>("/orders", { method: "POST", body: JSON.stringify(payload) }),
  orders: (email: string) => request<Order[]>(`/orders?email=${encodeURIComponent(email)}`),
};
