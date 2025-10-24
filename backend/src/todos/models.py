from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from src.models import Base, BaseModel

class Todo(Base, BaseModel):
    __tablename__ = "todos"

    title = Column(String(20), nullable=False)
    description = Column(String(100), nullable=True)
    due_date = Column(Date, nullable=False)
