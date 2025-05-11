from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.telethon_client.client import client
from app.telethon_client.handlers import get_post_info, get_posts_info, get_channel_info
from app.exceptions import (
    NotFoundException,
    ForbiddenException,
    InvalidException,
    CustomErrorException,
)

router = APIRouter()

# GET /tg-api/channels/{channel_name}/posts/?limit=100


@router.get("/channels/{channel_name}/posts/")
async def get_posts(channel_name: str, limit: int):
    res = await get_posts_info(client, channel_name, limit=limit)
    if res and isinstance(res, dict) and (code_error := res.get("code")):
        message = res.get("message")
        if code_error == "PostNotFoundError":
            raise NotFoundException(message, code_error)
        elif code_error == "ChannelPrivateError":
            raise ForbiddenException(message, code_error)
        elif code_error == "ChannelInvalidError":
            raise InvalidException(message, code_error)
        elif code_error == "ValueError":
            raise NotFoundException(message, code_error)
        elif code_error == "Exception":
            raise CustomErrorException(500, "Не получен ответ от АПИ")
    else:
        return res


@router.get("/channels/{channel_name}/posts/{id}")
async def get_post(channel_name: str, id: int):
    res = await get_posts_info(client, channel_name, post_id=id)
    if res and (code_error := res.get("code")):
        message = res.get("message")
        if code_error == "PostNotFoundError":
            raise NotFoundException(message, code_error)
        elif code_error == "ChannelPrivateError":
            raise ForbiddenException(message, code_error)
        elif code_error == "ChannelInvalidError":
            raise InvalidException(message, code_error)
        elif code_error == "ValueError":
            raise NotFoundException(message, code_error)
        elif code_error == "Exception":
            raise CustomErrorException(500, "Не получен ответ от АПИ")
    else:
        return res


@router.get("/channels/{channel_name}")
async def get_channel(channel_name: str):
    res = await get_channel_info(client, channel_name)
    if res and (code_error := res.get("code")):
        message = res.get("message")
        if code_error == "UsernameNotOccupiedError":
            raise NotFoundException(message, code_error)
        elif code_error == "UsernameInvalidError":
            raise InvalidException(message, code_error)
        elif code_error == "ChannelPrivateError":
            raise ForbiddenException(message, code_error)
        elif code_error == "ChannelInvalidError":
            raise InvalidException(message, code_error)
        elif code_error == "ValueError":
            raise NotFoundException(message, code_error)
        elif code_error == "Exception":
            raise CustomErrorException(500, "Не получен ответ от АПИ")
    else:
        return res
