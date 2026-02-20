import asyncio
import re
from telethon import TelegramClient, events
import uvloop

# ========================
# 👇 معلومات حسابك
# ========================
API_ID = 22439207
API_HASH = '52d91e24dd0e4331a89556a9b9ef65da'
PHONE_NUMBER = '+213542067920'  # ضع الرقم الجديد هنا
SESSION_NAME = 'auto_fisher_session'
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
client = TelegramClient(SESSION_NAME, API_ID, API_HASH, connection_retries=0, timeout=3, flood_sleep_threshold=0)

last_processed_message_id = {}
processed_codes = set()

def extract_codes(text):
    if not text: return []
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
    await asyncio.gather(*tasks,
