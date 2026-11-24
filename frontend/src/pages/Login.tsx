import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getApiErrorMessage } from "../services/api";
import { login } from "../services/authService";
import "./Auth.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage("");
    setIsSubmitting(true);

    try {
      await login({ email: email.trim(), password });
      navigate("/dashboard", { replace: true });
    } catch (error: unknown) {
      setErrorMessage(
        getApiErrorMessage(error, "Unable to sign in. Please try again."),
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="registration-page">
      <Link className="registration-brand" to="/" aria-label="StockFlow home">
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
      </Link>

      <section className="registration-card" aria-labelledby="login-title">
        <div className="registration-eyebrow">WELCOME BACK</div>
        <h1 id="login-title">Sign in to StockFlow</h1>
        <p className="registration-intro">
          Enter your account details to continue to your workspace.
        </p>

        <form className="registration-form" onSubmit={handleSubmit}>
          <label htmlFor="login-email">Work email</label>
          <input
            id="login-email"
            name="email"
            type="email"
            autoComplete="email"
            placeholder="you@company.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />

          <label htmlFor="login-password">Password</label>
          <input
            id="login-password"
            name="password"
            type="password"
            autoComplete="current-password"
            placeholder="Your password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
          <p className="registration-hint">Your password is case-sensitive.</p>

          {errorMessage && (
            <p className="registration-message registration-error" role="alert">
              {errorMessage}
            </p>
          )}
          <button
            className="registration-submit"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <p className="registration-switch">
          New to StockFlow? <Link to="/register">Create an account</Link>
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

export default Login;