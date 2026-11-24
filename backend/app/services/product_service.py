from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models.product import Product
from app.models.stock_adjustment import StockAdjustment
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    StockAdjustmentCreate,
)


class DuplicateSkuError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


def _find_product(
    db: Session,
    product_id: int,
    organization_id: int,
) -> Product | None:
    statement = (
        select(Product)
        .options(joinedload(Product.organization))
        .where(
            Product.id == product_id,
            Product.organization_id == organization_id,
        )
    )
    return db.scalar(statement)


def get_products(db: Session, organization_id: int) -> list[Product]:
    statement = (
        select(Product)
        .options(joinedload(Product.organization))
        .where(Product.organization_id == organization_id)
        .order_by(Product.name, Product.id)
    )
    return list(db.scalars(statement).all())


def get_product(
    db: Session,
    product_id: int,
    organization_id: int,
) -> Product:
    product = _find_product(db, product_id, organization_id)
    if product is None:
        raise ProductNotFoundError
    return product


def create_product(
    db: Session,
    product_data: ProductCreate,
    organization_id: int,
) -> Product:
    duplicate = db.scalar(
        select(Product.id).where(
            Product.organization_id == organization_id,
            Product.sku == product_data.sku,
        )
    )
    if duplicate is not None:
        raise DuplicateSkuError

    product = Product(
        organization_id=organization_id,
        **product_data.model_dump(),
    )
    db.add(product)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        duplicate = db.scalar(
            select(Product.id).where(
                Product.organization_id == organization_id,
                Product.sku == product_data.sku,
            )
        )
        if duplicate is not None:
            raise DuplicateSkuError from None
        raise

    return get_product(db, product.id, organization_id)


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate,
    organization_id: int,
) -> Product:
    product = get_product(db, product_id, organization_id)
    duplicate = db.scalar(
        select(Product.id).where(
            Product.organization_id == organization_id,
            Product.sku == product_data.sku,
            Product.id != product_id,
        )
    )
    if duplicate is not None:
        raise DuplicateSkuError

    for field, value in product_data.model_dump().items():
        setattr(product, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        duplicate = db.scalar(
            select(Product.id).where(
                Product.organization_id == organization_id,
                Product.sku == product_data.sku,
                Product.id != product_id,
            )
        )
        if duplicate is not None:
            raise DuplicateSkuError from None
        raise

    return get_product(db, product_id, organization_id)


def delete_product(
    db: Session,
    product_id: int,
    organization_id: int,
) -> None:
    product = get_product(db, product_id, organization_id)
    db.delete(product)
    db.commit()


def adjust_stock(
    db: Session,
    product_id: int,
    organization_id: int,
    user_id: int,
    adjustment_data: StockAdjustmentCreate,
) -> StockAdjustment:
    product = db.scalar(
        select(Product)
        .where(
            Product.id == product_id,
            Product.organization_id == organization_id,
        )
        .with_for_update()
    )
    if product is None:
        raise ProductNotFoundError

    previous_quantity = product.quantity_on_hand
    quantity_after = previous_quantity + adjustment_data.quantity_delta
    if quantity_after < 0:
        raise InsufficientStockError

    adjustment = StockAdjustment(
        product_id=product.id,
        adjusted_by_user_id=user_id,
        quantity_delta=adjustment_data.quantity_delta,
        previous_quantity=previous_quantity,
        quantity_after=quantity_after,
        note=adjustment_data.note,
    )
    product.quantity_on_hand = quantity_after
    db.add(adjustment)
    db.commit()
    db.refresh(adjustment)
    return adjustment


def get_stock_adjustments(
    db: Session,
    product_id: int,
    organization_id: int,
) -> list[StockAdjustment]:
    get_product(db, product_id, organization_id)
    statement = (
        select(StockAdjustment)
        .where(StockAdjustment.product_id == product_id)
        .order_by(
            StockAdjustment.created_at.desc(),
            StockAdjustment.id.desc(),
        )
        .limit(50)
    )
    return list(db.scalars(statement).all())