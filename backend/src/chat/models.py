from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from src.models import Base, BaseModel


class Conversation(Base, BaseModel):
    __tablename__ = "conversations"
    __table_args__ = (
        UniqueConstraint(
            "user_a_id", "user_b_id", name="uq_conversation_users"
        ),
    )

    user_a_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_b_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user_a = relationship("src.users.models.User", foreign_keys=[user_a_id])
    user_b = relationship("src.users.models.User", foreign_keys=[user_b_id])


# New Message model: references a single Conversation and a single User
class Message(Base, BaseModel):
    __tablename__ = "messages"

    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    text = Column(Text, nullable=False)

    # relationships
    conversation = relationship("src.chat.models.Conversation", backref="messages")
    user = relationship("src.users.models.User")
