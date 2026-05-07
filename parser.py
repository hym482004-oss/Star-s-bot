# 2D logic will go here later
# 2D BOT LOGIC ENGINE

def parse_message(text):
    return text
import re

# alias system
ALIASES = {
    "du": "DU",
    "dubai": "DU",
    "ဒူ": "DU",
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


def parse_message(text: str):
    text = normalize(text)

    # split lines
    lines = text.split("\n")

    result = {
        "raw": text,
        "lines": lines,
    }

    return result
