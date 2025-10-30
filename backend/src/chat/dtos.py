from pydantic import BaseModel, model_validator
from datetime import datetime


class ConversationStart(BaseModel):
    user_a_id: int
    user_b_id: int

    @model_validator(mode="after")
    def users_must_be_different(self) -> "ConversationStart":
        # both fields are typed so None should not normally appear,
        # but keep an explicit check to provide a clear error message.
        if self.user_a_id is None or self.user_b_id is None:
            raise ValueError("Both user_a_id and user_b_id must be provided")
        if self.user_a_id == self.user_b_id:
            raise ValueError("Conversation must be between two different users")
        return self


class ConversationOut(BaseModel):
    id: int
    user_a_id: int
    user_b_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageOut(BaseModel):
    id: int
    conversation_id: int
    user_id: int
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}


# Model representing a conversation with nested messages.
# Messages are ordered newest -> oldest.
class ConversationWithMessagesOut(BaseModel):
    id: int
    user_a_id: int
    user_b_id: int
    created_at: datetime
    messages: list[MessageOut]

    model_config = {"from_attributes": True}


# New DTO for creating a message: requires conversation_id,
# user_id, and non-empty text
class MessageCreate(BaseModel):
    conversation_id: int
    user_id: int
    text: str

    @model_validator(mode="after")
    def text_must_not_be_empty(self) -> "MessageCreate":
        # strip whitespace and ensure not empty
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text must be a non-empty string")
        # normalize text (trim)
        self.text = self.text.strip()
        return self
