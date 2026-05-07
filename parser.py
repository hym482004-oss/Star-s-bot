import re

# =====================
# 🔥 RULE KEYWORDS
# =====================
RULES = {
    "direct": ["ဒဲ့", " ", "-", "*", "/", "."],

    "r": ["r", "အာ"],

    "pat": ["ပတ်", "ပါ", "အပါ"],

    "pat_pu": ["ပတ်ပူး", "ပူးပို", "ပတ်ပူးပို", "ထပ်", "ထန်", "ထိပ်ပိတ်", "ထိပ်နောက်"],

    "top": ["ထိပ်", "ထ", "top", "t"],

    "brake": ["ဘရိတ်", "bk"],

    "even_brake": ["စုံဘရိတ်", "စဘရိတ်", "စုံbk", "မbk", "မဘရိတ်"],

    "khwe": ["ခွေ", "ခ", "အခွေ"],

    "khwe_pu": ["ခွေပူး", "ပူး", "အပူး"],

    "power": ["ပါဝါ", "pw", "ပဝ"],

    "nk": ["နက္ခတ်", "nk", "နက်", "နခ"],

    "bro": ["ညီကို", "ညီအကို", "ညီအစ်ကို"],

    "pait": ["ပိတ်", "အပိတ်", "ပ"],

    "ma_pu": ["မပူး"],

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

def extract_price_full(text):
    """
    Return (price_norm, price_rev)
    """
    # Pattern: 500r100 or 500 R 100
    match_rev = re.search(r'(\d+)\s*[rR]\s*(\d+)', text)
    # Pattern: ...r500 or ... 500
    match_simple = re.search(r'(\d+)\s*$', text)
    
    if match_rev:
        return int(match_rev.group(1)), int(match_rev.group(2))
    elif match_simple:
        return int(match_simple.group(1)), int(match_simple.group(1))
    else:
        return 0, 0

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
def calculate(rule, nums, price_norm, price_rev, line):

    n = len(nums)
    base = 0

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
        # 3bk, 8bk ဆိုရင် ရှေ့ကဂဏန်းကို ယူ၊ မရှိရင် 10
        if nums:
            base = int(nums[0])
        else:
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

    else: # direct
        base = len(nums) if nums else 0

    # --- Reverse Check ---
    is_reverse = bool(re.search(r'r|အာ', line))
    
    total = base * price_norm
    if is_reverse and price_rev != price_norm:
        total += base * price_rev

    return base, total


# =====================
# 🔥 MAIN PARSE
# =====================
def parse_message(text):

    raw_text = text
    work_text = clean_text(normalize(text))

    # Split by symbols
    work_text = work_text.replace("=", "\n")
    work_text = work_text.replace("-", "\n")
    work_text = work_text.replace("*", "\n")
    work_text = work_text.replace("/", "\n")
    work_text = work_text.replace(".", "\n")
    lines = work_text.splitlines()

    results = []
    grand_total = 0

    # Get Price ONCE from full text
    price_norm, price_rev = extract_price_full(raw_text)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        nums = extract_numbers(line)
        rule = detect_rule(line)

        base, total = calculate(rule, nums, price_norm, price_rev, line)

        grand_total += total

        results.append({
            "raw": line,
            "rule": rule,
            "base": base,
            "amount": price_norm,
            "total": int(total)
        })

    return {
        "lines": results,
        "grand_total": int(grand_total)
    }
