import asyncio
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import List
from src.dtos import TodoCreate, TodoOut
from src.database import get_async_db
from src.models import Todo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

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


@app.get(
    "/todos",
    response_model=List[TodoOut]
)
async def list_todos(db: AsyncSession = Depends(get_async_db)):
    """Return all todos as a list of TodoOut models."""
    result = await db.execute(select(Todo))
    todos = result.scalars().all()
    return todos


@app.get(
    "/todos/{todo_id}",
    response_model=TodoOut
)
async def get_todo(
    todo_id: int, db: AsyncSession = Depends(get_async_db)
):
    """Return a single todo by ID or raise 404 if not found."""
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id)
    )
    todo = result.scalar_one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    await asyncio.sleep(5)
    return todo


@app.post("/todos")
async def create_todo(
    todo: TodoCreate, db: AsyncSession = Depends(get_async_db)
):
    due_date = datetime.strptime(todo.due_date, "%d.%m.%Y").date()
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        due_date=due_date
    )
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)

    return db_todo
