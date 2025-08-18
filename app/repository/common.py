from sqlalchemy import asc, desc, text
from sqlalchemy.orm import Query

from app.schemas.common import Page


def find_paginated(
    query: Query, model: object, skip: int, limit: int, sort_by: str, order: str
):
    """
    Retrieves a paginated and sorted set of records from the database.
    Args:
        query (Query): The SQLAlchemy query object to execute the database operation.
        model (object): The SQLAlchemy model class used for sorting.
        skip (int): The number of records to skip (for pagination).
        limit (int): The maximum number of records to return.
        sort_by (str): The name of the model attribute to sort by.
        order (str): The sort order, either "asc" for ascending or "desc" for descending.
    Returns:
        Page: A Page object containing the paginated results and total count.
    """
    if order == "asc":
        query = query.order_by(asc(text(sort_by)))
    else:
        query = query.order_by(desc(text(sort_by)))
    query = query.offset(skip).limit(limit)
    return Page(data=query.all(), total=query.count())
