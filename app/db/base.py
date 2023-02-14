from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression


class utcnow(expression.FunctionElement):
    """declare type utcnow as DateTime"""

    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw) -> str:
    """specific command for postgresql for getting utc"""
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


Base = declarative_base()


class BaseModel(Base):
    """
    This class is the abstract model that inherited from other model
    """

    __abstract__ = True

    id = Column(Integer(), primary_key=True)
    created = Column(
        DateTime(),
        default=datetime.utcnow,
        server_default=utcnow(),
        nullable=False,
    )
    updated = Column(
        DateTime(),
        default=datetime.utcnow,
        onupdate=utcnow(),
        nullable=False,
        server_default=utcnow(),
        server_onupdate=utcnow(),
    )
