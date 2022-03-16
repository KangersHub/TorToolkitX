# -*- coding: utf-8 -*-
# (c) YashDK [yash-dk@github]
# (c) modified by AmirulAndalib [amirulandalib@github]

import logging
import math
import time

from ..core.getVars import get_val
from .Human_Format import human_readable_bytes, human_readable_timedelta

# logging.basicConfig(level=logging.DEBUG)


async def progress(
    current, total, message, file_name, start, time_out, cancel_msg=None, updb=None
):

    now = time.time()
    diff = now - start
    if round(diff % time_out) == 0 or current == total:
        if cancel_msg is not None:
            # dirty alt. was not able to find something to stop upload
            # todo inspect with "StopAsyncIteration"
            if updb.get_cancel_status(cancel_msg.chat_id, cancel_msg.id):
                raise Exception("🗑 ᴄᴀɴᴄᴇʟ ᴛᴏ ᴜᴘʟᴏᴀᴅ")

        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = human_readable_timedelta(seconds=elapsed_time / 1000)

        estimated_total_time = human_readable_timedelta(
            seconds=estimated_total_time / 1000
        )

        progress = "<b>🎳Prog:</b> [{0}{1}] <b>-</b> {2}%\n".format(
            "".join(
                [get_val("COMPLETED_STR") for i in range(math.floor(percentage / 10))]
            ),
            "".join(
                [
                    get_val("REMAINING_STR")
                    for i in range(10 - math.floor(percentage / 10))
                ]
            ),
            round(percentage, 2),
        )

        tmp = progress + "👀<b>Status:</b> {0} <b>Of</b> {1}\n⏱<b>Speed:</b> {2}/s\n🕒<b>ETA:</b> {3}\n📡<b>Using Engine:</b> Telethon".format(
            human_readable_bytes(current),
            human_readable_bytes(total),
            human_readable_bytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        try:
            if not message.photo:
                await message.edit(
                    text="**📤__ᴜᴘʟᴏᴀᴅɪɴɢ...__** \n\n🗂<b>File Name:</b> {} \n{}".format(file_name, tmp)
                )
            else:
                await message.edit(
                    caption="**📤__ᴜᴘʟᴏᴀᴅɪɴɢ...__** \n\n🗂<b>File Name:</b> {} \n{}".format(file_name, tmp)
                )
        except Exception as e:
            logging.error(e)
        return
    else:
        return
