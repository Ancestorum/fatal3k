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
import emoji
import requests
from urllib import request
from hashlib import md5, sha256
import json

def rmv_emoji(text):
    demt = emoji.demojize(text)
    crex = ':{1,1}[a-z_]{1,}:{1,1}'
    emfl = re.findall(crex, demt)
    
    for eli in emfl:
        demt = demt.replace(eli, '')
    
    if demt:    
        return demt.strip()
    return emoji.demojize(text)

def tgfile_exists(ufid):
    sql = '''SELECT * FROM tgfiles WHERE ufid="%s";''' % (ufid)
    qres = sqlquery(d('tgfiles.db'), sql)
    
    if qres:
        return True
    return False

def rmv_exp_tg_files(days=10):
    files = get_tg_files()
    dis = days * 86400
    curt = trunc(time.time())
    dltd = 0
    
    if files:
        for fl in files:
            ufid = fl[0]
            utime = fl[2]
            
            exd = utime + dis
            
            if curt >= exd:
                if rmv_tg_file(ufid):
                    dltd += 1
    if dltd:
        log_null_cmdr('Removed %s expired file(s)!' % (dltd), 'syslogs/output.log')

def rmv_tg_file(ufid):
    if tgfile_exists(ufid):
        sql = '''DELETE FROM tgfiles WHERE ufid="%s";''' % (ufid)
   
        sqlquery(d('tgfiles.db'), sql)
    
        return True
    return False
    
def set_tg_file(ufid, filename):
    if not tgfile_exists(ufid):
        sql = '''INSERT INTO tgfiles (ufid, flnm) VALUES ("%s", "%s");''' % (ufid, filename)
    else:
        sql = '''UPDATE tgfiles SET "flnm"="%s" WHERE "ufid"="%s";''' % (filename, ufid)
    
    qres = sqlquery(d('tgfiles.db'), sql)
    
    if qres != '':
        return True
    return False

def get_tg_file(ufid):
    sql = '''SELECT flnm FROM tgfiles WHERE ufid="%s";''' % (ufid)
    
    qres = sqlquery(d('tgfiles.db'), sql)
    
    if qres:
        return qres[0][0]
    return False

def get_tg_files():
    sql = '''SELECT ufid, flnm, utime FROM tgfiles;'''
    
    qres = sqlquery(d('tgfiles.db'), sql)
    
    if qres:
        return qres
    return False

def get_tg_chid(gtitle):
    sql = '''SELECT id FROM tgchatids WHERE gname="%s";''' % (gtitle)
    qres = sqlquery(d('tgchatids.db'), sql)
    
    if qres:
        return qres[0][0]
    return False

def get_tg_usrid(fnme):
    sql = '''SELECT id FROM tguserids WHERE fname="%s";''' % (fnme.strip())
    qres = sqlquery(d('tguserids.db'), sql)
    
    if qres:
        return qres[0][0]
    return False

def get_tg_fnme(usrid):
    if type(usrid) != int:
        return False 

    sql = '''SELECT fname FROM tguserids WHERE id=%s;''' % (usrid)
    qres = sqlquery(d('tguserids.db'), sql)
    
    if qres:
        return qres[0][0]
    return False

def get_tg_usrn(usrid):
    if type(usrid) != int:
        return False

    sql = '''SELECT usrn FROM tguserids WHERE id=%s;''' % (usrid)
    qres = sqlquery(d('tguserids.db'), sql)
    
    if qres:
        return qres[0][0]
    return False

def set_tg_usrid(usrid, fnme, usrn=''):
    if type(usrid) != int:
        return False 
    
    if not usrid_exists(usrid):
        if usrn:
            sql = '''INSERT INTO tguserids (id, fname, usrn) VALUES (%s, "%s", "%s");''' % (usrid, fnme.strip(), usrn.strip())
        else:
            sql = '''INSERT INTO tguserids (id, fname) VALUES (%s, "%s");''' % (usrid, fnme.strip())
    else:
        if usrn:
            sql = '''UPDATE tguserids SET "fname"="%s", "usrn"="%s" WHERE "id"=%s;''' % (fnme.strip(), usrn.strip(), usrid)
        else:
            sql = '''UPDATE tguserids SET "fname"="%s" WHERE "id"=%s;''' % (fnme.strip(), usrid)
    
    qres = sqlquery(d('tguserids.db'), sql)
    
    if qres != '':
        return True
    return False

