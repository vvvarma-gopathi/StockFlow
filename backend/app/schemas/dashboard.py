from pydantic import BaseModel

from app.schemas.product import ProductResponse


class DashboardSummary(BaseModel):
    total_products: int
    total_quantity: int
    low_stock_items: list[ProductResponse]
