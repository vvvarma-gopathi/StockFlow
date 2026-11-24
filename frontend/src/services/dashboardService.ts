import { api } from "./api";
import type { Product } from "./productService";

export interface DashboardSummary {
  total_products: number;
  total_quantity: number;
  low_stock_items: Product[];
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  const response = await api.get<DashboardSummary>("/dashboard/summary");
  return response.data;
}