def set_tg_usr_acc(usrid, acc):
    if (type(usrid) != int) or (type(acc) != int):
        return False 
    
    if usrid_exists(usrid):
        sql = '''UPDATE tguserids SET acc=%s WHERE id=%s;''' % (acc, usrid)
    
    qres = sqlquery(d('tguserids.db'), sql)
    
    return qres

def chid_exists(chid):
    if type(chid) != int:
        return False 

    sql = '''SELECT * FROM tgchatids WHERE id=%s;''' % (chid)
    qres = sqlquery(d('tgchatids.db'), sql)
    
    if qres:
        return True
    return False

def rmv_tg_usrid(usrid):
    if type(usrid) != int:
        return False 
    
    if usrid_exists(usrid):
        sql = '''DELETE FROM tgusrids WHERE id=%s;''' % (usrid)
    else:
        return False
   
    qres = sqlquery(d('tguserids.db'), sql)
    
    return qres

def rmv_tg_chid(chid):
    if type(chid) != int:
        return False 
    
    if chid_exists(chid):
        sql = '''DELETE FROM tgchatids WHERE id=%s;''' % (chid)
    else:
        return False
   
    qres = sqlquery(d('tgchatids.db'), sql)
    
    return qres

def set_tg_chid(chid, gtitle):
    if type(chid) != int:
        return False 
    
    gtitle = gtitle.replace('"', '&quot;')
    
    if not chid_exists(chid):
        sql = '''INSERT INTO tgchatids (id, gname) VALUES (%s, "%s");''' % (chid, gtitle.strip())
    else:
        sql = '''UPDATE tgchatids SET "gname"="%s" WHERE id=%s;''' % (gtitle.strip(), chid)
    
    qres = sqlquery(d('tgchatids.db'), sql)
    
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
        file_uid = message.document.file_unique_id
    elif message.animation:
        file_id = message.animation.file_id
        file_uid = message.animation.file_unique_id
    else:    
        file_id = message.photo[-1].file_id
        file_uid = message.photo[-1].file_unique_id
    
    file_url = tbot.get_file_url(file_id)
    
    if not tgfile_exists(file_uid):
        thrn = '%s/save_and_upload' % (cid)
        call_in_sep_thr(thrn, save_and_upload, file_url)
    else:
        filename = get_tg_file(file_uid)
        
        if not is_var_set(cid, 'tgm_pen_up_fls'):
            set_fatal_var(cid, 'tgm_pen_up_fls', [filename])
        else:
            pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
            pupf.append(filename)
    
    time.sleep(0.3)
    
    if message.chat.type == 'private':
        tbot.delete_message(chatid, messid)
        
        pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
        
        filename = pupf[-1]
        pupf.remove(filename)
        
        purl = get_cfg_param('tgurl_prefix')
        rmsg = '%s%s' %(purl, filename)
        ndt = message.date
        
        set_tg_file(file_uid, filename)
        
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
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', chatid)):
            pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
            
            filename = pupf[-1]
            pupf.remove(filename)
            
            purl = get_cfg_param('tgurl_prefix')
            rmsg = '%s%s' %(purl, filename)
            ndt = message.date
            
            set_tg_file(file_uid, filename)
            
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

    if caption:
        caption = rmv_emoji(caption)

    if not is_var_set(cid, 'tgm_msg_buf'):
        set_fatal_var(cid, 'tgm_msg_buf', [])

    if message.video_note:
        video_id = message.video_note.file_id
        video_uid = message.video_note.file_unique_id
    else:
        if message.video.file_size > 20000000:
            video_id = message.video.thumb.file_id
            video_uid = message.video.thumb.file_unique_id
        else:    
            video_id = message.video.file_id
            video_uid = message.video.file_unique_id
    
    file_url = tbot.get_file_url(video_id)
    
    if not tgfile_exists(video_uid):
        thrn = '%s/save_and_upload' % (cid)
        call_in_sep_thr(thrn, save_and_upload, file_url)
    else:
        filename = get_tg_file(video_uid)
    
        if not is_var_set(cid, 'tgm_pen_up_fls'):
            set_fatal_var(cid, 'tgm_pen_up_fls', [filename])
        else:
            pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
            pupf.append(filename)
    
    time.sleep(0.3)
    
    if message.chat.type == 'private':
        tbot.delete_message(chatid, messid)
        
        pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
        
        filename = pupf[-1]
        pupf.remove(filename)
        
        purl = get_cfg_param('tgurl_prefix')
        rmsg = '%s%s' %(purl, filename)
        ndt = message.date
        
        set_tg_file(video_uid, filename)
        
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
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', chatid)):
            pupf = get_fatal_var(cid, 'tgm_pen_up_fls')
            
            filename = pupf[-1]
            pupf.remove(filename)
            
            purl = get_cfg_param('tgurl_prefix')
            rmsg = '%s%s' %(purl, filename)
            ndt = message.date
            
            set_tg_file(video_uid, filename)
            
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
            audio_id = message.audio.file_id
            audio_uid = message.audio.file_unique_id
        else:
            audio_id = message.voice.file_id
            audio_uid = message.voice.file_unique_id
        
        file_url = tbot.get_file_url(audio_id)
        
        resp, filename = save_and_upload(file_url)
        
        set_tg_file(audio_uid, filename)
        
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

