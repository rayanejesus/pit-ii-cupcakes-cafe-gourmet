import { useEffect, useMemo, useState } from "react";
import { Coffee, Minus, Plus, Search, ShoppingBag, Trash2 } from "lucide-react";
import { api } from "./services/api";
import type { CartItem, Category, Order, Product } from "./types/catalog";
import "./index.css";

const SHIPPING_FEE = 8.5;
const FALLBACK_IMAGE = "/images/products/red-velvet.jpg";
const PRODUCT_IMAGES: Record<string, string> = {
  "Red Velvet": "/images/products/red-velvet.jpg",
  "Chocolate Trufado": "/images/products/chocolate-trufado.jpg",
  "Baunilha com Morango": "/images/products/baunilha-morango.jpg",
  "Cenoura com Brigadeiro": "/images/products/cenoura-brigadeiro.jpg",
  "Doce de Leite": "/images/products/doce-leite.jpg",
  "Limão Siciliano": "/images/products/limao-siciliano.jpg",
  "Espresso Gourmet": "/images/products/espresso-gourmet.jpg",
  "Cappuccino Cremoso": "/images/products/cappuccino-cremoso.jpg",
  "Latte de Baunilha": "/images/products/latte-baunilha.jpg",
  "Café Especial Coado": "/images/products/cafe-especial-coado.jpg",
};
const money = (value: string | number) => `R$ ${Number(value).toFixed(2).replace(".", ",")}`;
type CheckoutStep = "cart" | "review";
type CheckoutData = { name: string; email: string; address: string; payment: "PIX" | "CARTAO" };

