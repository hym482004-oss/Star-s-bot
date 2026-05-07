import re

def get_combinations(text):
    text = text.lower().replace(' ', '').replace('*', '-').replace('/', '-')
    
    # Market & Discount Logic
    discount = 0
    market_found = ""
    
    markets = {
        'du': (['dubai', 'ဒူ', 'du'], 0.07),
        'me': (['mega', 'me', 'မီ'], 0.07),
        'maxi': (['maxi', 'max', 'မက်ဆီ', 'မက်စီ', 'စီစီ'], 0.07),
        'lao': (['lao', 'loa', 'လာအို', 'လာလာ'], 0.07),
        'ld': (['london', 'ld', 'လန်လန်', 'လန်ဒန်'], 0.07),
        'mm': (['mm', 'မြန်မာ'], 0.10),
        'glo': (['global', 'glo', 'ဂလို'], 0.03)
    }

    for key, (aliases, rate) in markets.items():
        if any(alias in text for alias in aliases):
            discount = rate
            market_found = key.upper()
            break

    total_amt = 0
    # Error checking: ဂဏန်းအတွဲလိုက်ကြီးဖြစ်နေပြီး ပိုက်ဆံမပါရင် (ဥပမာ 35 45 6)
    # ဒါပေမယ့် တွက်နည်းထဲမှာ ပါသွားရင် error မတက်အောင် logic ထည့်ထားတယ်

    # 1. R (အာ) Logic: 12r500
    r_matches = re.findall(r'(\d{2})r(\d+)', text)
    for num, amt in r_matches:
        total_amt += int(amt) * 2

    # 2. Direct: 12-500, 12=500, 12ဒဲ့500
    d_matches = re.findall(r'(\d{2})(?:[=-]|ဒဲ့)(\d+)', text)
    for num, amt in d_matches:
        total_amt += int(amt)

    # 3. ပတ်သီး: 9ပတ် 1000 (19 ကွက်)
    p_matches = re.findall(r'(\d)(?:ပတ်|အပါ|ပါ|by|bi|ch)(\d+)', text)
    for digit, amt in p_matches:
        total_amt += int(amt) * 19

    # 4. ပတ်ပူးပို: 9ပတ်အပူးပို (20 ကွက်)
    pp_matches = re.findall(r'(\d)(?:ပတ်ပူး|ပူးပို|ပတ်ပူးပို|ထန|ထပ|ထိပ်ပိတ်|ထိပ်နောက်)(\d+)', text)
    for digit, amt in pp_matches:
        total_amt += int(amt) * 20

    # 5. ထိပ်စီး: 2ထိပ် 500 (10 ကွက်)
    t_matches = re.findall(r'(\d)(?:ထိပ်|ထ|top|t)(\d+)', text)
    for digit, amt in t_matches:
        total_amt += int(amt) * 10

    # 6. ဘရိတ်: 1ဘရိတ် 1000 (10 ကွက်) - 385bk500 လိုမျိုး ခွဲထုတ်ခြင်း
    bk_matches = re.findall(r'(\d+)(?:ဘရိတ်|bk)(\d+)', text)
    for digits, amt in bk_matches:
        total_amt += (len(digits) * 10 * int(amt))

    # 7. ခွေဂဏန်း: 123ခွေ 500 (n * n-1)
    k_matches = re.findall(r'(\d{3,})(?:ခွေ|အခွေ|ခ)(\d+)', text)
    for digits, amt in k_matches:
        n = len(digits)
        total_amt += (n * (n - 1)) * int(amt)

    # 8. အပူးပါခွေ: 123ပူး 500 (ခွေ + n)
    kp_matches = re.findall(r'(\d{3,})(?:ပူး|အပူးပါ|ခပ|အခွေပူး)(\d+)', text)
    for digits, amt in kp_matches:
        n = len(digits)
        total_amt += ((n * (n - 1)) + n) * int(amt)

    # 9. အပူးစုံ: 10 ကွက်
    if 'အပူးစုံ' in text or 'အပူး' in text or 'ပူး' in text:
        pu_amt = re.findall(r'(?:အပူးစုံ|အပူး|ပူး)(\d+)', text)
        for amt in pu_amt: total_amt += int(amt) * 10

    # 10. စုံဘရိတ်: 50 ကွက်
    sbk_matches = re.findall(r'(?:စုံဘရိတ်|စုံbk|စဘရိတ်)(\d+)', text)
    for amt in sbk_matches: total_amt += 50 * int(amt)

    # 11. ကပ်: 234ကို678ကပ်R (n * n)
    kap_matches = re.findall(r'(\d+)ကို(\d+)ကပ်r?(\d+)', text)
    for d1, d2, amt in kap_matches:
        total_amt += (len(d1) * len(d2)) * int(amt)
        if 'r' in text.lower(): total_amt *= 2

    return total_amt, discount, market_found
