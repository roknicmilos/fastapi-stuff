from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_async_db
from src.chat.models import Conversation
from src.chat.dtos import ConversationCreate, ConversationOut
from src.users.models import User

router = APIRouter()


@router.post("/conversations", response_model=ConversationOut)
async def start_conversation(
    conv: ConversationCreate, db: AsyncSession = Depends(get_async_db)
):
    user_a_id, user_b_id = sorted(conv.user_ids)

    # Verify both users exist
    result = await db.execute(select(User).where(
        User.id.in_([user_a_id, user_b_id]))
    )
    users = result.scalars().all()
    if len(users) != 2:
        raise HTTPException(
            status_code=404, detail="One or both users not found"
        )

    # Check if conversation already exists
    result = await db.execute(
        select(Conversation).where(
            Conversation.user_a_id == user_a_id,
            Conversation.user_b_id == user_b_id,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    db_conv = Conversation(user_a_id=user_a_id, user_b_id=user_b_id)
    db.add(db_conv)
    await db.commit()
    await db.refresh(db_conv)
    return db_conv


@router.get("/conversations/by_users", response_model=ConversationOut)
async def get_conversation_by_users(
    user_ids: list[int] = Query(
        ..., description="Provide exactly two user ids"
    ),
    db: AsyncSession = Depends(get_async_db)
):
    if len(user_ids) != 2:
        raise HTTPException(
            status_code=400, detail="Exactly two user ids must be provided"
        )
    if user_ids[0] == user_ids[1]:
        raise HTTPException(
            status_code=400, detail="User ids must be different"
        )

    user_a_id, user_b_id = sorted(user_ids)

    result = await db.execute(
        select(Conversation).where(
            Conversation.user_a_id == user_a_id,
            Conversation.user_b_id == user_b_id,
        )
    )
    conv = result.scalar_one_or_none()
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

