from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.chats import Chat
from app.db.models.messages import Message


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, chat_id: int) -> Optional[Chat]:
        stmt = select(Chat).where(Chat.id == chat_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_with_messages(
        self,
        chat_id: int,
        limit: int = 20,
    ) -> Optional[Chat]:
        chat_stmt = select(Chat).where(Chat.id == chat_id)
        chat_result = await self.db.execute(chat_stmt)
        chat = chat_result.scalar_one_or_none()
        if not chat:
            return None

        messages_stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        messages_result = await self.db.execute(messages_stmt)
        messages = list(messages_result.scalars().all())
        chat.messages = messages
        return chat

    async def create(self, chat: Chat) -> Chat:
        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    async def delete(self, chat: Chat) -> None:
        await self.db.delete(chat)
        await self.db.commit()


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, message: Message) -> Message:
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_by_chat_id(self, chat_id: int) -> list[Message]:
        stmt = select(Message).where(Message.chat_id == chat_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_last_by_chat_id(self, chat_id: int, limit: int) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
