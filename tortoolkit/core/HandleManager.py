# -*- coding: utf-8 -*-
# (c) YashDK [yash-dk@github]
# (c) modified by AmirulAndalib [amirulandalib@github]

import asyncio as aio
import logging
import os
import re
import shutil
import time
from functools import partial

import psutil
from pyrogram import __version__ as pyrover
from telethon import TelegramClient
from telethon import __version__ as telever
from telethon import events
from telethon.tl.types import KeyboardButtonCallback

from tortoolkit import __version__

from .. import tor_db, upload_db, uptime, user_db, var_db
from ..core.getCommand import get_command
from ..core.getVars import get_val
from ..core.speedtest import get_speed
from ..functions import Human_Format
from ..functions.admin_check import is_admin
from ..functions.instadl import _insta_post_downloader
from ..functions.Leech_Module import (
    cancel_torrent,
    check_link,
    get_status,
    get_transfer,
    pause_all,
    purge_all,
    resume_all,
)
from ..functions.rclone_upload import get_config
from ..functions.tele_upload import upload_a_file
from .settings import handle_setting_callback, handle_settings
from .ttk_ytdl import (
    handle_ytdl_callbacks,
    handle_ytdl_command,
    handle_ytdl_file_download,
    handle_ytdl_playlist,
    handle_ytdl_playlist_down,
)
from .user_settings import handle_user_setting_callback, handle_user_settings

torlog = logging.getLogger(__name__)
import signal

from PIL import Image

from .status.menu import create_status_menu, create_status_user_menu
from .status.status import Status


