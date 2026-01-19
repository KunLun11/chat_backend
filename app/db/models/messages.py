from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import AuditBase


if TYPE_CHECKING:
    from app.db.models.chats import Chat


class Message(AuditBase):
    __tablename__ = "message"

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chat.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="ID чата",
    )
    text: Mapped[str] = mapped_column(
        String(5000),
        nullable=False,
        doc="Текст",
    )
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")


__all__ = [
    "Message",
]
