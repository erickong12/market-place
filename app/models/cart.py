from uuid import uuid4
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class CartItem(Base):
    __tablename__ = "cart"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    buyer_id = Column(String, ForeignKey("users.id"))
    seller_inventory_id = Column(String, ForeignKey("seller_inventory.id"))
    quantity = Column(Integer, nullable=False)

    buyer = relationship("User", back_populates="cart_items")
    seller_inventory = relationship("SellerInventory", back_populates="cart_items")
