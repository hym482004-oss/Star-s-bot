import re

# =====================
# 🔥 KEYWORDS (longer-first + group order matters)
# =====================
KEYWORDS = {
    "bro": ["ညီအစ်ကို", "ညီအကို", "ညီကို"],

    "pat_pu": ["ပတ်ပူးပို", "ပူးပို", "ပတ်ပူး", "ပတ်အကွက်20", "ထိပ်ပိတ်", "ထိပ်နောက်", "ထန", "ထပ"],
    "pat": ["ပတ်သီး", "အပါ", "ပတ်", "ပါ", "ch", "p"],

    "even_brake": ["စုံဘရိတ်", "စဘရိတ်", "စုံbk", "စုံBk", "မbk", "မBk", "မဘရိတ်"],
    "brake": ["ဘရိတ်", "bk", "Bk"],

    "top": ["ထိပ်စီး", "ထိပ်", "top", "Top", "t", "T", "ထ"],

    "power": ["ပါဝါ", "power", "pw", "ပဝ"],
    "nk": ["နက္ခတ်", "nk", "Nk", "နက", "နခ"],

    "ten": ["ဆယ်ပြည့်", "ဆယ်ပြည်", "ဆယ့်ပြည်"],

    # ပိတ် group (single-char "ပ","န" ကို boundary နဲ့ပဲဖမ်းမယ်)
    "pait": ["အပိတ်", "ပိတ်", "နောက်"],

    # ပူး fixed group (အပူး 500 လို digits မပါတဲ့အခါ)
    "puu_fixed": ["အပူးစုံ", "အပူးအစုံ", "အပူးအကုန်", "အပူး", "ပူး", "puu", "ပုး"],

    # စပူး/မပူး => 5 ကွက်
    "so_pu": ["စပူး", "စုံပူး", "မပူး"],

    # စစ/မမ/စမ... => 25 ကွက်
    "sam": ["စုံစုံ", "စုံမ", "စစ", "မမ", "စမ", "မစ", "စုူံစူံ", "စူံစုံ", "စုံစူံ"],

    # ခွေ / ခွေပူး
    "khwe_pu": ["အပူးပါခွေပူး", "အပူးပါခွေ", "အပူးအပြီးပါ", "ခွေပူး", "အခွေပူး", "ခပ", "ခွေပူး"],
    "khwe": ["အခွေ", "ခွေ", "ခ"],

    # ကပ်
    "kap": ["အကပ်", "ကပ်", "ကို"],

    # direct marker (ဒါမတွေ့ရင်လည်း default direct ပဲ)
    "direct": ["ဒဲ့", "=", "-", "*", "/", ".", ":"],
}

RULE_ORDER = [
    "bro",
    "pat_pu", "pat",
    "even_brake", "brake",
    "top",
    "power", "nk",
    "ten",
    "pait",
    "khwe_pu", "khwe",
    "kap",
    "so_pu",
    "sam",
    "puu_fixed",
    "direct",
]

SEPS_CLASS = r"[ \t,\-*/=.:]"

def _contains_token(text: str, token: str) -> bool:
    """single-char (e.g. 'ပ','န') ကိုတော့ separator boundary နဲ့ပဲ match လုပ်"""
    if not token:
        return False
    t = text.lower()
    k = token.lower()

    # ASCII tokens: simple contains
    if re.fullmatch(r"[a-z0-9]+", k):
        return k in t

    # single Burmese char => require boundary
    if len(k) == 1:
        return re.search(rf"(?:^|{SEPS_CLASS}){re.escape(k)}(?:$|{SEPS_CLASS})", t) is not None

    return k in t

def detect_rule(line: str) -> str:
    for rule in RULE_ORDER:
        for k in KEYWORDS.get(rule, []):
            if _contains_token(line, k):
                return rule
    return "direct"

def has_reverse(line: str) -> bool:
    # r / R should not match inside 'brake'
    if re.search(r"(?i)(?:^|[^a-z0-9])r(?:\s*\d+)?", line):
        return True
    if "အာ" in line:
        return True
    return False

