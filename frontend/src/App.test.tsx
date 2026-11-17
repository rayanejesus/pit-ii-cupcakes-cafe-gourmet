import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import App from "./App";

vi.mock("./services/api", () => ({
  api: {
    products: vi.fn().mockResolvedValue([{ id: 1, name: "Red Velvet", description: "Delicioso", price: "18.90", stock: 5, image_url: "image", ingredients: "cacau", allergens: "leite", available: true, category_id: 1, category: { id: 1, name: "Cupcakes" } }]),
    categories: vi.fn().mockResolvedValue([{ id: 1, name: "Cupcakes" }]),
    createOrder: vi.fn().mockResolvedValue({ id: 1, subtotal: "18.90", shipping: "8.50", total: "27.40", status: "AGUARDANDO_PAGAMENTO", items: [] }),
  },
}));

beforeEach(() => vi.stubGlobal("localStorage", { getItem: () => null, setItem: () => undefined, clear: () => undefined }));
describe("customer storefront", () => {
  it("renders products and filters by search", async () => {
    render(<App />);
    expect(await screen.findByText("Red Velvet")).toBeInTheDocument();
    expect(screen.getByAltText("Fotografia de Red Velvet")).toHaveAttribute("src", "/images/products/red-velvet.jpg");
    fireEvent.change(screen.getByLabelText("Buscar produtos"), { target: { value: "inexistente" } });
    await waitFor(() => expect(screen.queryByText("Red Velvet")).not.toBeInTheDocument());
    expect(screen.getByText("Nenhum produto encontrado")).toBeInTheDocument();
  });
  it("adds a product to cart", async () => {
    render(<App />);
    fireEvent.click(await screen.findByText("Adicionar"));
    expect(screen.getByLabelText("Abrir carrinho")).toHaveTextContent("1");
  });
  it("changes and removes quantities from the cart", async () => {
    render(<App />);
    fireEvent.click(await screen.findByText("Adicionar"));
    fireEvent.click(screen.getByLabelText("Abrir carrinho"));
    fireEvent.click(screen.getByLabelText("Aumentar Red Velvet"));
    const quantityControls = screen.getByLabelText("Aumentar Red Velvet").parentElement;
    expect(quantityControls).toHaveTextContent("2");
    fireEvent.click(screen.getByLabelText("Diminuir Red Velvet"));
    expect(quantityControls).toHaveTextContent("1");
    fireEvent.click(screen.getByLabelText("Remover Red Velvet"));
    expect(screen.getByText("Seu carrinho está vazio.")).toBeInTheDocument();
  });
  it("reviews and confirms an order once", async () => {
    render(<App />);
    fireEvent.click(await screen.findByText("Adicionar"));
    fireEvent.click(screen.getByLabelText("Abrir carrinho"));
    fireEvent.change(screen.getByPlaceholderText("Nome completo"), { target: { value: "Ana Souza" } });
    fireEvent.change(screen.getByPlaceholderText("E-mail"), { target: { value: "ana@example.com" } });
    fireEvent.change(screen.getByPlaceholderText("Endereço de entrega"), { target: { value: "Rua das Flores, 10" } });
    fireEvent.click(screen.getByText("Revisar pedido"));
    expect(screen.getByText("Revise seu pedido")).toBeInTheDocument();
    expect(screen.getByText("Taxa de entrega")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /Confirmar pedido/ }));
    await waitFor(() => expect(screen.getByText("Número do pedido: #1")).toBeInTheDocument());
  });
});
