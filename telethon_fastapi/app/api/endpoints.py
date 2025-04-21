from fastapi import APIRouter, HTTPException
from app.telethon_client.client import client
from app.telethon_client.handlers import get_recent_info_posts

router = APIRouter()


@router.get("/get-post-info/{channel_title}/{limit}")
async def get_post_info(channel_title: str, limit: int = 10):
    try:
        res = await get_recent_info_posts(client, channel_title, limit)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
