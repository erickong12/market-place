from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductOut


class SellerInventoryCreate(BaseModel):
    product_id: int
    price: float
    quantity: int


class SellerInventoryUpdate(SellerInventoryCreate):
    id: str


class SellerInventoryOut(BaseModel):
    id: str
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class SellerInventoryResponse(BaseModel):
    id: int
    product: ProductOut
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class SellerInventoryDetailResponse(BaseModel):
    id: str
    product_id: str
    product_name: str
    product_image: str
    product_description: str
    seller_id: str
    seller_name: str

    model_config = ConfigDict(from_attributes=True)


class SellerInventoryPageResponse(BaseModel):
    page: int
    size: int
    skip: int
    total_record: int
    result: list[SellerInventoryDetailResponse]
