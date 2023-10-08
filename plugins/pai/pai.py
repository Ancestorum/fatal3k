# -*- coding: utf-8 -*-

#  fatal pseudo AI plugin v1.2
#  pai plugin

#  Idea from © 2009, Pavel Vishnevsky aka awel
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

def check_obscene_words(body):
    obscene_words = ['бляд', ' блят', ' бля ', ' блять ', ' плять ', ' хуй', ' ибал', ' ебал', 'нахуй', ' хуй', ' хуи', 'хуител', ' хуя', 'хуя', ' хую', ' хуе', ' ахуе', ' охуе', 'хуев', ' хер ', ' хер', 'хер', ' пох ', ' нах ', 'писд', 'пизд', 'рizd', ' пздц ', ' еб', ' епана ', ' епать ', ' ипать ', ' выепать ', ' ибаш', ' уеб', 'проеб', 'праеб', 'приеб', 'съеб', 'сьеб', 'взъеб', 'взьеб', 'въеб', 'вьеб', 'выебан', 'перееб', 'недоеб', 'долбоеб', 'долбаеб', ' ниибац', ' неебац', ' неебат', ' ниибат', ' пидар', ' рidаr', ' пидар', ' пидор', 'педор', 'пидор', 'пидарас', 'пидараз', ' педар', 'педри', 'пидри', ' заеп', ' заип', ' заеб', 'ебучий', 'ебучка ', 'епучий', 'епучка ', ' заиба', 'заебан', 'заебис', ' выеб', 'выебан', ' поеб', ' наеб', ' наеб', 'сьеб', 'взьеб', 'вьеб', ' гандон', ' гондон', 'пахуи', 'похуис', ' манда ', 'мандав', ' залупа', ' залупог']

    body = body.lower()
    body = ' ' + body + ' '
    
    for x in obscene_words:
        if body.count(x):
            return True
    return False

def get_pai_phrases(gch):
    cid = get_client_id()
    
    sql = 'SELECT * FROM phrases ORDER BY id DESC;'
    phrases = sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql)
    return phrases

def find_phrases(phrases, phrase):
    if phrases:
        fophli = [pli for pli in phrases if phrase in pli[1]]
        return fophli

def show_phrases(phrases, start=0, end=10):
    rng = []
    
    if phrases:
        if start == 0 and end == 10:
            if len(phrases) >= 10:
                rng = list(range(10))
            else:
                rng = list(range(len(phrases)))
        else:
            rng = list(range(end - start))
    
    nphli = ['%s) %s: %s' % (li + start + 1, phrases[li + start][0], phrases[li + start][1]) for li in rng]
            
    return nphli

def get_pai_nicks(gch):
    cid = get_client_id()
    
    sql = 'SELECT nick FROM users ORDER BY uleave;'
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
    
    if qres:
        nicks = [nil[0] for nil in qres]
        return nicks
    return []

def get_ronoff_list(gch, param):
    ronoff_list = get_gch_param(gch, param, '')
    ronoff_list = str_to_list(ronoff_list)
        
    return ronoff_list

def set_ronoff_list(gch, param, ronoff_list):
    ronoff_list = list_to_str(ronoff_list) 
    set_gch_param(gch, param, ronoff_list)

def rmv_nick(gch, body):
    cid = get_client_id()
    
    body = body.strip()
    
    if not body: 
        return body
    
    conf_nicks = list(get_dict_fatal_var(cid, 'gchrosters', gch))
    nicks = get_pai_nicks(gch)
    nbli = body.split(',')
    nbli = [nbl.split(':') for nbl in nbli]
    nbli2 = []
    
    for nbl in nbli:
        nbli2.extend(nbl)
    
    nbli = [nbl.strip() for nbl in nbli2]
    
    fonil = []
    
    for nil in nicks:
        for nbl in nbli:
            if nil == nbl:
                fonil.append(nil)
    
    for nil in fonil:
        body = body.replace(nil, '', 1)
    
    body = body.strip()
    
    if not body: 
        return body
    
    for nil in conf_nicks:
        if nil in body.split(' ')[0]:
            fpar = body.split(' ')[0]
            body = body.replace(fpar, '', 1)
            break
    
    body = body.strip()
    
    if not body: 
        return body
    
    if len(body) >= 2:
        if body:
            while body[:1] == ':' or body[:1] == ',':
                body = body[1:].strip()
    elif len(body) == 1 and body in [':', ',']:
        body = ''
    
    body = body.strip()
    return body
    
