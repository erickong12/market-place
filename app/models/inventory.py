from uuid import uuid4
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class SellerInventory(Base):
    __tablename__ = "seller_inventory"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    seller_id = Column(String, ForeignKey("users.id"))
    product_id = Column(String, ForeignKey("products.id"))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    delete = Column(Boolean, default=False)

    seller = relationship("User")
    product = relationship("Product")