def split_bets_and_amounts(line: str):
    """
    return:
      bets: list[str]  (amount numbers removed)
      amount_sum: int  (normal + R amounts)
      rev_flag: bool   (R keyword exists)
    """
    raw = line
    rev_flag = has_reverse(raw)

    # 1) reverse amounts: r200 / အာ200
    rev_amounts = [int(x) for x in re.findall(r"(?i)(?:^|[^a-z0-9])(?:r|အာ)\s*(\d+)", raw)]

    # remove reverse amount parts so they don't get treated as bet numbers
    tmp = re.sub(r"(?i)(?:r|အာ)\s*\d+", " ", raw)

    # 2) find all remaining numbers (candidates: bet numbers + maybe normal amount)
    nums = [m.group(0) for m in re.finditer(r"\d+", tmp)]

    normal_amount = 0

    # heuristic: normal amount usually >= 3 digits (500,1000,5000...)
    # take the RIGHTMOST >=3-digit as amount if exists
    idx_amount = None
    for i in range(len(nums) - 1, -1, -1):
        if len(nums[i]) >= 3:
            idx_amount = i
            break

    # if no >=3-digit and NO reverse amount => last number is amount (e.g. "12 50")
    if idx_amount is None and not rev_amounts and len(nums) >= 2:
        idx_amount = len(nums) - 1

    if idx_amount is not None and nums:
        normal_amount = int(nums[idx_amount])
        bets = [n for j, n in enumerate(nums) if j != idx_amount]
    else:
        bets = nums

    amount_sum = normal_amount + sum(rev_amounts)
    return bets, amount_sum, rev_flag

# =====================
# 🔥 CALC ENGINE (your spec)
# =====================
def calculate(rule: str, bets: list[str], amount_sum: int, rev_flag: bool):
    # base slots
    if rule == "bro":
        base = 20

    elif rule == "pat":
        base = 19

    elif rule == "pat_pu":
        base = 20

    elif rule in ("top", "brake"):
        # each bet digit => 10 slots (3ထိပ် + 8ထိပ် => 20)
        base = (len(bets) * 10) if bets else 10

    elif rule in ("power", "nk", "pait", "ten"):
        base = 10

    elif rule == "puu_fixed":
        # "အပူး 500" => 10 slots (00..99 doubles)
        # "123ပူး 500" လို bets ပါလာရင် khwe_pu အနေနဲ့အောက်မှာ handle လုပ်မယ်
        base = 10

    elif rule == "so_pu":
        base = 5

    elif rule == "sam":
        base = 25

    elif rule == "khwe":
        # n = digit count of all bets joined (e.g., 123 -> 3)
        digits = "".join(bets)
        n = len(digits)
        base = n * (n - 1)

    elif rule == "khwe_pu":
        # N×N
        digits = "".join(bets)
        n = len(digits)
        base = n * n

    elif rule == "kap":
        # a×b where a,b are digit lengths of first two bet numbers
        if len(bets) >= 2:
            base = len(bets[0]) * len(bets[1])
        else:
            base = 0

    else:  # direct
        base = len(bets)

    # if "ပူး" keyword but bets ပါနေပြီး digits>=3 ဆို khwe_pu သဘောတရားထား (123ပူး)
    if rule == "puu_fixed" and bets:
        digits = "".join(bets)
        if len(digits) >= 3:
            base = len(digits) * len(digits)  # N×N

    # Reverse => base 2 ဆ (ကွက် ၂ ဆ)
    eff_base = base * 2 if rev_flag else base

    total = eff_base * amount_sum
    return eff_base, total

# =====================
# 🔥 MAIN PARSE (newline only)
# =====================
def parse_message(text: str):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    results = []
    grand_total = 0

    for line in lines:
        rule = detect_rule(line)
        bets, amount_sum, rev_flag = split_bets_and_amounts(line)

        base, total = calculate(rule, bets, amount_sum, rev_flag)

        grand_total += total
        results.append({
            "raw": line,
            "rule": rule,
            "base": int(base),
            "amount_sum": int(amount_sum),
            "total": int(total),
        })

    return {"lines": results, "grand_total": int(grand_total)}
    
