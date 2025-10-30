from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import asyncio
import json
from datetime import datetime
import os
from redis.asyncio import Redis

from src.database import get_async_db
from src.todos.models import Todo
from src.todos.dtos import TodoCreate, TodoOut
from src.ws import ws_manager

router = APIRouter()

# Redis client used for caching within the todos router
redis = Redis.from_url(
    os.getenv("REDIS_URL"), encoding="utf-8", decode_responses=True
)


@router.get("/todos", response_model=list[TodoOut])
async def list_todos(db: AsyncSession = Depends(get_async_db)):
    """Return all todos as a list of TodoOut models."""
    result = await db.execute(select(Todo).order_by(desc(Todo.created_at)))
    todos = result.scalars().all()
    return todos


@router.get("/todos/{todo_id}", response_model=TodoOut)
async def get_expensive_todo(
    todo_id: int, db: AsyncSession = Depends(get_async_db)
):
    cache_key = f"todo:{todo_id}"
    cached_todo = await redis.get(cache_key)
    if cached_todo:
        data = json.loads(cached_todo)
        return TodoOut.model_validate(data)

    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    await asyncio.sleep(5)

    todo_out = TodoOut.model_validate(todo)
    await redis.setex(cache_key, 20, todo_out.model_dump_json())

    return todo


@router.post("/todos")
async def create_todo(
    todo: TodoCreate, db: AsyncSession = Depends(get_async_db)
):
    due_date = datetime.strptime(todo.due_date, "%d.%m.%Y").date()
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        due_date=due_date,
    )
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)

    todo_out = TodoOut.model_validate(db_todo)
    await ws_manager.broadcast(todo_out.model_dump_json())
    return db_todo
