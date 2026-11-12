import { FormEvent, useEffect, useState } from "react";
import { api, Product, ProductInput } from "./api";

const clp = new Intl.NumberFormat("es-CL", {
  style: "currency",
  currency: "CLP",
  maximumFractionDigits: 0,
});

const emptyForm: ProductInput = { sku: "", name: "", stock: 0, minStock: 0, priceClp: 0 };

export default function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [form, setForm] = useState<ProductInput>(emptyForm);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      setProducts(await api.list());
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await api.create(form);
      setForm(emptyForm);
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const onDelete = async (id: number) => {
    try {
      await api.remove(id);
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const low = products.filter((p) => p.lowStock).length;

  return (
    <main className="shell">
      <header className="masthead">
        <h1>PymeInsight</h1>
        <p className="summary">
          {loading
            ? "Cargando inventario…"
            : products.length === 0
            ? "Aún no hay productos. Agrega el primero en el formulario."
            : low === 0
            ? `Tienes ${products.length} productos y todos tienen stock suficiente.`
            : `Tienes ${products.length} productos y ${low} necesitan reposición.`}
        </p>
      </header>

      {error && (
        <p role="alert" className="error">
          {error}
        </p>
      )}

      <div className="layout">
        <section aria-labelledby="inv-title">
          <h2 id="inv-title">Inventario</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Stock</th>
                  <th className="num">Precio</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {products.map((p) => (
                  <tr key={p.id} className={p.lowStock ? "low" : undefined}>
                    <td>
                      <strong>{p.name}</strong>
                      <span className="sku">{p.sku}</span>
                    </td>
                    <td>
                      <div className="gauge" aria-hidden="true">
                        <span
                          style={{
                            width: `${Math.min(100, (p.stock / Math.max(p.minStock * 2, 1)) * 100)}%`,
                          }}
                        />
                      </div>
                      {p.stock} de mínimo {p.minStock}
                      {p.lowStock && <em className="flag">Reponer</em>}
                    </td>
                    <td className="num">{clp.format(p.priceClp)}</td>
                    <td>
                      <button className="ghost" onClick={() => onDelete(p.id)}>
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <aside aria-labelledby="new-title">
          <h2 id="new-title">Nuevo producto</h2>
          <form onSubmit={onSubmit}>
            <label>
              Código (SKU)
              <input required value={form.sku} onChange={(e) => setForm({ ...form, sku: e.target.value })} />
            </label>
            <label>
              Nombre
              <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </label>
            <div className="pair">
              <label>
                Stock
                <input type="number" min={0} required value={form.stock}
                  onChange={(e) => setForm({ ...form, stock: Number(e.target.value) })} />
              </label>
              <label>
                Stock mínimo
                <input type="number" min={0} required value={form.minStock}
                  onChange={(e) => setForm({ ...form, minStock: Number(e.target.value) })} />
              </label>
            </div>
            <label>
              Precio en pesos
              <input type="number" min={0} required value={form.priceClp}
                onChange={(e) => setForm({ ...form, priceClp: Number(e.target.value) })} />
            </label>
            <button type="submit">Guardar producto</button>
          </form>
        </aside>
      </div>
    </main>
  );
}
