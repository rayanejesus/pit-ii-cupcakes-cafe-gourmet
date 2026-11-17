import type { Category, Order, Product } from "../types/catalog";

export function normalizeApiUrl(configuredUrl: string | undefined, isDevelopment: boolean): string {
  const value = configuredUrl?.trim();
  if (!value) return isDevelopment ? "http://localhost:8000/api" : "";
  return value.replace(/\/+$/, "").endsWith("/api")
    ? value.replace(/\/+$/, "")
    : `${value.replace(/\/+$/, "")}/api`;
}

const API_URL = normalizeApiUrl(import.meta.env.VITE_API_URL, import.meta.env.DEV);

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  if (!API_URL) throw new Error("VITE_API_URL não está configurada.");
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
