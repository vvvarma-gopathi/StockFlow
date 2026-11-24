from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    StockAdjustmentCreate,
    StockAdjustmentResponse,
)
from app.services.product_service import (
    DuplicateSkuError,
    InsufficientStockError,
    ProductNotFoundError,
    adjust_stock as adjust_stock_record,
    create_product as create_product_record,
    delete_product as delete_product_record,
    get_product as get_product_record,
    get_products as list_product_records,
    get_stock_adjustments as list_stock_adjustments,
    update_product as update_product_record,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProductResponse:
    try:
        return create_product_record(
            db,
            product_data,
            current_user.organization_id,
        )
    except DuplicateSkuError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists in your organization.",
        ) from error


@router.get("", response_model=list[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ProductResponse]:
    return list_product_records(db, current_user.organization_id)


@router.post(
    "/{product_id}/adjustments",
    response_model=StockAdjustmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def adjust_stock(
    product_id: int,
    adjustment_data: StockAdjustmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StockAdjustmentResponse:
    try:
        return adjust_stock_record(
            db,
            product_id,
            current_user.organization_id,
            current_user.id,
            adjustment_data,
        )
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        ) from error
    except InsufficientStockError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The adjustment cannot reduce stock below zero.",
        ) from error


@router.get(
    "/{product_id}/adjustments",
    response_model=list[StockAdjustmentResponse],
)
def get_stock_adjustments(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[StockAdjustmentResponse]:
    try:
        return list_stock_adjustments(
            db,
            product_id,
            current_user.organization_id,
        )
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        ) from error


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProductResponse:
    try:
        return get_product_record(
            db,
            product_id,
            current_user.organization_id,
        )
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        ) from error


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProductResponse:
    try:
        return update_product_record(
            db,
            product_id,
            product_data,
            current_user.organization_id,
        )
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        ) from error
    except DuplicateSkuError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists in your organization.",
        ) from error


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    try:
        delete_product_record(
            db,
            product_id,
            current_user.organization_id,
        )
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        ) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)