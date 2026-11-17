import { useEffect, useMemo, useState } from "react";
import { Coffee, ShoppingBag, Search, Trash2 } from "lucide-react";
import { api } from "./services/api";
import type { CartItem, Category, Product } from "./types/catalog";
import "./index.css";

const money = (value: string | number) => `R$ ${Number(value).toFixed(2).replace(".", ",")}`;

export default function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [cart, setCart] = useState<CartItem[]>(() => JSON.parse(localStorage.getItem("cart") ?? "[]"));
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [checkout, setCheckout] = useState(false);

  useEffect(() => { Promise.all([api.products(), api.categories()]).then(([items, cats]) => { setProducts(items); setCategories(cats); }).catch(error => setMessage(error.message)); }, []);
  useEffect(() => localStorage.setItem("cart", JSON.stringify(cart)), [cart]);
  const subtotal = useMemo(() => cart.reduce((total, item) => total + Number(item.product.price) * item.quantity, 0), [cart]);
  const add = (product: Product) => setCart(items => {
    const found = items.find(item => item.product.id === product.id);
    return found ? items.map(item => item.product.id === product.id ? { ...item, quantity: item.quantity + 1 } : item) : [...items, { product, quantity: 1 }];
  });
  const placeOrder = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    try {
      const order = await api.createOrder({ customer_name: data.get("name"), customer_email: data.get("email"), address: data.get("address"), payment_method: data.get("payment"), items: cart.map(item => ({ product_id: item.product.id, quantity: item.quantity })) });
      setCart([]); setCheckout(false); setMessage(`Pedido #${order.id} criado! Total: ${money(order.total)}. Pagamento pendente.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Erro ao criar pedido."); }
  };
  const filtered = products.filter(product => !search || product.name.toLowerCase().includes(search.toLowerCase()));
  return <div className="min-h-screen bg-cream text-espresso">
    <header className="sticky top-0 z-10 bg-espresso text-white shadow-lg"><div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4">
      <div className="flex items-center gap-2"><Coffee className="text-pink" /><span className="text-xl font-bold">Grão & Doçura</span></div>
      <button className="relative" aria-label="Abrir carrinho" onClick={() => setCheckout(true)}><ShoppingBag /><span className="absolute -right-2 -top-2 rounded-full bg-orange px-2 text-xs">{cart.length}</span></button>
    </div></header>
    <main className="mx-auto max-w-6xl px-5 py-10"><section className="mb-10 rounded-3xl bg-pink p-8"><p className="mb-2 font-semibold text-orange">CAFÉ ARTESANAL • DOCES ESPECIAIS</p><h1 className="max-w-xl text-4xl font-black md:text-6xl">Pequenos momentos, grandes sabores.</h1><p className="mt-4 max-w-xl">Cupcakes feitos à mão e cafés selecionados para transformar sua pausa.</p></section>
      <div className="mb-8 flex flex-wrap gap-3"><label className="flex flex-1 items-center gap-2 rounded-xl bg-white px-4 py-3 shadow-sm"><Search size={18}/><input aria-label="Buscar produtos" className="w-full outline-none" placeholder="Buscar sabores..." value={search} onChange={event => setSearch(event.target.value)} /></label>{categories.map(cat => <button key={cat.id} className={`rounded-xl px-4 py-2 ${category === String(cat.id) ? "bg-orange text-white" : "bg-white"}`} onClick={() => setCategory(category === String(cat.id) ? "" : String(cat.id))}>{cat.name}</button>)}</div>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{filtered.filter(product => !category || product.category_id === Number(category)).map(product => <article className="overflow-hidden rounded-2xl bg-white shadow-sm" key={product.id}><img className="h-52 w-full object-cover" src={product.image_url} alt={product.name}/><div className="p-5"><p className="text-sm text-orange">{product.category.name}</p><h2 className="mt-1 text-xl font-bold">{product.name}</h2><p className="my-3 text-sm text-gray-600">{product.description}</p><div className="flex items-center justify-between"><strong>{money(product.price)}</strong><button className="rounded-lg bg-espresso px-4 py-2 text-sm text-white hover:bg-orange" onClick={() => add(product)}>Adicionar</button></div></div></article>)}</div>
      {message && <p role="status" className="mt-6 rounded-xl bg-pink p-4">{message}</p>}
    </main>
    {checkout && <div className="fixed inset-0 z-20 overflow-auto bg-black/50 p-4"><div className="mx-auto mt-10 max-w-lg rounded-2xl bg-white p-6"><div className="flex justify-between"><h2 className="text-2xl font-bold">Seu pedido</h2><button onClick={() => setCheckout(false)}>Fechar</button></div>{cart.length === 0 ? <p className="py-8">Seu carrinho está vazio.</p> : <><div className="my-5 space-y-3">{cart.map(item => <div className="flex items-center justify-between border-b pb-2" key={item.product.id}><span>{item.quantity}x {item.product.name}</span><button aria-label={`Remover ${item.product.name}`} onClick={() => setCart(items => items.filter(current => current.product.id !== item.product.id))}><Trash2 size={16}/></button></div>)}</div><p className="mb-4 text-right text-lg font-bold">Subtotal: {money(subtotal)}</p><form className="space-y-3" onSubmit={placeOrder}><input required name="name" className="field" placeholder="Nome completo"/><input required name="email" type="email" className="field" placeholder="E-mail"/><input required name="address" className="field" placeholder="Endereço de entrega"/><select name="payment" className="field"><option value="PIX">Pix (simulado)</option><option value="CARTAO">Cartão (simulado)</option></select><button className="w-full rounded-xl bg-orange py-3 font-bold text-white">Confirmar pedido • {money(subtotal + 8.5)}</button></form></>}</div></div>}
  </div>;
}
