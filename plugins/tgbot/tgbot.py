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

import telebot
             
def get_tg_chid(gtitle):
    cid = get_client_id()
    
    gtitle = gtitle.replace('&quot;', '"')

    sql = "SELECT id FROM tgchatids WHERE gname='%s';" % (gtitle)
    qres = sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)
    
    if qres:
        return qres[0][0]
    return False

def get_tg_usrid(fnme):
    cid = get_client_id()
    
    fnme = fnme.replace('&quot;', '"')

    sql = "SELECT id FROM tguserids WHERE fname='%s';" % (fnme.strip())
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
    
    if qres:
        return qres[0][0]
    return False

def get_tg_fnme(usrid):
    cid = get_client_id()
    
    if type(usrid) != int:
        return False 

    sql = "SELECT fname FROM tguserids WHERE id='%s';" % (usrid)
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
    
    if qres:
        return qres[0][0]
    return False

def get_tg_usrn(usrid):
    cid = get_client_id()
    
    if type(usrid) != int:
        return False 

    sql = "SELECT usrn FROM tguserids WHERE id='%s';" % (usrid)
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
    
    if qres:
        return qres[0][0]
    return False

def set_tg_usrid(usrid, fnme, usrn=''):
    cid = get_client_id()
    
    if type(usrid) != int:
        return False 
    
    fnme = fnme.replace('"', '&quot;')
    
    if usrn:
        usrn = usrn.replace('"', '&quot;')
    else:
        usrn = ''
    
    if not usrid_exists(usrid):
        if usrn:
            sql = "INSERT INTO tguserids (id, fname, usrn) VALUES ('%s', '%s', '%s');" % (usrid, fnme.strip(), usrn.strip())
        else:
            sql = "INSERT INTO tguserids (id, fname) VALUES ('%s', '%s');" % (usrid, fnme.strip())
    else:
        if usrn:
            sql = "UPDATE tguserids SET \"fname\"='%s', \"usrn\"='%s' WHERE \"id\"='%s';" % (fnme.strip(), usrn.strip(), usrid)
        else:
            sql = "UPDATE tguserids SET \"fname\"='%s' WHERE \"id\"='%s';" % (fnme.strip(), usrid)
    
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
    
    if qres != '':
        return True
    return False

def get_tg_usr_acc(usrid):
    cid = get_client_id()
    
    if type(usrid) != int:
        return False 
    
    if usrid_exists(usrid):
        sql = "SELECT acc FROM tguserids WHERE \"id\"='%s';" % (usrid)
    
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
    
    if qres:
        return qres[0][0]
    return False

def set_tg_usr_acc(usrid, acc):
    cid = get_client_id()
    
    if (type(usrid) != int) or (type(acc) != int):
        return False 
    
    if usrid_exists(usrid):
        sql = "UPDATE tguserids SET \"acc\"='%s' WHERE \"id\"='%s';" % (acc, usrid)
    
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
    
    return qres

def usrid_exists(usrid):
    cid = get_client_id()
    
    if type(usrid) != int:
        return False 

    sql = "SELECT * FROM tguserids WHERE id='%s';" % (usrid)
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
    
    if qres:
        return True
    return False

def chid_exists(chid):
    cid = get_client_id()
    
    if type(chid) != int:
        return False 

    sql = "SELECT * FROM tgchatids WHERE id='%s';" % (chid)
    qres = sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)
    
    if qres:
        return True
    return False

def rmv_tg_usrid(usrid):
    cid = get_client_id()
    
    if type(usrid) != int:
        return False 
    
    if usrid_exists(usrid):
        sql = 'DELETE FROM tgusrids WHERE id="%s";' % (usrid)
   
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
    
    return qres

def rmv_tg_chid(chid):
    cid = get_client_id()
    
    if type(chid) != int:
        return False 
    
    if chid_exists(chid):
        sql = 'DELETE FROM tgchatids WHERE id="%s";' % (chid)
   
    qres = sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)
    
    return qres

def set_tg_chid(chid, gtitle):
    cid = get_client_id()
    
    if type(chid) != int:
        return False 
    
    gtitle = gtitle.replace('"', '&quot;')
    
    if not chid_exists(chid):
        sql = "INSERT INTO tgchatids (id, gname) VALUES ('%s', '%s');" % (chid, gtitle.strip())
    else:
        sql = "UPDATE tgchatids SET \"gname\"='%s' WHERE \"id\"='%s';" % (gtitle.strip(), chid)
    
    qres = sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)
    
    if qres != '':
        return True
    return False

