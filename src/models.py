from sqlalchemy import Column, Integer, String, Date
from src.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(20), nullable=False)
    description = Column(String(100), nullable=True)
    due_date = Column(Date, nullable=False)
