from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.settings import (
    OrganizationSettingsResponse,
    OrganizationSettingsUpdate,
)
from app.services.settings_service import (
    OrganizationNotFoundError,
    get_organization_settings,
    update_organization_settings,
)

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=OrganizationSettingsResponse)
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrganizationSettingsResponse:
    try:
        return get_organization_settings(db, current_user.organization_id)
    except OrganizationNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        ) from error


@router.put("", response_model=OrganizationSettingsResponse)
def update_settings(
    settings: OrganizationSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrganizationSettingsResponse:
    try:
        return update_organization_settings(
            db,
            current_user.organization_id,
            settings,
        )
    except OrganizationNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        ) from error
