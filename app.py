import asyncio
import re
import base64
import os
from telethon import TelegramClient, events
import uvloop

# ========================
API_ID = 22439207
API_HASH = '52d91e24dd0e4331a89556a9b9ef65da'
SESSION_NAME = 'render_session'
# ========================

CHANNELS = [
    '@ho275275', '@Supercashly', '@lootearn_Com',
    '@mist_cash', '@flashproxybot5g', '@skyproxybot5G'
]

TARGET_BOTS = [
    '@MaskProxyBot', '@Skyproxy5G_bot', '@Flashproxy5G_bot'
]

uvloop.install()

# قراءة وفك تشفير الجلسة
try:
    with open('session_base64.txt', 'r') as f:
        session_base64 = f.read().strip()
    
    # فك التشفير وكتابة الملف
    session_data = base64.b64decode(session_base64)
    with open(f'{SESSION_NAME}.session', 'wb') as f:
        f.write(session_data)
    print(f"✅ تم إنشاء ملف الجلسة: {SESSION_NAME}.session بحجم {len(session_data)} بايت")
except Exception as e:
    print(f"❌ خطأ في قراءة ملف الجلسة: {e}")

# التحقق من وجود الملف
if os.path.exists(f'{SESSION_NAME}.session'):
    print(f"✅ ملف الجلسة موجود بحجم {os.path.getsize(f'{SESSION_NAME}.session')} بايت")
else:
    print("❌ ملف الجلسة غير موجود!")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

last_processed_message_id = {}
processed_codes = set()

def extract_codes(text):
    if not text: return []
    return re.findall(r'\b[A-Z0-9]{12}\b', text.upper())

async def ultra_fast_send(bot_username, text):
    try:
        await client.send_message(bot_username, text)
    except Exception as e:
        print(f"⚠️ خطأ في الإرسال: {e}")

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
    if not text: return
    
    codes = extract_codes(text)
    if not codes: return
    
    print(f"🎯 تم العثور على {len(codes)} كود")
    for code in codes:
        if code in processed_codes:
            continue
        processed_codes.add(code)
        print(f"🚀 إرسال {code}")
        await attack_all_bots(code)
    
    if len(processed_codes) > 1000:
        processed_codes.clear()

async def main():
    if not os.path.exists(f'{SESSION_NAME}.session'):
        print("❌ لا يمكن البدء: ملف الجلسة غير موجود!")
        return
        
    await client.start()
    me = await client.get_me()
    print("=" * 60)
    print("🔥 نظام الصيد الفوري شغال!")
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
