from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.telethon_client.client import start_client, stop_client
from app.api.endpoints import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_client()
    yield
    await stop_client()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api")
