from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional

app = FastAPI()


class TodoCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Title of the TODO task"
    )
    description: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="Description of the TODO task"
    )
    due_date: str = Field(
        ...,
        description="Due date in DD.MM.YYYY format"
    )

    @validator('due_date')
    def validate_due_date(cls, v):
        try:
            # Parse the date from DD.MM.YYYY format
            parsed_date = datetime.strptime(v, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError('Date must be in DD.MM.YYYY format')

        # Check if the date is in the future
        if parsed_date <= date.today():
            raise ValueError('Due date must be in the future')

        return v


@app.get("/")
def read_root():
    return {"message": "hello world"}


@app.post("/todos")
def create_todo(todo: TodoCreate):
    # Format the response message
    description_text = (
        f"Description: {todo.description}"
        if todo.description
        else ""
    )

    message = (
        f"You've successfully created a new TODO task labeled: "
        f"\"{todo.title}\". Make sure you finish it by {todo.due_date}!"
    )

    return {
        "message": message,
        "details": description_text
    }
