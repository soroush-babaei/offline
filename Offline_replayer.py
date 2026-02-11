import os
from telethon import TelegramClient

api_id = 31744059
api_hash = "e4ff9d5154c2d8e1a14dc71425acdbd2"

session_name = "personal_session"

# Use proxy only locally, not on PythonAnywhere
use_proxy = not os.getenv('PYTHONANYWHERE_DOMAIN')

if use_proxy:
    proxy = (
        "http",
        "91.107.172.155",
        443
    )
    client = TelegramClient(
        session_name,
        api_id,
        api_hash,
        proxy=proxy
    )
else:
    # Direct connection (no proxy) for PythonAnywhere
    client = TelegramClient(
        session_name,
        api_id,
        api_hash
    )

client.start()
print("✅ Connected using MTProxy")
client.run_until_disconnected()
