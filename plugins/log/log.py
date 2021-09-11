# -*- coding: utf-8 -*-

#  fatal plugin
#  log plugin

#  Initial Copyright © Anaлl Verrier <elghinn@free.fr>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Copyright © 2009-2012 Ancestors Soft

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

__all__ = []

import math
import re

from fatalapi import *

def log_write_header(fp, source, xxx_todo_changeme):
    (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = xxx_todo_changeme
    source = source.encode('utf-8')
    
    if not is_groupchat(source):
        gch_jid = source.split('%', 1)[0]
        
        if is_groupchat(gch_jid):
            gch_nick = source.split('%', 1)[-1]
            source = '%s/%s' % (gch_jid, gch_nick)

    date = time.strftime('%A, %B %d, %Y', (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
    fp.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dt">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>%s</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="keywords" content="xmpp,jabber,conference,chatroom,groupchat,MUC,multi-user conference">
<style type="text/css">
<!--
.userjoin {color: #009900; font-style: italic; font-weight: bold}
.userleave {color: #dc143c; font-style: italic; font-weight: bold}
.statuschange {color: #a52a2a; font-weight: bold}
.rachange {color: #0000FF; font-weight: bold}
.userkick {color: #FF7F50; font-weight: bold}
.userban {color: #DAA520; font-weight: bold}
.nickchange {color: #FF69B4; font-style: italic; font-weight: bold}
.timestamp {color: #aaa;}
.timestamp a {color: #aaa; text-decoration: none;}
.system {color: #090; font-weight: bold;}
.emote {color: #800080;}
.self {color: #0000AA;}
.selfmoder {color: #DC143C;}
.normal {color: #483d8b;}
#mark { color: #aaa; text-align: right; font-family: monospace; letter-spacing: 3px }
h1 { color: #369; font-family: sans-serif; border-bottom: #246 solid 3pt; letter-spacing: 3px; margin-left: 20pt;}
h2 { color: #639; font-family: sans-serif; letter-spacing: 2px; text-align: center }
a.h1 {text-decoration: none;color: #369;}
#//-->
</style>
</head>
<body>
<div id="mark">fatal-bot log</div>
<h1><a class="h1" href="xmpp:%s?join" title="Join room">%s</a></h1>
<h2>%s</h2>
<div>
<tt>
""".encode('utf-8') % (' - '.join([source, date]), source, source, date))

def log_write_footer(fp):
    fp.write('\n</tt>\n</div>\n</body>\n</html>')

def log_get_fp(type, source, xxx_todo_changeme1):
    (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = xxx_todo_changeme1
    if not is_groupchat(source):
        gch_jid = source.split('/', 1)[0]
        
        if is_groupchat(gch_jid):
            gch_nick = source.split('/', 1)[-1]
            source = gch_jid + '%' + gch_nick

    if type == 'public':
        logdir = get_cfg_param('public_log_dir')
    else:
        logdir = get_cfg_param('private_log_dir')

    if logdir[-1] == '/':
        logdir = logdir[:-1]

    str_year = str(year)
    str_month = str(month)
    str_day = str(day)
        
    str_month = str_month.zfill(2)
    str_day = str_day.zfill(2)

    filename = '.'.join(['/'.join([logdir, source, str_year, str_month, str_day]), 'html'])
    alt_filename = '.'.join(['/'.join([logdir, source, str_year, str_month, str_day]), '_alt.html'])

    pathex = '/'.join([logdir, source, str_year, str_month]).encode('utf-8')

    if not os.path.exists(pathex):
        pexli = [logdir, logdir + '/' + source, logdir + '/' + source + '/' + str_year, logdir + '/' + source + '/' + str_year + '/' + str_month]
        pneli = [li for li in pexli if not os.path.exists(li.encode('utf-8'))]
        
        try:
            for dli in pneli:
                os.mkdir(dli.encode('utf-8'))
        except Exception:
            pass

    if param_exists('', source):
        lpath = get_param(source)
        
        if os.path.exists(lpath.encode('utf-8')):
            fp_old = open(get_param(source).encode('utf-8'), 'a', encoding='utf-8')
            
            sfn = str(fp_old.name).split('/')[-1].split('.', 1)[0]
            sfn_day = 35
            
            if sfn.isdigit():
                sfn_day = int(sfn)
            
            if sfn_day < day:
                log_write_footer(fp_old)
                
            fp_old.close()
            
        if os.path.exists(filename.encode('utf-8')):
            fp = open(filename.encode('utf-8'), 'a', encoding='utf-8')
            return fp
        else:
            set_param(source, filename)
            fp = open(filename.encode('utf-8'), 'w', encoding='utf-8')
            log_write_header(fp, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
            return fp
    else:
        if os.path.exists(filename.encode('utf-8')):
            set_param(source, filename)
            fp = open(alt_filename.encode('utf-8'), 'a', encoding='utf-8')
            return fp
        else:
            set_param(source, filename)
            fp = open(filename.encode('utf-8'), 'w', encoding='utf-8')
            log_write_header(fp, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
            return fp

def log_regex_url(matchobj):
    return '<a href="' + matchobj.group(0) + '">' + matchobj.group(0) + '</a>'

def get_logw_state(gch):
    cid = get_client_id()
    
    if not param_exists(gch, 'logw'):
        set_gch_param(gch, 'logw', '0')
        set_fatal_var(cid, 'log_write', gch, 0)
    else:
        logw = int(get_gch_param(gch, 'logw', '0'))
        set_fatal_var(cid, 'log_write', gch, logw)

def handler_logw_control(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
    
    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))

        if int(parameters) > 1:
            return reply(type, source, l('Invalid syntax!'))

        if parameters == '1':
            set_gch_param(groupchat, 'logw', '1')
            set_fatal_var(cid, 'log_write', groupchat, 1)
            return reply(type, source, l('Logging has been turned on!'))
        else:
            set_gch_param(groupchat, 'logw', '0')
            set_fatal_var(cid, 'log_write', groupchat, 0)
            return reply(type, source, l('Logging has been turned off!'))
    else:
        if get_gch_param(groupchat, 'logw', '1') == '1':
            return reply(type, source, l('Logging is turned on!'))
        else:
            return reply(type, source, l('Logging is turned off!'))
        
def log_handler_message(type, source, body):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not body:
        return

    if type == 'public' and is_param_set('public_log_dir') and is_var_set(cid, 'log_write', groupchat):
        nick = source[2]
        
        ismoder = 0
        
        if is_groupchat(groupchat) and is_gch_user(groupchat, nick) and get_gch_role(groupchat, nick) == 'moderator':
            ismoder = 1
        
        log_write(body, nick, type, groupchat, ismoder)
    elif type == 'private' and is_param_set('private_log_dir'):
        jid = get_true_jid(source)
        gch_jid = jid.split('/', 1)[0]
        
        if gch_jid == groupchat:
            gch_jid = jid.split('/')[-1]
        
        log_write(body, gch_jid, type, jid)

def log_handler_outgoing_message(target, body, obody):
    if is_groupchat(target) or not body:
        return
    
    nick = get_cfg_param('default_nick')
    
    jid = get_true_jid(target)

    if type(target) is str:
        gch_jid = target.split('/', 1)[0]
        
    if type(target) is type:
        gch_jid = target.getStripped()
    else:
        gch_jid = target
        
    if is_groupchat(gch_jid):
        nick = get_bot_nick(gch_jid)
        
        if not nick:
            nick = get_cfg_param('default_nick')
    
    log_write(body, nick, 'private', jid)

def log_write(body, nick, type, jid, ismoder=0):
    if not is_groupchat(jid):
        jid = get_true_jid(jid)
        
    decimal = str(int(math.modf(time.time())[0] * 100000))
    (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()

    body = body.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    body = re.sub('(http|ftp)(\:\/\/[^\s<]+)', log_regex_url, body)
    body = body.replace('\n', '<br/>')
    #body = body.encode('utf-8')
    #nick = nick.encode('utf-8')
    
    timestamp = '[%.2i:%.2i:%.2i]' % (hour, minute, second)

    try:
        fp = log_get_fp(type, jid, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
    except Exception:
        log_exc_error()
        return

    fp.write('<span class="timestamp"><a id="t' + timestamp[1:-1] + '.' + decimal + '" href="#t' + timestamp[1:-1] + '.' + decimal + '">' + timestamp + '</a></span> ')

    defnick = get_cfg_param('default_nick')
    #defnick = defnick.encode('utf-8')

    if not nick:
        fp.write('<span class="system">%s</span><br />\n' % (body))
    elif body[:3].lower() == '/me':
        fp.write('<span class="emote">* %s%s</span><br />\n' % (nick, body[3:]))
    elif type == 'public' or nick == defnick:
        if nick == '@$$leave$$@':
            fp.write('<span class="userleave">%s</span><br />\n' % (body))
        elif nick == '@$$join$$@':
            fp.write('<span class="userjoin">%s</span><br />\n' % (body))
        elif nick == '@$$status$$@':
            fp.write('<span class="statuschange">%s</span><br />\n' % (body))
        elif nick == '@$$ra$$@':
            fp.write('<span class="rachange">%s</span><br />\n' % (body))
        elif nick == '@$$userkick$$@':
            fp.write('<span class="userkick">%s</span><br />\n' % (body))
        elif nick == '@$$userban$$@':
            fp.write('<span class="userban">%s</span><br />\n' % (body))
        elif nick == '@$$nickchange$$@':
            fp.write('<span class="nickchange">%s</span><br />\n' % (body))
        else:
            if ismoder:
                fp.write('<span class="selfmoder">&lt;%s&gt;</span> %s<br />\n' % (nick, body))
            else:
                fp.write('<span class="self">&lt;%s&gt;</span> %s<br />\n' % (nick, body))
    else:
        fp.write('<span class="normal">&lt;%s&gt;</span> %s<br />\n' % (nick, body))

    fp.close()

def log_handler_join(groupchat, nick, aff, role):
    cid = get_client_id()
    
    if is_groupchat(groupchat):
        if not is_var_set(cid, 'log_write', groupchat):
            return
    
    log_write('%s joins the room as %s and %s' % (nick, role, aff), '@$$join$$@', 'public', groupchat)

def log_handler_leave(groupchat, nick, reason, code):
    cid = get_client_id()
    
    if is_groupchat(groupchat):
        if not is_var_set(cid, 'log_write', groupchat):
            return

    if code:
        if code == '307':
            if reason:
                log_write('%s has been kicked (%s)' % (nick, reason), '@$$userkick$$@', 'public', groupchat)
            else:
                log_write('%s has been kicked' % (nick), '@$$userkick$$@', 'public', groupchat)
        elif code == '301':
            if reason:
                log_write('%s has been banned (%s)' % (nick, reason), '@$$userban$$@', 'public', groupchat)
            else:
                log_write('%s has been banned' % (nick), '@$$userban$$@', 'public', groupchat)
    else:
        if reason:
            log_write('%s leaves the room (%s)' % (nick, reason), '@$$leave$$@', 'public', groupchat)
        else:
            log_write('%s leaves the room' % (nick), '@$$leave$$@', 'public', groupchat)

def log_handler_presence(prs):
    cid = get_client_id()
    
    stmsg, status, code, reason, newnick = '', '', '', '', ''
    groupchat = prs.getFrom().getStripped()
    
    if is_groupchat(groupchat):
        if not is_var_set(cid, 'log_write', groupchat):
            return
    
    nick = prs.getFrom().getResource()
    code = prs.getStatusCode()
    
    if code == '303':
        newnick = prs.getNick()
        log_write('%s now is known as %s' % (nick, newnick), '@$$nickchange$$@', 'public', groupchat)
    else:
        if not prs.getType() == 'unavailable':
            try:
                stmsg = prs.getStatus()
            except:
                stmsg = ''
                
            try:
                status = prs.getShow()
            except:
                status = 'online'
            
            if not status:
                status = 'online'
                
            if stmsg:
                log_write('%s is now %s (%s)' % (nick, status, stmsg), '@$$status$$@', 'public', groupchat)
            else:
                log_write('%s is now %s' % (nick, status), '@$$status$$@', 'public', groupchat)

if is_param_set('public_log_dir'):
    register_command_handler(handler_logw_control, 'logging', 30)

    register_stage1_init(get_logw_state)
    register_message_handler(log_handler_message)
    register_join_handler(log_handler_join)
    register_leave_handler(log_handler_leave)
    register_presence_handler(log_handler_presence)
    
if is_param_set('private_log_dir'):
    register_outgoing_message_handler(log_handler_outgoing_message)
