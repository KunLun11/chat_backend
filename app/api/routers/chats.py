from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.deps.chats import get_chat_service
from app.schemas.chats import ChatCreate, ChatResponse, ChatWithMessagesResponse
from app.services.chats import ChatService
from app.services.exceptions import BlValidationError

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_data: ChatCreate,
    service: ChatService = Depends(get_chat_service),
):
    try:
        chat = await service.create_chat(chat_data.title)
        return chat
    except BlValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{chat_id}", response_model=ChatWithMessagesResponse)
async def get_chat(
    chat_id: int,
    service: ChatService = Depends(get_chat_service),
    limit: Annotated[int, Query(ge=1, le=100, description="Количество сообщений")] = 20,
):
    chat = await service.get_chat_with_last_messages(chat_id, limit)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found",
        )
    return chat


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: int,
    service: ChatService = Depends(get_chat_service),
):
    deleted = await service.delete_chat(chat_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found",
        )
