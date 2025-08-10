from pydantic import BaseModel

class CartItemCreate(BaseModel):
    seller_inventory_id: int
    quantity: int

class CartItemOut(BaseModel):
    id: int
    seller_inventory_id: int
    quantity: int

    class Config:
        orm_mode = True