def count_phrase(gch):
    cid = get_client_id()
    
    sql = 'SELECT id FROM phrases;'
    count = sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql)
    return count

def save_phrase(phrase, gch):
    cid = get_client_id()
    
    sql = "INSERT INTO phrases (phrase) VALUES (?);" 
    
    rep = sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql, phrase.strip())
    
    return rep

def del_phrase(phrase_id, gch):
    cid = get_client_id()
    
    if isinstance(phrase_id, int):
        sql = "DELETE FROM phrases WHERE id=?;"
        
        rep = sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql, phrase_id)
        
        return rep
    elif phrase_id.isdigit():
        sql = "DELETE FROM phrases WHERE id=?;"
        
        rep = sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql, phrase_id)
        
        return rep
    else:
        sql = "SELECT COUNT(id) FROM phrases WHERE phrase LIKE ?;"
        
        qres = sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql, '%{}%'.format(phrase_id))
        
        if qres:
            cnt = qres[0][0]
            
            if cnt:
                sql = "DELETE FROM phrases WHERE phrase LIKE ?;"
                
                sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql, '%{}%'.format(phrase_id))
                
            return cnt
        else:
            return ''

def get_reply(phrase, gch):
    cid = get_client_id()
    
    rep = ''
    rep_phrase = ''
    words = phrase.split(' ')
    
    keyword = words[random.randrange(len(words))]
    length = len(words)
    src = random.randrange(length)

    keyword = keyword[src:src + random.randrange(length) + 2]

    cid = get_client_id()

    sql = "SELECT * FROM phrases WHERE phrase LIKE ? ORDER BY RANDOM() LIMIT 1;"
    rep = sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql, '%{}%'.format(keyword))
    
    if rep:
        rep = list(rep[0])
        
        if len(rep) >= 2:
            rep_phrase = rep[1]
            
        set_fatal_var(cid, 'last_phrase_id', gch, rep[0])
    return rep_phrase.strip()

def get_pai_state(gch):
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/pai_phrases.db' % (cid, gch)):
        sql = 'CREATE TABLE phrases (id INTEGER PRIMARY KEY AUTOINCREMENT, phrase TEXT NOT NULL, UNIQUE(phrase));'
        sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX iphrases ON phrases (id, phrase);'
        sqlquery('dynamic/%s/%s/pai_phrases.db' % (cid, gch), sql)

    if not param_exists(gch, 'pai_on'):
        set_gch_param(gch, 'pai_on', '0')
        
    if not param_exists(gch, 'pai_learn'):
        set_gch_param(gch, 'pai_learn', '0')
        
    if not param_exists(gch, 'pai_occ'):
        set_gch_param(gch, 'pai_occ', '10')
        set_fatal_var(cid, 'pai_occ', gch, 90)
    else:
        pai_occ = 100 - int(get_gch_param(gch, 'pai_occ', '10'))
        set_fatal_var(cid, 'pai_occ', gch, pai_occ)
        
    if not param_exists(gch, 'pai_think'):
        set_gch_param(gch, 'pai_think', '5')
    
    if not param_exists(gch, 'pai_chpm'):
        set_gch_param(gch, 'pai_chpm', '350')
    
    if not param_exists(gch, 'pai_ron'):
        set_gch_param(gch, 'pai_ron', '')
        
    if not param_exists(gch, 'pai_roff'):
        set_gch_param(gch, 'pai_roff', '')