def handler_tgaccess(message):
    if (time.time() - message.date) > 8:
        return
    
    cid = get_client_id()
    
    tbot = get_fatal_var(cid, 'tgbot')
    
    accdesc = {'-100': l('(full ignoring)'), '-1': l('(blocked)'), \
        '0': l('(none)'), '1': l('(low user)'), '10': l('(user)'), \
        '11': l('(member)'), '15': l('(moderator)'), '16': l('(moderator)'),\
        '20': l('(admin)'), '30': l('(owner)'), '40': l('(joiner)'), \
        '100': l('(suderadmin)')}
    
    usrid = message.from_user.id
    chid = message.chat.id
    
    command = message.text.split()[0]
    
    parameters = message.text.replace(command, '') 
    
    if not parameters:
        level = get_tg_usr_acc(usrid)
        
        levdesc = accdesc[str(level)]
        
        tbot.reply_to(message, '%s %s' % (level, levdesc))
    else:
        parameters = parameters.strip()
        
        if parameters.startswith('@'):
            parameters = parameters.replace('@', '')
        
        usridb = get_tg_usrid(parameters)
        
        if usridb:
            level = get_tg_usr_acc(int(usridb))
            
            levdesc = accdesc[str(level)]
            
            tbot.reply_to(message, '%s %s' % (level, levdesc))
        else:
            tbot.reply_to(message, l('Not found!'))    

def handler_tgaccess_jcmd(type, source, parameters):
    reply(type, source, l('This command you can only use in Telegram!'))

def handle_photo_content(message):
    cid = get_client_id()
    
    tbot = get_fatal_var(cid, 'tgbot')
    
    if message.chat.type == 'private':
        photo_id = message.photo[-1].file_id
        
        file_url = tbot.get_file_url(photo_id)
       
        tbot.reply_to(message, file_url)
        
def handle_video_content(message):
    cid = get_client_id()
    
    tbot = get_fatal_var(cid, 'tgbot')
        
    if message.chat.type == 'private':
        video_id = message.video.file_id
        
        file_url = tbot.get_file_url(video_id)
       
        tbot.reply_to(message, file_url)

def command_messages(message):
    if (time.time() - message.date) > 8:
        return

    cid = get_client_id()
    tbot = get_fatal_var(cid, 'tgbot')
    
    fbdn_cmds = ['access']
    
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
        
        if wprname in fbdn_cmds:
            tbot.reply_to(message, l('This command you can only use in jabber! Use /tgaccess for this function!'))
            return
        
        real_access = get_int_fatal_var('commands', wprname, 'access')
        usracc = int(get_tg_usr_acc(usrid))
        
        if usracc >= real_access:
            cparams = message.text.replace(cmdname, '') 
                           
            comm_hnd = get_fatal_var('command_handlers', wprname)

            if comm_hnd:
                comm_hnd('telegram', ['', '', ''], cparams.strip())
            else:
                tbot.reply_to(message, l('Unknown command!'))
        else:
            tbot.reply_to(message, l('Too few rights!'))   
    else:
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', 'telegram')):
            set_fatal_var(cid, 'tgm_grp_chid', message.chat.id)
            
            rep = '[%s]<%s> %s' % (message.chat.title, fname, message.text)
            
            if is_var_set(cid, 'watchers', 'telegram', 'gchs'):
                wgchs = list(get_dict_fatal_var(cid, 'watchers', 'telegram', 'gchs'))
                
                for wgch in wgchs:
                    msg(wgch, rep)    

def tgm_polling_proc():
    cid = get_client_id()
    tbot = get_fatal_var(cid, 'tgbot')
    
    try:
        tbot.infinity_polling(interval=0, timeout=3)
    except Exception:
        log_exc_error()     

def init_tgm_bot():
    cid = get_client_id()
  
    if not is_var_set(cid, 'tgbot'):
        bot_api_token = get_cfg_param('tgbot_api_token')

        tbot = telebot.TeleBot(bot_api_token)
        
        set_fatal_var(cid, 'tgbot', tbot)
        
        tbot.register_message_handler(handler_tgaccess, commands=['tgaccess'])
        tbot.register_message_handler(command_messages, content_types=['text'])
        tbot.register_message_handler(handle_photo_content, content_types=['photo'])
        tbot.register_message_handler(handle_video_content, content_types=['video'])
        
        call_in_sep_thr(cid + '/init_tgm_bot', tgm_polling_proc) 
        
def create_tg_tables():
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/tguserids.db' % (cid)):
        sql = '''CREATE TABLE tguserids (idn INTEGER PRIMARY KEY AUTOINCREMENT,
            id VARCHAR(30) NOT NULL, fname VARCHAR(30) NOT NULL, usrn VARCHAR(30) DEFAULT "",
            acc INTEGER NOT NULL DEFAULT 10, UNIQUE (id));''' 
        
        sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX itguserids ON tguserids (idn);'
        sqlquery('dynamic/%s/tguserids.db' % (cid), sql) 

    if not is_db_exists('dynamic/%s/tgchatids.db' % (cid)):
        sql = '''CREATE TABLE tgchatids (idn INTEGER PRIMARY KEY AUTOINCREMENT,
            id VARCHAR(30) NOT NULL, gname VARCHAR(30) NOT NULL, UNIQUE (id));'''
        sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX itgchatids ON tgchatids (idn);'
        sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)

if is_param_set('tgbot_api_token'):
    register_command_handler(handler_tgaccess_jcmd, 'tgaccess', 10)

    register_stage0_init(create_tg_tables)
    register_stage0_init(init_tgm_bot)