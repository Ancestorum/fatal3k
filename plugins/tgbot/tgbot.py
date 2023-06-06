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

from fatalapi import *

import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
             
_bot_api_token = get_cfg_param('tgbot_api_token')

tbot = telebot.TeleBot(_bot_api_token)
atbot = AsyncTeleBot(_bot_api_token)

def handler_tgaccess(type, source, parameters):
    cid = get_client_id()
    
    accdesc = {'-100': l('(full ignoring)'), '-1': l('(blocked)'), \
        '0': l('(none)'), '1': l('(low user)'), '10': l('(user)'), \
        '11': l('(member)'), '15': l('(moderator)'), '16': l('(moderator)'),\
        '20': l('(admin)'), '30': l('(owner)'), '40': l('(joiner)'), \
        '100': l('(suderadmin)')}
    
    lmsg = get_fatal_var(cid, 'last_tg_msg')
    usrid = lmsg.from_user.id
    chid = lmsg.chat.id
    
    if not parameters:
        level = get_tg_usr_acc(usrid)
        
        levdesc = accdesc[str(level)]
        
        tbot.reply_to(lmsg, '%s %s' % (level, levdesc))
    else:
        parameters = parameters.strip()
        
        if parameters.startswith('@'):
            parameters = parameters.replace('@', '')
        
        usridb = get_tg_usrid(parameters)
        
        if usridb:
            level = get_tg_usr_acc(int(usridb))
            
            levdesc = accdesc[str(level)]
            
            tbot.reply_to(lmsg, '%s %s' % (level, levdesc))
        else:
            tbot.reply_to(lmsg, l('Not found!'))    

@atbot.message_handler(content_types=['photo'])
async def handle_photo_content(message):
    if message.chat.type == 'private':
        photo_id = message.photo[-1].file_id
        
        file_url = await atbot.get_file_url(photo_id)
       
        await atbot.reply_to(message, file_url)
        
@atbot.message_handler(content_types=['video'])
async def handle_video_content(message):
    if message.chat.type == 'private':
        video_id = message.video.file_id
        
        file_url = await atbot.get_file_url(video_id)
       
        await atbot.reply_to(message, file_url)

@atbot.message_handler(content_types=['text'])
async def command_messages(message):
    if (time.time() - message.date) > 8:
        return
    
    cid = get_client_id()
    mchat = message.chat.type
    usrid = message.from_user.id
    fname = message.from_user.first_name
    usern = message.from_user.username 
    
    if not usrid_exists(usrid):
        if set_tg_usrid(usrid, fname, usern):
            badm = get_int_cfg_param('tgbot_admin_id')
           
            if usrid == badm:
                set_tg_usr_acc(usrid, 100)
    else:
        dfnme = get_tg_fnme(usrid)
        dusrn = get_tg_usrn(usrid)
        
        if (dfnme != fname) or (dusrn != usern):
            set_tg_usrid(usrid, fname, usern)
        
    if (mchat == 'group') or (mchat == 'supergroup'):
        if not chid_exists(message.chat.id): 
            set_tg_chid(message.chat.id, message.chat.title)
    
    set_fatal_var(cid, 'last_tg_msg', message)
    
    if not is_var_set(cid, 'tgm_grp_chid'):
        if is_param_set('tgm_chat_id'):
            pchid = get_int_cfg_param('tgm_chat_id')
            set_fatal_var(cid, 'tgm_grp_chid', pchid)
    
    if message.text.startswith('/'):
        cmdname = message.text.split()[0]
        wprname = cmdname.replace('/','').strip()
        
        real_access = get_int_fatal_var('commands', wprname, 'access')
        usracc = int(get_tg_usr_acc(usrid))
        
        if usracc >= real_access:
            cparams = message.text.replace(cmdname, '') 
                           
            comm_hnd = get_fatal_var('command_handlers', wprname)

            if comm_hnd:
                comm_hnd('telegram', ['', '', ''], cparams.strip())
            else:
                await atbot.reply_to(message, l('Unknown command!'))
        else:
            await atbot.reply_to(message, l('Too few rights!'))   
    else:
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', 'telegram')):
            set_fatal_var(cid, 'tgm_grp_chid', message.chat.id)
            
            rep = '[%s]<%s> %s' % (message.chat.title, fname, message.text)
            
            if is_var_set(cid, 'watchers', 'telegram', 'gchs'):
                wgchs = list(get_dict_fatal_var(cid, 'watchers', 'telegram', 'gchs'))
                
                for wgch in wgchs:
                    msg(wgch, rep)    

def polling_proc():
    try:
        while True:
            asyncio.run(atbot.polling())

            time.sleep(10)
    except Exception:
        pass      

def start_tgm_polling():
    cid = get_client_id()
    
    set_fatal_var(cid, 'tgbot', tbot)
    
    call_in_sep_thr(cid + '/tbot_polling', polling_proc) 

def create_tg_chids_table():
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/tgchatids.db' % (cid)):
        sql = '''CREATE TABLE tgchatids (idn INTEGER PRIMARY KEY AUTOINCREMENT,
            id VARCHAR(30) NOT NULL, gname VARCHAR(30) NOT NULL, UNIQUE (id));'''
        sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX itgchatids ON tgchatids (idn);'
        sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)
        
def create_tg_usrids_table():
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/tguserids.db' % (cid)):
        sql = '''CREATE TABLE tguserids (idn INTEGER PRIMARY KEY AUTOINCREMENT,
            id VARCHAR(30) NOT NULL, fname VARCHAR(30) NOT NULL, usrn VARCHAR(30) DEFAULT "",
            acc INTEGER NOT NULL DEFAULT 10, UNIQUE (id));''' 
        
        sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX itguserids ON tguserids (idn);'
        sqlquery('dynamic/%s/tguserids.db' % (cid), sql)    

register_command_handler(handler_tgaccess, 'tgaccess', 10)

register_stage0_init(create_tg_usrids_table)
register_stage0_init(create_tg_chids_table)
register_stage0_init(start_tgm_polling)