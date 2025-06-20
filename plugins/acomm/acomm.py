# -*- coding: utf-8 -*-

#  fatal plugin
#  acomm plugin

#  Copyright © 2009-2024 Ancestors Soft

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

def comp_acomm_rexps(gch=''):
    cid = get_client_id()
    
    qli = get_all_rules(gch)
    
    if qli != '':
        bpts = []
        cpts = []
        spts = []
        npts = []
        jpts = []
        ival = 300
        
        for acomm in qli:
            rid = '%s' % (acomm[0])
            
            entity = acomm[1]
            
            if '/' in entity:
                entity = entity.split('/')
                ival = entity[1].strip()
                entity = entity[0]

                if ival.isdigit():
                    ival = int(ival) * 60
                else:
                    ival = 300

            exp = acomm[2]
            command = acomm[3]
            params = acomm[4]
            
            try:
                if not entity == 'cvar':
                    exp = re.compile(exp)
            except Exception:
                exp = None
            
            if entity == 'body':
                bpts.append((rid, exp, command, params))
            elif entity == 'caps':
                cpts.append((rid, exp, command, params))
            elif entity == 'status':
                spts.append((rid, exp, command, params))
            elif entity == 'nick':
                npts.append((rid, exp, command, params))
            elif entity == 'jid':
                jpts.append((rid, exp, command, params))
            elif entity == 'cvar':
                add_fatal_task('check_changed_var%s' % (rid), check_cvar_val, (gch, exp, command, params), ival=ival)
        
        if not is_groupchat(gch):
            return
        
        set_fatal_var(cid, 'comp_acomm_exp', gch, 'body', bpts)
        set_fatal_var(cid, 'comp_acomm_exp', gch, 'caps', cpts)
        set_fatal_var(cid, 'comp_acomm_exp', gch, 'status', spts)
        set_fatal_var(cid, 'comp_acomm_exp', gch, 'nick', npts)
        set_fatal_var(cid, 'comp_acomm_exp', gch, 'jid', jpts)

def rmv_acomm_rule(gch, rid):
    cid = get_client_id()
    
    sql = "DELETE FROM acomm WHERE id=?;"

    dbp = 'dynamic/%s/%s/acomm.db' % (cid, gch)

    if not is_groupchat(gch):
        dbp = 'dynamic/%s/acomm.db' % (cid)

    qres = sqlquery(dbp, sql, rid)

    return qres

def rmv_all_rules(gch=''):
    cid = get_client_id()
    
    sql = 'DELETE FROM acomm;'
    
    dbp = 'dynamic/%s/%s/acomm.db' % (cid, gch)

    if not is_groupchat(gch):
        dbp = 'dynamic/%s/acomm.db' % (cid)
    
    qres = sqlquery(dbp, sql)

    return qres

def get_all_rules(gch=''):
    cid = get_client_id()

    sql = 'SELECT * FROM acomm;'

    dbp = 'dynamic/%s/%s/acomm.db' % (cid, gch)

    if not is_groupchat(gch):
        dbp = 'dynamic/%s/acomm.db' % (cid)
    
    qres = sqlquery(dbp, sql)
    return qres

def get_acomm_rules(gch, entity):
    cid = get_client_id()

    sql = "SELECT exp, command, params FROM acomm WHERE entity=?;"

    dbp = 'dynamic/%s/%s/acomm.db' % (cid, gch)

    if not is_groupchat(gch):
        dbp = 'dynamic/%s/acomm.db' % (cid)

    qres = sqlquery(dbp, sql, entity)
    return qres

def set_acomm_rule(gch, entity, exp, command, params=''):
    cid = get_client_id()

    sql = "INSERT INTO acomm (entity, exp, command, params) VALUES (?, ?, ?, ?);"
    
    args = entity.strip(), exp.strip(), command.strip(), params.strip()

    dbp = 'dynamic/%s/%s/acomm.db' % (cid, gch)

    if not is_groupchat(gch):
        dbp = 'dynamic/%s/acomm.db' % (cid)

    qres = sqlquery(dbp, sql, *args)

    return qres

def handler_acomm_body(type, source, body):
    cid = get_client_id()
    
    groupchat = source[1]
    snick = source[2]
    bnick = get_bot_nick(groupchat)
    sjid = get_true_jid(source)

    if not is_groupchat(groupchat) or sjid == cid or snick == bnick:
        return
    
    if type == 'public':
        bpts = list(get_dict_fatal_var(cid, 'comp_acomm_exp', groupchat, 'body'))
        
        for bpli in bpts:
            exp = bpli[1]
            comm = bpli[2]
            params = bpli[3]
            
            acomm = get_real_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            params = srepl(params, '%nick%', snick)
            params = srepl(params, '%jid%', sjid)
            params = srepl(params, '%groupchat%', groupchat)
            params = srepl(params, '%body%', body)
            
            if is_var_set('commands', rcomm) and exp:
                if exp.findall(body):
                    call_command_handlers(rcomm, 'null', source, params, rcomm)

