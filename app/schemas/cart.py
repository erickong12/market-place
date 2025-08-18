from pydantic import BaseModel, ConfigDict


class CartItemCreate(BaseModel):
    seller_inventory_id: int
    quantity: int


class CartItemResponse(BaseModel):
    id: int
    quantity: int
    inventory_id: int
    price: float
    product_id: str
    product_name: str
    image: str
    seller_id: str
    seller_name: str

    model_config = ConfigDict(from_attributes=True)