function createIdempotencyKey() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) return crypto.randomUUID();
  return `order-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

function productImage(product: Product) {
  return PRODUCT_IMAGES[product.name] ?? product.image_url ?? FALLBACK_IMAGE;
}

export default function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [cart, setCart] = useState<CartItem[]>(() => JSON.parse(localStorage.getItem("cart") ?? "[]"));
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [message, setMessage] = useState("");
  const [checkout, setCheckout] = useState<CheckoutStep | null>(null);
  const [checkoutData, setCheckoutData] = useState<CheckoutData | null>(null);
  const [idempotencyKey, setIdempotencyKey] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [confirmation, setConfirmation] = useState<Order | null>(null);

  useEffect(() => {
    Promise.all([api.products(), api.categories()])
      .then(([items, cats]) => { setProducts(items); setCategories(cats); })
      .catch(error => setMessage(error.message));
  }, []);
  useEffect(() => localStorage.setItem("cart", JSON.stringify(cart)), [cart]);

  const subtotal = useMemo(
    () => cart.reduce((total, item) => total + Number(item.product.price) * item.quantity, 0),
    [cart],
  );
  const total = subtotal + SHIPPING_FEE;
  const add = (product: Product) => setCart(items => {
    const found = items.find(item => item.product.id === product.id);
    return found
      ? items.map(item => item.product.id === product.id ? { ...item, quantity: item.quantity + 1 } : item)
      : [...items, { product, quantity: 1 }];
  });
  const decrease = (productId: number) => setCart(items => items.flatMap(item => {
    if (item.product.id !== productId) return [item];
    return item.quantity > 1 ? [{ ...item, quantity: item.quantity - 1 }] : [];
  }));
  const remove = (productId: number) => setCart(items => items.filter(item => item.product.id !== productId));

  const startCheckout = () => {
    setMessage("");
    setCheckout("cart");
  };
  const reviewOrder = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    setCheckoutData({
      name: String(data.get("name") ?? ""),
      email: String(data.get("email") ?? ""),
      address: String(data.get("address") ?? ""),
      payment: data.get("payment") === "CARTAO" ? "CARTAO" : "PIX",
    });
    setIdempotencyKey(createIdempotencyKey());
    setCheckout("review");
  };
  const confirmOrder = async () => {
    if (!checkoutData || submitting || cart.length === 0) return;
    setSubmitting(true);
    try {
      const order = await api.createOrder({
        customer_name: checkoutData.name,
        customer_email: checkoutData.email,
        address: checkoutData.address,
        payment_method: checkoutData.payment,
        items: cart.map(item => ({ product_id: item.product.id, quantity: item.quantity })),
      }, idempotencyKey);
      setCart([]);
      setCheckout(null);
      setCheckoutData(null);
      setConfirmation(order);
      setMessage("");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Erro ao criar pedido.");
    } finally {
      setSubmitting(false);
    }
  };
  const filtered = products.filter(product =>
    (!search || product.name.toLowerCase().includes(search.toLowerCase()))
    && (!category || product.category_id === Number(category)),
  );

  return <div className="min-h-screen bg-cream text-espresso">
    <header className="sticky top-0 z-10 bg-espresso text-white shadow-lg"><div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4">
      <div className="flex items-center gap-2"><Coffee className="text-pink" /><span className="text-xl font-bold">Grão & Doçura</span></div>
      <button className="relative" aria-label="Abrir carrinho" onClick={startCheckout}><ShoppingBag /><span className="absolute -right-2 -top-2 rounded-full bg-orange px-2 text-xs">{cart.length}</span></button>
    </div></header>
    <main className="mx-auto max-w-6xl px-5 py-10"><section className="mb-10 rounded-3xl bg-pink p-8"><p className="mb-2 font-semibold text-orange">CAFÉ ARTESANAL • DOCES ESPECIAIS</p><h1 className="max-w-xl text-4xl font-black md:text-6xl">Pequenos momentos, grandes sabores.</h1><p className="mt-4 max-w-xl">Cupcakes feitos à mão e cafés selecionados para transformar sua pausa.</p></section>
      <div className="mb-8 flex flex-wrap gap-3"><label className="flex flex-1 items-center gap-2 rounded-xl bg-white px-4 py-3 shadow-sm"><Search size={18}/><input aria-label="Buscar produtos" className="w-full outline-none" placeholder="Buscar sabores..." value={search} onChange={event => setSearch(event.target.value)} /></label>{categories.map(cat => <button key={cat.id} className={`rounded-xl px-4 py-2 ${category === String(cat.id) ? "bg-orange text-white" : "bg-white"}`} onClick={() => setCategory(category === String(cat.id) ? "" : String(cat.id))}>{cat.name}</button>)}</div>
      {filtered.length === 0 ? <div className="rounded-2xl bg-white p-8 text-center shadow-sm"><h2 className="text-xl font-bold">Nenhum produto encontrado</h2><p className="mt-2 text-gray-600">Tente buscar outro sabor ou remover o filtro de categoria.</p></div> : <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{filtered.map(product => <article className="overflow-hidden rounded-2xl bg-white shadow-sm" key={product.id}><img className="h-52 w-full object-cover" src={productImage(product)} alt={`Fotografia de ${product.name}`} loading="lazy" onError={event => { event.currentTarget.onerror = null; event.currentTarget.src = FALLBACK_IMAGE; }}/><div className="p-5"><p className="text-sm text-orange">{product.category.name}</p><h2 className="mt-1 text-xl font-bold">{product.name}</h2><p className="my-3 text-sm text-gray-600">{product.description}</p><div className="flex items-center justify-between"><strong>{money(product.price)}</strong><button className="rounded-lg bg-espresso px-4 py-2 text-sm text-white hover:bg-orange" onClick={() => add(product)}>Adicionar</button></div></div></article>)}</div>}
      {confirmation && <div role="status" className="mt-6 rounded-xl bg-pink p-4"><strong>Pedido confirmado com sucesso!</strong><p>Número do pedido: #{confirmation.id}</p><p>Status inicial: {confirmation.status === "AGUARDANDO_PAGAMENTO" ? "Aguardando pagamento" : confirmation.status}</p><div className="mt-2">{confirmation.items.map(item => <p key={`${item.product_name}-${item.quantity}`}>{item.quantity}x {item.product_name}</p>)}</div><p className="mt-2 font-bold">Total: {money(confirmation.total)}</p><p className="text-sm">Pagamento pendente (simulado).</p></div>}
      {message && <p role="alert" className="mt-6 rounded-xl bg-pink p-4">{message}</p>}
    </main>
    {checkout && <div className="fixed inset-0 z-20 overflow-auto bg-black/50 p-4"><div className="mx-auto mt-10 max-w-lg rounded-2xl bg-white p-6">
      <div className="flex justify-between"><h2 className="text-2xl font-bold">{checkout === "review" ? "Revise seu pedido" : "Seu pedido"}</h2><button onClick={() => setCheckout(null)}>Fechar</button></div>
      {cart.length === 0 ? <p className="py-8">Seu carrinho está vazio.</p> : checkout === "review" && checkoutData ? <div className="space-y-4">
        <div className="rounded-xl bg-cream p-4"><h3 className="font-bold">Produtos</h3>{cart.map(item => <p key={item.product.id}>{item.quantity}x {item.product.name} — {money(Number(item.product.price) * item.quantity)}</p>)}</div>
        <div className="rounded-xl bg-cream p-4"><h3 className="font-bold">Entrega</h3><p>{checkoutData.name}</p><p>{checkoutData.email}</p><p>{checkoutData.address}</p><p>Pagamento: {checkoutData.payment === "PIX" ? "Pix (simulado)" : "Cartão (simulado)"}</p></div>
        <Summary subtotal={subtotal} />
        <button className="w-full rounded-xl bg-orange py-3 font-bold text-white disabled:opacity-50" disabled={submitting} onClick={confirmOrder}>{submitting ? "Confirmando..." : `Confirmar pedido • ${money(total)}`}</button>
        <button className="w-full rounded-xl border py-3" disabled={submitting} onClick={() => setCheckout("cart")}>Voltar e editar</button>
      </div> : <><div className="my-5 space-y-3">{cart.map(item => <div className="flex items-center justify-between border-b pb-3" key={item.product.id}><span>{item.product.name}</span><div className="flex items-center gap-2"><button aria-label={`Diminuir ${item.product.name}`} onClick={() => decrease(item.product.id)}><Minus size={16}/></button><span>{item.quantity}</span><button aria-label={`Aumentar ${item.product.name}`} onClick={() => add(item.product)}><Plus size={16}/></button><button aria-label={`Remover ${item.product.name}`} onClick={() => remove(item.product.id)}><Trash2 size={16}/></button></div></div>)}</div><Summary subtotal={subtotal}/><form className="space-y-3" onSubmit={reviewOrder}><input required name="name" className="field" placeholder="Nome completo"/><input required name="email" type="email" className="field" placeholder="E-mail"/><input required name="address" className="field" placeholder="Endereço de entrega"/><select name="payment" className="field"><option value="PIX">Pix (simulado)</option><option value="CARTAO">Cartão (simulado)</option></select><button className="w-full rounded-xl bg-orange py-3 font-bold text-white">Revisar pedido</button></form></>}
    </div></div>}
  </div>;
}

function Summary({ subtotal }: { subtotal: number }) {
  return <div className="space-y-1 border-t py-3"><p className="flex justify-between">Subtotal <span>{money(subtotal)}</span></p><p className="flex justify-between">Taxa de entrega <span>{money(SHIPPING_FEE)}</span></p><p className="flex justify-between text-lg font-bold">Total <span>{money(subtotal + SHIPPING_FEE)}</span></p></div>;
}
