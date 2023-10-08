# -*- coding: utf-8 -*-

#  fatal plugin
#  censor plugin

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
from muc import kick, ban, visitor, del_banned

def comp_gcensor_rexps():
    cid = get_client_id()
    
    gqli = get_all_rules()
    
    if gqli != '':
        cpts = []
        
        for cexp in gqli:
            rid = '%s' % (cexp[0])
            exp = cexp[1]
            reason = cexp[2]
            
            try:
                exp = re.compile(exp)
            except Exception:
                exp = None
            
            cpts.append((rid, exp, reason))
                
        set_fatal_var(cid, 'comp_gcensor_exp', cpts)

def comp_censor_rexps(gch):
    cid = get_client_id()
    
    qli = get_all_rules(gch)
    
    if qli != '':
        cpts = []
        
        for cexp in qli:
            rid = '%s' % (cexp[0])
            exp = cexp[1]
            reason = cexp[2]
            
            try:
                exp = re.compile(exp)
            except Exception:
                exp = None
            
            cpts.append((rid, exp, reason))
                
        set_fatal_var(cid, 'comp_censor_exp', gch, cpts)

def rmv_censor_rule(gch, rid):
    sql = "DELETE FROM censor WHERE id=?;"
    
    cid = get_client_id()
    
    if gch: 
        qres = sqlquery('dynamic/%s/%s/censor.db' % (cid, gch), sql, rid)
    else:
        qres = sqlquery('dynamic/%s/gcensor.db' % (cid), sql, rid)
        
    return qres

def rmv_all_rules(gch=''):
    sql = 'DELETE FROM censor;'
    
    cid = get_client_id()
    
    if gch: 
        qres = sqlquery('dynamic/%s/%s/censor.db' % (cid, gch), sql)
    else:
        qres = sqlquery('dynamic/%s/gcensor.db' % (cid), sql)

    return qres

def get_all_rules(gch=''):
    sql = 'SELECT * FROM censor;'
    
    cid = get_client_id()
    
    if gch:
        qres = sqlquery('dynamic/%s/%s/censor.db' % (cid, gch), sql)
    else:
        qres = sqlquery('dynamic/%s/gcensor.db' % (cid), sql)
    
    return qres

def set_censor_rule(gch, exp, reason=''):
    sql = "INSERT INTO censor (exp, reason) VALUES (?, ?);"
    args = exp.strip(), reason.strip()
    
    cid = get_client_id()
    
    if gch: 
        qres = sqlquery('dynamic/%s/%s/censor.db' % (cid, gch), sql, *args)
    else:
        qres = sqlquery('dynamic/%s/gcensor.db' % (cid), sql, *args)

    return qres

def handler_censor_body(type, source, body):
    cid = get_client_id()
    
    groupchat = source[1]
    snick = source[2]
    sjid = get_true_jid(source)
    bjid = get_client_id()
    ulvl = user_level(source, groupchat)

    if not is_groupchat(groupchat) or sjid == bjid or ulvl > 11:
        return
    
    if type == 'public':
        gcpts = list(get_dict_fatal_var(cid, 'comp_gcensor_exp'))
        cpts = list(get_dict_fatal_var(cid, 'comp_censor_exp', groupchat))
        gcpts.extend(cpts)
        cpts = gcpts
        
        cres = get_gch_param(groupchat, 'censor_result', 'kick')
        
        for cpli in cpts:
            exp = cpli[1]
            reason = cpli[2]
            
            if reason:
                reason = l('Invalid message: %s') % (reason)
            else:
                reason = l('Invalid message!')
            
            if exp:
                if exp.findall(body):
                    if cres == 'kick':
                        kick(groupchat, snick, reason)
                    elif cres == 'ban':
                        del_banned(groupchat, snick)
                        ban(groupchat, sjid, reason)
                    elif cres == 'visitor':
                        visitor(groupchat, snick, reason)
                        reply(type, source, reason)
                    elif cres == 'warn':
                        reply(type, source, reason)
      
