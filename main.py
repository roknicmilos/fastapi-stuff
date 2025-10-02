from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator, ValidationError
from datetime import date, datetime
from typing import Optional

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}

    for error in exc.errors():
        field_name = error["loc"][-1]  # Get the field name (last item in location)
        error_msg = error["msg"]

        # Remove "Value error, " prefix if present
        if error_msg.startswith("Value error, "):
            error_msg = error_msg[13:]

        if field_name not in errors:
            errors[field_name] = []
        errors[field_name].append(error_msg)

    return JSONResponse(
        status_code=400,
        content={"errors": errors}
    )


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
