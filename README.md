# StockFlow – SaaS Inventory Management System

StockFlow is a multi-tenant SaaS inventory management application designed to help small businesses manage products, track available stock, and identify low-stock items through a centralized dashboard.

The application provides organization-based data isolation, product management, inventory quantity updates, and configurable low-stock thresholds.

## Features

### Authentication & Organization Management
- User registration with email, password, and organization name.
- Secure JWT-based authentication.
- Password hashing using bcrypt.
- Automatic organization creation during registration.
- Organization-level data isolation.

### Product Management
- Create, view, update, and delete products.
- Manage product name, SKU, description, cost price, and selling price.
- Enforce SKU uniqueness within an organization.
- Search products by name or SKU.
- View product inventory information through individual product tiles.

### Inventory Management
- Update in-hand product quantities directly from the Products section.
- Manage available stock without navigating to a separate editing page.
- Track inventory quantities for individual products.

### Dashboard
- Total product count.
- Total inventory quantity.
- Low-stock product overview.
- Organization-specific inventory statistics.

### Low-Stock Management
- Configure a default low-stock threshold through Settings.
- Set custom low-stock thresholds for individual products.
- Automatically use the organization's default threshold when a product does not have a custom threshold.
- Identify low-stock products based on their effective threshold.

**Low-stock calculation:**

`Quantity on Hand <= Effective Low-Stock Threshold`

The effective threshold is determined using the following priority:

1. Product-specific threshold, when configured.
2. Organization default threshold, when no custom threshold exists.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript |
| Styling | Tailwind CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL (Supabase) |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Hashing | bcrypt |
| Database Migrations | Alembic |
| Frontend Deployment | Vercel |
| Backend Deployment | Render |

## Project Architecture

The project follows a modular architecture with separate frontend and backend applications maintained within a single repository.

```text
stockflow/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── dependencies/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── routes/
│   │   ├── utils/
│   │   └── tests/
│   │
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── routes/
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── vite.config.ts
│   ├── .env.example
│   └── Dockerfile
│
├── docs/
│   ├── architecture.md
│   └── api-documentation.md
│
├── .github/
│   └── copilot-instructions.md
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Getting Started

Follow these instructions to run StockFlow locally.

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- Node.js and npm
- Git
- PostgreSQL database access (Supabase or local PostgreSQL)

### 1. Clone the Repository

```bash
git clone github.com/vvvarma-gopathi/StockFlow
```

Navigate into the project:

```bash
cd stockflow
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Backend Environment Variables

Create a `.env` file inside the backend directory using `.env.example` as a reference.

Example:

```env
DATABASE_URL=your_supabase_postgresql_connection_string

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

FRONTEND_URL=http://localhost:5173
```

Use the actual variable names defined in the backend configuration. Never commit your `.env` file or expose database credentials and JWT secrets.

### 4. Run Database Migrations

From the backend directory, run:

```bash
alembic upgrade head
```

This applies the existing database migrations to your configured PostgreSQL database.

### 5. Start the Backend Server

```bash
uvicorn app.main:app --reload
```

Backend will be available at:

```text
http://localhost:8000
```

FastAPI interactive API documentation:

```text
http://localhost:8000/docs
```

### 6. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

### 7. Configure Frontend Environment Variables

Create a `.env` file inside the frontend directory.

Example:

```env
VITE_API_URL=http://localhost:8000
```

Use the exact environment variable expected by the frontend API configuration.

### 8. Start the Frontend

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

You can now access StockFlow through your browser.

## Deployment

StockFlow uses separate deployment environments for the frontend, backend, and database.

| Component | Hosting Provider |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| Database | Supabase PostgreSQL |

### Frontend Deployment – Vercel

1. Push the frontend code to GitHub.
2. Import the repository into Vercel.
3. Set the project root directory to `frontend`.
4. Configure the production build command:

```bash
npm run build
```

5. Configure the output directory:

```text
dist
```

6. Add the required frontend environment variables.

Example:

```env
VITE_API_URL=https://your-backend.onrender.com
```

7. Deploy the application.

### Backend Deployment – Render

1. Create a new Web Service in Render.
2. Connect the GitHub repository.
3. Set the root directory to `backend`.
4. Configure the build command:

```bash
pip install -r requirements.txt
```

5. Configure the start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

6. Configure backend environment variables:

```env
DATABASE_URL=your_supabase_postgresql_connection_string
SECRET_KEY=your_production_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=https://your-frontend.vercel.app
```

7. Ensure database migrations are applied before the application starts serving requests.
8. Deploy the backend.

### Database – Supabase

StockFlow uses Supabase-hosted PostgreSQL.

1. Create a Supabase project.
2. Obtain the PostgreSQL connection string.
3. Configure the connection string in the Render environment variables.
4. Apply Alembic migrations.
5. Ensure the database is accessible from the deployed backend.

**Important:** Keep database credentials and authentication secrets in environment variables. Never expose them in frontend code or commit them to GitHub.

## Multi-Tenant Data Isolation

StockFlow follows an organization-based multi-tenancy approach.

Each registered user is associated with an organization, and products are linked to their respective organization.

All authenticated inventory operations use the organization associated with the logged-in user.

This ensures that one organization cannot access or modify another organization's inventory data.

## Current Scope

StockFlow focuses on essential inventory management functionality.

The current MVP does not include:

- Multi-warehouse inventory management.
- Product variants and categories.
- E-commerce platform integrations.
- Order management.
- Purchase orders and supplier management.
- Subscription billing and payment processing.
- Advanced inventory analytics.
- Detailed stock movement history.

## Future Improvements

Potential enhancements include:

- Inventory movement tracking.
- CSV product import and export.
- Multiple warehouse support.
- Supplier management.
- Inventory notifications.
- Advanced reporting and analytics.

**StockFlow – Simplifying Inventory Management.**
