import re

def get_combinations(text):
    text = text.lower().replace(' ', '').replace('*', '-').replace('/', '-')
    
    discount = 0
    market_found = ""
    
    markets = {
        'DUBAI': (['dubai', 'ဒူ', 'du', 'ဒူဘိုင်း'], 0.07),
        'MEGA': (['mega', 'me', 'မီ', 'မီဂါ'], 0.07),
        'MAXI': (['maxi', 'max', 'မက်ဆီ', 'မက်စီ', 'စီစီ'], 0.07),
        'LAO': (['lao', 'loa', 'လာအို', 'လာလာ', 'loadon'], 0.07),
        'LONDON': (['london', 'ld', 'လန်လန်', 'လန်ဒန်'], 0.07),
        'MM': (['mm', 'မြန်မာ'], 0.10),
        'GLOBAL': (['global', 'glo', 'ဂလို'], 0.03)
    }

    for key, (aliases, rate) in markets.items():
        if any(alias in text for alias in aliases):
            discount = rate
            market_found = key
            break

    total_amt = 0

    # 1. R (အာ): 12r500
    r_matches = re.findall(r'(\d{2})r(\d+)', text)
    for num, amt in r_matches:
        total_amt += int(amt) * 2

    # 2. Direct: 12-500, 12=500, 12ဒဲ့500
    d_matches = re.findall(r'(\d{2})(?:[=-]|ဒဲ့)(\d+)', text)
    for num, amt in d_matches:
        total_amt += int(amt)

    # 3. ပတ်သီး: 9ပတ် 1000
    p_matches = re.findall(r'(\d)(?:ပတ်|အပါ|ပါ|by|bi|ch)(\d+)', text)
    for digit, amt in p_matches:
        total_amt += int(amt) * 19

    # 4. ပတ်ပူးပို/ထိပ်နောက်: 9ပတ်အပူးပို 500
    pp_matches = re.findall(r'(\d)(?:ပတ်ပူး|ပူးပို|ပတ်ပူးပို|ထန|ထပ|ထိပ်ပိတ်|ထိပ်နောက်)(\d+)', text)
    for digit, amt in pp_matches:
        total_amt += int(amt) * 20

    # 5. ထိပ်စီး: 2ထိပ် 500
    t_matches = re.findall(r'(\d)(?:ထိပ်|ထ|top|t)(\d+)', text)
    for digit, amt in t_matches:
        total_amt += int(amt) * 10

    # 6. ဘရိတ်: 1ဘရိတ် 1000 (385bk500 ခွဲတွက်ခြင်းအပါအဝင်)
    bk_matches = re.findall(r'(\d+)(?:ဘရိတ်|bk)(\d+)', text)
    for digits, amt in bk_matches:
        total_amt += (len(digits) * 10 * int(amt))

    # 7. ခွေဂဏန်း: 123ခွေ 500
    k_matches = re.findall(r'(\d{3,})(?:ခွေ|အခွေ|ခ)(\d+)', text)
    for digits, amt in k_matches:
        n = len(digits)
        total_amt += (n * (n - 1)) * int(amt)

    # 8. အပူးပါခွေ: 123ပူး 500
    kp_matches = re.findall(r'(\d{3,})(?:ပူး|အပူးပါ|ခပ|အခွေပူး)(\d+)', text)
    for digits, amt in kp_matches:
        n = len(digits)
        total_amt += ((n * (n - 1)) + n) * int(amt)

    # 9. အပူးစုံ/ဆယ်ပြည့်/ညီကို/ပါဝါ/နက္ခတ်
    special_patterns = {
        r'(?:အပူးစုံ|အပူး|ပူး)(\d+)': 10,
        r'(?:စုံပူး|မပူး)(\d+)': 5,
        r'(?:စုံဘရိတ်|စုံbk|စဘရိတ်|မဘရိတ်|မbk)(\d+)': 50,
        r'(?:ဆယ်ပြည့်)(\d+)': 10,
        r'(?:ပါဝါ|ပဝ|pw|power)(\d+)': 10,
        r'(?:နက္ခတ်|nk|နက|နခ)(\d+)': 10,
        r'(?:ညီကို|ညီအကို|ညီအစ်ကို)(\d+)': 20
    }
    for pat, multiplier in special_patterns.items():
        matches = re.findall(pat, text)
        for amt in matches:
            total_amt += int(amt) * multiplier

    # 10. စုံစုံ/မမ/စမ/မစ (25 ကွက်)
    sone_ma = re.findall(r'(?:စစ|မမ|စမ|မစ|စုံစုံ|စုံမ|မစုံ|မမ)(\d+)', text)
    for amt in sone_ma:
        total_amt += 25 * int(amt)

    # 11. ကပ်: 234ကို678ကပ်R
    kap_matches = re.findall(r'(\d+)ကို(\d+)ကပ်r?(\d+)', text)
    for d1, d2, amt in kap_matches:
        total_amt += (len(d1) * len(d2)) * int(amt)
        if 'r' in text.lower(): total_amt *= 2

    return total_amt, discount, market_found
p