def handle_sticker_content(message):
    if (time.time() - message.date) > 8:
        return

    cid = get_client_id()
    
    tbot = get_fatal_var(cid, 'tgbot')
    chatid = message.chat.id
    messid = message.message_id
    fname = message.from_user.first_name
    lname = message.from_user.last_name
    usern = message.from_user.username
    
    sticker_id = message.sticker.file_id
    sticker_uid = message.sticker.file_unique_id
    
    file_url = tbot.get_file_url(sticker_id)
    
    if message.chat.type == 'private':
        resp, filename = save_and_upload(file_url)    
        
        set_tg_file(sticker_uid, filename)
        
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
    else:
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', chatid)):
            fext = file_url.split('.')[-1]
            filename = ''

            if fext != 'tgs':
                resp, filename = save_and_upload(file_url)
                
                set_tg_file(sticker_uid, filename)
                
                purl = get_cfg_param('tgurl_prefix')
                
                if filename:
                    filename = '%s%s' %(purl, filename)            
            else:
                filename = message.sticker.emoji
                
                if filename:
                    filename = emoji.demojize(filename)
            
            if lname:
                if fname != lname:
                    lname = ' ' + lname
                else:
                    lname = ''
            else:
                lname = ''    
            
            if filename:
                if usern and fname != usern:
                    rep = '[%s]<%s%s (@%s)> %s' % (message.chat.title, fname, lname, usern, filename)
                else:
                    rep = '[%s]<%s%s> %s' % (message.chat.title, fname, lname, filename)
                
                if is_var_set(cid, 'watchers', chatid, 'gchs'):
                    wgchs = list(get_dict_fatal_var(cid, 'watchers', chatid, 'gchs'))
                    
                    for wgch in wgchs:
                        msg(wgch, rep)    

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
            
            if usern:
                source = [usrid, chatid, '@%s' % (usern)]
            else:
                source = [usrid, chatid, fname]
            
            call_command_handlers(wprname, 'telegram', source, cparams.strip(), wprname)
        else:
            tbot.reply_to(message, l('Unknown command!'))
    else:
        if message.chat.type == 'private':
            txt = message.text
            
            fp = open('static/emot/icondef.xml', 'a', encoding='utf-8')
    
            icos = '''  <icon>
    <text>%s</text>
    <object mime="image/png">%s.png</object>
  </icon>\n'''
            
            if txt.isdigit():
                set_fatal_var(cid, 'digitex_c', int(txt))
                
                set_fatal_var(cid, 'digit_text', txt.zfill(4))
                tbot.send_document(chatid, open('static/emot/sepd04/%s.png' % (txt.zfill(4)), 'rb'))
            else:
                dtxt = str(get_fatal_var(cid, 'digitex_c')).zfill(4)
                emot = emoji.demojize(message.text)
                
                fp.write(icos % (emot, dtxt))
                
                tbot.send_message(chatid, emot)
                
                fnm = inc_fatal_var(cid, 'digitex_c')
                set_fatal_var(cid, 'digit_text', str(fnm).zfill(4))
                
                try:
                    tbot.send_document(chatid, open('static/emot/sepd04/%s.png' % (str(fnm).zfill(4)), 'rb'))
                except Exception:
                    pass
        
            fp.close()
        
        if (message.chat.type != 'private') and (is_var_set(cid, 'watchers', chatid)):
            url = ''
            
            from_usr = ''
            rto = ''
            ffn = ''
            fln = ''
            fus = ''
            
            if message.forward_from:
                ffn = message.forward_from.first_name
                
                if message.forward_from.last_name:
                    fln = ' ' + message.forward_from.last_name
                    
                if message.forward_from.username:
                    fus = message.forward_from.username
                
                if fus and ffn != fus:
                    from_usr = l('Forward from %s%s (@%s):') % (ffn, fln, fus)
                else:
                    from_usr = l('Forward from %s%s:') % (ffn, fln)
                
                from_usr += '\n\n'
           
            if message.reply_to_message:
                rtl = ''
                rtu = ''
                
                rtm = message.reply_to_message
                rtf = rtm.from_user.first_name
                
                if rtm.from_user.last_name and rtf != rtm.from_user.last_name:
                    rtl = ' ' + rtm.from_user.last_name + ': '
                
                if rtm.from_user.username:               
                    rtu = rtm.from_user.username
                
                if rtm.forward_from:
                    fwf = rtm.forward_from
                    
                    rtf = ''
                    rtl = ''
                    rtu = ''
                    
                    rtf = fwf.first_name
                    
                    if fwf.last_name and rtf != fwf.last_name:
                        rtl = ' ' + fwf.last_name
                        
                    if fwf.username:
                        rtu = fwf.username
                
                if rtm.text:
                    rtx = rtm.text
                elif rtm.caption:
                    rtx = rtm.caption
                else:
                    rtx = ''
                
                if rtm.forward_from_chat:
                    rtf = rmv_emoji(rtm.forward_from_chat.title)
                    
                    #if not rtm.caption:
                    rtl = ''
                        
                    rtu = ''
                
                fur = ''
                file_uid = ''
                
                if rtm.photo:
                    file_uid = rtm.photo[-1].file_unique_id
                elif rtm.video:
                    file_uid = rtm.video.file_unique_id
                elif rtm.document:
                    file_uid = rtm.document.file_unique_id
                elif rtm.animation:
                    file_uid = rtm.animation.file_unique_id
                elif rtm.video_note:
                    file_uid = rtm.video_note.file_unique_id
                elif rtm.audio:
                    file_uid = rtm.audio.file_unique_id
                elif rtm.voice:
                    file_uid = rtm.voice.file_unique_id
                elif rtm.sticker:
                    file_uid = rtm.sticker.file_unique_id
                
                fur = get_tg_file(file_uid)
                
                if fur:
                    purl = get_cfg_param('tgurl_prefix')
                    fur = '%s%s' %(purl, fur)
                    rto = '\n\n>> %s' % (fur)
                
                if rtm.caption_entities:
                    for cent in rtm.caption_entities:
                        if cent.type == 'text_link':
                            offs = cent.offset
                        
                            deml = len(rmv_emoji(rtx))
                            rtxl = len(rtx)
                            co = rtxl - deml
                            ic = co // 2
                            
                            sti = offs
                            rtx = rtx[0:sti-ic]
                            rtx = rtx.strip()
                            break
                
                rtx = rmv_emoji(rtx)
                
                if len(rtx) >= 100:
                    rtx = rtx[0:100] + '...'
                
                rtx = rtx.replace('\n', '\n>> ')
                rtx = rtx.replace('\n\n', '\n\n>> ')
                
                if rtu and rtf != rtu:
                    if rtx:
                        rtx = ': ' + rtx
                    
                    rto += '\n\n>> %s%s (@%s)%s' % (rtf, rtl, rtu, rtx)
                else:
                    if rtx:
                        rtx = ': ' + rtx 
                    
                    rto += '\n\n>> %s%s%s' % (rtf, rtl, rtx)
           
            if message.entities:
                for ment in message.entities:
                    if ment.type == 'text_link':
                        url = ment.url
                        break
            
            mtxt = rmv_emoji(message.text)
            
            lname = ''
            
            if message.from_user.last_name:
                if fname != lname:
                    lname = ' ' + message.from_user.last_name
            
            if usern and fname != usern:
                rep = '[%s]<%s%s (@%s)> %s%s%s' % (message.chat.title, fname, lname, usern, from_usr, mtxt, rto)
            else:
                rep = '[%s]<%s%s> %s%s%s' % (message.chat.title, fname, lname, from_usr, mtxt, rto)
            
            if url:
                rep += '\n\n%s' % (url)
            
            if is_var_set(cid, 'watchers', chatid, 'gchs'):
                wgchs = list(get_dict_fatal_var(cid, 'watchers', chatid, 'gchs'))
                
                for wgch in wgchs:
                    msg(wgch, rep)    

