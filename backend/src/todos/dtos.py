from datetime import date, datetime

from pydantic import BaseModel, Field, validator


class TodoCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Title of the TODO task",
    )
    description: str | None = Field(
        None,
        min_length=3,
        max_length=100,
        description="Description of the TODO task",
    )
    due_date: str = Field(
        ...,
        description="Due date in DD.MM.YYYY format",
    )

    @validator("due_date")
    def validate_due_date(cls, v: str) -> str:
        try:
            parsed_date = datetime.strptime(v, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Date must be in DD.MM.YYYY format") from None
        if parsed_date <= date.today():
            raise ValueError("Due date must be in the future")
        return v


class TodoOut(BaseModel):
    """Pydantic model for outgoing Todo objects (response)."""

    id: int = Field(..., description="Unique identifier of the TODO")
    title: str = Field(..., description="Title of the TODO task")
    description: str | None = Field(
        None, description="Description of the TODO task"
    )
    due_date: date = Field(..., description="Due date as a date object")
    created_at: datetime = Field(
        ..., description="Timestamp of when the TODO was created"
    )

    class Config:
        from_attributes = True
