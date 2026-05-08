import re

# =====================
# 🔥 RULE KEYWORDS
# =====================
RULES = {
    # ⚠️ direct ထဲက " " (space) ဖယ်လိုက်ပါ (အမြဲ direct ဖြစ်သွားတတ်လို့)
    "direct": ["ဒဲ့", "-", "*", "/", ".", ":"],
    "r": ["r", "အာ"],
    "pat_pu": ["ပတ်ပူး", "ပူးပို", "ပတ်ပူးပို", "ထပ်", "ထန်", "ထိပ်ပိတ်", "ထိပ်နောက်"],
    "pat": ["ပတ်", "ပါ", "p", "အပါ", "by", "bi"],
    "top": ["ထိပ်", "ထ", "top", "t"],
    "even_brake": ["စုံဘရိတ်", "စဘရိတ်", "စုံbk", "မbk", "မဘရိတ်"],
    "brake": ["ဘရိတ်", "bk"],
    "khwe_pu": ["ခွေပူး", "ပူး", "အပူး"],
    "khwe": ["ခွေ", "ခ", "အခွေ"],
    "power": ["ပါဝါ", "pw", "ပဝ"],
    "nk": ["နက္ခတ်", "nk", "နက်", "နခ"],
    "bro": ["ညီကို", "ညီအကို", "ညီအစ်ကို"],
    "ma_pu": ["မပူး", "မပိတ်"],
    "pait": ["ပိတ်", "အပိတ်", "ပိတိ", "ပ"],
    "so_pu": ["စုံပူး"],
    "sam": ["စမ", "စစ", "မမ", "စုံစုံ", "စုံမ", "မစုံ"],
    "khap": ["ခပ်"],
    "kap": ["ကပ်", "ကို", "အကပ်"]
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
    text = re.sub(r'\b(me|mega|မီ|မီဂါ)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(du|dubai|ဒူ|ဒူဘိုင်း)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(mm)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(lao|laos|loadon|laodon|လာအို|လာလာ)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(ld|london|လန်ဒန်|လန်လန်)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(glo|global|ဂလို)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(maxi|max|မက်ဆီ|မက်စီ)\s*\d+\b', '', text, flags=re.IGNORECASE)
    return text

# =====================
# ✅ Extract "nums" and "amount" per line
# =====================
def split_nums_and_price(line):
    """
    line ထဲက:
    - amount (ထိုးကြေး) ကို ခွဲထုတ်မယ်
    - amount ကို nums ထဲကနေ ဖယ်ပြီး nums ကိုသာ ပြန်မယ်

    Rules:
    1) 'r100' / 'အာ100' ရှိရင် 100 ကို amount သတ်မှတ်
    2) မရှိရင် last number ကို amount သတ်မှတ်
    """
    raw = line

    # case: r100 / r 100 / အာ100 / အာ 100
    m = re.search(r'(?i)(r|အာ)\s*(\d+)', raw)
    if m:
        price = int(m.group(2))
        # r100 ကို line ထဲကနေ ဖယ် (amount ကို nums ထဲမဝင်စေဖို့)
        without_price = re.sub(r'(?i)(r|အာ)\s*\d+', ' ', raw)
        nums = re.findall(r'\d+', without_price)
        return nums, price, raw

    # else: last number = price
    all_nums = re.findall(r'\d+', raw)
    if not all_nums:
        return [], 0, raw

    price = int(all_nums[-1])

    # last number တစ်ခုပဲ ဖယ်
    without_price = re.sub(r'(\d+)(?!.*\d)', ' ', raw)
    nums = re.findall(r'\d+', without_price)
    return nums, price, raw

# =====================
# ✅ RULE DETECT (priority fix)
# =====================
RULE_ORDER = [
    "pat_pu", "pat",
    "even_brake", "brake",
    "khwe_pu", "khwe",
    "top",
    "power", "nk", "bro",
    "ma_pu", "pait", "so_pu", "sam",
    "khap", "kap",
    "direct"
]

def detect_rule(text):
    t = text.lower()
    for rule in RULE_ORDER:
        for k in RULES.get(rule, []):
            if k and (k.lower() in t):
                return rule
    return "direct"

# =====================
# 🔥 CALC ENGINE
# =====================
def calculate(rule, nums, price_norm, line):

    n = len(nums)
    base = 0

    if rule == "khwe":
        base = n * (n - 1)

    elif rule == "khwe_pu":
        if nums:
            all_digits = ''.join(nums)  # nums are strings of digits
            count = len(all_digits)
            base = count * count
        else:
            base = 0

    elif rule == "pat":
        base = 19

    elif rule == "pat_pu":
        base = 20

    elif rule == "top":
        base = (len(nums) * 10) if nums else 10

    elif rule == "brake":
        base = (len(nums) * 10) if nums else 10

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
        base = 50

    elif rule == "so_pu":
        base = 25

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

    else:  # direct
        base = len(nums) if nums else 0

    # Ignore single digit like 4 in 4:30
    if len(nums) == 1 and len(nums[0]) == 1 and (":" in line or "." in line):
        base = 0

    # Reverse (r / အာ) => double
    is_reverse = bool(re.search(r'(?i)(r|အာ)\s*\d+', line))
    total = base * price_norm
    if is_reverse:
        total += base * price_norm

    return base, total

# =====================
# 🔥 MAIN PARSE
# =====================
def parse_message(text):

    work_text = clean_text(normalize(text))

    # Split by symbols (space, -, *, /, ., :, =)
    work_text = work_text.replace("=", "\n")
    work_text = work_text.replace("-", "\n")
    work_text = work_text.replace("*", "\n")
    work_text = work_text.replace("/", "\n")
    work_text = work_text.replace(".", "\n")
    work_text = work_text.replace(":", "\n")
    lines = work_text.splitlines()

    results = []
    grand_total = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        nums, price_norm, raw_line = split_nums_and_price(line)
        rule = detect_rule(raw_line)

        base, total = calculate(rule, nums, price_norm, raw_line)

        grand_total += total

        results.append({
            "raw": raw_line,
            "rule": rule,
            "base": base,
            "amount": price_norm,
            "total": int(total)
        })

    return {
        "lines": results,
        "grand_total": int(grand_total)
    }
