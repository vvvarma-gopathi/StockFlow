import { useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router-dom";
import { getApiErrorMessage } from "../services/api";
import { signup } from "../services/authService";
import "./Auth.css";

function Register() {
  const [organizationName, setOrganizationName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const passwordMismatch =
    confirmPassword.length > 0 && password !== confirmPassword;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (password !== confirmPassword) {
      return;
    }

    setErrorMessage("");
    setSuccessMessage("");
    setIsSubmitting(true);

    try {
      const result = await signup({
        organization_name: organizationName.trim(),
        email: email.trim(),
        password,
      });
      setSuccessMessage(
        `${result.organization.name} is ready. Your account has been created.`,
      );
    } catch (error: unknown) {
      setErrorMessage(
        getApiErrorMessage(
          error,
          "Unable to create your account. Please try again.",
        ),
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="registration-page">
      <a className="registration-brand" href="/" aria-label="StockFlow home">
        <span className="registration-brand-mark" aria-hidden="true">
          <svg viewBox="0 0 32 32" fill="none">
            <path
              d="M16 3.5 27 9.75v12.5L16 28.5 5 22.25V9.75L16 3.5Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinejoin="round"
            />
            <path
              d="m5.5 10 10.5 6 10.5-6M16 16v12"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinejoin="round"
            />
          </svg>
        </span>
        <span>StockFlow</span>
      </a>

      <section className="registration-card" aria-labelledby="registration-title">
        <div className="registration-eyebrow">GET STARTED</div>
        <h1 id="registration-title">Create your account</h1>
        <p className="registration-intro">
          Set up your workspace and start managing your inventory.
        </p>

        <form className="registration-form" onSubmit={handleSubmit}>
          <label htmlFor="organization-name">Organization name</label>
          <input
            id="organization-name"
            name="organizationName"
            type="text"
            autoComplete="organization"
            placeholder="My Test Store"
            maxLength={255}
            value={organizationName}
            onChange={(event) => setOrganizationName(event.target.value)}
            required
          />

          <label htmlFor="email">Work email</label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            placeholder="you@company.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />

          <label htmlFor="password">Password</label>
          <div className="registration-password">
            <input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              autoComplete="new-password"
              placeholder="At least 8 characters"
              minLength={8}
              maxLength={72}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
            <button
              className="password-visibility"
              type="button"
              aria-pressed={showPassword}
              aria-label={showPassword ? "Hide passwords" : "Show passwords"}
              onClick={() => setShowPassword((visible) => !visible)}
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
          <p className="registration-hint">
            Use at least 8 characters. Passwords are limited to 72 UTF-8 bytes.
          </p>

          <label htmlFor="confirm-password">Confirm password</label>
          <div className="registration-password">
            <input
              id="confirm-password"
              name="confirmPassword"
              type={showPassword ? "text" : "password"}
              autoComplete="new-password"
              placeholder="Re-enter your password"
              minLength={8}
              maxLength={72}
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              aria-invalid={passwordMismatch}
              aria-describedby={
                passwordMismatch ? "confirm-password-error" : undefined
              }
              required
            />
          </div>
          {passwordMismatch && (
            <p
              className="registration-password-error"
              id="confirm-password-error"
              role="alert"
            >
              Passwords do not match.
            </p>
          )}

          {errorMessage && (
            <p className="registration-message registration-error" role="alert">
              {errorMessage}
            </p>
          )}
          {successMessage && (
            <p
              className="registration-message registration-success"
              role="status"
            >
              {successMessage}
            </p>
          )}

          <button
            className="registration-submit"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Creating account..." : "Create account"}
          </button>
        </form>

        <p className="registration-switch">
          Already have an account? <Link to="/">Sign in</Link>
        </p>
        <p className="registration-terms">
          Your organization’s inventory is private to your workspace.
        </p>
      </section>

      <footer className="registration-footer">
        Inventory management, made simple.
      </footer>
    </main>
  );
}

export default Register;