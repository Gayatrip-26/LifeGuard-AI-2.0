import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiJson, networkErrorMessage } from "../lib/api";
import "./Auth.css";

export default function Register() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await apiJson(
        "/auth/register",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        },
        { label: "register" }
      );
      navigate("/login", { replace: true });
    } catch (err) {
      console.error("[LifeGuard] register failed", err);
      setError(networkErrorMessage(err, "Registration"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth">
      <div className="auth__panel">
        <h1 className="auth__title">Create account</h1>
        <p className="auth__subtitle">Password must be at least 8 characters.</p>
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
              autoComplete="new-password"
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          <button className="auth__submit" type="submit" disabled={submitting}>
            {submitting ? "Creating…" : "Register"}
          </button>
        </form>
        <p className="auth__footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
