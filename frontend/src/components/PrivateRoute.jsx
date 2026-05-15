import { Navigate, useLocation } from "react-router-dom";
import { getToken } from "../lib/auth";

export default function PrivateRoute({ children }) {
  const location = useLocation();
  if (!getToken()) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
  return children;
}
