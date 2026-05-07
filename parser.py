import re

# =====================
# 🔥 RULE KEYWORDS (သင့်ရဲ့ original + ပြည့်စုံ)
# =====================
RULES = {
    "direct": ["ဒဲ့", " ", "-", "*", "/", ".", ":"],
    "r": ["r", "R", "အာ"],
    "pat": ["ပတ်", "ပါ", "p", "အပါ", "by", "bi", "ပတ်သီး"],
    "pat_pu": ["ပတ်ပူး", "ပူးပို", "ပတ်ပူးပို", "ထပ်", "ထန်", "ထိပ်ပိတ်", "ထိပ်နောက်", "ပတ်အကွက်20"],
    "top": ["ထိပ်", "ထ", "top", "t", "Top", "T"],
    "brake": ["ဘရိတ်", "bk", "Bk"],
    "even_brake": ["စုံဘရိတ်", "စဘရိတ်", "စုံbk", "မbk", "မဘရိတ်", "မBk"],
    "khwe": ["ခွေ", "ခ", "အခွေ", "ခွေဂဏန်း"],
    "khwe_pu": ["ခွေပူး", "ပူး", "အပူး", "အပူးပါ"],
    "dek": ["ဆယ်ပြည့်"],
    "so_pu": ["စုံပူး", "အပူးစုံ"],
    "sam": ["စမ", "စစ", "မမ", "မစ", "စုံစုံ", "စုံမ", "မစုံ"],
    "khap": ["ခပ်"],
    "kap": ["ကပ်", "ကို", "အကပ်"],
    "power": ["ပါဝါ", "pw", "ပဝ"],
    "nk": ["နက္ခတ်", "nk", "နက်", "နခ"],
    "bro": ["ညီကို", "ညီအကို", "ညီအစ်ကို"],
    "pait": ["ပိတ်", "အပိတ်", "ပ"]
}

# =====================
# 🔥 NORMALIZE & CLEAN (Fixed)
# =====================
def normalize(text):
    return text.lower().strip()

def clean_text(text):
    # Remove 2D names + numbers
    patterns = [
        r'\b(?:me|mega|မီ|မီဂါ)\s*\d*\b',
        r'\b(?:du|dubai|ဒူ|ဒူဘိုင်း)\s*\d*\b',
        r'\b(?:mm|MM)\s*\d*\b',
        r'\b(?:lao|laos|loadon|laodon|လာအို|လာလာ)\s*\d*\b',
        r'\b(?:ld|london|လန်ဒန်|လန်လန်)\s*\d*\b',
        r'\b(?:glo|global|ဂလို)\s*\d*\b',
        r'\b(?:maxi|max|မက်ဆီ|မက်စီ)\s*\d*\b'
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return text.strip()

# =====================
# 🔥 EXTRACT (Fixed)
# =====================
def extract_numbers(text):
    """Clean number extraction (1-99 only)"""
    numbers = re.findall(r'\b\d{1,2}\b', text)
    return [int(num) for num in numbers if 0 <= int(num) <= 99]

def extract_price_full(text):
    """Fixed price extraction"""
    # R price first
    match_rev = re.search(r'[rRအာ]\s*(\d+)', text, re.IGNORECASE)
    if match_rev:
        return int(match_rev.group(1)), int(match_rev.group(1))
    
    # Last number as price
    numbers = re.findall(r'\b\d+\b', text)
    if numbers:
        return int(numbers[-1]), int(numbers[-1])
    
    return 0, 0

# =====================
# 🔥 RULE DETECT (Fixed)
# =====================
def detect_rule(text):
    text_lower = normalize(text)
    for rule, keys in RULES.items():
        for k in keys:
            if k.lower() in text_lower:
                return rule
    return "direct"

# =====================
# 🔥 CALC ENGINE (Fixed & Complete)
# =====================
def calculate(rule, nums, price_norm, price_rev, line):
    if not nums or price_norm == 0:
        return 0, 0
    
    n = len(nums)
    base = 0

    # All rules with correct calculations
    rule_map = {
        "khwe": lambda: n * (n - 1),
        "khwe_pu": lambda: (n * (n - 1)) + n,
        "pat": lambda: 19,
        "pat_pu": lambda: 20,
        "top": lambda: 10,
        "brake": lambda: len(''.join(map(str, nums))) if nums else 10,
        "even_brake": lambda: 50,
        "dek": lambda: 10,
        "so_pu": lambda: 10,
        "sam": lambda: 25,
        "power": lambda: 10,
        "nk": lambda: 10,
        "bro": lambda: 20,
        "pait": lambda: 10,
        "ma_pu": lambda: 5,
        "khap": lambda: len(str(nums[0]))**2 if nums else 0,
        "kap": lambda: len(str(nums[0])) * len(str(nums[1])) if len(nums) >= 2 else 0,
        "direct": lambda: n
    }
    
    base = rule_map.get(rule, lambda: n)()
    
    # Ignore time patterns (4:30, 12.45)
    if len(nums) == 1 and len(str(nums[0])) == 1 and re.search(r'[:.]', line):
        base = 0

    # Reverse calculation
    is_reverse = bool(re.search(r'[rRအာ]', line, re.IGNORECASE))
    total = base * price_norm
    if is_reverse:
        total *= 2  # Fixed: multiply by 2 instead of add

    return base, total

# =====================
# 🔥 MAIN PARSE (Fixed)
# =====================
def parse_message(text):
    raw_text = text
    work_text = clean_text(normalize(text))

    # Better splitting
    work_text = re.sub(r'[=\-*/:.ဒဲ့]+', '\n', work_text)
    lines = [line.strip() for line in work_text.split('\n') if line.strip()]

    results = []
    grand_total = 0
    price_norm, price_rev = extract_price_full(raw_text)

    for line in lines:
        nums = extract_numbers(line)
        rule = detect_rule(line)
        base, total = calculate(rule, nums, price_norm, price_rev, line)
        
        if total > 0:
            grand_total += total
            results.append({
