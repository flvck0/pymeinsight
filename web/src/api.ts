export interface Product {
  id: number;
  sku: string;
  name: string;
  stock: number;
  minStock: number;
  priceClp: number;
  lowStock: boolean;
}

export interface DayForecast {
  date: string;
  units: number;
}

export interface Forecast {
  sku: string | null;
  horizon_days: number;
  predictions: DayForecast[];
}

export type ProductInput = Omit<Product, "id" | "lowStock">;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    throw new Error(`No se pudo completar la acción (código ${res.status}).`);
  }
  return res.status === 204 ? (undefined as T) : res.json();
}

export const api = {
  list: () => request<Product[]>("/api/products"),
  create: (p: ProductInput) =>
    request<Product>("/api/products", { method: "POST", body: JSON.stringify(p) }),
  forecast: (sku: string) =>
    request<Forecast>(`/ml/forecast/demo/${encodeURIComponent(sku)}?horizon_days=7`),
  remove: (id: number) => request<void>(`/api/products/${id}`, { method: "DELETE" }),
};
