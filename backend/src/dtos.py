from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional

class TodoCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description=(
            "Title of the TODO task"
        ),
    )
    description: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description=(
            "Description of the TODO task"
        ),
    )
    due_date: str = Field(
        ...,
        description=(
            "Due date in DD.MM.YYYY format"
        ),
    )

    @validator("due_date")
    def validate_due_date(cls, v):
        try:
            parsed_date = datetime.strptime(v, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Date must be in DD.MM.YYYY format")
        if parsed_date <= date.today():
            raise ValueError("Due date must be in the future")
        return v


class TodoOut(BaseModel):
    """Pydantic model for outgoing Todo objects (response)."""
    id: int = Field(
        ..., description="Unique identifier of the TODO"
    )
    title: str = Field(
        ..., description="Title of the TODO task"
    )
    description: Optional[str] = Field(
        None,
        description="Description of the TODO task"
    )
    due_date: date = Field(
        ..., description="Due date as a date object"
    )

    class Config:
        from_attributes = True
