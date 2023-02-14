from sqlalchemy import Column, Integer, String, Text

from app.db.base import BaseModel


class Product(BaseModel):
    """represent data model product"""

    __tablename__ = "products"

    title = Column(String)
    description = Column(Text)
    stocks = Column(Integer, default=0)
