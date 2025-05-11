from telethon.tl.types import InputPeerChannel, MessageEntityTextUrl
from telethon.tl.functions.channels import GetMessagesRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import User, Chat, Channel
from telethon import TelegramClient
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    UsernameInvalidError,
    UsernameNotOccupiedError,
    MessageIdInvalidError,
)
from typing import Union


async def check_connect(client: TelegramClient) -> str:
    try:
        me = await client.get_me()
        return f"ID: {me.id}, Имя: {me.first_name}"
    except Exception as e:
        return f"Error: {e}"


async def get_channel_info(client: TelegramClient, channel_name: str) -> dict:
    try:
        channel = await client.get_entity(channel_name)
        res_channel = await client(GetFullChannelRequest(channel))
        res_message = await client.get_messages(channel, limit=1)
        total_posts = res_message[0].id if res_message[0].id else 0
        return {
            "data": {
                "channel_id": channel.id,
                "channel_name": channel_name,
                "title": channel.title,
                "description": res_channel.full_chat.about,
                "created_at": channel.date,
                "is_verified": channel.verified,
                "is_restricted": channel.restricted,
                "is_scam": channel.scam,
                "is_fake": channel.fake,
                "join_request": channel.join_request,
                "subscribers_count": res_channel.full_chat.participants_count,
                "total_posts": total_posts,
            },
        }
    except UsernameNotOccupiedError:
        return {
            "code": "UsernameNotOccupiedError",
            "message": f"Канал с {channel_name} не существует",
        }
    except UsernameInvalidError:
        return {
            "code": "UsernameInvalidError",
            "message": f"Некорректный username: {channel_name}",
        }
    except ChannelPrivateError:
        return {
            "code": "ChannelPrivateError",
            "message": f"Канал {channel_name} приватный и недоступен",
        }
    except ChannelInvalidError:
        return {
            "code": "ChannelInvalidError",
            "message": f"Канал {channel_name} недействителен или не существует",
        }
    except ValueError:
        return {
            "code": "ValueError",
            "message": f"Не удалось найти канал {channel_name}",
        }
    except Exception as e:
        return {"code": "Exception", "message": f"Неизвестная ошибка: {e}"}


async def get_posts_info(
    client: TelegramClient, channel_title: str, post_id: int = 0, limit: int = 1
) -> list[dict]:
    try:
        channel = await client.get_entity(channel_title)
        peer_channel = InputPeerChannel(channel.id, channel.access_hash)
        if post_id:
            post = await client.get_messages(peer_channel, ids=post_id)
            res = await get_post_info(client, channel, post)
            return res
        posts = await client.get_messages(peer_channel, limit=limit)
        res_posts = []
        for post in posts:
            res = await get_post_info(client, channel, post)
            res_posts.append(res)
        return res_posts
    except MessageIdInvalidError:
        return {
            "code": "PostNotFoundError",
            "message": f"Пост с {post.id} не существует",
        }
    except ChannelPrivateError:
        return {
            "code": "ChannelPrivateError",
            "message": f"Канал с постом {post.id} приватный и недоступен",
        }
    except ChannelInvalidError:
        return {
            "code": "ChannelInvalidError",
            "message": f"Канал с постом {post.id} недействителен или не существует",
        }
    except ValueError:
        return {
            "code": "ValueError",
            "message": f"Не удалось найти канал с постом {post.id}",
        }
    except Exception as e:
        return {"code": "Exception", "message": f"Неизвестная ошибка: {e}"}


async def get_post_info(client: TelegramClient, channel, post) -> dict:
    # try:
    # channel = await client.get_entity(channel_title)
    # peer_channel = InputPeerChannel(channel.id, channel.access_hash)
    # post = await client.get_messages(peer_channel, ids=post_id)
    cnt_comments_post = await get_count_comments_for_post(client, channel, post.id)
    res = (
        [
            {"url": entity.url}
            for entity in post.entities
            if isinstance(entity, MessageEntityTextUrl)
        ]
        if post.entities
        else []
    )
    return {
        "data": {
            "post_id": post.id,
            "channel_id": channel.id,
            "forwarded_from_id": post.fwd_from.from_id.channel_id
            if post.fwd_from and post.fwd_from.from_id.channel_id
            else post.fwd_from,
            "created_at": post.date,
            "text": post.message,
            "links": res,
            "is_post": post.post,
            "is_pinned": post.pinned,
            "restriction_reason": post.restriction_reason,
            "views_count": post.views if post.views else 0,
            "reactions": post.reactions,
            "comments_count": cnt_comments_post,
            "comments_enabled": post.replies.comments if post.replies else None,
            "forwards_count": post.forwards,
        },
    }
    # except MessageIdInvalidError:
    #     return {
    #         "code": "PostNotFoundError",
    #         "message": f"Пост с {post.id} не существует",
    #     }
    # except ChannelPrivateError:
    #     return {
    #         "code": "ChannelPrivateError",
    #         "message": f"Канал с постом {post.id} приватный и недоступен",
    #     }
    # except ChannelInvalidError:
    #     return {
    #         "code": "ChannelInvalidError",
    #         "message": f"Канал с постом {post.id} недействителен или не существует",
    #     }
    # except ValueError:
    #     return {
    #         "code": "ValueError",
    #         "message": f"Не удалось найти канал с постом {post.id}",
    #     }
    # except Exception as e:
    #     return {"code": "Exception", "message": f"Неизвестная ошибка: {e}"}


async def get_count_comments_for_post(
    client: TelegramClient,
    channel: Union[User, Chat, Channel],
    post_id: int,
) -> int:
    try:
        peer_channel = InputPeerChannel(channel.id, channel.access_hash)
        comments = await client.get_messages(
            entity=peer_channel,
            reply_to=post_id,
            limit=1,
        )
        return comments.total
    except Exception:
        return 0


async def get_count_reactions_for_post(
    client: TelegramClient,
    channel: Union[User, Chat, Channel],
    post_id: int,
) -> int:
    try:
        cnt = 0
        reactions = await client(GetMessagesRequest(channel, [post_id]))
        for msg in reactions.messages:
            if msg.reactions and msg.reactions.results:
                cnt += msg.reactions.results[0].count
        return cnt
    except Exception:
        return 0


async def get_last_post_id(
    client: TelegramClient,
    channel: Union[User, Chat, Channel],
) -> int:
    # channel = await client.get_entity(channel_title)
    last_message = await client.get_messages(channel, limit=1)
    if last_message:
        return last_message[0].id
    return 0
