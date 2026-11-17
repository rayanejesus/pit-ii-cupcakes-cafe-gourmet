import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import App from "./App";

vi.mock("./services/api", () => ({
  api: {
    products: vi.fn().mockResolvedValue([{ id: 1, name: "Red Velvet", description: "Delicioso", price: "18.90", stock: 5, image_url: "image", ingredients: "cacau", allergens: "leite", available: true, category_id: 1, category: { id: 1, name: "Cupcakes" } }]),
    categories: vi.fn().mockResolvedValue([{ id: 1, name: "Cupcakes" }]),
    createOrder: vi.fn().mockResolvedValue({ id: 1, total: "27.40" }),
  },
}));

beforeEach(() => vi.stubGlobal("localStorage", { getItem: () => null, setItem: () => undefined, clear: () => undefined }));
describe("customer storefront", () => {
  it("renders products and filters by search", async () => {
    render(<App />);
    expect(await screen.findByText("Red Velvet")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Buscar produtos"), { target: { value: "inexistente" } });
    await waitFor(() => expect(screen.queryByText("Red Velvet")).not.toBeInTheDocument());
  });
  it("adds a product to cart", async () => {
    render(<App />);
    fireEvent.click(await screen.findByText("Adicionar"));
    expect(screen.getByLabelText("Abrir carrinho")).toHaveTextContent("1");
  });
});