def msg_worker(message, public=False):
    cid = get_client_id()
    tbot = get_fatal_var(cid, 'tgbot')
    chatid = message.chat.id
    caption = message.caption
    fname = message.from_user.first_name
    lname = message.from_user.last_name
    usern = message.from_user.username
    chat_title = message.chat.title
    mult = ''
    cr = ''
    
    if caption:
        caption = rmv_emoji(caption)
    
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
            
            if ltime - mtime > 2:
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

    if not is_var_set(cid, 'watchers', chatid):
        return

    from_chat = ''
    
    if message.forward_from_chat:
        from_chat = l('Forward from chat %s:') % (rmv_emoji(message.forward_from_chat.title))
        from_chat += '\n\n'

    url = ''
    
    if message.caption_entities:
        for cape in message.caption_entities:
            if cape.type == 'text_link':
                url = cape.url
                break
    
    if lname:
        if fname != lname:
            lname = ' ' + lname
        else:
            lname = ''
    else:
        lname = ''
    
    if usern and fname != usern:
        if caption:
            rep = '[%s]<%s%s (@%s)> %s%s%s\n%s%s' % (chat_title, fname, lname, usern, mult, from_chat, rep, cr, caption)
        else:
            rep = '[%s]<%s%s (@%s)> %s%s%s' % (chat_title, fname, lname, usern, mult, from_chat, rep)
    else:
        if caption:
            rep = '[%s]<%s%s> %s%s%s\n%s%s' % (chat_title, fname, lname, mult, from_chat, rep, cr, caption)
        else:    
            rep = '[%s]<%s%s> %s%s%s' % (chat_title, fname, lname, mult, from_chat, rep)
    
    if url:
        rep += ' (%s)' % (url)
    
    if is_var_set(cid, 'watchers', chatid, 'gchs'):
        wgchs = list(get_dict_fatal_var(cid, 'watchers', chatid, 'gchs'))
                        
        for wgch in wgchs:
            fatalapi.msg(wgch, rep)    

