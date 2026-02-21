import asyncio
import base64
import os
from telethon import TelegramClient
import uvloop

# ========================
API_ID = 22439207
API_HASH = '52d91e24dd0e4331a89556a9b9ef65da'
SESSION_NAME = 'test_session'
# ========================

uvloop.install()

print("📂 جاري فك تشفير الجلسة...")
with open('session_base64.txt', 'r') as f:
    session_base64 = f.read().strip()

# فك التشفير
session_data = base64.b64decode(session_base64)
print(f"✅ تم فك التشفير: {len(session_data)} بايت")

# حفظ الملف
with open(f'{SESSION_NAME}.session', 'wb') as f:
    f.write(session_data)
print(f"✅ تم حفظ الملف: {SESSION_NAME}.session")

# التحقق من الملف
if os.path.exists(f'{SESSION_NAME}.session'):
    size = os.path.getsize(f'{SESSION_NAME}.session')
    print(f"✅ حجم الملف: {size} بايت")
    
    # محاولة قراءة أول 100 بايت للتأكد
    with open(f'{SESSION_NAME}.session', 'rb') as f:
        header = f.read(100)
    print(f"📋 أول 100 بايت: {header[:50].hex()}...")
else:
    print("❌ الملف لم يتم حفظه!")

print("\n✅ الاختبار اكتمل")