def handler_censor_status(prs):
    cid = get_client_id()
    
    frmjid = prs.getFrom()
    groupchat = get_stripped(frmjid)
    snick = get_resource(frmjid)
    source = [groupchat + '/' + snick, groupchat, snick]
    sjid = get_true_jid(source)
    bjid = get_client_id()
    ulvl = user_level(source, groupchat)

    if not is_groupchat(groupchat) or sjid == bjid or ulvl > 11:
        return
    
    status = prs.getStatus()
    
    gcpts = list(get_dict_fatal_var(cid, 'comp_gcensor_exp'))
    cpts = list(get_dict_fatal_var(cid, 'comp_censor_exp', groupchat))
    gcpts.extend(cpts)
    cpts = gcpts

    cres = get_gch_param(groupchat, 'censor_result', 'kick')

    for cpli in cpts:
        if not status:
            break
        
        exp = cpli[1]
        reason = cpli[2]
        
        if reason:
            reason = l('Invalid status: %s') % (reason)
        else:
            reason = l('Invalid status!')
        
        if exp:
            if exp.findall(status):
                if cres == 'kick':
                    kick(groupchat, snick, reason)
                elif cres == 'ban':
                    del_banned(groupchat, snick)
                    ban(groupchat, sjid, reason)
                elif cres == 'visitor':
                    visitor(groupchat, snick, reason)
                    reply(type, source, reason)
                elif cres == 'warn':
                    reply(type, source, reason)
    
    scode = prs.getStatusCode()
    ptype = prs.getType()

    if scode == '303' and ptype == 'unavailable':
        newnick = prs.getNick()
        source = [groupchat + '/' + newnick, groupchat, newnick]
        
        for cpli in cpts:
            exp = cpli[1]
            reason = cpli[2]
            
            if reason:
                reason = l('Invalid nick: %s') % (reason)
            else:
                reason = l('Invalid nick!')
            
            if exp:
                if exp.findall(newnick):
                    if cres == 'kick':
                        kick(groupchat, newnick, reason)
                    elif cres == 'ban':
                        del_banned(groupchat, snick)
                        del_banned(groupchat, newnick)
                        ban(groupchat, sjid, reason)
                    elif cres == 'visitor':
                        visitor(groupchat, newnick, reason)
                        reply(type, source, reason)
                    elif cres == 'warn':
                        reply(type, source, reason)

def handler_censor_join(groupchat, nick, aff, role):
    cid = get_client_id()
    
    snick = nick
    source = [groupchat + '/' + snick, groupchat, snick]
    sjid = get_true_jid(source)
    bjid = get_client_id()
    ulvl = user_level(source, groupchat)

    if sjid == bjid or ulvl > 11:
        return

    gcpts = list(get_dict_fatal_var(cid, 'comp_gcensor_exp'))
    cpts = list(get_dict_fatal_var(cid, 'comp_censor_exp', groupchat))
    gcpts.extend(cpts)
    cpts = gcpts    
    
    cres = get_gch_param(groupchat, 'censor_result', 'kick')
    
    for cpli in cpts:
        exp = cpli[1]
        reason = cpli[2]
        
        if reason:
            reason = l('Invalid nick: %s') % (reason)
        else:
            reason = l('Invalid nick!')
        
        if exp:
            if exp.findall(snick):
                if cres == 'kick':
                    kick(groupchat, snick, reason)
                elif cres == 'ban':
                    del_banned(groupchat, snick)
                    ban(groupchat, sjid, reason)
                elif cres == 'visitor':
                    visitor(groupchat, snick, reason)
                    reply(type, source, reason)
                elif cres == 'warn':
                    reply(type, source, reason)

