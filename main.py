import telebot
import re
import os
from threading import Thread
from flask import Flask

# =========================
# KEEP ALIVE SERVER
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running", 200

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# =========================
# BOT CONFIGURATION
# =========================
BOT_TOKEN = "8663479446:AAEHOXsSBCxpwh7fK3AbtEbbIAouBMFM9R4"
bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

ADMINS = ["@admin1", "@owner"]

# =========================
# NORMALIZE TEXT
# =========================
def normalize(text):
    text = text.lower()
    text = text.replace("=", "\n")
    text = text.replace("-", "\n")
    text = text.replace("/", " ")
    text = text.replace(".", " ")
    text = text.replace("*", " ")
    text = re.sub(r'\s+', ' ', text)
    return text

# =========================
# 🧮 COUNT ENGINE
# =========================
def calculate_count(line):
    nums = re.findall(r'\d+', line)
    if not nums:
        return 0, False

    is_reverse = 'r' in line or 'အာ' in line

    # --- PA PUU / PA ---
    if "ပါပူး" in line:
        return 20, is_reverse
    elif "ပါ" in line or "ပတ်" in line:
        return 19, is_reverse

    # --- MA PUU / SO PUU ---
    elif "မပူး" in line:
        return 5, is_reverse
    elif "စုံပူး" in line:
        return 5, is_reverse

    # --- KHWE / KHWE PUU ---
    elif "ခွေ" in line:
        n = len(nums[0])
        if "ပူး" in line:
            return (n * (n - 1)) + n, is_reverse
        else:
            return n * (n - 1), is_reverse

    # --- SO BK / MA BK ---
    elif "စုံဘရိတ်" in line or "စုံbk" in line:
        return 50, is_reverse
    elif "မဘရိတ်" in line or "မbk" in line:
        return 50, is_reverse

    # --- BK / BREAK ---
    elif "bk" in line or "ဘရိတ်" in line:
        return 10, is_reverse

    # --- TOP / HT ---
    elif "ထိပ်" in line or "top" in line or "t" in line:
        return 10, is_reverse

    # --- PATTERN (စမ စစ မမ...) ---
    elif any(x in line for x in ["စမ", "စစ", "မမ", "စုံစုံ", "စုံမ", "မစ်"]):
        return 25, is_reverse

    # --- KHAP / KAP ---
    elif "ခပ်" in line:
        n = len(nums[0])
        return n * n, is_reverse
    elif "ကပ်" in line or "ကို" in line:
        if len(nums) >= 2:
            return len(nums[0]) * len(nums[1]), is_reverse
        else:
            n = len(nums[0])
            return n * n, is_reverse

    # --- POWER / NK / HPU ---
    elif any(x in line for x in ['pw', 'ပါဝါ', 'နက္ခတ်', 'နက်', 'နခ', 'အပူး', 'ph']):
        return 10, is_reverse

    # --- YI KO / BROTHER ---
    elif "ညီကို" in line or "ညီအကို" in line:
        return 20, is_reverse

    # --- DEFAULT: LIST OF NUMBERS ---
    else:
        return len(nums), is_reverse

# =========================
# START COMMAND
# =========================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ စာရင်းစတွက်ပေးပါမယ်ရှင့်")

# =========================
# MAIN HANDLER
# =========================
@bot.message_handler(func=lambda m: True)
def handle(message):
    user = message.from_user.first_name or "User"

    try:
        text = message.text
        if not text:
            return

        raw_text = text
        lower_text = text.lower()

        # 🛑 REMOVE: Me 10 / Du7 / MM10 etc.
        text = re.sub(r'\bme\s*\d+\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdu\s*\d+\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmm\s*\d+\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\blaos\s*\d+\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\bld\s*\d+\b', '', text, flags=re.IGNORECASE)

        lower_text = text.lower()

        # =========================
        # FILTER
        # =========================
        trigger_words = [
            'ခွေ','ပူး','ထိပ်','bk','ကပ်','ခပ်','စမ','မမ','pw','nk','r','အာ',
            'ပါ','ပတ်','ဘရိတ်','နက္ခတ်','အပူး','စုံပူး','မပူး','ညီကို'
        ]

        has_digits = bool(re.search(r'\d', text))
        has_trigger = any(w in lower_text for w in trigger_words)

        if not has_digits and not has_trigger:
            return

        # =========================
        # PRICE DETECT
        # =========================
        price_match = re.search(r'(\d+)\s*[rR]\s*(\d+)', raw_text)
        price_match2 = re.search(r'(\d+)\s*$', raw_text)

        if price_match:
            price_norm = int(price_match.group(1))
            price_rev = int(price_match.group(2))
        elif price_match2:
            price_norm = int(price_match2.group(1))
            price_rev = price_norm
        else:
            price_norm = 0
            price_rev = 0

        # =========================
        # SPLIT LINES
        # =========================
        lines = [l.strip() for l in normalize(text).split("\n") if l.strip()]

        total_amount = 0

        for line in lines:
            count, is_reverse = calculate_count(line)

            if count == 0:
                continue

            if is_reverse:
                total_amount += (count * price_norm) + (count * price_rev)
            else:
                total_amount += count * price_norm

        # =========================
        # CHECK IF NO TOTAL
        # =========================
        if total_amount == 0 and has_digits:
            bot.reply_to(
                message,
                f"📢 {' '.join(ADMINS)}\n⚠️ {user} ရဲ့ဒါလေးလာစစ်ပေးပါရှင့်"
            )
            return

        # =========================
        # COMPANY & % SYSTEM
        # =========================
        percent = 7
        comp_name = "Company"

        if "mega" in lower_text or "မီ" in lower_text:
            comp_name = "Mega"
            percent = 7
        elif "du" in lower_text:
            comp_name = "Du"
            percent = 7
        elif "mm" in lower_text:
            comp_name = "MM"
            percent = 10
        elif "laos" in lower_text or "ld" in lower_text:
            comp_name = "Laos"
            percent = 7
        else:
            # Name မပါရင် Admin ခေါ်
            bot.reply_to(
                message,
                f"📢 {' '.join(ADMINS)}\n⚠️ {user} ရဲ့ဒါလေးလာစစ်ပေးပါရှင့်"
            )
            return

        discount = total_amount * (percent / 100)
        final = total_amount - discount

        # =========================
        # REPLY FORMAT
        # =========================
        reply = (
            f"👤 {user}\n"
            f"{comp_name} Total = {int(total_amount):,} ကျပ်\n"
            f"{percent}% Cash Back = {int(discount):,} ကျပ်\n"
            f"Total = {int(final):,} ကျပ်ဘဲ လွဲပါရှင့်\n"
            f"ကံကောင်းပါစေ"
        )

        bot.reply_to(message, reply)

    except Exception as e:
        print("ERROR:", e)

# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling()
