import re

# alias system
ALIASES = {
    "du": "DU", "dubai": "DU", "ဒူ": "DU",
    "mega": "MEGA", "me": "MEGA",
    "max": "MAX", "maxi": "MAX",
    "glo": "GLO", "global": "GLO",
    "ld": "LD", "london": "LD",
    "lao": "LAO",
    "mm": "MM",
}

def normalize(text: str):
    text = text.lower()
    for k, v in ALIASES.items():
        text = re.sub(rf"\b{k}\b", v.lower(), text)
    return text


def extract_numbers(line):
    return re.findall(r"\d+", line)


def extract_r(line):
    match = re.search(r"r\s*(\d+)", line)
    return int(match.group(1)) if match else 0


# 🔥 CORE CALCULATION (basic version)
def calculate_block(nums, r):
    count = len(nums)

    # basic rule simulation (simplified engine)
    if count == 1:
        base = 1
    elif count == 2:
        base = 2
    elif count >= 3:
        base = 3
    else:
        base = 0

    total = base * r if r else base * 100

    return {
        "count": count,
        "base": base,
        "r": r,
        "total": total
    }


def clean_lines(text):
    lines = text.split("\n")
    return [l for l in lines if re.search(r"\d", l)]


def parse_line(line):
    nums = extract_numbers(line)
    r_value = extract_r(line)

    calc = calculate_block(nums, r_value)

    return {
        "raw": line,
        "numbers": nums,
        "r": r_value,
        "calc": calc
    }


def parse_message(text: str):
    text = normalize(text)
    lines = clean_lines(text)

    parsed = [parse_line(l) for l in lines]

    return {
        "raw": text,
        "lines": parsed
    }
