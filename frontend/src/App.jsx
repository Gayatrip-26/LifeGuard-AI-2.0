import { BrowserRouter, Link, Navigate, Route, Routes } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { clearToken, getToken } from "./lib/auth";
import "./App.css";

function App() {
  const loggedIn = !!getToken();

  function logout() {
    clearToken();
    window.location.href = "/login";
  }

  return (
    <BrowserRouter>
      <div className="app-shell">
        <header className="app-header">
          <Link to={loggedIn ? "/dashboard" : "/login"} className="app-brand">
            LifeGuard AI 2.0
          </Link>
          <nav className="app-nav">
            {loggedIn ? (
              <>
                <Link to="/dashboard">Dashboard</Link>
                <button type="button" className="app-logout" onClick={logout}>
                  Log out
                </button>
                <span className="app-pill">Signed in</span>
              </>
            ) : (
              <>
                <Link to="/login">Sign in</Link>
                <Link to="/register">Register</Link>
              </>
            )}
          </nav>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/dashboard"
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              }
            />
            <Route
              path="/"
              element={
                <Navigate to={loggedIn ? "/dashboard" : "/login"} replace />
              }
            />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