def handler_censor_control(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
    
    if parameters:
        strp = parameters.strip()
        
        if len(strp) == 1 and strp == '-':
            res = rmv_all_rules(groupchat)
            
            if res != '':
                comp_censor_rexps(groupchat)
                
                return reply(type, source, l('List of censor rules has been cleared!'))
            else:
                return reply(type, source, l('Delete error!'))
        elif len(strp) > 1 and strp[:1] == '-' and strp[1:].isdigit():
            rnum = int(strp[1:])
            res = get_all_rules(groupchat)
            
            if res:
                if rnum <= len(res) and rnum > 0:
                    dnum = res[rnum - 1]
                    rid = dnum[0]
                    
                    res = rmv_censor_rule(groupchat, rid)
                    
                    if res != '':
                        comp_censor_rexps(groupchat)
                        
                        return reply(type, source, l('Censor rule has been removed!'))
                    else:
                        return reply(type, source, l('Delete error!'))
                else:
                    return reply(type, source, l('Invalid number of censor rule!'))
            else:
                if res == '':
                    return reply(type, source, l('Unknown error!'))
                else:
                    return reply(type, source, l('List of censor rules is empty!'))
        else:
            prsr = safe_split(strp)
            
            rexp = prsr[0]
            reason = prsr[1]
            
            if not rexp:
                return reply(type, source, l('Regular expression has not specified!'))
                
            res = set_censor_rule(groupchat, rexp, reason)

            if res != '':
                comp_censor_rexps(groupchat)
                
                return reply(type, source, l('Censor rule has been added!'))
            else:
                return reply(type, source, l('Insert error!'))
    else:
        res = get_all_rules(groupchat)
            
        if res:
            rlst = []
            
            for rli in res:
                if rli[2]:
                    rlst.append(l('%s / Reason: %s') % (rli[1], rli[2]))
                else:
                    rlst.append(rli[1])
                    
            nrl = get_num_list(rlst)
            rep = l('List of censor rules (total: %s):\n\n%s') % (len(nrl), '\n'.join(nrl))
            
            if type == 'public':
                reply(type, source, l('Look in private!'))
            
            return reply('private', source, rep)
        else:
            if res == '':
                return reply(type, source, l('Unknown error!'))
            else:
                return reply(type, source, l('List of censor rules is empty!'))

def handler_gcensor_control(type, source, parameters):
    if parameters:
        strp = parameters.strip()
        
        if len(strp) == 1 and strp == '-':
            res = rmv_all_rules()
            
            if res != '':
                comp_gcensor_rexps()
                
                return reply(type, source, l('List of global censor rules has been cleared!'))
            else:
                return reply(type, source, l('Delete error!'))
        elif len(strp) > 1 and strp[:1] == '-' and strp[1:].isdigit():
            rnum = int(strp[1:])
            res = get_all_rules()
            
            if res:
                if rnum <= len(res) and rnum > 0:
                    dnum = res[rnum - 1]
                    rid = dnum[0]
                    
                    res = rmv_censor_rule('', rid)
                    
                    if res != '':
                        comp_gcensor_rexps()
                        
                        return reply(type, source, l('Global censor rule has been removed!'))
                    else:
                        return reply(type, source, l('Delete error!'))
                else:
                    return reply(type, source, l('Invalid number of global censor rule!'))
            else:
                if res == '':
                    return reply(type, source, l('Unknown error!'))
                else:
                    return reply(type, source, l('List of global censor rules is empty!'))
        else:
            prsr = safe_split(strp)
            
            rexp = prsr[0]
            reason = prsr[1]
            
            if not rexp:
                return reply(type, source, l('Regular expression has not specified!'))
                
            res = set_censor_rule('', rexp, reason)

            if res != '':
                comp_gcensor_rexps()
                
                return reply(type, source, l('Global censor rule has been added!'))
            else:
                return reply(type, source, l('Insert error!'))
    else:
        res = get_all_rules()
            
        if res:
            rlst = []
            
            for rli in res:
                if rli[2]:
                    rlst.append(l('%s / Reason: %s') % (rli[1], rli[2]))
                else:
                    rlst.append(rli[1])
            
            nrl = get_num_list(rlst)
            rep = l('List of global censor rules (total: %s):\n\n%s') % (len(nrl), '\n'.join(nrl))
            
            if type == 'public':
                reply(type, source, l('Look in private!'))
            
            return reply('private', source, rep)
        else:
            if res == '':
                return reply(type, source, l('Unknown error!'))
            else:
                return reply(type, source, l('List of global censor rules is empty!'))

def handler_censor_result(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    parameters = parameters.strip()

    if parameters:
        if not parameters in ['ignore', 'warn', 'kick', 'ban', 'visitor']:
            return reply(type, source, l('Invalid syntax!'))
        
        set_gch_param(groupchat, 'censor_result', parameters)
        return reply(type, source, l('Censor result action has been set to %s!') % (parameters))
    else:
        cenres = get_gch_param(groupchat, 'censor_result', 'ignore')
        return reply(type, source, l('Censor result action is set to %s.') % (cenres))         
    
def init_censor_db(gch):
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/censor.db' % (cid, gch)):
        sql = '''CREATE TABLE censor(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     exp VARCHAR NOT NULL,
                                     reason VARCHAR);'''
                                     
        sqlquery('dynamic/%s/%s/censor.db' % (cid, gch), sql)
        
        sql = 'CREATE INDEX icensor ON censor (id);'
        sqlquery('dynamic/%s/%s/censor.db' % (cid, gch), sql)
        
    if not param_exists(gch, 'censor_result'):
        set_gch_param(gch, 'censor_result', 'kick')

    comp_censor_rexps(gch)

def init_gcensor_db():
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/gcensor.db' % (cid)):
        sql = '''CREATE TABLE censor(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     exp VARCHAR NOT NULL, 
                                     reason VARCHAR);'''
                                     
        sqlquery('dynamic/%s/gcensor.db' % (cid), sql)
        
        sql = 'CREATE INDEX icensor ON censor (id);'
        sqlquery('dynamic/%s/gcensor.db' % (cid), sql)
    
    comp_gcensor_rexps()

register_stage0_init(init_gcensor_db)
register_stage1_init(init_censor_db)
register_presence_handler(handler_censor_status)
register_join_handler(handler_censor_join)
register_message_handler(handler_censor_body)

register_command_handler(handler_gcensor_control, 'gcensor', 100)
register_command_handler(handler_censor_control, 'censor', 20)
register_command_handler(handler_censor_result, 'cresult', 20)
