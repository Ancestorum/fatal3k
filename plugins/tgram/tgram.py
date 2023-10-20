# -*- coding: utf-8 -*-

#  fatal plugin
#  tgram plugin

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
from telethon import TelegramClient, events

from telethon.errors import SessionPasswordNeededError, PhoneCodeExpiredError, \
                            PasswordHashInvalidError, PhoneCodeEmptyError, \
                            PhoneCodeHashEmptyError, PhoneCodeInvalidError
                            
import telethon.utils as utils

import asyncio

def tgram_send_msg(eid, msg):
    client = cgv('tgram_client')
    coro = client.send_message(eid, msg)
    craiot(coro)

async def new_message_handler(event):
    user_id = get_int_cfg_param('tgram_user_id')
    
    log_null_cmdr(event.stringify() + '\n\n', 'syslogs/tgevn.log')
    
    csv('tgram_last_event', event)
    
    try:
        if event.sender_id == user_id and event.is_private:
            csv('tgram_fav_event', event)
            log_null_cmdr(event.text + '\n', 'syslogs/tgfav.log')
            #await client.download_media(event.message.media, 'dynamic/files')
    except Exception:
        log_exc_error()

async def album_handler(event):
    pass
    #Printing the caption
    #print(event.text)
    
    #Counting how many photos or videos the album has
    #print('Got an album with', len(event), 'items')
    #print(event[0].message)

def tgram_signin_code(type, source, parameters):
    groupchat = source[1]
    code = parameters.strip()
    
    if is_groupchat(groupchat):
        return reply(type, source, l('This command can not be used in groupchat!'))
    
    if not code or not code.isdigit():
        return reply(type, source, l('Invalid syntax!'))
    
    if not is_event_init('tgram_code_event'):
        return reply(type, source, l('This code already has been entered or expired!'))
    
    csv('tgram_signin_code', code)
    set_fatal_event('tgram_code_event')

def init_tgram_handlers():
    client = cgv('tgram_client')
    
    client.add_event_handler(new_message_handler, events.NewMessage)
    client.add_event_handler(album_handler, events.Album)

def tgram_polling_proc():
    asyncio.run(tgram_start())

async def tgram_start():
    api_id = get_int_cfg_param('tgram_api_id')
    api_hash = get_cfg_param('tgram_api_hash')
    phone = get_cfg_param('tgram_phone')
    
    client = TelegramClient(d('fatal3k'), api_id, api_hash, system_version='5.15.90', app_version='3.0')
    
    csv('tgram_client', client)

    init_tgram_handlers()

    try:
        await client.connect()
    except IOError:
        await client.connect()

    if not await client.is_user_authorized():
        await client.sign_in(phone)

        self_user = None
        
        isaent = False
        repent = None
        
        admin = ''
        
        admins = get_lst_cfg_param('admins')

        if admins:
            admin = admins[0]
        
        if is_param_set('tgbot_api_token') and iscvs('tgbot') and is_param_set('tgbot_admin_id'):
            mess = l('In order to sign in Telegram client you have to enter secret code! To enter code use command /tgcode.')
            userid = get_int_cfg_param('tgbot_admin_id')
            repent = lambda m: msg('telegram', m, userid)
            repent(mess)
            isaent = True
        elif is_ruser_prsnt(admin):
            prefix = get_cfg_param('comm_prefix')
            mess = l('In order to sign in Telegram client you have to enter secret code! To enter code use command %stgcode.') % (prefix)
            repent = lambda m: msg(admin, m)
            repent(mess)
            isaent = True
        elif is_param_seti('show_console'):
            prompt = get_fatal_var('con_last_prompt') 
            repent = lambda m: msg('console', m)
                        
            if not is_var_set('is_console_hide'):
                mess = l('In order to sign in Telegram client you have to enter secret code! To enter code use command tgcode.')
                repent(mess)
                
                if prompt:
                    sys.stdout.write('\n' + prompt)
                    sys.stdout.flush()
            else:
                os_uname = get_os_uname()
                
                if os_uname:
                    mess = l('Please press Ctrl+D and enter secret code using tgcode command.')
                else:
                    mess = l('Please press Ctrl+Z and Return to enter secret code using tgcode command.')
                
                repent(mess)
                
            isaent = True
        
        tries = 0
        tret = ''
        
        while self_user is None:
            tries +=+ 1
            
            if tries > 1:
                tret = '\n\n'
            
            if not isaent: 
                print(tret + 'Telegram client signing in. Sending code request...')
                code = input('\nEnter the code you just received (%s): ' % (tries))
                repent = lambda m: msg('console', m)
            else:
                iawt_fatal_event('tgram_code_event')
                code = cgv('tgram_signin_code')
                
            try:
                self_user = await client.sign_in(code=code)
            except PhoneCodeExpiredError:
                mess = l('It seems that the secret code you provided is expired!')
                repent(mess)
            except SessionPasswordNeededError:
                if is_param_set('tgram_password'):
                    password = get_cfg_param('tgram_password')
                    try:
                        self_user = await client.sign_in(password=password)
                    except PasswordHashInvalidError:
                        mess = l('Password is invalid! Provide right password!')
                        repent(mess)
                else:
                    mess = l('Password is required to sign in! Provide it through "tgram_password" param in fatal.conf')
                    repent(mess)
            except (PhoneCodeEmptyError, PhoneCodeHashEmptyError, PhoneCodeInvalidError):
                mess = l('Invalid code! Please try again!')
                repent(mess)
        
        mess = l('Signed in successfully as %s!') % (utils.get_display_name(self_user))
        
        repent(mess)
        
        await client.send_message('me', mess)
    
    csv('tgram_loop', client.loop)
    
    await client.run_until_disconnected()

def init_tgram_client():
    cid = get_client_id()
    
    if not iscvs('tgram_client'):
        if is_param_set('tgram_api_id'):
            call_in_sep_thr(cid + '/init_tgram_client', tgram_polling_proc)

register_command_handler(tgram_signin_code, 'tgcode', 100)
register_stage2_init(init_tgram_client)
