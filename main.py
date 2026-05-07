@dp.message()
async def handle(message: Message):

    text = message.text.lower()

    # ✅ 2D names
    markets = ["du", "mega", "max", "glo", "ld", "lao", "mm"]

    # ✅ detect calculation text
    has_number = bool(re.search(r"\d", text))
    has_amount = bool(re.search(r"r\d+|\d+\s*%", text))

    # ❌ ignore normal chat
    if not has_number:
        return

    # ❌ no market name
    if not any(m in text for m in markets):

        admins = await message.chat.get_administrators()

        mentions = []

        for admin in admins:
            user = admin.user

            if user.username:
                mentions.append(f"@{user.username}")

        mention_text = " ".join(mentions)

        await message.reply(
            f"⚠️ 2D name မပါသေးပါ\n\n"
            f"{mention_text}\n"
            f"ဒါလေးလာစစ်ပေးပါရှင့်"
        )

        return

    # ✅ parse
    data = parse_message(message.text)

    result = ""

    for line in data["lines"]:

        result += (
            f"📌 {line['raw']}\n"
            f"🎯 {line['rule']}\n"
            f"🔢 {line['calc']['base']} ကွက်\n"
            f"💰 {line['r']}\n"
            f"📦 {line['calc']['total']}\n\n"
        )

    result += f"✅ TOTAL = {data['grand_total']}"

    await message.reply(result)
