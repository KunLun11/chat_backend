from fastapi import APIRouter, Depends, HTTPException, status

from app.deps.chats import get_chat_service
from app.schemas.messages import MessageCreate, MessageResponse
from app.services.chats import ChatService
from app.services.exceptions import BlValidationError

router = APIRouter(prefix="/chats/{chat_id}/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    chat_id: int,
    message_data: MessageCreate,
    service: ChatService = Depends(get_chat_service),
):
    try:
        message = await service.create_message(chat_id, message_data.text)
        return message
    except BlValidationError as e:
        error_msg = str(e)
        if "Chat with id" in error_msg and "not found" in error_msg:
            raise HTTPException(status_code=404, detail=error_msg)
        else:
            raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}",
        )
