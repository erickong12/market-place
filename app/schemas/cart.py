from pydantic import BaseModel, ConfigDict


class CartItemCreate(BaseModel):
    seller_inventory_id: str
    quantity: int


class CartItemResponse(BaseModel):
    id: str
    quantity: int
    inventory_id: str
    price: float
    product_id: str
    product_name: str
    image: str
    seller_id: str
    seller_name: str

    model_config = ConfigDict(from_attributes=True)
