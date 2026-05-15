import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { apiJson, networkErrorMessage } from "../lib/api";
import { setToken } from "../lib/auth";
import "./Auth.css";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/dashboard";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const body = await apiJson(
        "/auth/login",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        },
        { label: "login" }
      );
      if (!body.access_token) {
        throw new Error("No access token returned.");
      }
      setToken(body.access_token);
      navigate(from, { replace: true });
    } catch (err) {
      console.error("[LifeGuard] login failed", err);
      setError(networkErrorMessage(err, "Login"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth">
      <div className="auth__panel">
        <h1 className="auth__title">Sign in</h1>
        <p className="auth__subtitle">LifeGuard AI 2.0</p>
        {error && (
          <div className="auth__error" role="alert">
            {error}
          </div>
        )}
        <form className="auth__form" onSubmit={handleSubmit}>
          <label className="auth__label">
            Email
            <input
              className="auth__input"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
          <label className="auth__label">
            Password
            <input
              className="auth__input"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          <button className="auth__submit" type="submit" disabled={submitting}>
            {submitting ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <p className="auth__footer">
          No account? <Link to="/register">Create one</Link>
        </p>
      </div>
    </div>
  );
}