def handler_pai(type, source, body):
    cid = get_client_id()
    
    groupchat = source[1]
    pai_on = 0
    
    if is_groupchat(groupchat):
        pai_on = int(get_gch_param(groupchat, 'pai_on', '0'))
        
    if pai_on == 1:
        nick = source[2]
        conf_nicks = list(get_dict_fatal_var(cid, 'gchrosters', groupchat))
        bot_nick = get_bot_nick(groupchat)
        learning = int(get_gch_param(groupchat, 'pai_learn', '0'))
        occurrence_freq = int(get_gch_param(groupchat, 'pai_occ', '10'))
        chpm = int(get_gch_param(groupchat, 'pai_chpm', '350'))
        cprfx = get_comm_prefix(groupchat)
        
        chps = chpm / 60.0
        
        reply_on = get_ronoff_list(groupchat, 'pai_ron')
        reply_off = get_ronoff_list(groupchat, 'pai_roff')
        
        think = int(get_gch_param(groupchat, 'pai_think', '0'))		
        
        comm_alias = ''

        if body:
            comm_alias = body.split(' ')[0]
            command = ''
            
            if comm_alias.startswith(cprfx):
                command = comm_alias.replace(cprfx, '', 1)
            else:
                command = comm_alias
            
            cname = get_real_cmd_name(command) 

            if cname:
                command = cname

            if not is_var_set('commands', command):
                command = ''

        aliaso = get_fatal_var(cid, 'alias')
        
        if type == 'public' and not nick in reply_off:
            if (nick != bot_nick and nick) and not (command or comm_alias in aliaso.aliaslist[groupchat] or comm_alias in aliaso.galiaslist):
                
                if bot_nick in body:
                    body = rmv_nick(groupchat, body)
                    
                    if body:
                        comm_alias = body.split(' ')[0]
                    
                    if command or comm_alias in aliaso.aliaslist[groupchat] or comm_alias in aliaso.galiaslist:
                        return
                    
                    rep = get_reply(body, groupchat)
                    
                    if learning and body and len(body) <= 255 and len(body) >= 3:
                        if check_obscene_words(body) == False:
                            if body.split(' ')[0] == '/me':
                                for nki in conf_nicks:
                                    if nki in body:
                                        body = body.replace(nki, '%nick%')
                                        break
                            
                            if not body[0] in [cprfx, '*', '.', '-', '!']:
                                save_phrase(body, groupchat)
                        
                    if rep:
                        time.sleep(random.randrange(3, think))
                        time.sleep(len(rep) / chps)
                        
                        if rep.split(' ')[0] == '/me':
                            if '%nick%' in rep:
                                rep = rep.replace('%nick%', nick)
                            
                            return msg(groupchat, rep)
                        else:	
                            return reply(type, source, rep)
                elif [ron for ron in reply_on if ron in body] and not [roff for roff in reply_off if roff in body]:
                    rep = get_reply(body, groupchat)
                    
                    if rep:
                        time.sleep(random.randrange(3, think))
                        time.sleep(len(rep) / chps)
                        
                        if rep.split(' ')[0] == '/me':
                            if '%nick%' in rep:
                                rep = rep.replace('%nick%', nick)
                            
                            return msg(groupchat, rep)
                        else:	
                            return reply(type, source, rep)
                else:
                    if get_int_fatal_var(cid, 'pai_occ', groupchat) == 0:
                        paoc = 100 - occurrence_freq
                        set_fatal_var(cid, 'pai_occ', groupchat, paoc)
                        
                        body = rmv_nick(groupchat, body)
                        
                        rep = get_reply(body, groupchat)
                        
                        if learning and body and len(body) <= 255 and len(body) >= 3:
                            if check_obscene_words(body) == False:
                                if body.split(' ')[0] == '/me':
                                    for nki in conf_nicks:
                                        if nki in body:
                                            body = body.replace(nki, '%nick%')
                                            break
                            
                                if not body[0] in [cprfx, '*', '.', '-', '!']:
                                    save_phrase(body, groupchat)
                        
                        if rep:
                            time.sleep(random.randrange(3, think))
                            time.sleep(len(rep) / chps)
                            
                            if rep.split(' ')[0] == '/me':
                                if '%nick%' in rep:
                                    rep = rep.replace('%nick%', nick)
                                        
                                return msg(groupchat, rep)
                            else:	
                                return reply(type, source, rep)
                        return
                
                paoc = get_int_fatal_var(cid, 'pai_occ', groupchat)
                
                if paoc > 0:
                    paoc = paoc - 1
                    set_fatal_var(cid, 'pai_occ', groupchat, paoc)
        elif type == 'private':  # here private
            if nick != bot_nick and not (command or comm_alias in aliaso.aliaslist[groupchat] or comm_alias in aliaso.galiaslist):
                rep = get_reply(body, groupchat)
                
                if rep:
                    if rep.split(' ')[0] == '/me':
                        if '%nick%' in rep:
                            rep = rep.replace('%nick%', nick)

                    time.sleep(random.randrange(3, think))
                    time.sleep(len(rep) / chps)
                    return reply(type, source, rep)

