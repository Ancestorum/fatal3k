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
import requests
from urllib import request
from hashlib import md5, sha256
             
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

def set_tg_usr_acc(usrid, acc):
    cid = get_client_id()
    
    if (type(usrid) != int) or (type(acc) != int):
        return False 
    
    if usrid_exists(usrid):
        sql = "UPDATE tguserids SET \"acc\"='%s' WHERE \"id\"='%s';" % (acc, usrid)
    
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
    
    return qres

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

def saveurl(url, filename):
    try:
        request.urlretrieve(url, filename)
        return True
    except Exception:
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

def save_and_upload(file_url):
    cid = get_client_id()

    try:
        filename = file_url.split('/')[-1]
        
        flsdir = 'dynamic/%s/files' % (cid)
        
        pfilenm = '%s/%s' % (flsdir, filename)
        
        purl = get_cfg_param('tgpost_url')
        user = get_cfg_param('tgpost_user')
        pasw = get_cfg_param('tgpost_pass')
        
        curt = trunc(time.time())
        mins = time.strftime('%M', time.localtime(curt))
        curt = time.strftime('%d.%m.%Y-%H', time.localtime(curt))
        
        user = user + mins + filename
        
        sha256usr = sha256(user.encode())
        sha256usr = sha256usr.hexdigest()

        mins = int(mins)
        
        if mins >= 0 and mins <= 15:
            user = sha256usr[0:16]
        elif mins >= 16 and mins <= 30:
            user = sha256usr[16:32]
        elif mins >= 31 and mins <= 45:
            user = sha256usr[32:48]
        elif mins >= 46 and mins <= 59:
            user = sha256usr[48:64]
        
        pasw = pasw + curt + filename

        md5pass = md5(pasw.encode())
        md5pass = md5pass.hexdigest()
        
        purl = '%s?uhas=%s&phas=%s' % (purl, user, md5pass)

        ext = filename.split('.')[-1]
        
        filename = '%s.%s' % (user, ext)

        if not is_var_set(cid, 'tgm_pen_up_fls'):
            set_fatal_var(cid, 'tgm_pen_up_fls', [])

        pupf = get_fatal_var(cid, 'tgm_pen_up_fls')

        pupf.append(filename)
        
        if not os.path.exists(flsdir):
            os.mkdir(flsdir, 0o755)            
        
        saveurl(file_url, pfilenm)
        
        upfile = open(pfilenm, 'rb')

        resp = requests.post(purl, files = {"file": upfile})

        upfile.close()

        os.remove(pfilenm)
        
        return resp, filename
    except Exception:
        log_exc_error()
        return None, None

def handle_photo_content(message):
    if (time.time() - message.date) > 8:
        return

    cid = get_client_id()
    
    tbot = get_fatal_var(cid, 'tgbot')
    chatid = message.chat.id
    messid = message.message_id
    caption = message.caption
    fname = message.from_user.first_name
    usern = message.from_user.username 
    
    if not is_var_set(cid, 'tgm_msg_buf'):
        set_fatal_var(cid, 'tgm_msg_buf', [])
    
    if message.document:
        file_id = message.document.file_id
    elif message.animation:
        file_id = message.animation.file_id
    else:    
        file_id = message.photo[-1].file_id
    
    file_url = tbot.get_file_url(file_id)
    
    thrn = '%s/save_and_upload' % (cid)
    
    call_in_sep_thr(thrn, save_and_upload, file_url)
    
    time.sleep(0.1)
    
    if message.chat.type == 'private':
        tbot.delete_message(chatid, messid)
        
        pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
        
        filename = pupf[-1]
        pupf.remove(filename)
        
        purl = get_cfg_param('tgurl_prefix')
        rmsg = '%s%s' %(purl, filename)
        ndt = message.date
        
        tgmb = get_fatal_var(cid, 'tgm_msg_buf')
        
        thrn = '%s/tgm_msg_handler' % (cid)

        if tgmb:
            tgmb.append((ndt, rmsg))
            
            mtime = time.time()
            set_fatal_var(cid, 'tgm_mtime', mtime)
            
            if not is_thr_exists(thrn):
                call_in_sep_thr(thrn, msg_worker, message)
        else:
            tgmb.append((ndt, rmsg))
           
            mtime = time.time()
            set_fatal_var(cid, 'tgm_mtime', mtime)

            if not is_thr_exists(thrn):
                call_in_sep_thr(thrn, msg_worker, message)
    else:
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', 'telegram')):
            pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
            
            filename = pupf[-1]
            pupf.remove(filename)
            
            purl = get_cfg_param('tgurl_prefix')
            rmsg = '%s%s' %(purl, filename)
            ndt = message.date
            
            tgmb = get_fatal_var(cid, 'tgm_msg_buf')
            
            thrn = '%s/tgm_msg_handler' % (cid)

            if tgmb:
                tgmb.append((ndt, caption, rmsg))
                
                mtime = round(time.time(), 2)
                set_fatal_var(cid, 'tgm_mtime', mtime)
                
                if not is_thr_exists(thrn):
                    call_in_sep_thr(thrn, msg_worker, message, True)
            else:
                tgmb.append((ndt, caption, rmsg))
               
                mtime = round(time.time(), 2)
                set_fatal_var(cid, 'tgm_mtime', mtime)

                if not is_thr_exists(thrn):
                    call_in_sep_thr(thrn, msg_worker, message, True)
                    
