from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_async_db
from src.users.models import User
from src.users.dtos import UserCreate, UserOut

router = APIRouter()


@router.get("/users", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).order_by(User.created_at))
    users = result.scalars().all()
    return users


@router.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    # Ensure username is unique
    result = await db.execute(select(User).where(User.username == user.username))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = User(username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
