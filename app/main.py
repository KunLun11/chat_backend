from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import chats_router, messages_router

app = FastAPI(
    title="Chat API",
    description="API для управления чатами и сообщениями",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chats_router)
app.include_router(messages_router)
