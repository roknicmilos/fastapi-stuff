from fastapi import APIRouter, HTTPException, Depends, Query, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_async_db
from src.chat.models import Conversation
from src.chat.dtos import ConversationOut, ConversationStart
from src.users.models import User

router = APIRouter()


@router.post("/conversations", response_model=ConversationOut)
async def start_conversation(
    conv: ConversationStart,
    response: Response,
    db: AsyncSession = Depends(get_async_db)
):
    # Accept exactly two explicit fields: user_id and agent_id
    user_a_id, user_b_id = sorted([conv.user_id, conv.agent_id])

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
        # Return 200 when conversation already exists
        response.status_code = status.HTTP_200_OK
        return existing

    db_conv = Conversation(user_a_id=user_a_id, user_b_id=user_b_id)
    db.add(db_conv)
    await db.commit()
    await db.refresh(db_conv)

    # Return 201 when newly created
    response.status_code = status.HTTP_201_CREATED
    return db_conv


@router.get("/conversations", response_model=list[ConversationOut])
async def list_conversations(db: AsyncSession = Depends(get_async_db)):
    """Return all conversations."""
    result = await db.execute(select(Conversation))
    conversations = result.scalars().all()
    return conversations


@router.get("/conversations/by_users", response_model=ConversationOut)
async def get_conversation_by_users(
    user_a: str = Query(
        ..., description="Username of the first user (user_a)"
    ),
    user_b: str = Query(
        ..., description="Username of the second user (user_b)"
    ),
    db: AsyncSession = Depends(get_async_db)
):
    """Find a conversation by two usernames provided as separate query params.

    The two usernames must be different. The users are looked up by username
    to obtain their IDs; IDs are then ordered and used to query the Conversation
    table (same ordering convention used elsewhere).
    """
    if user_a == user_b:
        raise HTTPException(
            status_code=400, detail="Usernames must be different"
        )

    result = await db.execute(
        select(Conversation).where(
            Conversation.user_a_id == int(user_a),
            Conversation.user_b_id == int(user_b),
        )
    )
    conversation = result.scalar_one_or_none()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation
