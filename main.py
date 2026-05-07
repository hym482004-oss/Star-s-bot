from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("8390093427:AAFEQ0vlEiH9quvHA1RnXIzinkgS7Wfe2aE")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("2D Bot စပြီး run နေပြီ ✅")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
