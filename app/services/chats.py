from typing import Optional

from app.db.models.chats import Chat
from app.db.models.messages import Message
from app.db.repo import ChatRepository, MessageRepository
from app.services.exceptions import BlValidationError


class ChatService:
    def __init__(self, chat_repo: ChatRepository, message_repo: MessageRepository):
        self.chat_repo = chat_repo
        self.message_repo = message_repo

    async def create_chat(self, title: str) -> Chat:
        if not title:
            raise BlValidationError("The title cannot be empty")
        if not 1 <= len(title) <= 200:
            raise BlValidationError("Title must be between 1 and 200 characters")
        chat = Chat(title=title)
        return await self.chat_repo.create(chat)

    async def get_chat_with_last_messages(
        self, chat_id: int, limit: int = 20
    ) -> Optional[Chat]:
        if not 1 <= limit <= 100:
            limit = 20

        chat = await self.chat_repo.get_by_id_with_messages(chat_id, limit)
        return chat

    async def create_message(self, chat_id: int, text: str) -> Message:
        chat = await self.chat_repo.get_by_id(chat_id)
        if not chat:
            raise BlValidationError("Chat not found")
        if not text:
            raise BlValidationError("The text cannot be empty")
        if not 1 <= len(text) <= 5000:
            raise BlValidationError("Text must be between 1 and 5000 characters")
        message = Message(chat_id=chat_id, text=text)
        return await self.message_repo.create(message)

    async def delete_chat(self, chat_id: int) -> bool:
        chat = await self.chat_repo.get_by_id(chat_id)
        if not chat:
            return False
        await self.chat_repo.delete(chat)
        return True
