from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator, AsyncGenerator

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# Sync engine (for existing code and migrations)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async engine
async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


# Dependency for getting DB session (sync)
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency for getting async DB session
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
