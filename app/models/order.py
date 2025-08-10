from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.utils.enums import OrderStatus


class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    buyer_id = Column(String, ForeignKey("users.id"))
    seller_id = Column(String, ForeignKey("users.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    buyer = relationship("User", foreign_keys=[buyer_id])
    seller = relationship("User", foreign_keys=[seller_id])
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"))
    seller_inventory_id = Column(String, ForeignKey("seller_inventory.id"))
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    seller_inventory = relationship("SellerInventory")
