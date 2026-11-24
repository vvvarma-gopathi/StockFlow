from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest
from app.utils.security import hash_password, verify_password


class EmailAlreadyRegisteredError(Exception):
    pass


def register_user(db: Session, signup: SignupRequest) -> User:
    existing_user = db.scalar(select(User).where(User.email == signup.email))
    if existing_user is not None:
        raise EmailAlreadyRegisteredError

    organization = Organization(name=signup.organization_name)
    user = User(
        email=str(signup.email),
        password_hash=hash_password(signup.password),
        organization=organization,
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing_user = db.scalar(select(User).where(User.email == signup.email))
        if existing_user is not None:
            raise EmailAlreadyRegisteredError from None
        raise

    db.refresh(user)
    return user


def authenticate_user(db: Session, credentials: LoginRequest) -> User | None:
    user = db.scalar(select(User).where(User.email == str(credentials.email)))
    if user is None or not verify_password(
        credentials.password, user.password_hash
    ):
        return None
    return user