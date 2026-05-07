import re

RULES = {
    "direct": ["ဒဲ့", " ", "-", "*", "/", ".", ":"],
    "r": ["r", "အာ"],
    "pat": ["ပတ်", "ပါ", "p", "အပါ", "by", "bi"],
    "pat_pu": ["ပတ်ပူး", "ပူးပို", "ပတ်ပူးပို", "ထပ်", "ထန်", "ထိပ်ပိတ်", "ထိပ်နောက်"],
    "top": ["ထိပ်", "ထ", "top", "t"],
    "brake": ["ဘရိတ်", "bk"],
    "even_brake": ["စုံဘရိတ်", "စဘရိတ်", "စုံbk", "မbk", "မဘရိတ်"],
    "khwe": ["ခွေ", "ခ", "အခွေ"],
    "khwe_pu": ["ခွေပူး", "ပူး", "အပူး", "ခပ"],
    "power": ["ပါဝါ", "pw", "ပဝ"],
    "nk": ["နက္ခတ်", "nk", "နက်", "နခ"],
    "bro": ["ညီကို", "ညီအကို", "ညီအစ်ကို"],
    "pait": ["ပိတ်", "အပိတ်", "ပ"],
    "ma_pu": ["မပူး"],
    "so_pu": ["စုံပူး"],
    "sam": ["စမ", "စစ", "မမ", "စုံစုံ", "စုံမ", "မစုံ"],
    "kap": ["ကပ်", "ကို", "အကပ်"]
}

def clean_text(text):
    # Market names တွေကို ဖယ်ထုတ်ပစ်မယ်
    to_remove = r'(me|mega|မီ|မီဂါ|du|dubai|ဒူ|ဒူဘိုင်း|mm|lao|laos|loadon|laodon|လာအို|လာလာ|ld|london|လန်ဒန်|လန်လန်|glo|global|ဂလို|maxi|max|မက်ဆီ|မက်စီ)'
    return re.sub(to_remove, '', text, flags=re.IGNORECASE)

def parse_message(text):
    raw_text = text.lower()
    work_text = clean_text(raw_text)
    
    # စာကြောင်းတွေကို အရင် ခွဲထုတ်မယ်
    lines = re.split(r'[\n\*\-/]', work_text)
    grand_total = 0

    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Line တစ်ကြောင်းချင်းစီက ပိုက်ဆံကို ရှာမယ်
        nums = re.findall(r'\d+', line)
        if not nums: continue
        
        price = int(nums[-1]) # နောက်ဆုံးဂဏန်းကို ပိုက်ဆံလို့ သတ်မှတ်မယ်
        main_nums = nums[:-1] if len(nums) > 1 else nums
        
        # Rule ကို စစ်မယ်
        rule = "direct"
        for r, keys in RULES.items():
            if any(k in line for k in keys):
                rule = r
                break
        
        base = 0
        if rule == "khwe": base = len(main_nums[0]) * (len(main_nums[0]) - 1) if main_nums else 0
        elif rule == "khwe_pu": base = (len(main_nums[0]) * (len(main_nums[0]) - 1)) + len(main_nums[0]) if main_nums else 0
        elif rule == "pat": base = 19
        elif rule == "pat_pu": base = 20
        elif rule == "top": base = 10
        elif rule == "brake": base = len(str(main_nums[0])) * 10 if main_nums else 10
        elif rule == "even_brake": base = 50
        elif rule == "bro": base = 20
        elif rule in ["power", "nk", "pait", "top"]: base = 10
        elif rule in ["ma_pu", "so_pu"]: base = 5
        elif rule == "sam": base = 25
        elif rule == "kap":
            if len(main_nums) >= 2: base = len(str(main_nums[0])) * len(str(main_nums[1]))
        else: base = len(main_nums)

        line_total = base * price
        if 'r' in line or 'အာ' in line:
            line_total *= 2
            
        grand_total += line_total

    return {"grand_total": int(grand_total)}
