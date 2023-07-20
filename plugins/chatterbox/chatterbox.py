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

def nick_space(nick):
    snick = ''
    for w in nick:
        snick = snick + w + ' '
    return snick[:-1]

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
    
    t = datetime.datetime.now()
    start_time =t.strftime('%d.%m.%Y %H:%M')
    
    if not is_db_exists('dynamic/%s/%s/chatterbox.db' % (cid, gch)):
        sql = 'CREATE TABLE talkers (talker CHAR(100), msgs INT);'
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

        sql = 'CREATE TABLE time (chat_time CHAR(16));'
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

        sql = 'CREATE INDEX italkers ON talkers(talker, msgs);'
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

        sql = 'CREATE INDEX itime ON time(chat_time);'
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

        sql = "INSERT INTO time (chat_time) VALUES ('%s');" % (start_time)
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

def stat_add(talker, gch):
    cid = get_client_id()

    sql = "SELECT * FROM talkers WHERE talker='%s';" % (talker)
    rep = sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

    if rep == []:
        sql = "INSERT INTO talkers (talker, msgs) VALUES ('%s', '%s');" % (talker, 1)
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)
    else:
        msgs = rep[0][1] + 1
        sql = "UPDATE talkers SET msgs='%s' WHERE talker='%s';" % (msgs, talker)
        sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

def stat_get(gch):
    cid = get_client_id()
    
    sql = "SELECT * FROM talkers"
    rep = sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)
    
    sql = "SELECT * FROM time"
    rep2 = sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

    return rep2, rep

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
    stats = stat_get(source[1])
    start_time = str(stats[0][0][0])
    talkers = stats[1]
    if not is_groupchat(source[1]):
        return reply(msg_type[0], source, l('This command can be used only in groupchat!'))
    
    if talkers != []:
        sort_chatt = sorted(talkers, key=lambda x: x[1], reverse=True)
    else:
        if target == 'private':
            return reply (target, source, l('There are no talkers in this MUC.'))
        else:
            return msg(source[1], l('There are no talkers in this MUC.'))
    userstat = ''
    item_count = 1
    for item in sort_chatt:
        if item_count > 10:
            continue
        username = nick_space(item[0])
        usermsgs = str(item[1])
        userstat = userstat + str(item_count) + '. ' + username + ' - ' + usermsgs + ' ' + l('messages\n')
        item_count += 1
    if target == 'private':
        return reply (target, source, l('From') + ' ' + start_time + ', ' + l('they wrote (top 10):\n') + userstat)
    else:
        return msg(source[1], l('From') + ' '+ start_time + ', ' + l('they wrote (top 10):\n') + userstat)

def handler_talkers_all(target, source, body):
    stats = stat_get(source[1])
    start_time = str(stats[0][0][0])
    talkers = stats[1]
    if not is_groupchat(source[1]):
        return reply(msg_type[0], source, l('This command can be used only in groupchat!'))
    
    if talkers != []:
        sort_chatt = sorted(talkers, key=lambda x: x[1], reverse=True)
    else:
        if target == 'private':
            return reply (target, source, l('There are no talkers in this groupchat!'))
        else:
            return msg(source[1], l('There are no talkers in this groupchat!'))
    userstat = ''
    item_count = 1
    for item in sort_chatt:
        username = nick_space(item[0])
        usermsgs = str(item[1])
        userstat = userstat + str(item_count) + '. ' + username + ' - ' + usermsgs + ' ' + l('messages\n')
        item_count += 1
    if target == 'private':
        return reply (target, source, l('From') + ' ' + start_time + ', ' + l('they wrote:\n') + userstat)
    else:
        return msg(source[1], l('From') + ' '+ start_time + ', ' + l('they wrote:\n') + userstat)

def handler_talkers_clean(target, source, body):
    if not is_groupchat(source[1]):
        return reply(target, source, l('This command can be used only in groupchat!'))

    cid = get_client_id()
    gch = source[1]
    
    sql = 'DELETE FROM talkers;'
    sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)
    sql = 'DELETE FROM time;'
    sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)
    t = datetime.datetime.now()
    start_time =t.strftime('%d.%m.%Y %H:%M')
    sql = "INSERT INTO time (chat_time) VALUES ('%s');" % (start_time)
    sqlquery('dynamic/%s/%s/chatterbox.db' % (cid, gch), sql)

    if target == 'private':
        return reply(target, source, l('List of talkers has been cleared!'))
    else:
        return msg(source[1], l('List of talkers has been cleared!'))

register_stage1_init(init_chatterbox_db)
register_command_handler(handler_talkers, 'talkers', 11)
register_command_handler(handler_talkers_clean, 'talkers_clean', 20)
register_command_handler(handler_talkers_all, 'talkers_all', 11)
register_message_handler(handler_chat_stat)