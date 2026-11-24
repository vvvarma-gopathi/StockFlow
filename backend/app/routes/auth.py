from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.auth import (
    AccessTokenResponse,
    LoginRequest,
    SignupRequest,
    SignupResponse,
)
from app.services.auth_service import (
    EmailAlreadyRegisteredError,
    authenticate_user,
    register_user,
)
from app.utils.security import TokenConfigurationError, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    signup_data: SignupRequest,
    db: Session = Depends(get_db),
) -> SignupResponse:
    try:
        user = register_user(db, signup_data)
        return SignupResponse.model_validate(user)
    except EmailAlreadyRegisteredError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        ) from error


@router.post("/login", response_model=AccessTokenResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
) -> AccessTokenResponse:
    user = authenticate_user(db, credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        access_token, expires_in = create_access_token(user.id)
    except TokenConfigurationError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured.",
        ) from error

    return AccessTokenResponse(access_token=access_token, expires_in=expires_in)
