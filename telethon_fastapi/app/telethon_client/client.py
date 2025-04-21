import os
from telethon import TelegramClient
from config import load_config

config = load_config()

session_path = config.session_path

if not os.path.exists(session_path):
    raise FileNotFoundError("Session file not found")

client = TelegramClient(
    session=session_path.replace(".session", ""),
    api_id=config.api_id,
    api_hash=config.api_hash,
)

async def start_client():
    if not client.is_connected():
        await client.start()
        print("Telethon client started")

async def stop_client():
    if client.is_connected():
        await client.disconnect()
        print("Telethon client stopped")