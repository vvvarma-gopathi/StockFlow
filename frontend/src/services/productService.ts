import { api } from "./api";

export interface Product {
  id: number;
  organization_id: number;
  name: string;
  sku: string;
  description: string | null;
  quantity_on_hand: number;
  cost_price: number | string | null;
  selling_price: number | string | null;
  low_stock_threshold: number | null;
  effective_low_stock_threshold: number;
  is_low_stock: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductInput {
  name: string;
  sku: string;
  description: string | null;
  quantity_on_hand: number;
  cost_price: number | null;
  selling_price: number | null;
  low_stock_threshold: number | null;
}

export async function getProducts(): Promise<Product[]> {
  const response = await api.get<Product[]>("/products");
  return response.data;
}

export async function createProduct(
  product: ProductInput,
): Promise<Product> {
  const response = await api.post<Product>("/products", product);
  return response.data;
}

export async function updateProduct(
  productId: number,
  product: ProductInput,
): Promise<Product> {
  const response = await api.put<Product>(`/products/${productId}`, product);
  return response.data;
}

export async function deleteProduct(productId: number): Promise<void> {
  await api.delete(`/products/${productId}`);
}