def handler_acomm_status(prs):
    cid = get_client_id()
    
    groupchat = get_stripped(prs.getFrom())
    snick = get_resource(prs.getFrom())
    bnick = get_bot_nick(groupchat)
    sjid = get_true_jid(groupchat + '/' + snick)

    if not is_groupchat(groupchat) or sjid == cid or snick == bnick:
        return
    
    status = prs.getStatus()
    spts = list(get_dict_fatal_var(cid, 'comp_acomm_exp', groupchat, 'status'))
    npts = list(get_dict_fatal_var(cid, 'comp_acomm_exp', groupchat, 'nick'))

    for spli in spts:
        if not status:
            break
        
        exp = spli[1]
        comm = spli[2]
        params = spli[3]
        
        acomm = get_real_cmd_name(comm)
        rcomm = comm
        
        if acomm:
            rcomm = acomm
        
        params = srepl(params, '%nick%', snick)
        params = srepl(params, '%jid%', sjid)
        params = srepl(params, '%groupchat%', groupchat)
        params = srepl(params, '%status%', status)

        if is_var_set('commands', rcomm) and exp:
            if exp.findall(status):
                cmd_hnd = get_fatal_var('command_handlers', rcomm)
                source = [groupchat + '/' + snick, groupchat, snick]
                cmd_hnd('null', source, params)
    
    scode = prs.getStatusCode()
    ptype = prs.getType()

    if scode == '303' and ptype == 'unavailable':
        newnick = prs.getNick()
        
        for npli in npts:
            exp = npli[1]
            comm = npli[2]
            params = npli[3]
            
            acomm = get_real_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            params = srepl(params, '%nick%', newnick)
            params = srepl(params, '%jid%', sjid)
            params = srepl(params, '%groupchat%', groupchat)
            
            if is_var_set('commands', rcomm) and exp:
                if exp.findall(newnick):
                    cmd_hnd = get_fatal_var('command_handlers', rcomm)
                    source = [groupchat + '/' + newnick, groupchat, newnick]
                    cmd_hnd('null', source, params)

def handler_acomm_join_jn(groupchat, nick, aff, role):
    cid = get_client_id()
    
    snick = nick
    bnick = get_bot_nick(groupchat)
    sjid = get_true_jid(groupchat + '/' + snick)

    fjid = get_fatal_var(cid, 'gchrosters', groupchat, nick, 'rjid')
    caps = get_fatal_var(cid, 'gchrosters', groupchat, nick, 'caps')
    if sjid == cid or snick == bnick:
        return

    jpts = list(get_dict_fatal_var(cid, 'comp_acomm_exp', groupchat, 'jid'))
    npts = list(get_dict_fatal_var(cid, 'comp_acomm_exp', groupchat, 'nick'))
    cpts = list(get_dict_fatal_var(cid, 'comp_acomm_exp', groupchat, 'caps'))
    
    for jpli in jpts:
        exp = jpli[1]
        comm = jpli[2]
        params = jpli[3]
        
        acomm = get_real_cmd_name(comm)
        rcomm = comm
        
        if acomm:
            rcomm = acomm
        
        params = srepl(params, '%nick%', snick)
        params = srepl(params, '%jid%', sjid)
        params = srepl(params, '%fjid%', fjid)
        params = srepl(params, '%groupchat%', groupchat)
        
        if is_var_set('commands', rcomm) and exp:
            if fjid:
                if exp.findall(fjid):
                    cmd_hnd = get_fatal_var('command_handlers', rcomm)
                    source = [groupchat + '/' + snick, groupchat, snick]
                    cmd_hnd('null', source, params)
                
    for npli in npts:
        exp = npli[1]
        comm = npli[2]
        params = npli[3]
        
        acomm = get_real_cmd_name(comm)
        rcomm = comm
        
        if acomm:
            rcomm = acomm
            
        params = srepl(params, '%nick%', snick)
        params = srepl(params, '%jid%', sjid)
        params = srepl(params, '%fjid%', fjid)
        params = srepl(params, '%groupchat%', groupchat)
        
        if is_var_set('commands', rcomm) and exp:
            if exp.findall(snick):
                cmd_hnd = get_fatal_var('command_handlers', rcomm)
                source = [groupchat + '/' + snick, groupchat, snick]
                cmd_hnd('null', source, params)
                
    for cpli in cpts:
        exp = cpli[1]
        comm = cpli[2]
        params = cpli[3]
        
        acomm = get_real_cmd_name(comm)
        rcomm = comm
        
        if acomm:
            rcomm = acomm
            
        params = srepl(params, '%nick%', snick)
        params = srepl(params, '%jid%', sjid)
        params = srepl(params, '%fjid%', fjid)
        params = srepl(params, '%groupchat%', groupchat)

        if is_var_set('commands', rcomm) and exp:
            if caps:
                capsvals = ' '.join(caps.values())
                if exp.findall(capsvals):
                    cmd_hnd = get_fatal_var('command_handlers', rcomm)
                    source = [groupchat + '/' + snick, groupchat, snick]
                    cmd_hnd('null', source, params)

