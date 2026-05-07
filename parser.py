import re

# alias system
ALIASES = {
    "du": "DU",
    "dubai": "DU",
    "mega": "MEGA",
    "me": "MEGA",
    "max": "MAX",
    "maxi": "MAX",
    "glo": "GLO",
    "global": "GLO",
    "ld": "LD",
    "london": "LD",
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
    return int(match.group(1)) if match else None


def parse_line(line):
    nums = extract_numbers(line)
    r_value = extract_r(line)

    return {
        "numbers": nums,
        "r": r_value
    }


def parse_message(text: str):
    text = normalize(text)
    lines = text.split("\n")

    parsed_lines = []

    for line in lines:
        parsed_lines.append(parse_line(line))

    return {
        "raw": text,
        "lines": parsed_lines
    }
