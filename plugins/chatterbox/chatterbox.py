# -*- coding: utf-8 -*-

#  fatal plugin
#  chatterbox plugin

#  Copyright © 2023 U2 <gx1608@mail.ru>
#  A bit of editions © 2023 Ancestors Soft

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
import datetime
from math import ceil

def is_url(msg):
    domens = ('https://', 'http://', '.ru', '.com', '.org', 
                '.ua', '.su', '.net', '.de', '.uk', '.ch', 
                '.info', '.nl', '.eu', '.jp', '.fr', '.cz',
                '.im',)
    msg = re.split('\n| ', msg.lower())
    
    for msg_s in msg:
        for domen in domens:
            url = msg_s.find(domen)
            if url != -1:
                return'True'

def init_chatterbox_db(gch): 
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/chatterbox.db' % (cid, gch)):
        sql = 'CREATE TABLE talkers (talker CHAR(100), msgs INT, since TEXT);'
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

        sql = 'CREATE INDEX italkers ON talkers(talker, msgs, since);'
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

def stat_add(talker, gch):
    cid = get_client_id()

    sql = "SELECT * FROM talkers WHERE talker='%s';" % (talker)
    rep = sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

    if not rep:
        t = datetime.datetime.now()
        since =t.strftime('%d.%m.%Y, %H:%M')
        sql = "INSERT INTO talkers (talker, msgs, since) VALUES ('%s', '%s', '%s');" % (talker, 1, since)
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)
    else:
        msgs = rep[0][1] + 1
        sql = "UPDATE talkers SET msgs='%s' WHERE talker='%s';" % (msgs, talker)
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

def stat_get(gch):
    cid = get_client_id()
    
    sql = "SELECT * FROM talkers"
    rep = sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)
    
    return rep

def handler_chat_stat(target, source, body):
    if is_url(body) == 'True':
        return ''

    if target == 'private':
        return ''

    nick = source[2]
    room = source[1]
    bot_nick = get_bot_nick(room)
    if bot_nick == nick:
        return ''

    prefix = get_comm_prefix(room)
    if body[0] == prefix:
        return ''

    stat_add(nick, room)

def handler_talkers(target, source, body):
    if not is_groupchat(source[1]):
        return reply(target, source, l('This command can be used only in groupchat!'))

    if body == '-':
        if user_level(source[0], source[1]) >= 20:
            return talkers_clean(target, source, body)
        else:
            if target == 'private':
                return reply (target, source, l('Too few rights!'))
            return reply(target, source, l('Too few rights!'))
                
    talkers = stat_get(source[1])
    
    if talkers != []:
        sort_chatt = sorted(talkers, key=lambda x: x[1], reverse=True)
    else:
        if target == 'private':
            return reply (target, source, l('There are no talkers in this groupchat yet!'))
        return msg(source[1], l('There are no talkers in this groupchat yet!'))

    if len(talkers) > 10:
        pages = ceil(len(talkers) / 10)
    else:
        pages = 1

    if not body.isdigit():
        page = 0
    else:
        page = int(body)
        
    if (page <= 0) or (page > pages):
        page = 0
    else:
        page = page - 1
        
    userstat = ''
    cnt = 0

    while cnt < 10:
        try:
            t_num = page * 10 + cnt + 1
            t_nick = ' '.join(list(sort_chatt[t_num - 1][0]))
            t_stat = sort_chatt[t_num - 1][1]
            t_since = sort_chatt[t_num - 1][2]
            userstat = userstat + l('%s) %s (since %s) - %s msgs\n') % (t_num, t_nick, t_since, t_stat)
        except:
            break
        cnt += 1
    
    if not userstat.strip():
        return reply(target, source, l('Unknown error!'))
    
    if target == 'private':
        if pages != 1:
            return reply(target, source, l('Talkers (total: %s; page: %s of %s):\n\n%s') % (len(talkers), page + 1, pages, userstat[:-1]))
        return reply(target, source, l('Talkers (total: %s):\n\n%s') % (len(talkers), userstat[:-1]))
    else:
        if pages != 1:
            return msg(source[1], l('Talkers (total: %s; page: %s of %s):\n\n%s') % (len(talkers), page + 1, pages, userstat[:-1]))
        return msg(source[1], l('Talkers (total: %s):\n\n%s') % (len(talkers), userstat[:-1]))

def talkers_clean(target, source, body):
    cid = get_client_id()
    gch = source[1]
    
    sql = 'DELETE FROM talkers;'
    sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

    if target == 'private':
        return reply(target, source, l('List of talkers has been cleared!'))
    return msg(source[1], l('List of talkers has been cleared!'))

register_stage1_init(init_chatterbox_db)
register_command_handler(handler_talkers, 'talkers', 11)
register_message_handler(handler_chat_stat)
