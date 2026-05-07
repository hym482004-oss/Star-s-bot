import os
import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from parser import get_combinations

# Railway Variables ထဲမှာ BOT_TOKEN ထည့်ရပါမယ်
TOKEN = os.getenv("BOT_TOKEN")
# သင်ပေးထားတဲ့ ID နှစ်ခုလုံးကို ထည့်ထားပေးပါတယ်
ALLOWED_GROUP_IDS = [-1003856540486, 6023513934] 

logging.basicConfig(level=logging.INFO)

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in ALLOWED_GROUP_IDS:
        return

    msg_text = update.message.text
    user = update.message.from_user
    
    total_raw, discount_rate, market_name = get_combinations(msg_text)
    
    if total_raw == 0:
        # ဂဏန်းတွဲပါပြီး amount မပါရင် သတိပေးချက် (ဥပမာ ၃၅ ၄၅ ၆)
        # အနည်းဆုံး ဂဏန်း ၂ လုံးအတွဲ ၂ ခုထက်ပိုပါပြီး ပိုက်ဆံမပါရင် error ပြမယ်
        if len(re.findall(r'\d{2}', msg_text)) >= 2 and not re.search(r'\d{3,}', msg_text):
            await update.message.reply_text("⚠️ တွက်နည်းထဲမှာ ပိုက်ဆံပမာဏ (amount) မပါတာ ရှိနေပါတယ်၊ ပြန်စစ်ပေးပါရှင့်။")
        return

    # Market Name မပါရင် Admin Mention ခေါ်ခြင်း
    if not market_name:
        admins = await update.effective_chat.get_administrators()
        mentions = " ".join([f"@{a.user.username}" for a in admins if not a.user.is_bot and a.user.username])
        await update.message.reply_text(f"{mentions} ဒါလေးလာစစ်ပေးပါရှင့် (Market Name မပါလို့ပါ)")
        return

    # တွက်ချက်မှု ရလဒ်
    cashback = total_raw * discount_rate
    final_total = total_raw - cashback

    # Bot Reply ပုံစံ (သင်ပေးထားသည့်အတိုင်း)
    response = (
        f"👤 {user.first_name}{market_name}\n"
        f"Total = {total_raw:,.0f} ကျပ်\n"
        f"{discount_rate*100:.0f}% Cash Back = {cashback:,.0f} ကျပ်\n"
        f"Total = {final_total:,.0f} ကျပ် ဘဲ လွဲပါရှင့်\n\n"
        f"ကံကောင်းပါစေ"
    )

    await update.message.reply_text(response)

if __name__ == '__main__':
    if not TOKEN:
        print("Error: BOT_TOKEN not found in environment variables.")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
        app.run_polling()
