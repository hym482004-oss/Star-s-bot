import asyncio
import os
import re
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from parser import parse_message

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

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
    text = message.text.lower()
    if not re.search(r"\d", text): return

    market_found = None
    percent = 7
    for key, names in MARKETS.items():
        if any(name in text for name in names):
            market_found = key
            percent = PERCENT.get(key, 7)
            break

    if not market_found:
        # Market name မပါရင် admin ကို mention ခေါ်ဖို့ logic
        return 

    data = parse_message(message.text)
    total_amount = data["grand_total"]
    
    if total_amount == 0: return

    discount = int(total_amount * (percent / 100))
    final = total_amount - discount
    user_name = message.from_user.first_name

    reply = (
        f"👤 {user_name}\n"
        f"{market_found} Total = {total_amount:,} ကျပ်\n"
        f"{percent}% Cash Back = {discount:,} ကျပ်\n"
        f"Total = {final:,} ကျပ်ဘဲ လွဲပါရှင့်\n\n"
        f"ကံကောင်းပါစေ"
    )
    await message.reply(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
