import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { getApiErrorMessage } from "../services/api";
import {
  getOrganizationSettings,
  updateOrganizationSettings,
} from "../services/settingsService";
import type { OrganizationSettings } from "../services/settingsService";
import "./Settings.css";

function Settings() {
  const [settings, setSettings] = useState<OrganizationSettings | null>(null);
  const [threshold, setThreshold] = useState("5");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    let active = true;

    getOrganizationSettings()
      .then((result) => {
        if (active) {
          setSettings(result);
          setThreshold(String(result.default_low_stock_threshold));
        }
      })
      .catch((error: unknown) => {
        if (active) {
          setErrorMessage(
            getApiErrorMessage(error, "Unable to load organization settings."),
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

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const parsedThreshold = Number(threshold);
    if (!Number.isSafeInteger(parsedThreshold) || parsedThreshold < 0) {
      setErrorMessage("Enter a non-negative whole number.");
      return;
    }

    if (!settings) {
      return;
    }

    setErrorMessage("");
    setSuccessMessage("");
    setIsSaving(true);
    try {
      const updatedSettings = await updateOrganizationSettings({
        default_low_stock_threshold: parsedThreshold,
        default_low_stock_threshold_enabled:
          settings.default_low_stock_threshold_enabled,
      });
      setSettings(updatedSettings);
      setThreshold(String(updatedSettings.default_low_stock_threshold));
      setSuccessMessage("Settings saved.");
    } catch (error: unknown) {
      setErrorMessage(
        getApiErrorMessage(error, "Unable to save settings. Please try again."),
      );
    } finally {
      setIsSaving(false);
    }
  }

  function toggleDefaultThreshold() {
    setSettings((current) =>
      current
        ? {
            ...current,
            default_low_stock_threshold_enabled:
              !current.default_low_stock_threshold_enabled,
          }
        : current,
    );
    setSuccessMessage("");
  }

  return (
    <section className="settings-page">
      <header className="settings-page-heading">
        <h1>Settings</h1>
        <p>Configure how low-stock items are identified for your organization.</p>
      </header>

      {errorMessage && (
        <p className="settings-message settings-error" role="alert">
          {errorMessage}
        </p>
      )}
      {successMessage && (
        <p className="settings-message settings-success" role="status">
          {successMessage}
        </p>
      )}

      <section className="settings-card" aria-labelledby="stock-settings-title">
        <header className="settings-card-heading">
          <h2 id="stock-settings-title">Low stock threshold</h2>
          <p>
            Choose the default stock level for products without a custom
            threshold.
          </p>
        </header>

        {isLoading ? (
          <p className="settings-loading" role="status">
            Loading settings...
          </p>
        ) : settings ? (
          <form className="settings-form" onSubmit={handleSubmit}>
            <label htmlFor="default-low-stock-threshold">
              Default low stock threshold
            </label>
            <input
              id="default-low-stock-threshold"
              name="defaultLowStockThreshold"
              type="number"
              min={0}
              step={1}
              value={threshold}
              onChange={(event) => {
                setThreshold(event.target.value);
                setSuccessMessage("");
              }}
              required
            />
            <small>
              Products with their own threshold continue to use that value.
            </small>

            <div className="settings-toggle-row">
              <div>
                <strong id="default-threshold-toggle-label">
                  Use this default threshold
                </strong>
                <span id="default-threshold-toggle-description">
                  When off, products without a custom threshold are not marked
                  low stock.
                </span>
              </div>
              <button
                className={`settings-toggle${settings.default_low_stock_threshold_enabled ? " enabled" : ""}`}
                type="button"
                role="switch"
                aria-checked={settings.default_low_stock_threshold_enabled}
                aria-labelledby="default-threshold-toggle-label"
                aria-describedby="default-threshold-toggle-description"
                onClick={toggleDefaultThreshold}
              >
                <span className="settings-toggle-knob" />
                <span className="settings-toggle-label">
                  {settings.default_low_stock_threshold_enabled ? "On" : "Off"}
                </span>
              </button>
            </div>

            <footer className="settings-form-actions">
              <button
                className="settings-save-button"
                type="submit"
                disabled={isSaving}
              >
                {isSaving ? "Saving..." : "Save settings"}
              </button>
            </footer>
          </form>
        ) : (
          <p className="settings-loading">
            Settings aren’t available right now.
          </p>
        )}
      </section>
    </section>
  );
}

export default Settings;
