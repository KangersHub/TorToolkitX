# -*- coding: utf-8 -*-
# (c) YashDK [yash-dk@github]
# (c) modified by AmirulAndalib [amirulandalib@github]

import logging
import traceback

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
)

from ..core.getVars import get_val

torlog = logging.getLogger(__name__)

# todo add alpha admin if needed


async def is_admin(client, user_id, chat_id, force_owner=False):
    if force_owner:
        return user_id == get_val("OWNER_ID")
    try:
        res = await client(GetParticipantRequest(channel=chat_id, user_id=user_id))

        try:
            if isinstance(
                res.participant,
                (
                    ChannelParticipantAdmin,
                    ChannelParticipantCreator,
                    ChannelParticipantsAdmins,
                ),
            ):
                return True
            else:

                return user_id in get_val("ALD_USR")
        except:
            torlog.info("Bot Accessed in Private {}".format(traceback.format_exc()))
            return False
    except Exception as e:
        torlog.info("Bot Accessed in Private {}".format(e))
        return user_id in get_val("ALD_USR")
