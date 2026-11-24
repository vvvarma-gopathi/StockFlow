from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class DuplicateSkuError(Exception):
    pass


class ProductNotFoundError(Exception):
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