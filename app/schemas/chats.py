from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.messages import MessageResponse


class ChatBase(BaseModel):
    title: str


class ChatCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def trim_title(cls, v):
        return v.strip() if isinstance(v, str) else v


class ChatResponse(ChatBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatWithMessagesResponse(ChatResponse):
    messages: list[MessageResponse]