def handler_pai_control(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))

        if int(parameters) > 1:
            return reply(type, source, l('Invalid syntax!'))

        if parameters == '1':
            set_gch_param(groupchat, 'pai_on', '1')
            return reply(type, source, l('Pseudo artificial intelligence has been turned on!'))
        else:
            set_gch_param(groupchat, 'pai_on', '0')
            return reply(type, source, l('Pseudo artificial intelligence has been turned off!'))
    else:
        paion = int(get_gch_param(groupchat, 'pai_on', '0'))
        
        if paion:
            return reply(type, source, l('Pseudo artificial intelligence is turned on!'))
        else:
            return reply(type, source, l('Pseudo artificial intelligence is turned off!'))

def handler_pai_learn(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))

        if int(parameters) > 1:
            return reply(type, source, l('Invalid syntax!'))

        if parameters == '1':
            set_gch_param(groupchat, 'pai_learn', '1')
            return reply(type, source, l('Pseudo artificial intelligence learning mode has been turned on!'))
        else:
            set_gch_param(groupchat, 'pai_learn', '0')
            return reply(type, source, l('Pseudo artificial intelligence learning mode has been turned off!'))
    else:
        pailearn = int(get_gch_param(groupchat, 'pai_learn', '0'))
        
        if pailearn:
            return reply(type, source, l('Pseudo artificial intelligence learning mode is turned on!'))
        else:
            return reply(type, source, l('Pseudo artificial intelligence learning mode is turned off!'))
            
def handler_pai_occ(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))

        if int(parameters) > 100:
            return reply(type, source, l('Invalid syntax!'))

        set_gch_param(groupchat, 'pai_occ', parameters)
        paiocc = 100 - int(parameters)
        set_fatal_var(cid, 'pai_occ', groupchat, paiocc)
        return reply(type, source, l('Level of reaction occurrence has been set to %s%%!') % (parameters))
    else:
        paiocc = get_gch_param(groupchat, 'pai_occ', '10')
        return reply(type, source, l('Level of reaction occurrence is set to %s%%!') % (paiocc))
            
def handler_pai_think(type, source, parameters):
    groupchat = source[1]

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))

        if int(parameters) > 100 or int(parameters) <= 3:
            return reply(type, source, l('Invalid syntax!'))

        set_gch_param(groupchat, 'pai_think', parameters)
        return reply(type, source, l('Think time before reaction occurrence has been set to %s sec.') % (parameters))
    else:
        paithink = get_gch_param(groupchat, 'pai_think', '5')
        return reply(type, source, l('Think time before reaction occurrence is set to %s sec.') % (paithink))

def handler_pai_chpm(type, source, parameters):
    groupchat = source[1]

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))

        if int(parameters) < 120 or int(parameters) > 600:
            return reply(type, source, l('Invalid syntax!'))

        set_gch_param(groupchat, 'pai_chpm', parameters)
        return reply(type, source, l('Pseudo char input speed has been set to %s chrs/min!') % (parameters))
    else:
        paichpm = get_gch_param(groupchat, 'pai_chpm', '350')
        return reply(type, source, l('Pseudo char input speed is set to %s chrs/min!') % (paichpm))

