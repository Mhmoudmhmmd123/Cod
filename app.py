import asyncio
import re
from telethon import TelegramClient, events
import uvloop
import os

# ========================
# 👇 معلومات حسابك
# ========================
API_ID = 22439207
API_HASH = '52d91e24dd0e4331a89556a9b9ef65da'
SESSION_NAME = 'phone_session'  # نفس اسم ملف الجلسة
# ========================

# القنوات المراقبة
CHANNELS = [
    '@ho275275',
    '@Supercashly',
    '@lootearn_Com',
    '@mist_cash',
    '@flashproxybot5g',
    '@skyproxybot5G'
]

# البوتات المستهدفة
TARGET_BOTS = [
    '@MaskProxyBot',
    '@Skyproxy5G_bot',
    '@Flashproxy5G_bot'
]

uvloop.install()

# التأكد من وجود ملف الجلسة
if not os.path.exists(f'{SESSION_NAME}.session'):
    print("❌ ملف الجلسة غير موجود!")
    exit(1)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH, 
                       connection_retries=0, 
                       timeout=3)

last_processed_message_id = {}
processed_codes = set()

def extract_codes(text):
    if not text: 
        return []
    return re.findall(r'\b[A-Z0-9]{12}\b', text.upper())

async def ultra_fast_send(bot_username, text):
    try:
        await client.send_message(bot_username, text)
    except:
        pass

async def attack_single_bot(bot_username, code):
    tasks = [
        ultra_fast_send(bot_username, "🎟️ تفعيل كوبون"),
        ultra_fast_send(bot_username, code),
        ultra_fast_send(bot_username, code)
    ]
    await asyncio.gather(*tasks, return_exceptions=True)

async def attack_all_bots(code):
    tasks = [attack_single_bot(bot, code) for bot in TARGET_BOTS]
    await asyncio.gather(*tasks, return_exceptions=True)

@client.on(events.NewMessage(chats=CHANNELS))
async def hunt_handler(event):
    chat_id = event.chat_id
    message_id = event.message.id
    
    if chat_id in last_processed_message_id:
        if message_id <= last_processed_message_id[chat_id]:
            return
    
    last_processed_message_id[chat_id] = message_id
    text = event.message.text
    if not text: 
        return
    
    codes = extract_codes(text)
    if not codes: 
        return
    
    for code in codes:
        if code in processed_codes:
            continue
        processed_codes.add(code)
        await attack_all_bots(code)
    
    if len(processed_codes) > 1000:
        processed_codes.clear()

async def main():
    await client.start()
    me = await client.get_me()
    print("=" * 60)
    print("🔥 نظام الصيد الفوري شغال على Render!")
    print("=" * 60)
    print(f"👤 الحساب: {me.first_name}")
    print(f"📡 مراقبة {len(CHANNELS)} قناة")
    print(f"🎯 استهداف {len(TARGET_BOTS)} بوت")
    print("=" * 60)
    print("⚡ في انتظار الأكواد...")
    print("=" * 60)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
