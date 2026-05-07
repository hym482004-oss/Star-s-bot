import asyncio
import os
import re
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from parser import parse_message

# Railway မှာ Variables (BOT_TOKEN) မဖြစ်မနေ ထည့်ပေးပါ
TOKEN = os.getenv("BOT_TOKEN")
# သင်ခွင့်ပြုမည့် Group ID (Optional - မထည့်လည်း အလုပ်လုပ်သည်)
ALLOWED_GROUP_IDS = [-1003856540486] 

bot = Bot(token=TOKEN)
dp = Dispatcher()

MARKETS = {
    "DU": ["du", "dubai", "ဒူ", "ဒူဘိုင်း"],
    "ME": ["me", "mega", "မီ", "မီဂါ"],
    "MAX": ["maxi", "max", "မက်ဆီ", "မက်စီ"],
    "GLO": ["glo", "global", "ဂလို"],
    "LD": ["ld", "london", "လန်ဒန်", "လန်လန်"],
    "LAO": ["lao", "laos", "loadon", "laodon", "လာအို", "လာလာ"],
    "MM": ["mm"]
}

PERCENT = {"DU": 7, "ME": 7, "MAX": 7, "GLO": 3, "LD": 7, "LAO": 7, "MM": 10}

@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Bot အဆင်သင့်ဖြစ်ပါပြီရှင့် ✅")

@dp.message()
async def handle(message: Message):
    # Security Check: သင်သတ်မှတ်ထားတဲ့ Group ID မဟုတ်ရင် အလုပ်မလုပ်အောင် (လိုအပ်လျှင် သုံးရန်)
    # if message.chat.id not in ALLOWED_GROUP_IDS: return

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
        admins = await message.chat.get_administrators()
        mentions = [f"@{a.user.username}" for a in admins if a.user.username]
        mention_str = " ".join(mentions) if mentions else "@owner @admin"
        await message.reply(f"📢 {mention_str}\n⚠️ ဒါလေးလာစစ်ပေးပါရှင့် (Market မပါလို့ပါ)")
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
