# 🔥 RULE KEYWORDS
RULES = {
    "pat": ["ပတ်", "အပါ", "ပါ"],
    "pat_pu": ["ပတ်ပူး", "ပူးပို", "ပတ်ပူးပို", "ထန", "ထပ", "ထိပ်ပိတ်", "ထိပ်နောက်"],
    "khwe": ["ခွေ", "အခွေ", "ခ"],
    "khwe_pu": ["ခွေပူး", "ခပ", "အခွေပူး"],
    "top": ["ထိပ်", "ထိပ်စီး", "အထိပ်", "ထ", "top", "t"],
    "brake": ["ဘရိတ်", "bk"],
    "even_brake": ["စုံဘရိတ်", "စုံbk", "စဘရိတ်"],
    "odd_brake": ["မဘရိတ်", "မbk"],
    "power": ["ပါဝါ", "ပဝ", "pw", "power"],
    "nk": ["နက္ခတ်", "နက", "နခ", "nk"],
    "bro": ["ညီကို", "ညီအကို", "ညီအစ်ကို"],
    "pait": ["ပိတ်", "အပိတ်"],
}


# 🔥 BLOCK COUNTS
BLOCKS = {
    "direct": 1,
    "r": 2,
    "pat": 19,
    "pat_pu": 20,
    "top": 10,
    "brake": 10,
    "even_brake": 50,
    "odd_brake": 50,
    "power": 10,
    "nk": 10,
    "bro": 20,
    "pait": 10,
}


def detect_rule(line):
    for rule, keywords in RULES.items():
        for kw in keywords:
            if kw in line:
                return rule

    return "direct"


def calculate_block(rule, nums, r):
    # KHWE
    if rule == "khwe":
        n = len(nums)
        base = n * (n - 1)

    # KHWE PU
    elif rule == "khwe_pu":
        n = len(nums)
        base = (n * (n - 1)) + n

    # CAP
    elif "ကပ်" in nums or "ကို" in nums:
        parts = re.split(r"ကပ်|ကို", nums)
        left = len(re.findall(r"\d", parts[0]))
        right = len(re.findall(r"\d", parts[-1]))
        base = left * right

    else:
        base = BLOCKS.get(rule, 1)

    # R double
    if r:
        total = base * r
    else:
        total = base * 100

    return {
        "rule": rule,
        "base": base,
        "r": r,
        "total": total
    }


def clean_lines(text):
    lines = text.split("\n")
    return [l.strip() for l in lines if l.strip()]


def parse_line(line):
    nums = extract_numbers(line)

    # amount
    amount_match = re.findall(r"r\s*(\d+)|(\d+)$", line)
    r_value = 0

    if amount_match:
        last = amount_match[-1]
        r_value = int(last[0] or last[1])

    # R detect
    has_r = bool(re.search(r"r|အာ", line))

    # rule detect
    rule = detect_rule(line)

    # calc
    calc = calculate_block(rule, nums, r_value)

    # reverse direct
    if has_r and rule == "direct":
        calc["base"] = 2
        calc["total"] = r_value * 2

    return {
        "raw": line,
        "numbers": nums,
        "rule": rule,
        "r": r_value,
        "calc": calc
    }


def parse_message(text: str):
    text = normalize(text)
    lines = clean_lines(text)

    parsed = [parse_line(l) for l in lines]

    grand_total = sum(x["calc"]["total"] for x in parsed)

    return {
        "raw": text,
        "lines": parsed,
        "grand_total": grand_total
    }
