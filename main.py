@dp.message()
async def handle(message: Message):
    data = parse_message(message.text)

    result = ""

    for line in data["lines"]:
        result += (
            f"📌 {line['raw']}\n"
            f"🎯 Rule : {line['rule']}\n"
            f"🔢 Blocks : {line['calc']['base']}\n"
            f"💰 Amount : {line['r']}\n"
            f"📦 Total : {line['calc']['total']}\n\n"
        )

    result += f"✅ GRAND TOTAL = {data['grand_total']}"

    await message.reply(result)
