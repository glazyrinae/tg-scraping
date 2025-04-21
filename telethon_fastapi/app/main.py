# from fastapi import FastAPI
# from fastapi import APIRouter, HTTPException

# # from bot.core import client, start_client, stop_client
# from bot.handlers.analytics import get_last_post_id
# from contextlib import asynccontextmanager


# import os
# from telethon import TelegramClient
# from config import load_config

# config = load_config()

# session_path = "/app/bot/saved_session/my_session_name.session"

# if not os.path.exists(session_path):
#     raise FileNotFoundError("Session file not found")

# client = TelegramClient(
#     session=session_path.replace(".session", ""),
#     api_id=config.api_id,
#     api_hash=config.api_hash,
# )


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Подключение
#     try:
#         if not client.is_connected():
#             await client.start()
#     except Exception as e:
#         raise
    
#     yield
    
#     # Отключение
#     try:
#         if client.is_connected():
#             await client.disconnect()
#     except Exception as e:
#         pass


# app = FastAPI(lifespan=lifespan)


# @app.get("/users")
# async def send_message():
#     try:
#         # Отправка сообщения
#         #await client.start()
#         res = await get_last_post_id(client, "testblg35465")
#         return {"status": f"Message sent - {res}"}
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=400, detail=str(e))


# # if __name__ == "__main__":
# #     with client:
# #         client.loop.run_until_complete(main())

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.telethon_client.client import start_client, stop_client, client
from app.api.endpoints import router as api_router

from app.telethon_client.handlers import get_recent_info_posts

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск при старте приложения
    await start_client()
    yield
    # Остановка при завершении
    await stop_client()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api")

# @app.get("/")
# async def root():
#     res = await get_recent_info_posts(client, "testblg35465")
#     return res #{"message": "Telethon + FastAPI working!"}