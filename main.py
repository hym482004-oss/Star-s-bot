from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio
import os
from dotenv import load_dotenv

from parser import parse_message

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("2D Bot စပြီး run နေပြီ ✅")


@dp.message()
async def handle(message: Message):
    data = parse_message(message.text)

    await message.reply(
        f"📦 RAW:\n{data['raw']}\n\n"
        f"📄 LINES:\n{data['lines']}"
    )


async def main():
    await dp.start_polling(bot)

asyncio.run(main())
