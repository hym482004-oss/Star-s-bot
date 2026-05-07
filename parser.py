import re

RULES = {
    "r": ["r", "အာ"],
    "khwe_pu": ["ခွေပူး", "ခပ", "အခွေပူး", "ပူးပါ"],
    "khwe": ["ခွေ", "အခွေ", "ခ"],
    "pat": ["ပတ်", "ပါ", "p", "အပါ", "by", "bi"],
    "pat_pu": ["ပတ်ပူး", "ပူးပို", "ပတ်ပူးပို", "ထပ်", "ထန်", "ထိပ်ပိတ်", "ထိပ်နောက်"],
    "top": ["ထိပ်", "ထ", "top", "t"],
    "brake": ["ဘရိတ်", "bk"],
    "even_brake": ["စုံဘရိတ်", "စဘရိတ်", "စုံbk", "မbk", "မဘရိတ်"],
    "power": ["ပါဝါ", "pw", "ပဝ"],
    "nk": ["နက္ခတ်", "nk", "နက်", "နခ"],
    "bro": ["ညီကို", "ညီအကို", "ညီအစ်ကို"],
    "sam": ["စမ", "စစ", "မမ", "စုံစုံ", "စုံမ", "မစုံ"],
    "kap": ["ကပ်", "ကို", "အကပ်"]
}

def clean_text(text):
    # Market name များကို ရှင်းလင်းခြင်း
    to_remove = r'(me|mega|မီ|မီဂါ|du|dubai|ဒူ|ဒူဘိုင်း|dubi|mm|lao|laos|loadon|laodon|လာအို|လာလာ|ld|london|လန်ဒန်|လန်လန်|glo|global|ဂလို|maxi|max|မက်ဆီ|မက်စီ)'
    return re.sub(to_remove, '', text, flags=re.IGNORECASE)

def parse_message(text):
    if not text: return {"grand_total": 0}
    
    # စာသားကို သန့်စင်ပြီး အပိုင်းလိုက်ခွဲခြင်း
    work_text = clean_text(text.lower())
    # အဓိက ခွဲခြားမည့် သင်္ကေတများ (\n, *, /, =)
    parts = re.split(r'[\n\*/=]', work_text)
    
    grand_total = 0

    for part in parts:
        part = part.strip()
        if not part: continue
        
        # ပိုက်ဆံပမာဏကို ရှာဖွေခြင်း (စာကြောင်းတစ်ကြောင်းချင်းစီ၏ နောက်ဆုံးဂဏန်း)
        nums = re.findall(r'\d+', part)
        if not nums: continue
        
        try:
            price = int(nums[-1]) # နောက်ဆုံးဂဏန်းသည် ပမာဏ
            main_nums = nums[:-1] if len(nums) > 1 else nums
            
            # Rule ရှာဖွေခြင်း
            rule = "direct"
            for r_key, keywords in RULES.items():
                if any(k in part for k in keywords):
                    rule = r_key
                    break
            
            base = 0
            # Logic များ
            if rule == "khwe":
                n = len(str(main_nums[0]))
                base = n * (n - 1)
            elif rule == "khwe_pu":
                n = len(str(main_nums[0]))
                base = (n * (n - 1)) + n
            elif rule == "pat": base = 19 * len(main_nums)
            elif rule == "pat_pu": base = 20 * len(main_nums)
            elif rule == "top": base = 10 * len(main_nums)
            elif rule == "brake": base = len(str(main_nums[0])) * 10
            elif rule == "even_brake": base = 50
            elif rule == "bro": base = 20
            elif rule in ["power", "nk"]: base = 10
            elif rule == "sam": base = 25
            elif rule == "kap":
                if len(main_nums) >= 2:
                    base = len(str(main_nums[0])) * len(str(main_nums[1]))
            else:
                # Direct ကွက်များ (ဥပမာ 12.13.14)
                # စာကြောင်းထဲရှိ ဂဏန်း ၂ လုံးတွဲအားလုံးကို ရေတွက်သည်
                all_twos = re.findall(r'\d{2}', part)
                # ပိုက်ဆံကို မပါအောင် ပြန်ဖယ်သည်
                if str(price) in all_twos: all_twos.remove(str(price))
                base = len(all_twos) if all_twos else len(main_nums)

            line_total = base * price
            
            # အာ (Reverse) စစ်ဆေးခြင်း
            if any(k in part for k in RULES["r"]):
                line_total *= 2
                
            grand_total += line_total
            
        except Exception:
            continue

    return {"grand_total": int(grand_total)}
