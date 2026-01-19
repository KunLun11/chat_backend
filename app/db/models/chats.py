from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import AuditBase


if TYPE_CHECKING:
    from app.db.models.messages import Message


class Chat(AuditBase):
    __tablename__ = "chat"

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        doc="Заголовок",
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Message.created_at.desc()",
    )


__all__ = [
    "Chat",
]
