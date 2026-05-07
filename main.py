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

# 🔥 2D NAME LIST
MARKETS = ["du", "mega", "မီ", "max", "glo", "ld", "lao", "mm"]
PERCENT = {
    "du": 7,
    "mega": 7,
    "မီ": 7,
    "max": 7,
    "glo": 7,
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

    # ❌ no 2D name → mention owner/admin
    market_found = None
    percent = 7
    for m in MARKETS:
        if m in text:
            market_found = m.upper()
            percent = PERCENT.get(m, 7)
            break

    if not market_found:
        admins = await message.chat.get_administrators()
        mentions = []
        for a in admins:
            if a.user.username:
                mentions.append(f"@{a.user.username}")
        if not mentions:
            mentions = ["@owner", "@admin1"] # Default

        await message.reply(
            f"📢 {' '.join(mentions)}\n"
            f"⚠️ {user_name} ရဲ့ဒါလေးလာစစ်ပေးပါရှင့်"
        )
        return

    # 🔥 PARSE
    data = parse_message(message.text)
    total_amount = data["grand_total"]
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