def handle_video_content(message):
    if (time.time() - message.date) > 8:
        return
    
    cid = get_client_id()
    
    tbot = get_fatal_var(cid, 'tgbot')
    chatid = message.chat.id
    messid = message.message_id
    caption = message.caption
    fname = message.from_user.first_name
    usern = message.from_user.username

    if not is_var_set(cid, 'tgm_msg_buf'):
        set_fatal_var(cid, 'tgm_msg_buf', [])

    if message.video_note:
        video_id = message.video_note.file_id
    else:
        if message.video.file_size > 20000000:
            video_id = message.video.thumb.file_id
        else:    
            video_id = message.video.file_id    
    
    file_url = tbot.get_file_url(video_id)
    
    thrn = '%s/save_and_upload' % (cid)
    
    call_in_sep_thr(thrn, save_and_upload, file_url)
    
    time.sleep(0.1)
    
    if message.chat.type == 'private':
        tbot.delete_message(chatid, messid)
        
        pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
        
        filename = pupf[-1]
        pupf.remove(filename)
        
        purl = get_cfg_param('tgurl_prefix')
        rmsg = '%s%s' %(purl, filename)
        ndt = message.date
        
        tgmb = get_fatal_var(cid, 'tgm_msg_buf')
        
        thrn = '%s/tgm_msg_handler' % (cid)

        if tgmb:
            tgmb.append((ndt, rmsg))
            
            mtime = round(time.time(), 2)
            set_fatal_var(cid, 'tgm_mtime', mtime)
            
            if not is_thr_exists(thrn):
                call_in_sep_thr(thrn, msg_worker, message)
        else:
            tgmb.append((ndt, rmsg))
           
            mtime = round(time.time(), 2)
            set_fatal_var(cid, 'tgm_mtime', mtime)

            if not is_thr_exists(thrn):
                call_in_sep_thr(thrn, msg_worker, message)
    else:
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', 'telegram')):
            pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
            
            filename = pupf[-1]
            pupf.remove(filename)
            
            purl = get_cfg_param('tgurl_prefix')
            rmsg = '%s%s' %(purl, filename)
            ndt = message.date
            
            tgmb = get_fatal_var(cid, 'tgm_msg_buf')
            
            thrn = '%s/tgm_msg_handler' % (cid)

            if tgmb:
                tgmb.append((ndt, caption, rmsg))
                
                mtime = round(time.time(), 2)
                set_fatal_var(cid, 'tgm_mtime', mtime)
                
                if not is_thr_exists(thrn):
                    call_in_sep_thr(thrn, msg_worker, message, True)
            else:
                tgmb.append((ndt, caption, rmsg))
               
                mtime = round(time.time(), 2)
                set_fatal_var(cid, 'tgm_mtime', mtime)

                if not is_thr_exists(thrn):
                    call_in_sep_thr(thrn, msg_worker, message, True)

def handle_audio_content(message):
    if (time.time() - message.date) > 8:
        return

    cid = get_client_id()
    
    tbot = get_fatal_var(cid, 'tgbot')
    chatid = message.chat.id
    messid = message.message_id
    
    if message.chat.type == 'private':
        if message.audio:
            video_id = message.audio.file_id
        else:
            video_id = message.voice.file_id
        
        file_url = tbot.get_file_url(video_id)
        
        resp, filename = save_and_upload(file_url)
        
        if not resp:
            tbot.send_message(chatid, l('Unknown error!'))
            return

        if resp.text == 'ok': 
            tbot.delete_message(chatid, messid)
            purl = get_cfg_param('tgurl_prefix')
            tbot.send_message(chatid, '%s%s' %(purl, filename))
        else:
            if resp.text: 
                tbot.send_message(chatid, resp.text)
            else:
                tbot.send_message(chatid, l('Unknown error!'))