def add_handlers(bot: TelegramClient):
    # bot.add_event_handler(handle_leech_command,events.NewMessage(func=lambda e : command_process(e,get_command("LEECH")),chats=ExecVars.ALD_USR))

    bot.add_event_handler(
        handle_leech_command,
        events.NewMessage(
            pattern=command_process(get_command("LEECH")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_purge_command,
        events.NewMessage(
            pattern=command_process(get_command("PURGE")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_pauseall_command,
        events.NewMessage(
            pattern=command_process(get_command("PAUSEALL")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_resumeall_command,
        events.NewMessage(
            pattern=command_process(get_command("RESUMEALL")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_status_command,
        events.NewMessage(
            pattern=command_process(get_command("STATUS")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_u_status_command,
        events.NewMessage(
            pattern=command_process(get_command("USTATUS")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_settings_command,
        events.NewMessage(
            pattern=command_process(get_command("SETTINGS")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_exec_message_f,
        events.NewMessage(
            pattern=command_process(get_command("EXEC")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        upload_document_f,
        events.NewMessage(
            pattern=command_process(get_command("UPLOAD")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_ytdl_command,
        events.NewMessage(
            pattern=command_process(get_command("YTDL")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_ytdl_playlist,
        events.NewMessage(
            pattern=command_process(get_command("PYTDL")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        about_me,
        events.NewMessage(
            pattern=command_process(get_command("ABOUT")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        get_logs_f,
        events.NewMessage(
            pattern=command_process(get_command("GETLOGS")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_test_command,
        events.NewMessage(pattern="/test", chats=get_val("ALD_USR")),
    )

    bot.add_event_handler(
        handle_server_command,
        events.NewMessage(
            pattern=command_process(get_command("SERVER")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        set_password_zip,
        events.NewMessage(
            pattern=command_process("/setpass"), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        handle_user_settings_,
        events.NewMessage(pattern=command_process(get_command("USERSETTINGS"))),
    )

    bot.add_event_handler(
        _insta_post_downloader,
        events.NewMessage(
            pattern=command_process(get_command("INSTADL")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        start_handler, events.NewMessage(pattern=command_process(get_command("START")))
    )

    bot.add_event_handler(
        clear_thumb_cmd,
        events.NewMessage(
            pattern=command_process(get_command("CLRTHUMB")), chats=get_val("ALD_USR")
        ),
    )

    bot.add_event_handler(
        set_thumb_cmd,
        events.NewMessage(
            pattern=command_process(get_command("SETTHUMB")), chats=get_val("ALD_USR")
        ),
    )
    # REMOVED HEROKU BLOCK
    bot.add_event_handler(
        speed_handler,
        events.NewMessage(
            pattern=command_process(get_command("SPEEDTEST")), chats=get_val("ALD_USR")
        ),
    )

    signal.signal(signal.SIGINT, partial(term_handler, client=bot))
    signal.signal(signal.SIGTERM, partial(term_handler, client=bot))
    bot.loop.run_until_complete(booted(bot))

    # *********** Callback Handlers ***********

    bot.add_event_handler(
        callback_handler_canc, events.CallbackQuery(pattern="torcancel")
    )

    bot.add_event_handler(handle_settings_cb, events.CallbackQuery(pattern="setting"))

    bot.add_event_handler(handle_upcancel_cb, events.CallbackQuery(pattern="upcancel"))

    bot.add_event_handler(handle_pincode_cb, events.CallbackQuery(pattern="getpin"))

    bot.add_event_handler(
        handle_ytdl_callbacks, events.CallbackQuery(pattern="ytdlsmenu")
    )

    bot.add_event_handler(
        handle_ytdl_callbacks, events.CallbackQuery(pattern="ytdlmmenu")
    )

    bot.add_event_handler(
        handle_ytdl_file_download, events.CallbackQuery(pattern="ytdldfile")
    )

    bot.add_event_handler(
        handle_ytdl_playlist_down, events.CallbackQuery(pattern="ytdlplaylist")
    )

    bot.add_event_handler(
        handle_user_setting_callback, events.CallbackQuery(pattern="usetting")
    )
    bot.add_event_handler(
        handle_server_command, events.CallbackQuery(pattern="fullserver")
    )


# REMOVED HEROKU BLOCK
# *********** Handlers Below ***********


async def handle_leech_command(e):
    if not e.is_reply:
        await e.reply("🥱𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝙰 𝙻𝚒𝚗𝚔 𝙾𝚛 𝙼𝚊𝚐𝚗𝚎𝚝")
    else:
        rclone = False
        tsp = time.time()
        buts = [[KeyboardButtonCallback("ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ", data=f"leechselect tg {tsp}")]]
        if await get_config() is not None:
            buts.append(
                [KeyboardButtonCallback("ᴛᴏ ᴅʀɪᴠᴇ", data=f"leechselect drive {tsp}")]
            )
        # tsp is used to split the callbacks so that each download has its own callback
        # cuz at any time there are 10-20 callbacks linked for leeching XD

        buts.append(
            [
                KeyboardButtonCallback(
                    "ᴜᴘʟᴏᴀᴅ ɪɴ ᴀ ᴢɪᴘ.[ᴛᴏɢɢʟᴇ]", data=f"leechzip toggle {tsp}"
                )
            ]
        )
        buts.append(
            [
                KeyboardButtonCallback(
                    "ᴇxᴛʀᴀᴄᴛ ꜰʀᴏᴍ ᴀʀᴄʜɪᴠᴇ.[ᴛᴏɢɢʟᴇ]", data=f"leechzipex toggleex {tsp}"
                )
            ]
        )

        conf_mes = await e.reply(
            f"𝙵𝚒𝚛𝚜𝚝 𝚌𝚕𝚒𝚌𝚔 𝚒𝚏 𝚢𝚘𝚞 𝚠𝚊𝚗𝚝 𝚝𝚘 𝚣𝚒𝚙 𝚝𝚑𝚎 𝚌𝚘𝚗𝚝𝚎𝚗𝚝𝚜 𝚘𝚛 𝚎𝚡𝚝𝚛𝚊𝚌𝚝 𝚊𝚜 𝚊𝚗 𝚊𝚛𝚌𝚑𝚒𝚟𝚎 (𝚘𝚗𝚕𝚢 𝚘𝚗𝚎 𝚠𝚒𝚕𝚕 𝚠𝚘𝚛𝚔 𝚊𝚝 𝚊 𝚝𝚒𝚖𝚎) 𝚝𝚑𝚎𝚗...\n\n<b>ᴄʜᴏᴏꜱᴇ ᴡʜᴇʀᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ʏᴏᴜʀ ꜰɪʟᴇꜱ:-</b>\nᴛʜᴇ ꜰɪʟᴇꜱ ᴡɪʟʟ ʙᴇ ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ ᴅᴇꜰᴀᴜʟᴛ ᴅᴇꜱᴛɪɴᴀᴛɪᴏɴ: <b>{𝚐𝚎𝚝_𝚟𝚊𝚕('𝙳𝙴𝙵𝙰𝚄𝙻𝚃_𝚃𝙸𝙼𝙴𝙾𝚄𝚃')}</b> 𝚊𝚏𝚝𝚎𝚛 𝟼𝟶 𝚜𝚎𝚌 𝚘𝚏 𝚗𝚘 𝚊𝚌𝚝𝚒𝚘𝚗 𝚋𝚢 𝚞𝚜𝚎𝚛.</u>\n\n<b>ꜱᴜᴘᴘᴏꜱᴇᴅ ᴀʀᴄʜɪᴠᴇꜱ ᴛᴏ ᴇxᴛʀᴀᴄᴛ:</b>\nzip, 7z, tar, gzip2, iso, wim, rar, tar.gz, tar.bz2",
            parse_mode="html",
            buttons=buts,
        )

        # zip check in background
        ziplist = await get_zip_choice(e, tsp)
        zipext = await get_zip_choice(e, tsp, ext=True)

        # blocking leech choice
        choice = await get_leech_choice(e, tsp)

        # zip check in backgroud end
        await get_zip_choice(e, tsp, ziplist, start=False)
        await get_zip_choice(e, tsp, zipext, start=False, ext=True)
        is_zip = ziplist[1]
        is_ext = zipext[1]

        # Set rclone based on choice
        if choice == "drive":
            rclone = True
        else:
            rclone = False

        await conf_mes.delete()

        if rclone:
            if get_val("RCLONE_ENABLED"):
                await check_link(e, rclone, is_zip, is_ext, conf_mes)
            else:
                await e.reply(
                    "<b>DRIVE IS DISABLED BY THE OWNER</b>", parse_mode="html"
                )
        else:
            if get_val("LEECH_ENABLED"):
                await check_link(e, rclone, is_zip, is_ext, conf_mes)
            else:
                await e.reply(
                    "<b>𝚃𝙶 𝙻𝙴𝙴𝙲𝙷 𝙸𝚂 𝙳𝙸𝚂𝙰𝙱𝙻𝙴𝙳 𝙱𝚈 𝚃𝙷𝙴 𝙾𝚆𝙽𝙴𝚁</b>", parse_mode="html"
                )


async def get_leech_choice(e, timestamp):
    # abstract for getting the confirm in a context

    lis = [False, None]
    cbak = partial(
        get_leech_choice_callback, o_sender=e.sender_id, lis=lis, ts=timestamp
    )

    # REMOVED HEROKU BLOCK

    e.client.add_event_handler(
        # lambda e: test_callback(e,lis),
        cbak,
        events.CallbackQuery(pattern="leechselect"),
    )

    start = time.time()
    defleech = get_val("DEFAULT_TIMEOUT")

    while not lis[0]:
        if (time.time() - start) >= 60:  # TIMEOUT_SEC:

            if defleech == "leech":
                return "tg"
            elif defleech == "rclone":
                return "drive"
            else:
                # just in case something goes wrong
                return "tg"
            break
        await aio.sleep(1)

    val = lis[1]

    e.client.remove_event_handler(cbak)

    return val


async def get_zip_choice(e, timestamp, lis=None, start=True, ext=False):
    # abstract for getting the confirm in a context
    # creating this functions to reduce the clutter
    if lis is None:
        lis = [None, None, None]

    if start:
        cbak = partial(
            get_leech_choice_callback, o_sender=e.sender_id, lis=lis, ts=timestamp
        )
        lis[2] = cbak
        if ext:
            e.client.add_event_handler(cbak, events.CallbackQuery(pattern="leechzipex"))
        else:
            e.client.add_event_handler(cbak, events.CallbackQuery(pattern="leechzip"))
        return lis
    else:
        e.client.remove_event_handler(lis[2])


async def get_leech_choice_callback(e, o_sender, lis, ts):
    # handle the confirm callback

    if o_sender != e.sender_id:
        return
    data = e.data.decode().split(" ")
    if data[2] != str(ts):
        return

    lis[0] = True
    if data[1] == "toggle":
        # encompasses the None situation too
        print("data ", lis)
        if lis[1] is True:
            await e.answer("𝚆𝚒𝚕𝚕 𝙽𝚘𝚝 𝚋𝚎 𝚣𝚒𝚙𝚙𝚎𝚍", alert=True)
            lis[1] = False
        else:
            await e.answer("𝚆𝚒𝚕𝚕 𝚋𝚎 𝚣𝚒𝚙𝚙𝚎𝚍", alert=True)
            lis[1] = True
    elif data[1] == "toggleex":
        print("exdata ", lis)
        # encompasses the None situation too
        if lis[1] is True:
            await e.answer("𝙸𝚝 𝚠𝚒𝚕𝚕 𝚗𝚘𝚝 𝚋𝚎 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚎𝚍.", alert=True)
            lis[1] = False
        else:
            await e.answer(
                "𝙸𝚏 𝚒𝚝 𝚒𝚜 𝚊 𝙰𝚛𝚌𝚑𝚒𝚟𝚎 𝚒𝚝 𝚠𝚒𝚕𝚕 𝚋𝚎 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚎𝚍. 𝙵𝚞𝚛𝚝𝚑𝚎𝚛 𝚒𝚗 𝚢𝚘𝚞 𝚌𝚊𝚗 𝚜𝚎𝚝 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍 𝚝𝚘 𝚎𝚡𝚝𝚛𝚊𝚌𝚝 𝚝𝚑𝚎 𝚉𝙸𝙿.",
                alert=True,
            )
            lis[1] = True
    else:
        lis[1] = data[1]


# add admin checks here - done
async def handle_purge_command(e):
    if await is_admin(e.client, e.sender_id, e.chat_id):
        await purge_all(e)
    else:
        await e.delete()


# REMOVED HEROKU BLOCK


async def handle_pauseall_command(e):
    if await is_admin(e.client, e.sender_id, e.chat_id):
        await pause_all(e)
    else:
        await e.delete()


async def handle_resumeall_command(e):
    if await is_admin(e.client, e.sender_id, e.chat_id):
        await resume_all(e)
    else:
        await e.delete()


async def handle_settings_command(e):
    if await is_admin(e.client, e.sender_id, e.chat_id):
        await handle_settings(e)
    await e.delete()


async def handle_status_command(e):
    cmds = e.text.split(" ")
    if len(cmds) > 1:
        if cmds[1] == "all":
            await get_status(e, True)
        else:
            await get_status(e)
    else:
        await create_status_menu(e)
    await e.delete()


async def handle_u_status_command(e):
    await create_status_user_menu(e)
    await e.delete()             


async def speed_handler(e):
    if await is_admin(e.client, e.sender_id, e.chat_id):
        await get_speed(e)


async def handle_test_command(e):
    pass


async def handle_settings_cb(e):
    if await is_admin(e.client, e.sender_id, e.chat_id):
        await handle_setting_callback(e)
    else:
        await e.answer("⚠️ 𝚆𝙰𝚁𝙽 ⚠️ 𝙳𝚘𝚗𝚝 𝚃𝚘𝚞𝚌𝚑 𝙾𝚠𝚗𝚎𝚛 𝚂𝚎𝚝𝚝𝚒𝚗𝚐𝚜.", alert=True)


async def handle_upcancel_cb(e):
    db = upload_db

    data = e.data.decode("UTF-8")
    torlog.info("Data is {}".format(data))
    data = data.split(" ")

    if str(e.sender_id) == data[3]:
        db.cancel_download(data[1], data[2])
        await e.answer("𝚄𝚙𝚕𝚘𝚊𝚍 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚌𝚊𝚗𝚌𝚎𝚕𝚎𝚍 ;)", alert=True)
    elif e.sender_id in get_val("ALD_USR"):
        db.cancel_download(data[1], data[2])
        await e.answer("UPLOAD CANCELED IN ADMIN MODE XD ;)", alert=True)
    else:
        await e.answer("𝙲𝚊𝚗'𝚝 𝙲𝚊𝚗𝚌𝚎𝚕 𝚘𝚝𝚑𝚎𝚛𝚜 𝚞𝚙𝚕𝚘𝚊𝚍 😡", alert=True)


async def callback_handler_canc(e):
    # TODO the msg can be deleted
    # mes = await e.get_message()
    # mes = await mes.get_reply_message()

    torlog.debug(f"Here the sender _id is {e.sender_id}")
    torlog.debug(
        "here is the allower users list {} {}".format(
            get_val("ALD_USR"), type(get_val("ALD_USR"))
        )
    )

    data = e.data.decode("utf-8").split(" ")
    torlog.debug("data is {}".format(data))

    is_aria = False
    is_mega = False

    if data[1] == "aria2":
        is_aria = True
        data.remove("aria2")

    if data[1] == "megadl":
        is_mega = True
        data.remove("megadl")

    if data[2] == str(e.sender_id):
        hashid = data[1]
        hashid = hashid.strip("'")
        torlog.info(f"Hashid :- {hashid}")

        await cancel_torrent(hashid, is_aria, is_mega)
        await e.answer("𝙻𝚎𝚎𝚌𝚑 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚌𝚊𝚗𝚌𝚎𝚕𝚎𝚍 ;)", alert=True)
    elif e.sender_id in get_val("ALD_USR"):
        hashid = data[1]
        hashid = hashid.strip("'")

        torlog.info(f"Hashid :- {hashid}")

        await cancel_torrent(hashid, is_aria, is_mega)
        await e.answer("𝙻𝚎𝚎𝚌𝚑 𝙷𝚊𝚜 𝙱𝚎𝚎𝚗 𝙲𝚊𝚗𝚌𝚎𝚕𝚎𝚍 𝙸𝚗 𝙰𝙳𝙼𝙸𝙽 𝙼𝙾𝙳𝙴 𝚇𝙳 ;)", alert=True)
    else:
        await e.answer("𝙲𝚊𝚗'𝚝 𝙲𝚊𝚗𝚌𝚎𝚕 𝚘𝚝𝚑𝚎𝚛𝚜 𝙻𝚎𝚎𝚌𝚑 😡", alert=True)


async def handle_exec_message_f(e):
    message = e
    client = e.client
    if await is_admin(client, message.sender_id, message.chat_id, force_owner=True):
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.id
        if message.is_reply:
            reply_to_id = message.reply_to_msg_id

        process = await aio.create_subprocess_shell(
            cmd, stdout=aio.subprocess.PIPE, stderr=aio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        e = stderr.decode()
        if not e:
            e = "𝙽𝚘 𝙴𝚛𝚛𝚘𝚛"
        o = stdout.decode()
        if not o:
            o = "𝙽𝚘 𝙾𝚞𝚝𝚙𝚞𝚝"
        else:
            _o = o.split("\n")
            o = "`\n".join(_o)
        OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"

        if len(OUTPUT) > 3900:
            with open("exec.text", "w+", encoding="utf8") as out_file:
                out_file.write(str(OUTPUT))
            await client.send_file(
                entity=message.chat_id,
                file="exec.text",
                caption=cmd,
                reply_to=reply_to_id,
            )
            os.remove("exec.text")
            await message.delete()
        else:
            await message.reply(OUTPUT)
    else:
        await message.reply("Only for owner")


async def handle_pincode_cb(e):
    data = e.data.decode("UTF-8")
    data = data.split(" ")

    if str(e.sender_id) == data[2]:
        db = tor_db
        passw = db.get_password(data[1])
        if isinstance(passw, bool):
            await e.answer("𝚝𝚘𝚛𝚛𝚎𝚗𝚝 𝚎𝚡𝚙𝚒𝚛𝚎𝚍 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚜𝚝𝚊𝚛𝚝𝚎𝚍 𝚗𝚘𝚠.")
        else:
            await e.answer(f"𝚈𝚘𝚞𝚛 𝙿𝚒𝚗𝚌𝚘𝚍𝚎 𝚒𝚜 {passw}", alert=True)

    else:
        await e.answer("𝙸𝚝'𝚜 𝚗𝚘𝚝 𝚢𝚘𝚞𝚛 𝚝𝚘𝚛𝚛𝚎𝚗𝚝.", alert=True)


async def upload_document_f(message):
    imsegd = await message.reply("⏳𝙿𝚛𝚘𝚌𝚎𝚜𝚜𝚒𝚗𝚐...")
    imsegd = await message.client.get_messages(message.chat_id, ids=imsegd.id)
    if await is_admin(
        message.client, message.sender_id, message.chat_id, force_owner=True
    ):
        if " " in message.text:
            recvd_command, local_file_name = message.text.split(" ", 1)
            recvd_response = await upload_a_file(
                local_file_name, imsegd, False, upload_db
            )
            # torlog.info(recvd_response)
    else:
        await message.reply("🧑🏻‍💻Only for owner")
    await imsegd.delete()


async def get_logs_f(e):
    if await is_admin(e.client, e.sender_id, e.chat_id, force_owner=True):
        e.text += " torlog.txt"
        await upload_document_f(e)
    else:
        await e.delete()


async def set_password_zip(message):
    # /setpass message_id password
    data = message.raw_text.split(" ")
    passdata = message.client.dl_passwords.get(int(data[1]))
    if passdata is None:
        await message.reply(f"No entry found for this job id {data[1]}")
    else:
        print(message.sender_id)
        print(passdata[0])
        if str(message.sender_id) == passdata[0]:
            message.client.dl_passwords[int(data[1])][1] = data[2]
            await message.reply(f"𝙿𝚊𝚜𝚜𝚠𝚘𝚛𝚍 𝚞𝚙𝚍𝚊𝚝𝚎𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢.")
        else:
            await message.reply(
                f"𝙲𝚊𝚗𝚗𝚘𝚝 𝚞𝚙𝚍𝚊𝚝𝚎 𝚝𝚑𝚎 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍 𝚝𝚑𝚒𝚜 𝚒𝚜 𝚗𝚘𝚝 𝚢𝚘𝚞𝚛 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍."
            )


async def start_handler(event):
    msg = "Hello This is V-Torrent Pro"
    await event.reply(msg, parse_mode="html")


def progress_bar(percentage):
    """Returns a progress bar for download"""
    # percentage is on the scale of 0-1
    comp = get_val("COMPLETED_STR")
    ncomp = get_val("REMAINING_STR")
    pr = ""

    if isinstance(percentage, str):
        return "NaN"

    try:
        percentage = int(percentage)
    except:
        percentage = 0

    for i in range(1, 11):
        if i <= int(percentage / 10):
            pr += comp
        else:
            pr += ncomp
    return pr


async def handle_server_command(message):
    print(type(message))
    if isinstance(message, events.CallbackQuery.Event):
        callbk = True
    else:
        callbk = False

    try:
        # Memory
        mem = psutil.virtual_memory()
        memavailable = Human_Format.human_readable_bytes(mem.available)
        memtotal = Human_Format.human_readable_bytes(mem.total)
        mempercent = mem.percent
        memfree = Human_Format.human_readable_bytes(mem.free)
    except:
        memavailable = "N/A"
        memtotal = "N/A"
        mempercent = "N/A"
        memfree = "N/A"

    try:
        # Frequencies
        cpufreq = psutil.cpu_freq()
        freqcurrent = cpufreq.current
        freqmax = cpufreq.max
    except:
        freqcurrent = "N/A"
        freqmax = "N/A"

    try:
        # Cores
        cores = psutil.cpu_count(logical=False)
        lcores = psutil.cpu_count()
    except:
        cores = "N/A"
        lcores = "N/A"

    try:
        cpupercent = psutil.cpu_percent()
    except:
        cpupercent = "N/A"

    try:
        # Storage
        usage = shutil.disk_usage("/")
        totaldsk = Human_Format.human_readable_bytes(usage.total)
        useddsk = Human_Format.human_readable_bytes(usage.used)
        freedsk = Human_Format.human_readable_bytes(usage.free)
    except:
        totaldsk = "N/A"
        useddsk = "N/A"
        freedsk = "N/A"

    try:
        upb, dlb = await get_transfer()
        dlb = Human_Format.human_readable_bytes(dlb)
        upb = Human_Format.human_readable_bytes(upb)
    except:
        dlb = "N/A"
        upb = "N/A"

    diff = time.time() - uptime
    diff = Human_Format.human_readable_timedelta(diff)

    if callbk:
        msg = (
            f"<b><i>ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ...</i></b>"
            f"\n\n"
            f"<b>ʙᴏᴛ ᴜᴘᴛɪᴍᴇ:</b> {diff}\n\n"
            "<b><i>ᴄᴘᴜ ꜱᴛᴀᴛꜱ...</i></b>\n"
            f"**ᴄᴏʀᴇꜱ:** {cores} ʟᴏɢɪᴄᴀʟ: {lcores}\n"
            f"**ᴄᴘᴜ ꜰʀᴇQᴜᴇɴᴄʏ:** {freqcurrent}  **ᴍʜᴢ ᴍᴀx:** {freqmax}\n"
            f"**ᴄᴘᴜ ᴜᴛɪʟɪᴢᴀᴛɪᴏɴ:** {cpupercent}%\n"
            "\n"
            "<b><i>ꜱᴛᴏʀᴀɢᴇ ꜱᴛᴀᴛꜱ...</i></b>\n"
            f"**ᴛᴏᴛᴀʟ:** {totaldsk}\n"
            f"**ᴜꜱᴇᴅ:** {useddsk}\n"
            f"**ꜰʀᴇᴇ:** {freedsk}\n"
            "\n"
            "<b><i>ᴍᴇᴍᴏʀʏ ꜱᴛᴀᴛꜱ...</i></b>\n"
            f"**ᴀᴠᴀɪʟᴀʙʟᴇ:** {memavailable}\n"
            f"**ᴛᴏᴛᴀʟ:** {memtotal}\n"
            f"**ᴜꜱᴇᴅ:** {mempercent}%\n"
            f"**ꜰʀᴇᴇ:** {memfree}\n"
            "\n"
            "<b><i>ᴛʀᴀɴꜱꜰᴇʀ ɪɴꜰᴏ...</i></b>\n"
            f"**ᴅᴏᴡɴʟᴏᴀᴅ:** {dlb}\n"
            f"**ᴜᴘʟᴏᴀᴅ:** {upb}\n"
        )
        await message.edit(msg, parse_mode="html", buttons=None)
    else:
        try:
            storage_percent = round((usage.used / usage.total) * 100, 2)
        except:
            storage_percent = 0

        msg = (
            f"<b><i>ʙᴏᴛ ꜱᴇʀᴠᴇʀ...</i></b>"
            f"\n\n"
            f"ʙᴏᴛ ᴜᴘᴛɪᴍᴇ: {diff}\n\n"
            f"ᴄᴘᴜ ᴜᴛɪʟɪᴢᴀᴛɪᴏɴ: {progress_bar(cpupercent)} - {cpupercent}%\n\n"
            f"ꜱᴛᴏʀᴀɢᴇ ᴜꜱᴇᴅ: {progress_bar(storage_percent)} - {storage_percent}%\n"
            f"ᴛᴏᴛᴀʟ: {totaldsk} ꜰʀᴇᴇ: {freedsk}\n\n"
            f"ᴍᴇᴍᴏʀʏ ᴜꜱᴇᴅ: {progress_bar(mempercent)} - {mempercent}%\n"
            f"ᴛᴏᴛᴀʟ: {memtotal} ꜰʀᴇᴇ: {memfree}\n\n"
            f"ᴛʀᴀɴꜱꜰᴇʀ ᴅᴏᴡɴʟᴏᴀᴅ: {dlb}\n"
            f"ᴛʀᴀɴꜱꜰᴇʀ ᴜᴘʟᴏᴀᴅ: {upb}\n"
        )
        await message.reply(
            msg,
            parse_mode="html",
            buttons=[[KeyboardButtonCallback("ɢᴇᴛ ᴅᴇᴛᴀɪʟᴇᴅ ꜱᴛᴀᴛᴜꜱ", "fullserver")]],
        )


async def about_me(message):
    db = var_db
    _, val1 = db.get_variable("RCLONE_CONFIG")
    if val1 is None:
        rclone_cfg = "No Rclone Config is loaded."
    else:
        rclone_cfg = "Rclone Config is loaded"

    val1 = get_val("RCLONE_ENABLED")
    if val1 is not None:
        if val1:
            rclone = "Rclone enabled by admin."
        else:
            rclone = "Rclone disabled by admin."
    else:
        rclone = "N/A"

    val1 = get_val("LEECH_ENABLED")
    if val1 is not None:
        if val1:
            leen = "⚠️Leech command enabled."
        else:
            leen = "⚠️Leech command disabled."
    else:
        leen = "N/A"

    diff = time.time() - uptime
    diff = Human_Format.human_readable_timedelta(diff)

    msg = (
        "<b>Name</b>: <code>TorToolkitX-Heroku</code>\n"
        f"<b>Version</b>: <code>{__version__}</code>\n"
        f"<b>Telethon Version</b>: {telever}\n"
        f"<b>Pyrogram Version</b>: {pyrover}\n"
        "<b>Created By</b>: @Yaknight\n\n"
        "<b>Modified By</b>: @XcodersHub\n\n"
        "<u>Currents Configs:-</u>\n\n"
        f"<b>Bot Uptime:-</b> {diff}\n"
        "<b>Torrent Download Engine:-</b> <code>qBittorrent [4.3.0 fix active]</code> \n"
        "<b>Direct Link Download Engine:-</b> <code>aria2</code> \n"
        "<b>Upload Engine:-</b> <code>RCLONE</code> \n"
        "<b>Youtube Download Engine:-</b> <code>yt-dlp</code>\n"
        f"<b>Rclone config:- </b> <code>{rclone_cfg}</code>\n"
        f"<b>Leech:- </b> <code>{leen}</code>\n"
        f"<b>Rclone:- </b> <code>{rclone}</code>\n"
        "\n"
        f"<b>Latest {__version__} Changelog :- </b>\n"
        "1.DB Optimizations.\n"
        "2.Database handling on disconnections..\n"
        "3.Support for ARM devices.\n"
        "4.Gdrive Support for PYTDL and YTDL\n"
        "5.Upload YT Playlist even when some vids are errored.\n"
        "6.Changed /server menu. Add /speedtest\n"
        "7.Minor fixes.\n"
        "8.Deploy takes less then 2 mins now.\n"
        "9.MegaDL added.\n"
        "10.Overall download and upload progress.\n"
        "11.Pixeldrain DL support.\n"
        "12.Alert on when the bot boots up.\n"
        "<b>13.Fixed Heroku Stuff.</b>\n"
    )

    await message.reply(msg, parse_mode="html")


async def set_thumb_cmd(e):
    thumb_msg = await e.get_reply_message()
    if thumb_msg is None:
        await e.reply("🥱𝚁𝚎𝚙𝚕𝚢 𝚝𝚘 𝚊 𝚙𝚑𝚘𝚝𝚘 𝚘𝚛 𝚙𝚑𝚘𝚝𝚘 𝚊𝚜 𝚊 𝚍𝚘𝚌𝚞𝚖𝚎𝚗𝚝.")
        return

    if thumb_msg.document is not None or thumb_msg.photo is not None:
        value = await thumb_msg.download_media()
    else:
        await e.reply("🥱𝚁𝚎𝚙𝚕𝚢 𝚝𝚘 𝚊 𝚙𝚑𝚘𝚝𝚘 𝚘𝚛 𝚙𝚑𝚘𝚝𝚘 𝚊𝚜 𝚊 𝚍𝚘𝚌𝚞𝚖𝚎𝚗𝚝.")
        return

    try:
        im = Image.open(value)
        im.convert("RGB").save(value, "JPEG")
        im = Image.open(value)
        im.thumbnail((320, 320), Image.ANTIALIAS)
        im.save(value, "JPEG")
        with open(value, "rb") as fi:
            data = fi.read()
            user_db.set_thumbnail(data, e.sender_id)
        os.remove(value)
    except Exception:
        torlog.exception("Set Thumb")
        await e.reply("𝙴𝚛𝚛𝚘𝚛𝚎𝚍 𝚒𝚗 𝚜𝚎𝚝𝚝𝚒𝚗𝚐 𝚝𝚑𝚞𝚖𝚋𝚗𝚊𝚒𝚕.")
        return

    try:
        os.remove(value)
    except:
        pass

    user_db.set_var("DISABLE_THUMBNAIL", False, str(e.sender_id))
    await e.reply(
        "𝚃𝚑𝚞𝚖𝚋𝚗𝚊𝚒𝚕 𝚜𝚎𝚝. 𝚝𝚛𝚢 𝚞𝚜𝚒𝚗𝚐 /𝚞𝚜𝚎𝚝𝚝𝚒𝚗𝚐𝚜 𝚝𝚘 𝚐𝚎𝚝 𝚖𝚘𝚛𝚎 𝚌𝚘𝚗𝚝𝚛𝚘𝚕."
    )


async def clear_thumb_cmd(e):
    user_db.set_var("DISABLE_THUMBNAIL", True, str(e.sender_id))
    await e.reply(
        "𝚃𝚑𝚞𝚖𝚋𝚗𝚊𝚒𝚕 𝚍𝚒𝚜𝚊𝚋𝚕𝚎𝚍. 𝚃𝚛𝚢 𝚞𝚜𝚒𝚗𝚐 /𝚞𝚜𝚎𝚝𝚝𝚒𝚗𝚐𝚜 𝚝𝚘 𝚐𝚎𝚝 𝚖𝚘𝚛𝚎 𝚌𝚘𝚗𝚝𝚛𝚘𝚕."
    )


async def handle_user_settings_(message):
    if not message.sender_id in get_val("ALD_USR"):
        if not get_val("USETTINGS_IN_PRIVATE") and message.is_private:
            return

    await handle_user_settings(message)
    await message.delete()


def term_handler(signum, frame, client):
    torlog.info("TERM RECEIVD")

    async def term_async():
        omess = None
        st = Status().Tasks
        msg = "Bot Rebooting Re Add your Tasks\n\n"
        for i in st:
            if not await i.is_active():
                continue

            omess = await i.get_original_message()
            if str(omess.chat_id).startswith("-100"):
                chat_id = str(omess.chat_id)[4:]
                chat_id = int(chat_id)
            else:
                chat_id = omess.chat_id

            sender = await i.get_sender_id()
            msg += f"<a href='tg://user?id={sender}'>REBOOT</a> - <a href='https://t.me/c/{chat_id}/{omess.id}'>Task</a>\n"

        if omess is not None:
            await omess.respond(msg, parse_mode="html")
        exit(0)

    client.loop.run_until_complete(term_async())


async def booted(client):
    chats = get_val("ALD_USR")
    for i in chats:
        try:
            await client.send_message(i, "𝙶𝚞𝚢𝚜 𝙸 𝙰𝚖 𝚁𝚎𝚊𝚍𝚢 𝚃𝚘 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐...")
        except Exception:
            torlog.info(f"Not found the entity {i}")


def command_process(command):
    return re.compile(command, re.IGNORECASE)
