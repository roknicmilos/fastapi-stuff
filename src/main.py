from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.dtos import TodoCreate
from datetime import date, datetime
from typing import Optional

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    errors = {}

    for error in exc.errors():
        field_name = error["loc"][
            -1]  # Get the field name (last item in location)
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
