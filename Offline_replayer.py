from telethon import TelegramClient, events, Button
from telethon.tl.functions.users import GetFullUserRequest
from datetime import datetime, time
import pytz
import os
import json

# ================== CONFIG ==================
api_id = 31744059
api_hash = "e4ff9d5154c2d8e1a14dc71425acdbd2"
session_name = "personal_session"

TIMEZONE = pytz.timezone("Asia/Tehran")
DATA_FILE = "/tmp/replied_users.json"  # مهم برای Cloud

PROFILE_URL = "https://t.me/your_username"

FOOTER = (
    "\n\n——\n"
    "🤖 این پیام به‌صورت خودکار ارسال شده\n"
    "🛠 ساخته شده توسط Soroush"
)
# ============================================


if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        replied_users = set(json.load(f))
else:
    replied_users = set()


def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(list(replied_users), f)


def now():
    return datetime.now(TIMEZONE)


def in_range(start, end):
    return start <= now().time() <= end


def offline_message():
    d = now().weekday()

    if d not in (3, 4) and in_range(time(7, 0), time(14, 15)):
        return "📚 من الان مدرسه‌ام، بعداً پاسخ میدم."

    if d == 5:
        if in_range(time(17, 0), time(18, 0)):
            return "💻 الان کلاس برنامه‌نویسی‌ام."
        if in_range(time(19, 0), time(21, 45)):
            return "🏋️‍♂️ الان باشگاهم."

    if d == 6 and in_range(time(17, 15), time(18, 45)):
        return "🌍 الان کلاس زبانم."

    return "❌ در دسترس نیستم."


client = TelegramClient(session_name, api_id, api_hash)


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private:
        return

    sender = await event.get_sender()
    user_id = sender.id

    if user_id in replied_users:
        return

    try:
        me = await client(GetFullUserRequest("me"))
        if me.user.status and me.user.status.__class__.__name__ == "UserStatusOnline":
            return
    except:
        pass

    text = offline_message()

    await event.respond(
        text + FOOTER,
        buttons=[
            [Button.url("📌 پروفایل من", PROFILE_URL)],
            [Button.inline("✅ متوجه شدم", b"ok")]
        ]
    )

    replied_users.add(user_id)
    save_users()


@client.on(events.CallbackQuery)
async def callback(event):
    await event.answer("👍", alert=False)


async def main():
    print("👤 Personal Auto Reply is running...")
    await client.run_until_disconnected()


client.start()
client.loop.run_until_complete(main())
