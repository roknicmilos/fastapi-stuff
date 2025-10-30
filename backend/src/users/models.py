from sqlalchemy import Column, String

from src.models import Base, BaseModel


class User(Base, BaseModel):
    __tablename__ = "users"

    username = Column(String(50), nullable=False, unique=True, index=True)
