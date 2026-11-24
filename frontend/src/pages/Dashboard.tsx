import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getApiErrorMessage } from "../services/api";
import { getDashboardSummary } from "../services/dashboardService";
import type { DashboardSummary } from "../services/dashboardService";
import { formatCurrency } from "../utils/formatCurrency";
import "./Dashboard.css";

function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    let active = true;

    getDashboardSummary()
      .then((result) => {
        if (active) {
          setSummary(result);
        }
      })
      .catch((error: unknown) => {
        if (active) {
          setErrorMessage(
            getApiErrorMessage(error, "Unable to load dashboard data."),
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

  return (
    <section className="dashboard-page">
      <header className="dashboard-page-heading">
        <div>
          <h1>Dashboard</h1>
          <p>Here’s an overview of your inventory.</p>
        </div>
        <Link className="dashboard-add-button" to="/products">
          <span aria-hidden="true">+</span>
          Add product
        </Link>
      </header>

      {errorMessage && (
        <p className="dashboard-error" role="alert">
          {errorMessage}
        </p>
      )}

      <div className="dashboard-stat-grid">
        <article className="dashboard-stat-card">
          <div className="dashboard-stat-icon products-icon" aria-hidden="true">
            <svg viewBox="0 0 32 32" fill="none">
              <path
                d="m16 3 11 6.2v13.6L16 29 5 22.8V9.2L16 3Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinejoin="round"
              />
              <path
                d="m5.5 9.5 10.5 6 10.5-6M16 15.5V28"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <div>
            <p>Total products</p>
            <strong>
              {summary
                ? summary.total_products.toLocaleString("en-IN")
                : "—"}
            </strong>
            <span>Products in your catalog</span>
          </div>
        </article>

        <article className="dashboard-stat-card">
          <div className="dashboard-stat-icon quantity-icon" aria-hidden="true">
            <svg viewBox="0 0 32 32" fill="none">
              <ellipse
                cx="16"
                cy="7"
                rx="10"
                ry="4"
                stroke="currentColor"
                strokeWidth="2"
              />
              <path
                d="M6 7v18c0 2.2 4.5 4 10 4s10-1.8 10-4V7M6 13c0 2.2 4.5 4 10 4s10-1.8 10-4M6 19c0 2.2 4.5 4 10 4s10-1.8 10-4"
                stroke="currentColor"
                strokeWidth="2"
              />
            </svg>
          </div>
          <div>
            <p>Total quantity</p>
            <strong>
              {summary ? summary.total_quantity.toLocaleString("en-IN") : "—"}
            </strong>
            <span>Units currently in stock</span>
          </div>
        </article>
      </div>

      <section className="dashboard-low-stock" aria-labelledby="low-stock-title">
        <header className="dashboard-low-stock-header">
          <div>
            <h2 id="low-stock-title">Low stock items</h2>
            <p>Products at or below their stock threshold</p>
          </div>
          <Link to="/products">
            View all products <span aria-hidden="true">→</span>
          </Link>
        </header>

        {isLoading ? (
          <p className="dashboard-loading" role="status">
            Loading inventory...
          </p>
        ) : !summary ? (
          <p className="dashboard-loading" role="status">
            Inventory data isn’t available right now.
          </p>
        ) : (
          <div className="dashboard-table-wrap">
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th scope="col">Product</th>
                  <th scope="col">SKU</th>
                  <th scope="col">Quantity</th>
                  <th scope="col">Status</th>
                  <th scope="col">Selling price</th>
                </tr>
              </thead>
              <tbody>
                {summary?.low_stock_items.map((product) => (
                  <tr key={product.id}>
                    <td>{product.name}</td>
                    <td>{product.sku}</td>
                    <td>{product.quantity_on_hand.toLocaleString("en-IN")}</td>
                    <td>
                      <span className="dashboard-low-stock-badge">
                        Low stock
                      </span>
                    </td>
                    <td>{formatCurrency(product.selling_price)}</td>
                  </tr>
                ))}
                {summary?.low_stock_items.length === 0 && (
                  <tr>
                    <td className="dashboard-empty-cell" colSpan={5}>
                      No products are currently at or below their stock
                      threshold.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </section>
  );
}

export default Dashboard;