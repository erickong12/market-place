import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    SELLER = "SELLER"
    BUYER = "BUYER"


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    READY = "READY_TO_PICKUP"
    DONE = "DONE"
    CANCELLED = "CANCELLED"
    AUTO_CANCELLED = "AUTO_CANCELLED"
