from pydantic import BaseModel, ConfigDict, Field


class OrganizationSettingsUpdate(BaseModel):
    default_low_stock_threshold: int = Field(ge=0)
    default_low_stock_threshold_enabled: bool


class OrganizationSettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    default_low_stock_threshold: int
    default_low_stock_threshold_enabled: bool
