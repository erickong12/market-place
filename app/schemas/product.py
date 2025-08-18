from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    iamge: Optional[str]
    inventory: list[str]

    model_config = ConfigDict(from_attributes=True)


class ProductOut(ProductResponse):
    id: str
    name: str
    description: Optional[str]
    image: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class ProductLandingPage(BaseModel):
    id: str
    name: str
    image: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class ProductPageResponse(BaseModel):
    page: int
    size: int
    skip: int
    total_record: int
    result: list[ProductResponse]


class ProductCreate(BaseModel):
    name: str
    image: Optional[str]
    description: Optional[str]


class ProductUpdate(ProductCreate):
    id: str
