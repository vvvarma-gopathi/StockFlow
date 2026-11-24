# StockFlow API

Configure PostgreSQL, copy `.env.example` to `.env`, and set `DATABASE_URL` to
your database connection string. Then run from the `backend` directory:

```powershell
.\env\Scripts\python.exe -m pip install -r requirements.txt
.\env\Scripts\python.exe -m alembic upgrade head
.\env\Scripts\python.exe -m uvicorn app.main:app --reload
```

Registration is available at `POST /api/auth/signup`. It accepts `email`,
`password`, and `organization_name`; a successful request returns the created
user and organization without returning the password hash.

Login is available at `POST /api/auth/login`. It accepts `email` and
`password`, and returns a short-lived HS256 bearer token. Set `JWT_SECRET_KEY`
to a unique random value of at least 32 bytes before using it, for example
with `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
New passwords are stored with bcrypt; login also accepts existing Argon2 hashes.

Run the backend tests with:

```powershell
.\env\Scripts\python.exe -m pip install -r requirements-dev.txt
.\env\Scripts\python.exe -m pytest
```
