from pydantic import BaseModel


class Page(BaseModel):
    data: list[object]
    total: int
