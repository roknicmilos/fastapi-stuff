from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.dtos import TodoCreate
from src.database import SessionLocal, engine, get_db
from src.models import Todo
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    errors = {}
    for error in exc.errors():
        field_name = error["loc"][-1]
        error_msg = error["msg"]
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
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    due_date = datetime.strptime(todo.due_date, "%d.%m.%Y").date()
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        due_date=due_date
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo
