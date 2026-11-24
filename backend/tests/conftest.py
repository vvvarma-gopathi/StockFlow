import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import main as main_module
from app.dependencies.database import get_db
from app.main import app
from app.utils import security


@pytest.fixture
def jwt_secret() -> str:
    return "test-secret-that-is-long-enough-for-hs256"


@pytest.fixture
def client(monkeypatch, jwt_secret):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
    monkeypatch.setattr(main_module, "engine", engine)
    monkeypatch.setattr(security, "JWT_SECRET_KEY", jwt_secret)

    def override_get_db():
        with testing_session_local() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client, testing_session_local
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()
