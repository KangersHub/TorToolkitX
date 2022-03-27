import logging

from speedtest import Speedtest

from ..functions.Human_Format import human_readable_bytes

torlog = logging.getLogger(__name__)


async def get_speed(message):
    imspd = await message.reply("⏱𝙿𝚛𝚘𝚌𝚎𝚜𝚜𝚒𝚗𝚐 𝚂𝚙𝚎𝚎𝚍𝚝𝚎𝚜𝚝...")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    (result["share"])
    string_speed = f"""
⏱**__ꜱᴘᴇᴇᴅᴛᴇꜱᴛ ʀᴇꜱᴜʟᴛ...__**

🖱**Server Name:** `{result["server"]["name"]}`
🌏**Country:** `{result["server"]["country"]}, {result["server"]["cc"]}`
👨🏻‍💼**Sponsor:** `{result["server"]["sponsor"]}`
📤**Upload:** `{human_readable_bytes(result["upload"] / 8)}/s`
📥**Download:** `{human_readable_bytes(result["download"] / 8)}/s`
📡**Ping:** `{result["ping"]} ms`
🧑🏻‍💻**ISP:** `{result["client"]["isp"]}`
"""
    await imspd.delete()
    await message.reply(string_speed, parse_mode="markdown")
    torlog.info(
        f'<b>🪛ꜱᴇʀᴠᴇʀ ꜱᴘᴇᴇᴅ ʀᴇꜱᴜʟ</b>\n\n<b>DL:</b> {human_readable_bytes(result["download"] / 8)}/s <b>UL:</b> {human_readable_bytes(result["upload"] / 8)}/s'
    )
