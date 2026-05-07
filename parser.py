import re

# =====================
# 🔥 RULE KEYWORDS
# =====================
RULES = {
    "direct": ["-", "=", " "],

    "r": ["r", "အာ"],

    "pat": ["ပတ်", "ပါ", "အပါ"],

    "pat_pu": ["ပတ်ပူး", "ခပ", "အခွေပူး", "ထပ", "ထန", "ထိပ်ပိတ်", "ထိပ်နောက်"],

    "top": ["ထိပ်", "ထ", "top", "t"],

    "brake": ["ဘရိတ်", "bk"],

    "even_brake": ["စုံဘရိတ်", "စဘရိတ်"],

    "khwe": ["ခွေ", "ခ", "အခွေ"],

    "khwe_pu": ["ခွေပူး"],

    "power": ["ပါဝါ", "pw", "ပဝ"],

    "nk": ["နက္ခတ်", "nk"],

    "bro": ["ညီကို", "ညီအကို", "ညီအစ်ကို"],

    "pait": ["ပိတ်", "အပိတ်", "ပ"]
}

# =====================
# 🔥 NORMALIZE
# =====================
def normalize(text):
    return text.lower()

# =====================
# 🔥 EXTRACT
# =====================
def extract_numbers(text):
    return re.findall(r"\d+", text)


def extract_amount(text):
    m = re.search(r"r\s*(\d+)|(\d+)$", text)
    if m:
        return int(m.group(1) or m.group(2))
    return 0


def extract_percent(text):
    m = re.search(r"(\d+)%", text)
    return int(m.group(1)) if m else 0


# =====================
# 🔥 RULE DETECT
# =====================
def detect_rule(text):
    for rule, keys in RULES.items():
        for k in keys:
            if k in text:
                return rule
    return "direct"


# =====================
# 🔥 CALC ENGINE
# =====================
def calculate(rule, nums, amount):

    n = len(nums)

    if rule == "khwe":
        base = n * (n - 1)

    elif rule == "khwe_pu":
        base = (n * (n - 1)) + n

    elif rule == "pat":
        base = 19

    elif rule == "pat_pu":
        base = 20

    elif rule == "top":
        base = 10

    elif rule == "brake":
        base = 10

    elif rule == "even_brake":
        base = 50

    elif rule == "power":
        base = 10

    elif rule == "nk":
        base = 10

    elif rule == "bro":
        base = 20

    elif rule == "pait":
        base = 10

    else:
        base = 1

    if amount:
        total = base * amount
    else:
        total = base * 100

    return base, total


# =====================
# 🔥 MAIN PARSE
# =====================
def parse_message(text):

    text = normalize(text)
    lines = text.split()

    results = []
    grand_total = 0

    for line in lines:

        nums = extract_numbers(line)
        amount = extract_amount(line)
        percent = extract_percent(line)

        rule = detect_rule(line)

        base, total = calculate(rule, nums, amount)

        # % deduction
        if percent:
            total = total - (total * percent / 100)

        grand_total += total

        results.append({
            "raw": line,
            "rule": rule,
            "base": base,
            "amount": amount,
            "percent": percent,
            "total": int(total)
        })

    return {
        "lines": results,
        "grand_total": int(grand_total)
    }
