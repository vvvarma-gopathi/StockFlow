import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { logout } from "../../services/authService";
import "./AppLayout.css";

function AppLayout() {
  const location = useLocation();
  const navigate = useNavigate();
  const pageTitle =
    location.pathname === "/products"
      ? "Products"
      : location.pathname === "/settings"
        ? "Settings"
        : "Dashboard";

  function handleLogout() {
    logout();
    navigate("/", { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <NavLink className="app-brand" to="/dashboard">
          <span className="app-brand-mark" aria-hidden="true">
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
        </NavLink>

        <div className="app-nav-label">WORKSPACE</div>
        <nav className="app-nav" aria-label="Workspace">
          <NavLink
            className={({ isActive }) =>
              `app-nav-link${isActive ? " active" : ""}`
            }
            to="/dashboard"
          >
            <span className="app-nav-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <rect
                  x="3.5"
                  y="3.5"
                  width="6"
                  height="6"
                  rx="1"
                  stroke="currentColor"
                  strokeWidth="1.8"
                />
                <rect
                  x="14.5"
                  y="3.5"
                  width="6"
                  height="6"
                  rx="1"
                  stroke="currentColor"
                  strokeWidth="1.8"
                />
                <rect
                  x="3.5"
                  y="14.5"
                  width="6"
                  height="6"
                  rx="1"
                  stroke="currentColor"
                  strokeWidth="1.8"
                />
                <rect
                  x="14.5"
                  y="14.5"
                  width="6"
                  height="6"
                  rx="1"
                  stroke="currentColor"
                  strokeWidth="1.8"
                />
              </svg>
            </span>
            Dashboard
          </NavLink>
          <NavLink
            className={({ isActive }) =>
              `app-nav-link${isActive ? " active" : ""}`
            }
            to="/products"
          >
            <span className="app-nav-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="m12 2.8 8.5 4.8v9L12 21.4l-8.5-4.8v-9L12 2.8Z"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinejoin="round"
                />
                <path
                  d="m3.8 7.8 8.2 4.7 8.2-4.7M12 12.5v8.4"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinejoin="round"
                />
              </svg>
            </span>
            Products
          </NavLink>
          <NavLink
            className={({ isActive }) =>
              `app-nav-link${isActive ? " active" : ""}`
            }
            to="/settings"
          >
            <span className="app-nav-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M4 6h9m4 0h3M4 12h3m4 0h9M4 18h11m4 0h1"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                />
                <circle
                  cx="15"
                  cy="6"
                  r="2"
                  fill="white"
                  stroke="currentColor"
                  strokeWidth="1.8"
                />
                <circle
                  cx="9"
                  cy="12"
                  r="2"
                  fill="white"
                  stroke="currentColor"
                  strokeWidth="1.8"
                />
                <circle
                  cx="17"
                  cy="18"
                  r="2"
                  fill="white"
                  stroke="currentColor"
                  strokeWidth="1.8"
                />
              </svg>
            </span>
            Settings
          </NavLink>
        </nav>

        <div className="app-sidebar-footer">
          <div className="app-user-avatar" aria-hidden="true">
            SF
          </div>
          <div className="app-user-label">
            <strong>StockFlow</strong>
            <span>Workspace</span>
          </div>
          <button
            className="app-logout"
            type="button"
            onClick={handleLogout}
            aria-label="Sign out"
            title="Sign out"
          >
            ↪
          </button>
        </div>
      </aside>

      <div className="app-main-column">
        <header className="app-topbar">
          <div className="app-breadcrumb">
            <span>Workspace</span>
            <span aria-hidden="true">/</span>
            <strong>{pageTitle}</strong>
          </div>
          <span className="app-topbar-avatar" aria-label="Signed in">
            SF
          </span>
        </header>
        <main className="app-main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default AppLayout;
