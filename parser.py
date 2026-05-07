import re

# 🔥 BASIC NORMALIZE
def normalize(text: str):
    return text.lower()


# 🔥 extract numbers
def extract_numbers(text):
    return re.findall(r"\d+", text)


# 🔥 extract amount
def extract_r(text):
    match = re.search(r"r\s*(\d+)|(\d+)%", text)
    if match:
        return int(match.group(1) or match.group(2))
    return 0


# 🔥 detect %
def extract_percent(text):
    match = re.search(r"(\d+)\s*%", text)
    return int(match.group(1)) if match else 0


# 🔥 RULE DETECT (simple version)
def detect_rule(text):
    if "ခွေ" in text:
        return "khwe"
    if "ခွေပူး" in text or "ခပ" in text:
        return "khwe_pu"
    if "ထိပ်" in text:
        return "top"
    if "ဘရိတ်" in text:
        return "brake"
    return "direct"


# 🔥 CALC ENGINE
def calculate(rule, nums, amount):
    n = len(nums)

    if rule == "khwe":
        base = n * (n - 1)

    elif rule == "khwe_pu":
        base = (n * (n - 1)) + n

    elif rule == "top":
        base = 10

    elif rule == "brake":
        base = 10

    else:
        base = 1

    total = base * (amount if amount else 100)

    return base, total


# 🔥 PARSE LINE
def parse_message(text):
    text = normalize(text)
    lines = text.split("\n")

    results = []

    grand_total = 0

    for line in lines:
        nums = extract_numbers(line)
        amount = extract_r(line)
        percent = extract_percent(line)

        rule = detect_rule(line)

        base, total = calculate(rule, nums, amount)

        # % deduction
        if percent:
            minus = total * percent / 100
            total = total - minus

        grand_total += total

        results.append({
            "raw": line,
            "rule": rule,
            "base": base,
            "amount": amount,
            "percent": percent,
            "total": total
        })

    return {
        "lines": results,
        "grand_total": grand_total
    }
