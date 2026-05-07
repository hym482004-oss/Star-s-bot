import re

def normalize_text(text):
    """စာကြောင်းကို သပ်ရပ်အောင် ပြုပြင်တာ၊ သင်္ကေတတွေကို နေရာချတာ"""
    text = text.lower()
    text = text.replace("=", "\n")
    text = text.replace("-", "\n")
    text = text.replace("/", " ")
    text = text.replace(".", " ")
    text = text.replace("*", " ")
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_price(text):
    """ဈေးနှုန်း ထုတ်ယူတာ၊ R ပါရင် ပုံမှန်၊ ပြောင်းပြန် ခွဲတာ"""
    # Pattern: 500r100 or 500 R 100
    match_rev = re.search(r'(\d+)\s*[rR]\s*(\d+)', text)
    # Pattern: 500 (တစ်ခုတည်း)
    match_norm = re.search(r'(\d+)\s*$', text)

    if match_rev:
        return int(match_rev.group(1)), int(match_rev.group(2))
    elif match_norm:
        return int(match_norm.group(1)), int(match_norm.group(1))
    else:
        return 0, 0

def clean_company_tags(text):
    """Me 10, Du7 စတာတွေကို ဖျက်ပစ်တာ"""
    text = re.sub(r'\bme\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdu\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bmm\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\blaos\s*\d+\b', '', text, flags=re.IGNORECASE)
    return text
