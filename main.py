import asyncio
import os
import re
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv

from parser import parse_message

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ BOT_TOKEN မရှိပါ!")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔥 MARKET & DISCOUNT
MARKETS = {
    "du": ["du", "dubai", "ဒူ", "ဒူဘိုင်း"],
    "me": ["me", "mega", "မီ", "မီဂါ", "MeGA", "mega"],
    "max": ["maxi", "max", "မက်ဆီ", "မက်စီ"],
    "glo": ["glo", "global", "ဂလို"],
    "ld": ["ld", "london", "လန်ဒန်", "လန်လန်"],
    "lao": ["lao", "laos", "loadon", "laodon", "လာအို", "လာလာ"],
    "mm": ["mm", "MM"]
}

PERCENT = {
    "du": 7, "me": 7, "max": 7, "glo": 3, 
    "ld": 7, "lao": 7, "mm": 10
}

@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("✅ Bot စပြီး run နေပြီ!\n💰 ဂဏန်းပို့ရင် တွက်ပေးမယ်")

@dp.message()
async def handle(message: Message):
    text = message.text or ""
    if not text:
        return
        
    user_name = message.from_user.first_name or "User"
    
    # No numbers = ignore
    if not re.search(r'\d', text):
        return

    # 🔥 MARKET DETECT
    text_lower = text.lower()
    market_found = None
    percent = 7
    
    for key, names in MARKETS.items():
        for name in names:
            if name.lower() in text_lower:
                market_found = key.upper()
                percent = PERCENT[key]
                break
        if market_found:
            break

    # No market = call admin
    if not market_found:
        try:
            admins = await message.chat.get_administrators()
            mentions = []
            for admin in admins[:3]:
                if admin.user.username:
                    mentions.append(f"@{admin.user.username}")
                elif admin.user.first_name:
                    mentions.append(admin.user.first_name)
            
            if mentions:
                admin_text = " ".join(mentions)
                await message.reply(
                    f"📢 {admin_text}\n"
                    f"⚠️ {user_name} ရဲ့ဒါလေးလာစစ်ပေးပါရှင့်"
                )
        except:
            pass
        return

    # 🔥 PARSE & CALC
    data = parse_message(text)
    total_amount = data["grand_total"]
    
    if total_amount == 0:
        return

    # Discount calculation
    discount = int(total_amount * (percent / 100))
    final = total_amount - discount

    # 🔥 PERFECT FORMAT
    reply = (
        f"👤 {user_name}\n"
        f"{market_found} Total = {total_amount:,} ကျပ်\n"
        f"{percent}% Cash Back = {discount:,} ကျပ်\n"
        f"Total = {final:,} ကျပ် ဘဲ လွဲပါရှင့်\n\n"
        f"✨ ကံကောင်းပါစေ ✨"
    )

    await message.reply(reply)

async def main():
    print("🚀 Bot starting...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
