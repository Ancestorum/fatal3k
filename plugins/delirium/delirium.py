# -*- coding: utf-8 -*-

#  fatal plugin
#  delirium_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Copyright © 2009-2023 Ancestors Soft

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

def poke_phrase_exists(poke_phrase, gch=''):
    sql = "SELECT * FROM pokes WHERE poke=?;"

    cid = get_client_id()

    if gch:
        qres = sqlquery('dynamic/%s/%s/pokes.db' % (cid, gch), sql, poke_phrase)
    else:
        qres = sqlquery('static/pokes.db', sql, poke_phrase)
    
    if qres:
        return True
    else:
        return False

def get_poke_phrase(rid, gch=''):
    sql = "SELECT poke FROM pokes WHERE id=?;"
    
    cid = get_client_id()
    
    if gch:
        qres = sqlquery('dynamic/%s/%s/pokes.db' % (cid, gch), sql, rid)
    else:
        qres = sqlquery('static/pokes.db', sql, rid)
    
    if qres:
        poke = qres[0][0]
        return poke
    else:
        return ''

def get_poke_phrases(gch):
    sql = 'SELECT * FROM pokes;'
    
    cid = get_client_id()
    
    pokes = sqlquery('dynamic/%s/%s/pokes.db' % (cid, gch), sql)
    
    if pokes:
        pokes = ['%d) %s: %s' % (pokes.index(pli) + 1, pli[0], pli[1]) for pli in pokes]
    
    return pokes
            
def get_rnd_poke_phrase(gch=''):
    sql = 'SELECT poke FROM pokes ORDER BY RANDOM() LIMIT 1;'
    
    cid = get_client_id()
    
    if gch:
        qres = sqlquery('dynamic/%s/%s/pokes.db' % (cid, gch), sql)
    else:
        qres = sqlquery('static/pokes.db', sql)
    
    if qres:
        rnd_poke = qres[0][0]
        return rnd_poke
    else:
        return ''

def del_poke_phrase(poke_id, gch):
    sql = "DELETE FROM pokes WHERE id=?;"
    
    cid = get_client_id()
    
    rep = sqlquery('dynamic/%s/%s/pokes.db' % (cid, gch), sql, poke_id)
    
    return rep	
        
def save_poke_phrase(poke_phrase, gch):
    sql = "INSERT INTO pokes(poke) VALUES (?);" 
    
    cid = get_client_id()
    
    rep = sqlquery('dynamic/%s/%s/pokes.db' % (cid, gch), sql, poke_phrase.strip())
    
    return rep
        
def handler_poke(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    nick = source[2]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
        
    if type == 'private':
        return reply(type, source, l('This command can be used only in public chat!'))
        
    if parameters:
        if not is_var_set(cid, 'poke_nicks', groupchat):
            set_fatal_var(cid, 'poke_nicks', groupchat, [])
        if len(get_fatal_var(cid, 'poke_nicks', groupchat)) >= 10:
            set_fatal_var(cid, 'poke_nicks', groupchat, [])
        else:
            if not is_var_set(cid, 'poke_nicks', groupchat, nick):
                get_fatal_var(cid, 'poke_nicks', groupchat).append(nick)
        if not parameters == get_bot_nick(groupchat):
            if is_gch_user(groupchat, parameters):
                pokes = []
                dn_poke = get_rnd_poke_phrase(groupchat)
                st_poke = get_rnd_poke_phrase()
                
                if dn_poke:
                    pokes.append(dn_poke)
                if st_poke:
                    pokes.append(st_poke)
                            
                rep = random.choice(pokes)
                rep = rep.replace('%nick%', parameters.strip())
                msg(groupchat, '/me %s' % (rep))
            else:
                return reply(type, source, l('User not found!'))
        else:
            return reply(type, source, l("Sneaky fuckin' Russian?"))
    else:
        rep = ''
        nicks = []
        
        if is_var_set(cid, 'poke_nicks', groupchat):
            nicks = get_fatal_var(cid, 'poke_nicks', groupchat)
        
        if nicks:
            nili = get_num_list(nicks)
        else:
            return reply(type, source, l('List of users used this command is empty!'))
        
        if type == 'public':
            reply(type, source, l('Look in private!'))
        
        rep = l('List of users used this command (total: %s):\n\n%s') % (len(nili), '\n'.join(nili))
        
        if type == 'console':
            return reply(type, source, rep)
        else:
            return reply('private', source, rep)
        
def handler_poke_add(type, source, parameters):
    groupchat = source[1]
    
    if not parameters:
        return reply(type, source, l('Invalid syntax!'))
    
    if not parameters.count('%nick%'):
        return reply(type, source, l('Replacement string not found: %nick%!'))
    
    res = save_poke_phrase(parameters, groupchat)
    
    if res != '':
        return reply(type, source, l('Poke phrase has been added!'))
    else:
        return reply(type, source, l('Insert error!'))
        
def handler_poke_del(type, source, parameters):
    groupchat = source[1]
    
    if not parameters:
        return reply(type, source, l('Invalid syntax!'))
    else:
        if not parameters.strip().isdigit():
            return reply(type, source, l('Invalid syntax!'))
        
        poke_id = int(parameters.strip())
        
        poke_phrase = get_poke_phrase(poke_id, groupchat)
        res = ''
        
        if poke_phrase:
            res = del_poke_phrase(poke_id, groupchat)

    if res != '':
        return reply(type, source, l('Poke phrase has been deleted!'))
    else:
        return reply(type, source, l('Poke phrase note found!'))
        
def handler_poke_list(type, source, parameters):
    groupchat = source[1]
    
    rep, res = '', get_poke_phrases(groupchat)
    
    if res:
        rep = l('List of poke phrases (total: %s):\n\n%s') % (len(res), '\n'.join(res))
        
        return reply(type, source, rep)
    else:
        return reply(type, source, l('List of poke phrases is empty!'))
        
def handler_test(type, source, parameters):
    return reply(type, source, l('Passed!'))
    
def handler_clean_conf(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    for x in range(1, 21):
        msg(groupchat, ' ')
        time.sleep(1.3)
    
    rep = l('Done!')
    
    if type == 'console':
        return reply(type, source, rep)
    else:
        return reply('private', source, rep)
    
def get_pokes_state(gch):
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/pokes.db' % (cid, gch)):
        sql = '''CREATE TABLE pokes(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    poke TEXT NOT NULL, 
                                    UNIQUE(poke));'''
                                    
        sqlquery('dynamic/%s/%s/pokes.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX ipokes ON pokes (poke);'
        sqlquery('dynamic/%s/%s/pokes.db' % (cid, gch), sql)
    
register_command_handler(handler_poke, 'poke', 10)
register_command_handler(handler_poke_add, 'poke_add', 20)
register_command_handler(handler_poke_del, 'poke_del', 20)
register_command_handler(handler_poke_list, 'poke_show', 20)
register_command_handler(handler_test, 'test')
register_command_handler(handler_clean_conf, 'clean', 15)

register_stage1_init(get_pokes_state)
