import { useEffect, useState } from "react";
import ProductForm from "../components/products/ProductForm";
import StockAdjustmentDialog from "../components/products/StockAdjustmentDialog";
import ProductsTable from "../components/products/ProductsTable";
import { getApiErrorMessage } from "../services/api";
import {
  createProduct,
  deleteProduct,
  getProducts,
  updateProduct,
} from "../services/productService";
import type {
  Product,
  ProductInput,
  StockAdjustment,
} from "../services/productService";
import "./Products.css";

function Products() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [adjustingProduct, setAdjustingProduct] = useState<Product | null>(
    null,
  );

  useEffect(() => {
    let active = true;

    getProducts()
      .then((result) => {
        if (active) {
          setProducts(result);
        }
      })
      .catch((error: unknown) => {
        if (active) {
          setErrorMessage(
            getApiErrorMessage(error, "Unable to load your products."),
          );
        }
      })
      .finally(() => {
        if (active) {
          setIsLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  function openCreateForm() {
    setEditingProduct(null);
    setIsFormOpen(true);
  }

  function openEditForm(product: Product) {
    setEditingProduct(product);
    setIsFormOpen(true);
  }

  async function handleSave(productData: ProductInput) {
    let savedProduct: Product;
    if (editingProduct) {
      savedProduct = await updateProduct(editingProduct.id, productData);
      setProducts((current) =>
        current.map((item) =>
          item.id === savedProduct.id ? savedProduct : item,
        ),
      );
    } else {
      savedProduct = await createProduct(productData);
      setProducts((current) => [savedProduct, ...current]);
    }

    setErrorMessage("");
    setIsFormOpen(false);
    setEditingProduct(null);
  }

  async function handleDelete(product: Product) {
    if (
      !window.confirm(
        `Delete "${product.name}"? This action cannot be undone.`,
      )
    ) {
      return;
    }

    setErrorMessage("");
    try {
      await deleteProduct(product.id);
      setProducts((current) =>
        current.filter((item) => item.id !== product.id),
      );
    } catch (error: unknown) {
      setErrorMessage(
        getApiErrorMessage(error, "Unable to delete this product."),
      );
    }
  }

  function handleStockAdjusted(adjustment: StockAdjustment) {
    setProducts((current) =>
      current.map((product) =>
        product.id === adjustment.product_id
          ? {
              ...product,
              quantity_on_hand: adjustment.quantity_after,
              is_low_stock:
                product.effective_low_stock_threshold !== null &&
                adjustment.quantity_after <=
                  product.effective_low_stock_threshold,
            }
          : product,
      ),
    );
  }

  return (
    <section className="products-page">
      <header className="products-page-heading">
        <div>
          <h1>Products</h1>
          <p>Manage your catalog and keep stock levels up to date.</p>
        </div>
        <button
          className="products-add-button"
          type="button"
          onClick={openCreateForm}
        >
          <span aria-hidden="true">+</span>
          Add product
        </button>
      </header>

      {errorMessage && (
        <p className="products-page-error" role="alert">
          {errorMessage}
        </p>
      )}

      <section className="products-list-card" aria-labelledby="product-list-title">
        <header className="products-list-heading">
          <div>
            <h2 id="product-list-title">All products</h2>
            <span>{isLoading || errorMessage ? "—" : products.length}</span>
          </div>
          <p>Product details and current stock</p>
        </header>
        {isLoading ? (
          <p className="products-loading" role="status">
            Loading products...
          </p>
        ) : errorMessage && products.length === 0 ? (
          <p className="products-loading" role="status">
            Products aren’t available right now.
          </p>
        ) : (
          <ProductsTable
            products={products}
            onEdit={openEditForm}
            onDelete={handleDelete}
            onAdjustStock={setAdjustingProduct}
          />
        )}
      </section>

      {isFormOpen && (
        <ProductForm
          key={editingProduct?.id ?? "new-product"}
          product={editingProduct}
          onCancel={() => setIsFormOpen(false)}
          onSave={handleSave}
        />
      )}
      {adjustingProduct && (
        <StockAdjustmentDialog
          product={adjustingProduct}
          onClose={() => setAdjustingProduct(null)}
          onAdjusted={handleStockAdjusted}
        />
      )}
    </section>
  );
}

export default Products;