import jwt
import pytest
from pwdlib import PasswordHash

from app.models.organization import Organization
from app.models.user import User
from app.utils import security
from app.utils.security import verify_password

def test_signup_creates_user_and_organization_without_returning_password(client):
    test_client, session_factory = client
    response = test_client.post(
        "/api/auth/signup",
        json={
            "email": "owner@example.com",
            "password": "secure-password",
            "organization_name": "My Test Store",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "owner@example.com"
    assert response.json()["organization"]["name"] == "My Test Store"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()
    with session_factory() as db:
        user = db.query(User).one()
        assert user.password_hash != "secure-password"
        assert user.password_hash.startswith("$2b$")
        assert verify_password("secure-password", user.password_hash)
        assert user.organization.default_low_stock_threshold == 5


def test_signup_rejects_duplicate_email_without_creating_another_organization(client):
    test_client, session_factory = client
    signup_data = {
        "email": "owner@example.com",
        "password": "secure-password",
        "organization_name": "My Test Store",
    }

    assert test_client.post("/api/auth/signup", json=signup_data).status_code == 201
    duplicate = test_client.post(
        "/api/auth/signup",
        json={
            **signup_data,
            "email": "OWNER@EXAMPLE.COM",
            "organization_name": "Another Store",
        },
    )

    assert duplicate.status_code == 409
    with session_factory() as db:
        assert db.query(Organization).count() == 1


def test_signup_requires_a_non_empty_organization_name(client):
    test_client, _ = client
    response = test_client.post(
        "/api/auth/signup",
        json={
            "email": "owner@example.com",
            "password": "secure-password",
            "organization_name": "   ",
        },
    )

    assert response.status_code == 422


def test_signup_rejects_password_over_bcrypt_byte_limit(client):
    test_client, _ = client
    response = test_client.post(
        "/api/auth/signup",
        json={
            "email": "owner@example.com",
            "password": "a" * 73,
            "organization_name": "My Test Store",
        },
    )

    assert response.status_code == 422


def test_login_returns_signed_access_token(client, jwt_secret):
    test_client, _ = client
    signup = test_client.post(
        "/api/auth/signup",
        json={
            "email": "owner@example.com",
            "password": "secure-password",
            "organization_name": "My Test Store",
        },
    )

    response = test_client.post(
        "/api/auth/login",
        json={"email": "OWNER@EXAMPLE.COM", "password": "secure-password"},
    )

    assert signup.status_code == 201
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires_in"] == 30 * 60
    claims = jwt.decode(
        response.json()["access_token"],
        jwt_secret,
        algorithms=["HS256"],
    )
    assert claims["sub"] == str(signup.json()["id"])
    assert claims["token_type"] == "access"


def test_login_rejects_invalid_password(client):
    test_client, _ = client
    test_client.post(
        "/api/auth/signup",
        json={
            "email": "owner@example.com",
            "password": "secure-password",
            "organization_name": "My Test Store",
        },
    )

    response = test_client.post(
        "/api/auth/login",
        json={"email": "owner@example.com", "password": "incorrect-password"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.parametrize(
    "password_hash",
    ["unrecognized-hash", "$2b$12$" + "x" * 53],
)
def test_login_rejects_invalid_password_hash(client, password_hash):
    test_client, session_factory = client
    with session_factory() as db:
        organization = Organization(name="Legacy Store")
        db.add(
            User(
                email="legacy@example.com",
                password_hash=password_hash,
                organization=organization,
            )
        )
        db.commit()

    response = test_client.post(
        "/api/auth/login",
        json={"email": "legacy@example.com", "password": "password"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_login_accepts_existing_argon2_password_hash(client):
    test_client, session_factory = client
    with session_factory() as db:
        organization = Organization(name="Legacy Store")
        db.add(
            User(
                email="legacy@example.com",
                password_hash=PasswordHash.recommended().hash("legacy-password"),
                organization=organization,
            )
        )
        db.commit()

    response = test_client.post(
        "/api/auth/login",
        json={"email": "legacy@example.com", "password": "legacy-password"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_requires_jwt_secret(client, monkeypatch):
    test_client, _ = client
    test_client.post(
        "/api/auth/signup",
        json={
            "email": "owner@example.com",
            "password": "secure-password",
            "organization_name": "My Test Store",
        },
    )
    monkeypatch.setattr(security, "JWT_SECRET_KEY", None)

    response = test_client.post(
        "/api/auth/login",
        json={"email": "owner@example.com", "password": "secure-password"},
    )

    assert response.status_code == 503