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


def clean_lines(text):
    # only keep lines that contain digits
    lines = text.split("\n")
    return [l for l in lines if re.search(r"\d", l)]


def parse_line(line):
    nums = extract_numbers(line)
    r_value = extract_r(line)

    return {
        "raw": line,
        "numbers": nums,
        "r": r_value,
        "count": len(nums)
    }


def parse_message(text: str):
    text = normalize(text)
    lines = clean_lines(text)

    parsed = [parse_line(l) for l in lines]

    return {
        "raw": text,
        "lines": parsed
    }