def tgm_polling_proc():
    cid = get_client_id()
    tbot = get_fatal_var(cid, 'tgbot')
    
    try:
        tbot.infinity_polling()
    except Exception:
        log_exc_error()     

def listener(messages):
    cid = get_client_id()
    
    if len(messages) >= 2:
        set_fatal_var(cid, 'tgmult_flag', 1)
    else:
        set_fatal_var(cid, 'tgmult_flag', 0)
    
    set_fatal_var(cid, 'last_tg_msgs', messages)
    
    if is_param_seti('tglog_json'):
        for msg in messages:
            json_str = msg.json
            bfjs = '\n' +  json.dumps(json_str, indent=4) + '\n\n' + '=' * 80 + '\n'
            log_null_cmdr(bfjs, 'syslogs/json.log')
    
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
        tbot.register_message_handler(handle_sticker_content, content_types=['sticker'])
        
        tbot.set_update_listener(listener)

def check_expired_tg_files():
    add_fatal_task('rmv_exp_tg_files', rmv_exp_tg_files, ival=3600)
        
def create_tg_tables():
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/tgfiles.db' % (cid)):
        sql = '''CREATE TABLE tgfiles (idn INTEGER PRIMARY KEY AUTOINCREMENT,
            ufid VARCHAR(30) NOT NULL, flnm VARCHAR(30) NOT NULL, 
            utime TIMESTAMP DEFAULT (strftime('%s', 'now')), UNIQUE (idn));''' 
        
        sqlquery('dynamic/%s/tgfiles.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX itgfiles ON tgfiles (idn);'
        
        sqlquery('dynamic/%s/tgfiles.db' % (cid), sql) 
    
    if not is_db_exists('dynamic/%s/tguserids.db' % (cid)):
        sql = '''CREATE TABLE tguserids (idn INTEGER PRIMARY KEY AUTOINCREMENT,
            id INTEGER NOT NULL, fname VARCHAR(30) NOT NULL, usrn VARCHAR(30) DEFAULT "",
            acc INTEGER NOT NULL DEFAULT 10, UNIQUE (id));''' 
        
        sqlquery('dynamic/%s/tguserids.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX itguserids ON tguserids (idn);'
        sqlquery('dynamic/%s/tguserids.db' % (cid), sql) 

    if not is_db_exists('dynamic/%s/tgchatids.db' % (cid)):
        sql = '''CREATE TABLE tgchatids (idn INTEGER PRIMARY KEY AUTOINCREMENT,
            id INTEGER NOT NULL, gname VARCHAR(30) NOT NULL, UNIQUE (id));'''
        sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX itgchatids ON tgchatids (idn);'
        sqlquery('dynamic/%s/tgchatids.db' % (cid), sql)

if is_param_set('tgbot_api_token'):
    register_command_handler(handler_tgaccess_jcmd, 'tgaccess', 10)

    register_stage0_init(create_tg_tables)
    register_stage2_init(init_tgm_bot)
    register_stage2_init(check_expired_tg_files)