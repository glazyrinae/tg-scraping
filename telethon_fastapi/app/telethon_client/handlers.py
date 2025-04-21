from collections import defaultdict
from telethon.tl.types import ReactionEmoji
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import GetMessagesRequest


async def test_connect(client) -> str:
    try:
        me = await client.get_me()
        return f"ID: {me.id}, Имя: {me.first_name}"
    except Exception as e:
        return f"Error: {e}"


async def get_recent_info_posts(client, channel_title: str, limit: int = 10):
    resset_posts_info = []
    channel = await client.get_entity(channel_title)
    posts = await client.get_messages(channel, limit=limit)
    for post in posts:
        cnt_comments_post = await get_count_comments_for_post(client, channel, post.id)
        cnt_reactions_post = await get_count_reactions_for_post(client, channel, post.id)
        resset_posts_info.append(
            {
                "post_id": post.id,
                "post_date": post.date,
                "content": post.text,
                "views": post.views if post.views else 0,
                "comments": cnt_comments_post,
                "reactions": cnt_reactions_post
            }
        )
    return resset_posts_info


async def get_count_comments_for_post(client, channel, post_id):
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

async def get_count_reactions_for_post(client, channel, post_id):
    try:
        cnt = 0
        reactions = await client(GetMessagesRequest(channel, [post_id]))
        for msg in reactions.messages:
            if msg.reactions and msg.reactions.results:
                cnt += msg.reactions.results[0].count
        return cnt
    except Exception:
        return 0


async def get_last_post_id(client, channel_title: str) -> int:
    channel = await client.get_entity(channel_title)
    last_message = await client.get_messages(channel, limit=1)
    if last_message:
        return last_message[0].id
    return 0