def handler_pai_ron(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    ron_list = parameters.split(' ')
    
    if parameters:
        if ',' in parameters or ':' in parameters:
            return reply(type, source, l('Invalid syntax!'))

        t_ron_list = get_ronoff_list(groupchat, 'pai_ron')
        ron_list = [ron for ron in ron_list if not ron in t_ron_list]	
            
        t_ron_list.extend(ron_list)
        
        roff_list = get_ronoff_list(groupchat, 'pai_roff')
        roff_list = [roff for roff in roff_list if not roff in ron_list]
        set_ronoff_list(groupchat, 'pai_roff', roff_list)
        set_ronoff_list(groupchat, 'pai_ron', t_ron_list)
        
        return reply(type, source, l('Reaction words and nicks has been added (total: %s): %s') % (len(ron_list), ', '.join(ron_list)))
    else:
        ron_list = get_ronoff_list(groupchat, 'pai_ron')
        
        if ron_list:
            return reply(type, source, l('Reaction words and nicks (total: %s):\n\n%s') % (len(ron_list), ', '.join(ron_list)))
        else:
            return reply(type, source, l('List of reaction words and nicks is empty!'))

def handler_pai_roff(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    roff_list = parameters.split(' ')
    
    if parameters:
        if ',' in parameters or ':' in parameters:
            return reply(type, source, l('Invalid syntax!'))

        t_roff_list = get_ronoff_list(groupchat, 'pai_roff')
        roff_list = [roff for roff in roff_list if not roff in t_roff_list]
            
        t_roff_list.extend(roff_list)
        
        ron_list = get_ronoff_list(groupchat, 'pai_ron')
        ron_list = [ron for ron in ron_list if not ron in roff_list]
        
        set_ronoff_list(groupchat, 'pai_roff', t_roff_list)
        set_ronoff_list(groupchat, 'pai_ron', ron_list)
        
        return reply(type, source, l('Ignoring words and nicks has been added (total: %s): %s') % (len(roff_list), ', '.join(roff_list)))
    else:
        roff_list = get_ronoff_list(groupchat, 'pai_roff')
        
        if roff_list:
            return reply(type, source, l('Ignoring words and nicks (total: %s):\n\n%s') % (len(roff_list), ', '.join(roff_list)))
        else:
            return reply(type, source, l('List of ignoring words and nicks is empty!'))

def handler_pai_roffd(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    roff_word = parameters.split(' ')[0]
    
    if parameters:
        if ',' in parameters or ':' in parameters:
            return reply(type, source, l('Invalid syntax!'))

        roff_list = get_ronoff_list(groupchat, 'pai_roff')
        
        if roff_word in roff_list:	
            roff_list.remove(roff_word)
            set_ronoff_list(groupchat, 'pai_roff', roff_list)
        else:
            return reply(type, source, l('Word not found!'))

        return reply(type, source, l('Word "%s" has been removed!') % (roff_word))
    else:
        roff_list = get_ronoff_list(groupchat, 'pai_roff')
        
        if roff_list:
            set_gch_param(groupchat, 'pai_roff', '')
            return reply(type, source, l('List of ignoring words and nicks has been cleared!'))
        else:
            return reply(type, source, l('List of ignoring words and nicks is empty!'))

def handler_pai_rond(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    ron_word = parameters.split(' ')[0]
    
    if parameters:
        if ',' in parameters or ':' in parameters:
            return reply(type, source, l('Invalid syntax!'))
      
        ron_list = get_ronoff_list(groupchat, 'pai_ron')	
            
        if ron_word in ron_list:	
            ron_list.remove(ron_word)
            set_ronoff_list(groupchat, 'pai_ron', ron_list)
        else:
            return reply(type, source, l('Word not found!'))

        return reply(type, source, l('Word "%s" has been removed!') % (ron_word))
    else:
        ron_list = get_ronoff_list(groupchat, 'pai_ron')
        
        if ron_list:
            set_gch_param(groupchat, 'pai_ron', '')
            return reply(type, source, l('List of reaction words and nicks has been cleared!'))
        else:
            return reply(type, source, l('List of reaction words and nicks is empty!'))

def handler_pai_add(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        res = save_phrase(parameters, groupchat)
        
        if not res:
            return reply(type, source, l('Phrase has been added!'))
        else:
            return reply(type, source, l('Insert error!'))
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_pai_del(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    parameters = parameters.strip()
    
    if parameters:
        res = del_phrase(parameters, groupchat)
        
        if res or res == [] or res == 0:
            if parameters.isdigit():
                return reply(type, source, l('Phrase number %s has been removed!') % (parameters))
            else:
                if len(parameters) >= 3:
                    if res:
                        return reply(type, source, l('Found and has been removed %s phrases!') % (res))
                    else:
                        return reply(type, source, l('Unable to find matches for remove!'))
                else:
                    return reply(type, source, l('Too short keyword or phrase, please specify some more than 3 characters long!'))
        else:
            return reply(type, source, l('Delete error!'))
    else:
        last_phid = get_int_fatal_var(cid, 'last_phrase_id', groupchat)
        
        res = del_phrase(last_phid, groupchat)
        
        if not res:
            return reply(type, source, l('Phrase number %s has been removed!') % (last_phid))
        else:
            return reply(type, source, l('Delete error!'))

def handler_pai_count(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    res = count_phrase(groupchat)
    count = len(res)
        
    if count:
        return reply(type, source, l('Total count of phrases: %s!') % (count))
    else:
        return reply(type, source, l('There are no phrases!'))

def handler_pai_show(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

#-----------------------Local Functions----------------------------------------
    
    def phrases_find(type, source, phrases, phrase):
        fophli = find_phrases(phrases, phrase)
                    
        if fophli:
            nphli = show_phrases(fophli)
            rep = l('Found phrases (total: %s):\n\n%s') % (len(nphli), '\n'.join(nphli))
            return reply(type, source, rep)	
        else:
            return reply(type, source, l('Phrases not found!'))

#--------------------End Of Local Functions------------------------------------
    
    phrases = get_pai_phrases(groupchat)
    tophs = len(phrases)
    
    if parameters:
        spltdp = parameters.split(' ', 1)
        nphrase = spltdp[0]
        
        if len(spltdp) == 1:
            if '-' in nphrase:
                nphrase = nphrase.split('-', 1)
                nphrase = [li for li in nphrase if li != '']
                
                if len(nphrase) == 2:
                    if nphrase[0].isdigit():
                        stn = int(nphrase[0])
                        
                        if not stn:
                            return reply(type, source, l('Invalid syntax!'))
                    else:
                        return phrases_find(type, source, phrases, parameters)

                    if nphrase[1].isdigit():
                        enn = int(nphrase[1])
                        
                        if enn > tophs:
                            return reply(type, source, l('Invalid range!'))
                    else:
                        return phrases_find(type, source, phrases, parameters)
                    
                    if stn > enn:
                        return reply(type, source, l('Invalid range!'))

                    head = ''
                    foot = ''
                            
                    if stn >= 2 and stn != enn:
                        head = l('[<---start---]\n\n')
                    
                    if enn < tophs and stn != enn:
                        foot = l('\n\n[---end--->]')
                    elif enn == tophs and tophs == 10:
                        foot = ''

                    nphli = show_phrases(phrases, stn - 1, enn)
                    rep = l('List of phrases (total: %s):\n\n%s%s%s') % (tophs, head, '\n'.join(nphli), foot)
                    return reply(type, source, rep)
            else:
                if nphrase.isdigit():
                    if int(nphrase) != 0 and int(nphrase) <= tophs:
                        nphrase = int(nphrase)
                        
                        nphli = show_phrases(phrases, nphrase - 1, nphrase)
                        rep = l('Phrase (total: %s):\n\n%s') % (tophs, '\n'.join(nphli))
                        return reply(type, source, rep)	
                    else:
                        return reply(type, source, l('Invalid syntax!'))
                else:
                    return phrases_find(type, source, phrases, nphrase)
        else:
            return phrases_find(type, source, phrases, parameters)
    else:
        foot = ''	
        
        if tophs > 10:
            foot = l('\n\n[---end--->]')
            
        nphli = show_phrases(phrases)
        
        if nphli:
            rep = l('List of phrases (total: %s):\n\n%s%s%s') % (tophs, '', '\n'.join(nphli), foot)
        else:
            rep = l('List of phrases is empty!')
        
        return reply(type, source, rep)

#-------------------------------------Handlers---------------------------------------------

register_command_handler(handler_pai_control, 'pai', 30)
register_command_handler(handler_pai_learn, 'pai_learn', 30)
register_command_handler(handler_pai_occ, 'pai_occ', 30)
register_command_handler(handler_pai_think, 'pai_think', 30)
register_command_handler(handler_pai_ron, 'pai_ron', 30)
register_command_handler(handler_pai_roff, 'pai_roff', 30)
register_command_handler(handler_pai_rond, 'pai_rond', 30)
register_command_handler(handler_pai_roffd, 'pai_roffd', 30)
register_command_handler(handler_pai_add, 'pai_add', 30)
register_command_handler(handler_pai_del, 'pai_del', 30)
register_command_handler(handler_pai_count, 'pai_count', 30)
register_command_handler(handler_pai_chpm, 'pai_chpm', 30)
register_command_handler(handler_pai_show, 'pai_show', 30)

register_stage1_init(get_pai_state)
register_message_handler(handler_pai)
