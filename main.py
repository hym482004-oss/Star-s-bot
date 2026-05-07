import asyncio
import os
import re
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from parser import parse_message

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔥 MARKET LIST & PERCENTAGE
MARKETS = {
    "du": ["du", "dubai", "ဒူ", "ဒူဘိုင်း"],
    "me": ["me", "mega", "မီ", "မီဂါ"],
    "max": ["maxi", "max", "မက်ဆီ", "မက်စီ"],
    "glo": ["glo", "global", "ဂလို"],
    "ld": ["ld", "london", "လန်ဒန်", "လန်လန်"],
    "lao": ["lao", "laos", "loadon", "laodon", "လာအို", "လာလာ"],
    "mm": ["mm"]
}

PERCENT = {
    "du": 9,  # Now set to 9% as requested
    "me": 7,
    "max": 7,
    "glo": 3,
    "ld": 7,
    "lao": 7,
    "mm": 10
}


@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Bot စပြီး run နေပြီ ✅")


@dp.message()
async def handle(message: Message):

    text = message.text.lower()
    user_name = message.from_user.first_name or "User"

    # ❌ no number → ignore
    if not re.search(r"\d", text):
        return

    # 🔍 DETECT MARKET
    market_found = None
    percent = 7
    for key, names in MARKETS.items():
        for name in names:
            if name.lower() in text:
                market_found = key.upper()
                percent = PERCENT.get(key, 7)
                break
        if market_found:
            break

    if not market_found:
        admins = await message.chat.get_administrators()
        mentions = []
        for a in admins:
            if a.user.username:
                mentions.append(f"@{a.user.username}")
        if not mentions:
            mentions = ["@owner", "@admin1"]

        await message.reply(
            f"📢 {' '.join(mentions)}\n"
            f"⚠️ {user_name} ရဲ့ဒါလေးလာစစ်ပေးပါရှင့်"
        )
        return

    # 🔥 PARSE
    data = parse_message(message.text)
    total_amount = data["grand_total"]
    
    if total_amount == 0:
        return # လုံးဝမတွက်ချက်ရင် ပြန်မပေးတော့ဘူး

    discount = int(total_amount * (percent / 100))
    final = total_amount - discount

    # 🔥 OUTPUT FORMAT
    reply = (
        f"👤 {user_name}\n"
        f"{market_found} Total = {total_amount:,} ကျပ်\n"
        f"{percent}% Cash Back = {discount:,} ကျပ်\n"
        f"Total = {final:,} ကျပ်ဘဲ လွဲပါရှင့်\n"
        f"ကံကောင်းပါစေ"
    )

    await message.reply(reply)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
