from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.product import Product
from app.schemas.dashboard import DashboardSummary
from app.services.product_service import get_products


class OrganizationNotFoundError(Exception):
    pass


def get_dashboard_summary(
    db: Session,
    organization_id: int,
) -> DashboardSummary:
    organization = db.get(Organization, organization_id)
    if organization is None:
        raise OrganizationNotFoundError

    total_products = db.scalar(
        select(func.count(Product.id)).where(
            Product.organization_id == organization_id
        )
    )
    total_quantity = db.scalar(
        select(func.coalesce(func.sum(Product.quantity_on_hand), 0)).where(
            Product.organization_id == organization_id
        )
    )
    products = get_products(db, organization_id)
    low_stock_items = [product for product in products if product.is_low_stock]

    return DashboardSummary(
        total_products=total_products or 0,
        total_quantity=total_quantity or 0,
        low_stock_items=low_stock_items,
    )
