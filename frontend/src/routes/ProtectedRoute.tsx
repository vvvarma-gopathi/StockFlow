import { Navigate, Outlet } from "react-router-dom";
import { ACCESS_TOKEN_STORAGE_KEY } from "../services/api";

function ProtectedRoute() {
  return sessionStorage.getItem(ACCESS_TOKEN_STORAGE_KEY) ? (
    <Outlet />
  ) : (
    <Navigate to="/" replace />
  );
}

export default ProtectedRoute;
