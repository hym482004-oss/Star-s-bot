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

    lines = text.split("\n")

    return {
        "raw": text,
        "lines": lines,
    }
