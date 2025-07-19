from telethon import TelegramClient, events
import time

# --- Your Telegram API credentials ---
api_id = 25848597
api_hash = '16d42602ef6a27fb414123fe9c350e4f'
session_name = 'rahad_user_session'

# --- Telegram IDs ---
source_channel = 'binance_announcements'         # public channel username (no @)
target_group_id = 1001480728319                 # your group ID
owner_id = 6674173941                            # your personal Telegram user ID

# --- Track start time ---
start_time = time.time()

# --- Initialize Telethon client ---
client = TelegramClient(session_name, api_id, api_hash)

# --- Forward messages from channel to group ---
@client.on(events.NewMessage(chats=source_channel))
async def forward_handler(event):
    try:
        await client.forward_messages(entity=target_group_id, messages=event.message)
        print("✅ Message forwarded.")
    except Exception as e:
        print("❌ Forwarding error:", e)

# --- Respond to /runtime from owner only ---
@client.on(events.NewMessage(chats=target_group_id, pattern=r'^/runtime$'))
async def runtime_handler(event):
    sender = await event.get_sender()
    if sender.id == owner_id:
        uptime = int(time.time() - start_time)
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60
        reply_text = f"⏱️ Bot uptime: {hours}h {minutes}m {seconds}s"
        await event.reply(reply_text)
    else:
        print(f"❌ Unauthorized /runtime by user ID: {sender.id}")

# --- Start bot ---
async def main():
    await client.start()
    print("🤖 Bot is running... Ctrl+C to stop.")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())