# -*- coding: utf-8 -*-

#  fatal plugin
#  tgbot plugin

#  Copyright © 2023 Ancestors Soft

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

__all__ = []

from fatalapi import *

import telebot
from telebot.async_telebot import AsyncTeleBot
import asyncio

_bot_api_token = get_cfg_param('bot_api_token')
_chat_id = get_int_cfg_param('tgm_chat_id')

tbot = telebot.TeleBot(_bot_api_token)
atbot = AsyncTeleBot(_bot_api_token)

def handler_tbot(type, source, parameters):
    if parameters:
        tbot.send_message(_chat_id, parameters)
        
        return reply(type, source, l('Sent!'))
    else:
        return reply(type, source, 'Invalid syntax!')

@atbot.message_handler(content_types=['text'])
async def get_text_messages(message):
    cmdname = message.text.split()[0]
    cparams = message.text.replace(cmdname, '') 
    
    comm_hnd = get_fatal_var('command_handlers', cmdname)
    
    jdres = get_cfg_param('admins')
    
    bjid = get_cfg_param('jid')
    
    dest_source = [bjid, '', '']

    if comm_hnd:
        await atbot.reply_to(message, comm_hnd('console', dest_source, cparams))
    else:
        await atbot.reply_to(message, l('Unknown command!'))

def polling_proc():
    while True:
        asyncio.run(atbot.polling())        
        time.sleep(10)

cid = get_cfg_param('jid')

call_in_sep_thr(cid + '/tbot_polling', polling_proc)

register_command_handler(handler_tbot, 'tgsend', 100)

