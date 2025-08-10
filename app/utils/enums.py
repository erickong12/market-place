import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    SELLER = "SELLER"
    BUYER = "BUYER"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    READY = "ready"
    DONE = "done"
    CANCELLED = "cancelled"
    AUTO_CANCELLED = "auto_cancelled"
