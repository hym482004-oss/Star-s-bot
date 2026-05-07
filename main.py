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
MARKETS = ["du", "mega", "max", "glo", "ld", "lao", "mm"]


@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Bot စပြီး run နေပြီ ✅")


@dp.message()
async def handle(message: Message):

    text = message.text.lower()

    # ❌ no number → ignore
    if not re.search(r"\d", text):
        return

    # ❌ no 2D name → mention owner/admin
    if not any(m in text for m in MARKETS):

        admins = await message.chat.get_administrators()

        mentions = []
        for a in admins:
            if a.user.username:
                mentions.append(f"@{a.user.username}")

        await message.reply(
            "⚠️ 2D name မပါသေးပါ\n\n"
            + " ".join(mentions)
            + "\nဒါလေးလာစစ်ပေးပါရှင့်"
        )
        return

    # 🔥 PARSE
    data = parse_message(message.text)

    # 🔥 ONLY TOTAL FORMAT OUTPUT
    for line in data["lines"]:

        reply = (
            f"👤 ထိုးသူ = {line['amount'] or 100}\n"
            f"2D name = OK\n"
            f"Total = {line['total']} ကျပ်\n"
            f"% Cash Back = {line['percent']}%\n"
            f"လွဲရမည့်ငွေ = {line['total']} ကျပ်\n\n"
            "ကံကောင်းပါစေ 🍀"
        )

        await message.reply(reply)

    # GRAND TOTAL
    await message.reply(f"🔥 GRAND TOTAL = {data['grand_total']}")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
