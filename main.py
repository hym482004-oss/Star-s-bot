import asyncio
import os
import re
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from parser import parse_message

# Token စစ်ဆေးခြင်း
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Logging setting (Error တွေကို Railway log မှာ ကြည့်လို့ရအောင်)
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
    # စာသားမပါရင် ကျော်မယ်
    if not message.text:
        return

    text = message.text.lower()
    
    # ဂဏန်း လုံးဝမပါရင် ဘာမှမလုပ်ဘူး
    if not re.search(r"\d", text):
        return

    # 🔍 Market ကို အရင်ရှာမယ်
    market_found = None
    percent = 7
    for key, names in MARKETS.items():
        if any(name in text for name in names):
            market_found = key
            percent = PERCENT.get(key, 7)
            break

    # Market မပါရင် Admin ကို Mention ခေါ်မယ်
    if not market_found:
        try:
            admins = await message.chat.get_administrators()
            mentions = [f"@{a.user.username}" for a in admins if a.user.username and not a.user.is_bot]
            mention_str = " ".join(mentions) if mentions else "Admin"
            await message.reply(f"📢 {mention_str}\n⚠️ ဒါလေးလာစစ်ပေးပါရှင့် (Market မပါလို့ပါ)")
        except Exception:
            # Group မဟုတ်ရင် admin mention ခေါ်လို့မရတဲ့အတွက် ဒီအတိုင်းပဲ အသိပေးမယ်
            await message.reply("⚠️ Market name (ဥပမာ- Du, Me) ထည့်ပေးပါရှင့်။")
        return

    # 🧮 Parser နဲ့ တွက်ချက်မယ်
    try:
        data = parse_message(message.text)
        total_amount = data["grand_total"]
        
        if total_amount == 0:
            return

        discount = int(total_amount * (percent / 100))
        final = total_amount - discount
        user_name = message.from_user.first_name or "User"

        reply = (
            f"👤 {user_name}\n"
            f"{market_found} Total = {total_amount:,} ကျပ်\n"
            f"{percent}% Cash Back = {discount:,} ကျပ်\n"
            f"Total = {final:,} ကျပ်ဘဲ လွဲပါရှင့်\n\n"
            f"ကံကောင်းပါစေ"
        )
        await message.reply(reply)
    except Exception as e:
        logging.error(f"Error calculating: {e}")
        # Error တက်ရင် ဘာမှပြန်မပြောဘဲ ငြိမ်နေစေချင်ရင် return ပဲလုပ်ပါ
        # await message.reply("⚠️ တွက်ချက်မှုမှာ အမှားအယွင်းရှိနေပါတယ်ရှင့်။")

async def main():
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
