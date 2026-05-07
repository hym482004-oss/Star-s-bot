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

# 🔥 2D names
MARKETS = ["du", "mega", "max", "glo", "ld", "lao", "mm"]


@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("2D Bot စပြီး run နေပြီ ✅")


@dp.message()
async def handle(message: Message):

    text = message.text.lower()

    # ❌ ignore no number
    if not re.search(r"\d", text):
        return

    # ❌ no 2D name → mention admin
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

    # 🔥 parse
    data = parse_message(message.text)

    for line in data["lines"]:

        reply_text = (
            f"ထိုးသူ = {line['amount']}\n"
            f"2D name = DETECTED\n"
            f"Total = {int(line['total'])} ကျပ်\n"
            f"% cash back = {line['percent']}%\n"
            f"လွဲရမည့်ငွေ = {int(line['total'])} ကျပ်\n\n"
            "ကံကောင်းပါစေ 🍀"
        )

        await message.reply(reply_text)

    await message.reply(f"✅ GRAND TOTAL = {int(data['grand_total'])}")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
