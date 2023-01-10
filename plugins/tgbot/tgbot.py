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

set_fatal_var('tgbot', tbot)

def handler_tbot(type, source, parameters):
    if parameters:
        tbot.send_message(_chat_id, parameters)
        
        return reply(type, source, l('Sent!'))
    else:
        return reply(type, source, 'Invalid syntax!')

@atbot.message_handler(content_types=['text'])
async def command_messages(message):
    set_fatal_var('last_tg_msg', message)
    
    if message.text.startswith('/'):
        cmdname = message.text.split()[0]
        wprname = cmdname.replace('/','')
        cparams = message.text.replace(cmdname, '') 
                       
        comm_hnd = get_fatal_var('command_handlers', wprname)

        if comm_hnd:
            comm_hnd('telegram', ['', '', ''], cparams)
        else:
            await atbot.reply_to(message, l('Unknown command!'))
    else:
        cid = get_client_id()
        
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', 'telegram')):
            rep = '[%s]<%s> %s' % (message.chat.title, message.from_user.first_name, message.text)
            
            if is_var_set(cid, 'watchers', 'telegram', 'gchs'):
                wgchs = list(get_dict_fatal_var(cid, 'watchers', 'telegram', 'gchs'))
                
                for wgch in wgchs:
                    msg(wgch, rep)    

def polling_proc():
    while True:
        asyncio.run(atbot.polling())        
        time.sleep(10)

cid = get_cfg_param('jid')

call_in_sep_thr(cid + '/tbot_polling', polling_proc) 

register_command_handler(handler_tbot, 'tgsend', 100)

