from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List


class ConversationCreate(BaseModel):
    user_ids: List[int] = Field(..., description="Exactly two user IDs")

    @validator("user_ids")
    def validate_two_users(cls, v):
        if not isinstance(v, list) or len(v) != 2:
            raise ValueError("Exactly two user IDs must be provided")
        if v[0] == v[1]:
            raise ValueError("Conversation must be between two different users")
        return v


class ConversationOut(BaseModel):
    id: int
    user_a_id: int
    user_b_id: int
    created_at: datetime

    class Config:
        from_attributes = True

