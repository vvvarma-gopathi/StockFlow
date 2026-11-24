import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { getApiErrorMessage } from "../../services/api";
import {
  adjustStock,
  getStockAdjustments,
} from "../../services/productService";
import type { Product, StockAdjustment } from "../../services/productService";
import "./StockAdjustmentDialog.css";

interface StockAdjustmentDialogProps {
  product: Product;
  onClose: () => void;
  onAdjusted: (adjustment: StockAdjustment) => void;
}

function StockAdjustmentDialog({
  product,
  onClose,
  onAdjusted,
}: StockAdjustmentDialogProps) {
  const [quantityDelta, setQuantityDelta] = useState("");
  const [note, setNote] = useState("");
  const [history, setHistory] = useState<StockAdjustment[] | null>(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    let active = true;

    getStockAdjustments(product.id)
      .then((result) => {
        if (active) {
          setHistory(result);
        }
      })
      .catch((error: unknown) => {
        if (active) {
          setErrorMessage(
            getApiErrorMessage(error, "Unable to load adjustment history."),
          );
        }
      });

    return () => {
      active = false;
    };
  }, [product.id]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const delta = Number(quantityDelta);
    if (!Number.isSafeInteger(delta) || delta === 0) {
      setErrorMessage("Enter a non-zero whole number of units to adjust.");
      return;
    }

    setErrorMessage("");
    setIsSaving(true);
    try {
      const adjustment = await adjustStock(product.id, delta, note.trim());
      onAdjusted(adjustment);
      setHistory((current) =>
        current ? [adjustment, ...current] : [adjustment],
      );
      setQuantityDelta("");
      setNote("");
    } catch (error: unknown) {
      setErrorMessage(
        getApiErrorMessage(error, "Unable to adjust stock. Please try again."),
      );
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div
      className="stock-adjustment-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget && !isSaving) {
          onClose();
        }
      }}
    >
      <section
        className="stock-adjustment-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="stock-adjustment-title"
      >
        <header className="stock-adjustment-header">
          <div>
            <p className="stock-adjustment-eyebrow">INVENTORY</p>
            <h2 id="stock-adjustment-title">Adjust stock</h2>
            <p className="stock-adjustment-product">
              {product.name} <span>·</span> {product.sku}
            </p>
          </div>
          <button
            className="stock-adjustment-close"
            type="button"
            onClick={onClose}
            disabled={isSaving}
            aria-label="Close stock adjustment"
          >
            ×
          </button>
        </header>

        <div className="stock-adjustment-current">
          <span>Current quantity</span>
          <strong>{product.quantity_on_hand.toLocaleString("en-IN")} units</strong>
        </div>

        <form className="stock-adjustment-form" onSubmit={handleSubmit}>
          <label htmlFor="stock-quantity-delta">Quantity change</label>
          <input
            id="stock-quantity-delta"
            name="quantityDelta"
            type="number"
            step={1}
            placeholder="e.g. +5 or -2"
            value={quantityDelta}
            onChange={(event) => setQuantityDelta(event.target.value)}
            required
          />
          <small>Use a positive number to add stock or a negative number to remove it.</small>

          <label htmlFor="stock-adjustment-note">Note</label>
          <textarea
            id="stock-adjustment-note"
            name="note"
            rows={3}
            maxLength={500}
            placeholder="Why is the stock changing?"
            value={note}
            onChange={(event) => setNote(event.target.value)}
            required
          />

          {errorMessage && (
            <p className="stock-adjustment-error" role="alert">
              {errorMessage}
            </p>
          )}

          <button
            className="stock-adjustment-submit"
            type="submit"
            disabled={isSaving}
          >
            {isSaving ? "Saving adjustment..." : "Save adjustment"}
          </button>
        </form>

        <section
          className="stock-adjustment-history"
          aria-labelledby="stock-adjustment-history-title"
        >
          <h3 id="stock-adjustment-history-title">Recent adjustments</h3>
          {history === null ? (
            <p className="stock-adjustment-history-empty" role="status">
              Loading history...
            </p>
          ) : history.length === 0 ? (
            <p className="stock-adjustment-history-empty">
              No adjustments recorded yet.
            </p>
          ) : (
            <ul>
              {history.map((entry) => (
                <li key={entry.id}>
                  <div className="stock-adjustment-entry-heading">
                    <strong
                      className={
                        entry.quantity_delta > 0
                          ? "stock-adjustment-increase"
                          : "stock-adjustment-decrease"
                      }
                    >
                      {entry.quantity_delta > 0 ? "+" : ""}
                      {entry.quantity_delta} units
                    </strong>
                    <time dateTime={entry.created_at}>
                      {new Date(entry.created_at).toLocaleString()}
                    </time>
                  </div>
                  <p>{entry.note}</p>
                  <span>
                    {entry.previous_quantity.toLocaleString("en-IN")} →{" "}
                    {entry.quantity_after.toLocaleString("en-IN")} units
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </section>
    </div>
  );
}

export default StockAdjustmentDialog;
