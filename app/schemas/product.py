
from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str | None
    image: str | None
    inventory: list[str]

    model_config = ConfigDict(from_attributes=True)


class ProductOut(ProductResponse):
    id: str
    name: str
    description: str | None
    image: str | None
    model_config = ConfigDict(from_attributes=True)


class ProductLandingPage(BaseModel):
    id: str
    name: str
    image: str | None
    model_config = ConfigDict(from_attributes=True)


class ProductPageResponse(BaseModel):
    page: int
    size: int
    skip: int
    total_record: int
    result: list[ProductResponse]


class ProductCreate(BaseModel):
    name: str
    description: str | None


class ProductUpdate(ProductCreate):
    id: str
