import re

# =====================
# 🔥 RULE KEYWORDS
# =====================
RULES = {
    "direct": ["-", "=", " "],

    "r": ["r", "အာ"],

    "pat": ["ပတ်", "ပါ", "အပါ"],

    "pat_pu": ["ပတ်ပူး", "ပူးပို", "ပတ်ပူးပို", "ထပ်", "ထန်", "ထိပ်ပိတ်", "ထိပ်နောက်"],

    "top": ["ထိပ်", "ထ", "top", "t"],

    "brake": ["ဘရိတ်", "bk"],

    "even_brake": ["စုံဘရိတ်", "စဘရိတ်", "စုံbk", "မbk", "မဘရိတ်"],

    "khwe": ["ခွေ", "ခ", "အခွေ"],

    "khwe_pu": ["ခွေပူး", "အခွေပူး"],

    "power": ["ပါဝါ", "pw", "ပဝ"],

    "nk": ["နက္ခတ်", "nk", "နက်", "နခ"],

    "bro": ["ညီကို", "ညီအကို", "ညီအစ်ကို"],

    "pait": ["ပိတ်", "အပိတ်", "ပ"],

    "ma_pu": ["မပူး"],

    "so_pu": ["စုံပူး"],

    "sam": ["စမ", "စစ", "မမ", "စုံစုံ", "စုံမ", "မစုံ"],

    "khap": ["ခပ်"],

    "kap": ["ကပ်", "ကို"]
}

# =====================
# 🔥 NORMALIZE
# =====================
def normalize(text):
    return text.lower()

# =====================
# 🔥 CLEAN TEXT
# =====================
def clean_text(text):
    """Me 10, Du7, MM10 စတာတွေကို ဖျက်ပစ်တာ"""
    text = re.sub(r'\bme\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdu\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bmm\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\blaos\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bld\s*\d+\b', '', text, flags=re.IGNORECASE)
    return text

# =====================
# 🔥 EXTRACT
# =====================
def extract_numbers(text):
    return re.findall(r"\d+", text)


def extract_amount(text):
    # R ပါရင် ပထမဂဏန်းကို ယူ၊ မပါရင် နောက်ဆုံးဂဏန်းကို ယူ
    m = re.search(r"(\d+)\s*r\s*(\d+)|(\d+)$", text)
    if m:
        return int(m.group(1) or m.group(3))
    return 0

def extract_amount_rev(text):
    # R ပါရင် ဒုတိယဂဏန်းကို ယူ
    m = re.search(r"(\d+)\s*r\s*(\d+)", text)
    if m:
        return int(m.group(2))
    return 0


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
def calculate(rule, nums, amount, amount_rev=0, is_reverse=False):

    n = len(nums)
    total = 0

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

    elif rule == "ma_pu":
        base = 5

    elif rule == "so_pu":
        base = 5

    elif rule == "sam":
        base = 25

    elif rule == "khap":
        if nums:
            n_digit = len(nums[0])
            base = n_digit * n_digit
        else:
            base = 0

    elif rule == "kap":
        if len(nums) >= 2:
            base = len(nums[0]) * len(nums[1])
        else:
            base = 0

    else:
        base = len(nums) if nums else 1

    # Calculate Total
    if is_reverse and amount_rev > 0:
        total = (base * amount) + (base * amount_rev)
    else:
        total = base * amount

    return base, total


# =====================
# 🔥 MAIN PARSE
# =====================
def parse_message(text):

    raw_text = text
    text = normalize(text)
    text = clean_text(text)

    # Split by symbols
    text = text.replace("=", "\n")
    text = text.replace("-", "\n")
    lines = text.splitlines()

    results = []
    grand_total = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        nums = extract_numbers(line)
        amount = extract_amount(raw_text)
        amount_rev = extract_amount_rev(raw_text)

        rule = detect_rule(line)
        is_reverse = any(k in line for k in ["r", "အာ"])

        base, total = calculate(rule, nums, amount, amount_rev, is_reverse)

        grand_total += total

        results.append({
            "raw": line,
            "rule": rule,
            "base": base,
            "amount": amount,
            "total": int(total)
        })

    return {
        "lines": results,
        "grand_total": int(grand_total)
    }
