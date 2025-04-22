from fastapi import APIRouter, HTTPException
from app.telethon_client.client import client
from app.telethon_client.handlers import get_recent_info_posts, add_user_to_channel

router = APIRouter()


@router.get("/get-post-info/{channel_title}/{limit}")
async def get_post_info(channel_title: str, limit: int = 10):
    try:
        res = await get_recent_info_posts(client, channel_title, limit)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/add-user-in-channel/{channel_title}")
async def add_user_in_channel(channel_title: str):
    #@testblg35465
    try:
        res = await add_user_to_channel(client, channel_title)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
