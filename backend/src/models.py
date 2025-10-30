from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BaseModel:
    """Mixin providing `id` and `created_at` columns for all models.

    Concrete models should inherit both from `Base` and `BaseModel`
    (e.g. `class User(Base, BaseModel):`).
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