def command_messages(message):
    if (time.time() - message.date) > 8:
        return

    cid = get_client_id()
    tbot = get_fatal_var(cid, 'tgbot')
    
    fbdn_cmds = ['access']
    
    mchat = message.chat.type
    chatid = message.chat.id
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
    
    if message.text.startswith('/'): 
        cmdname = message.text.split()[0]
        wprname = cmdname.replace('/','').strip()
        
        if wprname in fbdn_cmds:
            tbot.reply_to(message, l('This command you can only use in jabber! Use /tgaccess for this function!'))
            return
        
        real_access = get_int_fatal_var('commands', wprname, 'access')
        usracc = int(get_tg_usr_acc(usrid))
        
        cmdl = get_list_fatal_var('command_handlers')
        
        if wprname in cmdl:
            cparams = message.text.replace(cmdname, '') 
                           
            source = [str(chatid), str(usrid), fname]
            
            call_command_handlers(wprname, 'telegram', source, cparams.strip(), wprname)
        else:
            tbot.reply_to(message, l('Unknown command!'))
    else:
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', 'telegram')):
            url = ''
            
            if message.entities:
                for ment in message.entities:
                    if ment.type == 'text_link':
                        url = ment.url
                        break
            
            if usern and fname != usern:
                rep = '[%s]<%s (@%s)> %s' % (message.chat.title, fname, usern, message.text)
            else:
                rep = '[%s]<%s> %s' % (message.chat.title, fname, message.text)
            
            if url:
                rep += '\n\n%s' % (url)
            
            if is_var_set(cid, 'watchers', 'telegram', 'gchs'):
                wgchs = list(get_dict_fatal_var(cid, 'watchers', 'telegram', 'gchs'))
                
                for wgch in wgchs:
                    msg(wgch, rep)    

def msg_worker(message, public=False):
    cid = get_client_id()
    tbot = get_fatal_var(cid, 'tgbot')
    chatid = message.chat.id
    caption = message.caption
    fname = message.from_user.first_name
    usern = message.from_user.username
    chat_title = message.chat.title
    mult = ''
    cr = ''
        
    while True:
        time.sleep(0.3)
    
        tgmb = get_fatal_var(cid, 'tgm_msg_buf')
        
        if len(tgmb) == 1:
            cr = '\n'
            
            if not public:
                tbot.send_message(chatid, tgmb[-1][-1])
            else:
                rep = tgmb[-1][-1]
            
            set_fatal_var(cid, 'tgm_msg_buf', [])
            set_fatal_var(cid, 'tgm_pen_up_fls', [])
            break
        
        if len(tgmb) > 1:   
            rmsg = ''
            mult = '\n\n'
            
            ltime = round(time.time(), 2)
            mtime = round(get_fatal_var(cid, 'tgm_mtime'), 2)
            
            if ltime - mtime > 1:
                for msg in tgmb:
                    rmsg += msg[-1] + '\n' 
            
                    if not caption:
                        if msg[1]:
                            caption = msg[1]
            
                if not public:
                    tbot.send_message(chatid, rmsg)
                else:
                    rep = rmsg
                
                set_fatal_var(cid, 'tgm_msg_buf', [])
                set_fatal_var(cid, 'tgm_pen_up_fls', [])
                
                break
    
    if not public:
        return

    url = ''
    
    if message.caption_entities:
        for cape in message.caption_entities:
            if cape.type == 'text_link':
                url = cape.url
                break
    
    if usern and fname != usern:
        if caption:
            rep = '[%s]<%s (@%s)> %s%s\n%s%s' % (chat_title, fname, usern, mult, rep, cr, caption)
        else:
            rep = '[%s]<%s (@%s)> %s%s' % (chat_title, fname, usern, mult, rep)
    else:
        if caption:
            rep = '[%s]<%s> %s%s\n%s%s' % (chat_title, fname, mult, rep, cr, caption)
        else:    
            rep = '[%s]<%s> %s%s' % (chat_title, fname, mult, rep)
    
    if url:
        rep += ' (%s)' % (url)
    
    if is_var_set(cid, 'watchers', 'telegram', 'gchs'):
        wgchs = list(get_dict_fatal_var(cid, 'watchers', 'telegram', 'gchs'))
                        
        for wgch in wgchs:
            fatalapi.msg(wgch, rep)    

def tgm_polling_proc():
    cid = get_client_id()
    tbot = get_fatal_var(cid, 'tgbot')
    
    try:
        tbot.infinity_polling()
    except Exception:
        log_exc_error()     

def init_tgm_bot():
    cid = get_client_id()
  
    tbot = None
  
    if not is_var_set(cid, 'tgbot'):
        bot_api_token = get_cfg_param('tgbot_api_token')

        tbot = telebot.TeleBot(bot_api_token)
        
        set_fatal_var(cid, 'tgbot', tbot)
        
        call_in_sep_thr(cid + '/init_tgm_bot', tgm_polling_proc)
        
    tbot.register_message_handler(handler_tgaccess, commands=['tgaccess'])
    tbot.register_message_handler(command_messages, content_types=['text'])
    tbot.register_message_handler(handle_photo_content, content_types=['photo', 'document', 'animation'])
    tbot.register_message_handler(handle_video_content, content_types=['video', 'video_note'])
    tbot.register_message_handler(handle_audio_content, content_types=['audio', 'voice'])
        
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