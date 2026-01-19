from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repo import ChatRepository, MessageRepository
from app.db.session import get_db
from app.services.chats import ChatService


async def get_chat_service(db: Annotated[AsyncSession, Depends(get_db)]) -> ChatService:
    chat_repo = ChatRepository(db)
    message_repo = MessageRepository(db)
    return ChatService(chat_repo, message_repo)
