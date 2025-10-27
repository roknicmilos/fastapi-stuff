from pydantic import BaseModel, model_validator
from datetime import datetime


class ConversationStart(BaseModel):
    user_a_id: int
    user_b_id: int

    @model_validator(mode="after")
    def users_must_be_different(self):
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
