import type { Product } from "../../services/productService";
import { formatCurrency } from "../../utils/formatCurrency";
import "./ProductsTable.css";

interface ProductsTableProps {
  products: Product[];
  onEdit: (product: Product) => void;
  onDelete: (product: Product) => void;
  onAdjustStock: (product: Product) => void;
}

function ProductsTable({
  products,
  onEdit,
  onDelete,
  onAdjustStock,
}: ProductsTableProps) {
  if (products.length === 0) {
    return (
      <div className="products-empty">
        <div className="products-empty-icon" aria-hidden="true">
          ◇
        </div>
        <h2>No products yet</h2>
        <p>Add your first product to start tracking inventory.</p>
      </div>
    );
  }

  return (
    <div className="products-table-wrap">
      <table className="products-table">
        <thead>
          <tr>
            <th scope="col">Product</th>
            <th scope="col">SKU</th>
            <th scope="col">Quantity</th>
            <th scope="col">Stock status</th>
            <th scope="col">Selling price</th>
            <th scope="col">
              <span className="visually-hidden">Actions</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id}>
              <td>
                <div className="products-name">{product.name}</div>
                {product.description && (
                  <div className="products-description">
                    {product.description}
                  </div>
                )}
              </td>
              <td className="products-sku">{product.sku}</td>
              <td className="products-quantity">
                {product.quantity_on_hand.toLocaleString("en-IN")}
              </td>
              <td>
                <span
                  className={`stock-indicator${product.is_low_stock ? " low" : ""}`}
                >
                  {product.is_low_stock ? "Low stock" : "In stock"}
                </span>
              </td>
              <td className="products-price">
                {formatCurrency(product.selling_price)}
              </td>
              <td>
                <div className="products-row-actions">
                  <button
                    type="button"
                    onClick={() => onAdjustStock(product)}
                    aria-label={`Adjust stock for ${product.name}`}
                  >
                    Adjust stock
                  </button>
                  <button
                    type="button"
                    onClick={() => onEdit(product)}
                    aria-label={`Edit ${product.name}`}
                  >
                    Edit
                  </button>
                  <button
                    type="button"
                    className="products-delete"
                    onClick={() => onDelete(product)}
                    aria-label={`Delete ${product.name}`}
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProductsTable;
