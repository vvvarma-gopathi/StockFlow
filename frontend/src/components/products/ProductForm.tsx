import { useState } from "react";
import type { FormEvent } from "react";
import { getApiErrorMessage } from "../../services/api";
import type { Product, ProductInput } from "../../services/productService";
import "./ProductForm.css";

interface ProductFormProps {
  product: Product | null;
  onCancel: () => void;
  onSave: (product: ProductInput) => Promise<void>;
}

function ProductForm({ product, onCancel, onSave }: ProductFormProps) {
  const [name, setName] = useState(product?.name ?? "");
  const [sku, setSku] = useState(product?.sku ?? "");
  const [description, setDescription] = useState(product?.description ?? "");
  const [quantity, setQuantity] = useState(
    String(product?.quantity_on_hand ?? 0),
  );
  const [costPrice, setCostPrice] = useState(
    product?.cost_price === null || product?.cost_price === undefined
      ? ""
      : String(product.cost_price),
  );
  const [sellingPrice, setSellingPrice] = useState(
    product?.selling_price === null || product?.selling_price === undefined
      ? ""
      : String(product.selling_price),
  );
  const [lowStockThreshold, setLowStockThreshold] = useState(
    product?.low_stock_threshold === null ||
      product?.low_stock_threshold === undefined
      ? ""
      : String(product.low_stock_threshold),
  );
  const [isSaving, setIsSaving] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage("");
    setIsSaving(true);

    try {
      await onSave({
        name: name.trim(),
        sku: sku.trim(),
        description: description.trim() || null,
        quantity_on_hand: Number(quantity),
        cost_price: costPrice.trim() ? Number(costPrice) : null,
        selling_price: sellingPrice.trim() ? Number(sellingPrice) : null,
        low_stock_threshold: lowStockThreshold.trim()
          ? Number(lowStockThreshold)
          : null,
      });
    } catch (error: unknown) {
      setErrorMessage(
        getApiErrorMessage(error, "Unable to save this product. Try again."),
      );
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div
      className="product-dialog-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget && !isSaving) {
          onCancel();
        }
      }}
    >
      <section
        className="product-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="product-form-title"
      >
        <header className="product-dialog-header">
          <div>
            <p className="product-dialog-eyebrow">
              {product ? "PRODUCT DETAILS" : "NEW PRODUCT"}
            </p>
            <h2 id="product-form-title">
              {product ? "Edit product" : "Add a product"}
            </h2>
          </div>
          <button
            className="product-dialog-close"
            type="button"
            onClick={onCancel}
            disabled={isSaving}
            aria-label="Close product form"
          >
            ×
          </button>
        </header>

        <form className="product-form" onSubmit={handleSubmit}>
          <div className="product-form-grid">
            <label className="product-form-field product-form-wide">
              Product name
              <input
                autoFocus
                name="name"
                type="text"
                maxLength={255}
                value={name}
                onChange={(event) => setName(event.target.value)}
                required
              />
            </label>
            <label className="product-form-field">
              SKU
              <input
                name="sku"
                type="text"
                maxLength={100}
                value={sku}
                onChange={(event) => setSku(event.target.value)}
                required
              />
            </label>
            <label className="product-form-field">
              Quantity on hand
              <input
                name="quantity"
                type="number"
                min={0}
                step={1}
                value={quantity}
                onChange={(event) => setQuantity(event.target.value)}
                required
              />
            </label>
            <label className="product-form-field product-form-wide">
              Description <span>(optional)</span>
              <textarea
                name="description"
                rows={3}
                maxLength={5000}
                value={description}
                onChange={(event) => setDescription(event.target.value)}
              />
            </label>
            <label className="product-form-field">
              Cost price <span>(optional)</span>
              <input
                name="costPrice"
                type="number"
                min={0}
                step="0.01"
                value={costPrice}
                onChange={(event) => setCostPrice(event.target.value)}
              />
            </label>
            <label className="product-form-field">
              Selling price <span>(optional)</span>
              <input
                name="sellingPrice"
                type="number"
                min={0}
                step="0.01"
                value={sellingPrice}
                onChange={(event) => setSellingPrice(event.target.value)}
              />
            </label>
            <label className="product-form-field product-form-wide">
              Low-stock threshold <span>(optional)</span>
              <input
                name="lowStockThreshold"
                type="number"
                min={0}
                step={1}
                value={lowStockThreshold}
                onChange={(event) =>
                  setLowStockThreshold(event.target.value)
                }
              />
              <small>
                Leave blank to use the organization default when enabled.
              </small>
            </label>
          </div>

          {errorMessage && (
            <p className="product-form-error" role="alert">
              {errorMessage}
            </p>
          )}

          <footer className="product-form-actions">
            <button
              className="product-button product-button-secondary"
              type="button"
              onClick={onCancel}
              disabled={isSaving}
            >
              Cancel
            </button>
            <button
              className="product-button product-button-primary"
              type="submit"
              disabled={isSaving}
            >
              {isSaving ? "Saving..." : product ? "Save changes" : "Add product"}
            </button>
          </footer>
        </form>
      </section>
    </div>
  );
}

export default ProductForm;
