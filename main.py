import asyncio
import os
import re
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from parser import parse_message

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

MARKETS = {
    "DUBAI": ["du", "dubai", "ဒူ", "ဒူဘိုင်း", "dubi"],
    "MEGA": ["me", "mega", "မီ", "မီဂါ"],
    "MAX": ["maxi", "max", "မက်ဆီ", "မက်စီ"],
    "GLO": ["glo", "global", "ဂလို"],
    "LD": ["ld", "london", "လန်ဒန်", "လန်လန်"],
    "LAO": ["lao", "laos", "loadon", "laodon", "လာအို", "လာလာ"],
    "MM": ["mm"]
}

PERCENT = {"DUBAI": 7, "MEGA": 7, "MAX": 7, "GLO": 3, "LD": 7, "LAO": 7, "MM": 10}

@dp.message()
async def handle(message: Message):
    if not message.text: return
    text = message.text.lower()
    
    if text == "/start":
        await message.reply("✅ Bot စပြီး run နေပြီ!\\n💰 ဂဏန်းပို့ရင် တွက်ပေးမယ်")
        return

    if not re.search(r"\\d", text): return

    market_found = None
    percent = 7
    for key, names in MARKETS.items():
        if any(name in text for name in names):
            market_found = key
            percent = PERCENT.get(key, 7)
            break

    if not market_found:
        return # Market မပါရင် ဘာမှပြန်မလုပ်စေချင်ရင် ဒါအတိုင်းထားပါ

    try:
        data = parse_message(message.text)
        total_amount = data["grand_total"]
        if total_amount == 0: return

        discount = int(total_amount * (percent / 100))
        final = total_amount - discount
        user_name = message.from_user.first_name or "User"
        
        reply = (
            f"👤 {user_name}\\n"
            f"{market_found} Total = {total_amount:,} ကျပ်\\n"
            f"{percent}% Cash Back = {discount:,} ကျပ်\\n"
            f"Total = {final:,} ကျပ်ဘဲ လွဲပါရှင့်\\n\\n"
            f"ကံကောင်းပါစေ"
        )
        await message.reply(reply)
    except Exception as e:
        logging.error(f"Error: {e}")

async def main():
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