def check_cvar_val(groupchat, rexp, comm, params):
    gchp = get_md5(rexp)
    
    gch = groupchat
    
    if not is_groupchat(groupchat):
        groupchat = ''
    
    if param_exists(groupchat, gchp):
        if not is_groupchat(groupchat):
            groupchat = gch
            oval = get_param(gchp)
        else:
            oval = get_gch_param(groupchat, gchp)
        
        spov = oval.split(':=', 1)
        gch_jid = spov[0]
        oval = spov[1]
        
        nval = oval
        
        source = [gch_jid, groupchat, '']
        
        try:
            cn = gcp('comm_nested', '#')
            rec = rexp.count(cn)

            if (rec // 2) >= 1:
                nval = rep_nested_cmds('null', source, rexp)
            else:
                nval = eval(rexp)
            
            nval = nval.strip()
        except Exception:
            return False
        
        if nval == rexp:
            return False
        
        if (nval == '') or (oval == ''):
            return False
        
        if nval != oval and nval != '-1':
            if not is_groupchat(groupchat):
                set_param(gchp, '%s:=%s' % (gch_jid, nval))
            else:
                set_gch_param(groupchat, gchp, '%s:=%s' % (gch_jid, nval))
            
            call_command_handlers(comm, 'null', source, params.strip(), comm)

def handler_acomm_control(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if parameters:
        strp = parameters.strip()
        
        if len(strp) == 1 and strp == '-':
            qli = get_all_rules(groupchat)
            res = rmv_all_rules(groupchat)
            
            if res != '':
                comp_acomm_rexps(groupchat)
                
                for li in qli:
                    if li[1].startswith('cvar'):
                        gpar = get_md5(li[2])
                        rmv_gch_param(groupchat, gpar)
                        rmv_fatal_task('check_changed_var%s' % (li[0]))
                
                return reply(type, source, l('List of auto-command rules has been cleared!'))
            else:
                return reply(type, source, l('Delete error!'))
        elif len(strp) > 1 and strp[:1] == '-' and strp[1:].isdigit():
            rnum = int(strp[1:])
            res = get_all_rules(groupchat)
            
            if res:
                if rnum <= len(res) and rnum > 0:
                    dnum = res[rnum - 1]
                    rid = dnum[0]
                    
                    res = rmv_acomm_rule(groupchat, rid)
                    
                    if dnum[1].startswith('cvar'):
                        gpar = get_md5(dnum[2])
                        rmv_gch_param(groupchat, gpar)
                        rmv_fatal_task('check_changed_var%s' % (rid))
                    
                    if res != '':
                        comp_acomm_rexps(groupchat)
                        
                        return reply(type, source, l('Auto-command rule has been removed!'))
                    else:
                        return reply(type, source, l('Delete error!'))
                else:
                    return reply(type, source, l('Invalid number of auto-command rule!'))
            else:
                if res == '':
                    return reply(type, source, l('Unknown error!'))
                else:
                    return reply(type, source, l('List of auto-command rules is empty!'))
        else:
            ulvl = user_level(source, groupchat)
            prsr = parse_cmd_params(strp)
            
            entity = prsr[0]
            
            ival = 300
            
            if '/' in entity:
                entity = entity.split('/')
                ival = entity[1].strip()
                entity = entity[0]

                if ival.isdigit():
                    ival = int(ival) * 60
                else:
                    ival = 300
            
            rexp = prsr[1]
            cmdpr = prsr[2]
            
            if not entity or not entity in ('body', 'status', 'nick', 'jid', 'cvar', 'caps'):
                entity = 'body'
            
            if not is_groupchat(groupchat) and entity in ('body', 'status', 'nick', 'jid', 'caps'):
                return reply(type, source, l('This groups of acomm command allowed only in groupchats!'))                
            
            if not rexp:
                return reply(type, source, l('Regular expression has not specified!'))
            
            if not cmdpr:
                return reply(type, source, l('Command has not specified!'))
            
            aliaso = get_fatal_var(cid, 'alias')
            splcp = safe_split(cmdpr, ' ')
            
            comm = splcp[0]
            params = splcp[1]
            
            acomm = get_real_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            if is_var_set('commands', rcomm):
                cacc = get_int_fatal_var('commands', rcomm, 'access')
                
                racc = int(get_cmd_access(rcomm))
                
                if racc < 0:
                    racc = cacc
                
                if racc > ulvl:
                    return reply(type, source, l('Too few rights to use this command!'))
            elif rcomm in aliaso.galiaslist:
                alac = aliaso.gaccesslist[rcomm]
                
                if alac > ulvl:
                    return reply(type, source, l('Too few rights to use this alias!'))
            elif rcomm in aliaso.aliaslist[groupchat]:
                alac = aliaso.accesslist[groupchat][rcomm]
                
                if alac > ulvl:
                    return reply(type, source, l('Too few rights to use this alias!'))
            else:
                return reply(type, source, l('Command or alias not found!'))

            fent = ''

            if ival != 300:
                fent = '/%d' % (ival / 60)

            res = set_acomm_rule(groupchat, entity + fent, rexp, comm, params)
            
            if res != '':
                qli = get_all_rules(groupchat)
                rid = 0
                
                if qli:
                    rid = qli[-1][0]

            if entity == 'cvar':
                try:
                    cn = gcp('comm_nested', '#')
                    rec = rexp.count(cn)

                    if (rec // 2) >= 1:
                        cvar = rep_nested_cmds('null', source, rexp)
                    else:
                        cvar = eval(rexp)
                    
                    cvar = cvar.strip()
                    
                    trjid = get_true_jid(source)
                    
                    gchp = get_md5(rexp)
                    
                    if not is_groupchat(groupchat):
                        set_param(gchp, '%s:=%s' % (trjid, cvar))
                    else:
                        set_gch_param(groupchat, gchp, '%s:=%s' % (trjid, cvar))
                    
                    add_fatal_task('check_changed_var%s' % (rid), check_cvar_val, (groupchat, rexp, comm, params), ival=ival)
                except Exception:
                    log_exc_error()
                    res = ''
                
            if res != '':
                if not entity == 'cvar':
                    comp_acomm_rexps(groupchat)
                
                return reply(type, source, l('Auto-command rule has been added!'))
            else:
                return reply(type, source, l('Insert error!'))
    else:
        res = get_all_rules(groupchat)
            
        if res:
            rlst = ['%s: %s := %s %s' % (rli[1], rli[2], rli[3], rli[4]) for rli in res]
            nrl = get_num_list(rlst)
            rep = l('List of auto-command rules (total: %s):\n\n%s') % (len(nrl), '\n'.join(nrl))
            
            if type == 'public':
                reply(type, source, l('Look in private!'))
            
            return reply('private', source, rep)
        else:
            if res == '':
                return reply(type, source, l('Unknown error!'))
            else:
                return reply(type, source, l('List of auto-command rules is empty!'))
                
def handler_random_nick(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
       
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    bnick = get_bot_nick(groupchat) 
        
    nickl = get_list_fatal_var(cid, 'gchrosters', groupchat)
    
    nickl = [li for li in nickl if li != bnick] 
    
    rnm = random.randrange(0, len(nickl)) 
    
    if type == 'public':
        return msg(groupchat, nickl[rnm])
    return reply(type, source, nickl[rnm])    
                
def init_acomm_db(gch):
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/acomm.db' % (cid, gch)):
        sql = '''CREATE TABLE acomm(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    entity VARCHAR NOT NULL,
                                    exp VARCHAR NOT NULL,
                                    command VARCHAR NOT NULL,
                                    params VARCHAR);'''
                    
        sqlquery('dynamic/%s/%s/acomm.db' % (cid, gch), sql)
        
        sql = 'CREATE INDEX iacomm ON acomm (id);'
        sqlquery('dynamic/%s/%s/acomm.db' % (cid, gch), sql)

    comp_acomm_rexps(gch)

def init_acomm_rdb():
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/acomm.db' % (cid)):
        sql = '''CREATE TABLE acomm(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    entity VARCHAR NOT NULL,
                                    exp VARCHAR NOT NULL,
                                    command VARCHAR NOT NULL,
                                    params VARCHAR);'''
                    
        sqlquery('dynamic/%s/acomm.db' % (cid), sql)
        
        sql = 'CREATE INDEX iacomm ON acomm (id);'
        sqlquery('dynamic/%s/acomm.db' % (cid), sql)
    
    comp_acomm_rexps()

register_stage0_init(init_acomm_rdb)
register_stage1_init(init_acomm_db)
register_presence_handler(handler_acomm_status)
register_join_handler(handler_acomm_join_jn)
register_message_handler(handler_acomm_body)

register_command_handler(handler_acomm_control, 'acomm', 20)
register_command_handler(handler_random_nick, 'rnick', 20)
