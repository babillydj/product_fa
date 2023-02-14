import datetime
from typing import Union

from pydantic import BaseModel


class ProductBase(BaseModel):
    """base schema for model product"""

    title: str
    description: Union[str, None] = None
    stocks: int


class ProductCreate(ProductBase):
    """schema for create and update"""

    pass


class Product(ProductBase):
    """schema for get"""

    id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        orm_mode = True
