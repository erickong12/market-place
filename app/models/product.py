from uuid import uuid4
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    image = Column(String)
    description = Column(String)
    delete = Column(Boolean, default=False)

    inventory = relationship("SellerInventory", back_populates="product")
