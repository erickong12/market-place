from pydantic import BaseModel


class Page(BaseModel):
    data: list[object]
    total: int


class PageResponse(BaseModel):
    page: int
    size: int
    offset: int
    total_record: int
