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

def parse_message(text):
    if not text: return {"grand_total": 0}
    lines = text.lower().replace('=', '\\n').replace('*', '\\n').replace('/', '\\n').split('\\n')
    grand_total = 0

    for line in lines:
        line = line.strip()
        if not line: continue
        
        nums = re.findall(r'\\d+', line)
        if not nums: continue
        
        try:
            # စျေးနှုန်းကို ရှာဖွေခြင်း
            price = int(nums[-1])
            main_nums = nums[:-1]
            
            # Rule ရှာဖွေခြင်း
            rule = "direct"
            for r_key, keywords in RULES.items():
                if any(k in line for k in keywords):
                    rule = r_key
                    break
            
            base = 0
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
            elif rule == "bro": base = 20
            elif rule in ["power", "nk"]: base = 10
            elif rule == "sam": base = 50
            elif rule == "kap":
                if len(main_nums) >= 2:
                    # ကပ်ဂဏန်းများအတွက် (ဥပမာ- 7350/249)
                    base = len(str(main_nums[0])) * len(str(main_nums[1]))
            else:
                # ဒဲ့အကွက်များ (ဥပမာ- 12 13 14)
                all_twos = re.findall(r'\\d{2}', line)
                if str(price) in all_twos: all_twos.remove(str(price))
                base = len(all_twos) if all_twos else len(main_nums)

            # ဒဲ့တွက်ချက်မှု
            line_total = base * price
            
            # အာ (Reverse) စစ်ဆေးခြင်း
            if any(k in line for k in RULES["r"]):
                # r နောက်မှာ စျေးနှုန်းထပ်ပါရင် (ဥပမာ- 100r50)
                r_match = re.search(r'r\\s*(\\d+)', line)
                if r_match and int(r_match.group(1)) != price:
                    line_total = (base * price) + (base * int(r_match.group(1)))
                else:
                    line_total *= 2
                
            grand_total += line_total
        except Exception:
            continue

    return {"grand_total": int(grand_total)}
