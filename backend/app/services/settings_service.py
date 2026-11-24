from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.schemas.settings import OrganizationSettingsUpdate


class OrganizationNotFoundError(Exception):
    pass


def get_organization_settings(
    db: Session,
    organization_id: int,
) -> Organization:
    organization = db.get(Organization, organization_id)
    if organization is None:
        raise OrganizationNotFoundError
    return organization


def update_organization_settings(
    db: Session,
    organization_id: int,
    settings: OrganizationSettingsUpdate,
) -> Organization:
    organization = get_organization_settings(db, organization_id)
    organization.default_low_stock_threshold = (
        settings.default_low_stock_threshold
    )
    organization.default_low_stock_threshold_enabled = (
        settings.default_low_stock_threshold_enabled
    )
    db.commit()
    db.refresh(organization)
    return organization
