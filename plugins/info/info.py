# -*- coding: utf-8 -*-

#  fatal plugin
#  info plugin

#  Initial Copyright © 2007 Als <Als@exploru.net>
#  Parts of code Copyright © Bohdan Turkynewych aka Gh0st <tb0hdan[at]gmail.com>
#  Copyright © 2009-2016 Ancestors Soft

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
from math import trunc

def get_and_out_jids(type, source, gch, affiliation, succstr, failstr):
    iq = xmpp.Iq('get')
    Id = 'jids%s' % (time.time())
    iq.setID(Id)
    iq.setTo(gch)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    query.addChild('item', {'affiliation': affiliation})
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    jconn.SendAndCallForResponse(iq, get_jid_answ, {'type': type, 'source': source, 'succ': succstr, 'fail': failstr, 'sId': Id})

def get_jid_answ(coze, res, type, source, succ, fail, sId):
    try:
        if res:
            Id = res.getID()
            if not Id == sId:
                return reply(type, source, l('Unknown error!'))
            
            ptype = res.getType()
            
            if ptype == 'result':
                if type == 'public':
                    reply(type, source, l('Look in private!'))
                
                njids = parse_stanza(res)
                
                if njids:
                    rep = succ % (len(njids), '\n'.join(njids))
                else:
                    rep = fail
                    
                if type == 'console':
                    reply(type, source, rep)
                else:
                    return reply('private', source, rep)
            else:
                return reply(type, source, l('Unknown error!'))
    except Exception:
        log_exc_error()
        return reply(type, source, l('Unknown error!'))
                
def parse_stanza(stanza):
    if stanza:
        itlist = stanza.getTag('query').getTags('item')
        jlist = [li.getAttr('jid') for li in itlist]
        jlist.sort()
        rng = list(range(len(jlist)))
        njlist = ['%s) %s' % (li + 1, jlist[li]) for li in rng]
        return njlist
    else:
        return ''

def get_thr_list():
    thr_list = []
    enu_list = list(threading.enumerate())
    
    enu_list = [tid.getName() for tid in enu_list]
    enu_list.sort()
    
    for thname in enu_list:
        splcid = thname.split('/', 1)
        
        if len(splcid) < 2:
            clid = 'all'
            thrinf = splcid[0]
        else:    
            clid = splcid[0]
            thrinf = splcid[1]
        
        spthri = thrinf.split('.')
        
        if len(spthri) == 1:
            thr_list.append('%d) <%s>: "%s".' % (enu_list.index(thname) + 1, clid, thrinf))
        elif len(spthri) == 5:
            thr_list.append(l('%s) <%s>: "%s" in "%s" at %s:%s:%s.') % (enu_list.index(thname) + 1, clid, spthri[1], spthri[0], spthri[2], spthri[3], spthri[4]))
    
    return (len(enu_list), thr_list)

def is_rem_exists(gch, timerid):
    cid = get_client_id()
    
    sql = "SELECT * FROM reminds WHERE timerid='%s';" % (timerid)
    qres = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
    
    if qres:
        return True
    return False

def get_rem_rtime(gch, timerid):
    cid = get_client_id()
    
    sql = "SELECT rtime FROM reminds WHERE timerid='%s';" % (timerid)
    qres = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
    
    if qres:
        return qres[0][0]
    return 0
    
def get_rem_cts(gch, timerid):
    cid = get_client_id()
    
    sql = "SELECT ctms FROM reminds WHERE timerid='%s';" % (timerid)
    qres = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
    
    if qres:
        return qres[0][0]
    return 0

def check_timerid(gch, timerid):
    cid = get_client_id()
    
    sql = "SELECT * FROM reminds WHERE timerid='%s';" % (timerid)
    qres = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
    
    if qres:
        return False
    return True
 
def set_rem_mod(gch, mod, timerid):
    cid = get_client_id()

    upd_sql = '''UPDATE reminds SET  "mod"='%s' WHERE timerid='%s';''' % (mod, timerid)
    
    rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), upd_sql)
    
    return rep
    
def set_rem_cts(gch, cts, timerid):
    cid = get_client_id()

    upd_sql = '''UPDATE reminds SET  "ctms"='%s' WHERE timerid='%s';''' % (cts, timerid)
    
    rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), upd_sql)
    
    return rep
 
def set_rem_dts(gch, dts, timerid):
    cid = get_client_id()

    upd_sql = '''UPDATE reminds SET  "dsts"='%s' WHERE timerid='%s';''' % (dts, timerid)
    
    rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), upd_sql)
    
    return rep
 
def get_rem_mod(gch, timerid):
    cid = get_client_id()

    upd_sql = '''SELECT mod FROM reminds WHERE timerid='%s';''' % (timerid)
    
    rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), upd_sql)
    
    if rep:
        return rep[0][0]
    return 0
 
def set_run_cnt(gch, cnt, timerid):
    cid = get_client_id()

    upd_sql = '''UPDATE reminds SET  "cnt"='%s' WHERE timerid='%s';''' % (cnt, timerid)
    
    rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), upd_sql)
    
    return rep
    
def get_run_cnt(gch, timerid):
    cid = get_client_id()

    upd_sql = '''SELECT cnt FROM reminds WHERE timerid='%s';''' % (timerid)
    
    rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), upd_sql)
    
    if rep:
        return rep[0][0]
    return 0
 
def rem_timer(groupchat, cts, dts, nick, jid, mess, timerid='', cycle=False, mod='0'):
    cid = get_client_id()
    
    rsecs = trunc(dts - cts)
    
    if not nick:
        nick = get_rem_nick(groupchat, jid)
    
    source = [groupchat + '/' + nick, groupchat, nick]
    
    if is_groupchat(jid):
        type = 'public'
    else:
        type = 'private'
    
    if is_gch_user(groupchat, nick) or is_groupchat(jid):
        rcnt = 0
        
        if not cycle:
            del_remind(groupchat, jid, mess, timerid)
        else:
            rtimes = int(get_rem_rtime(groupchat, timerid))
            ncts = int(get_rem_cts(groupchat, timerid)) + (rtimes * 60)
            ndts = ncts + (rtimes * 60)
            cts = trunc(ncts)
            dts = trunc(ndts)
            
            if is_rem_exists(groupchat, timerid):
                imod = get_rem_mod(groupchat, timerid)
                rcnt = get_task_strd('cycle_%s' % (timerid))
                del_remind(groupchat, jid, mess, timerid)
                set_task_next('cycle_%s' % (timerid), dts)
                save_remind(groupchat, nick, jid, rtimes, cts, dts, mess, 'run', timerid, cycle, imod)
        
        strm = mess.strip()
        splm = strm.split(' ', 1)
        pcmd = splm[0]
        pars = ''

        if len(splm) > 1:
            pars = splm[1]
            pars = pars.strip()

        rcmd = get_real_cmd_name(pcmd)

        if rcmd:
            pcmd = rcmd

        fcmds = ['remind', 'ctask']

        if is_var_set('commands', pcmd):
            cmdacc = get_fatal_var('commands', pcmd, 'access')
            ulvl = user_level(source, groupchat)

            if ulvl >= cmdacc and not pcmd in fcmds:
                cmdhnd = get_fatal_var('command_handlers', pcmd)
                
                if not cycle:
                    thr_name = 'remind_%s' % (timerid)
                    call_in_sep_thr('%s/%s' % (cid, thr_name), cmdhnd, type, source, pars)
                else:
                    thr_name = 'cycle_%s' % (timerid)
                    
                    if mod in ['Q', 'q']:
                        call_in_sep_thr('%s/%s' % (cid, thr_name), cmdhnd, 'null', source, pars)
                    elif mod.isdigit():
                        if int(mod) > 0:
                            imod = int(get_rem_mod(groupchat, timerid)) 
                            imod -= 1
                            rcnt += 1
                            
                            set_rem_mod(groupchat, imod, timerid)
                            
                            call_in_sep_thr('%s/%s' % (cid, thr_name), cmdhnd, type, source, pars)
                            
                            if not imod:
                                del_remind(groupchat, jid, mess, timerid)
                                rmv_fatal_task(thr_name)
                        else:
                            call_in_sep_thr('%s/%s' % (cid, thr_name), cmdhnd, type, source, pars)
                    else:
                        call_in_sep_thr('%s/%s' % (cid, thr_name), cmdhnd, type, source, pars)
                    
                    rcnt = get_task_strd(thr_name)
                    set_run_cnt(groupchat, rcnt, timerid)
                    
                return

        if not cycle:
            atime = time.strftime('%H:%M:%S', time.localtime(dts))
        else:
            atime = time.strftime('%H:%M:%S', time.localtime(cts))
           
        if type == 'public':
            if not cycle:
                rep = l('Public remind at %s after %s:\n\n%s') % (atime, timeElapsed(rsecs), mess)
            else:
                rep = l('Public cycle task at %s after %s:\n\n%s') % (atime, timeElapsed(rsecs), mess) 
            
            msg(jid, rep)
        else:
            if not cycle:
                rep = l('Remind at %s after %s:\n\n%s') % (atime, timeElapsed(rsecs), mess)
            else:
                rep = l('Cycle task at %s after %s:\n\n%s') % (atime, timeElapsed(rsecs), mess)
            
            reply(type, source, rep)
        
        return rep
    
def get_ujoin_time(gch, nick):
    cid = get_client_id()
    
    nick = nick.replace('"', '&quot;')
    sql = "SELECT ujoin FROM users WHERE nick='%s';" % (nick)
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
    
    if qres:
        ujoin = qres[0][0]
        
        if ujoin and ujoin != 'None':
            return float(ujoin)
    return time.time()    
    
def get_info_jid(gch, nick):
    cid = get_client_id()
    
    nick = nick.replace('"', '&quot;')
    sql = "SELECT jid FROM users WHERE nick='%s';" % (nick)
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
    
    if qres:
        jid = qres[0][0]
        return jid
    else:
        return ''

def get_rem_nick(gch, jid):
    cid = get_client_id()
    
    nick = ''

    gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
    
    try:
        nickl = [li for li in gch_dic if jid == get_stripped(gch_dic[li]['rjid'])]
    except Exception:
        try:
            time.sleep(3)
            gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
            nickl = [li for li in gch_dic if jid == get_stripped(gch_dic[li]['rjid'])]
        except Exception:
            return nick
        
    if nickl:
        nick = nickl[-1]
        
    return nick
 
def save_remind(gch, nick, jid, rtime, ctms, dsts, mess, status, timerid, cycle=False, mod=0):
    cid = get_client_id()
    mess = mess.replace(r'"', r'&quot;')
    
    sql = '''INSERT INTO reminds (nick, jid, rtime, ctms, dsts, mess, status, timerid, ctask, mod) 
              VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (nick, jid, rtime, ctms, dsts, mess, status, timerid, int(cycle), mod)
    
    rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
    
    if rep != '':
        return rep
    else:
        upd_sql = '''UPDATE reminds SET "nick"='%s', "jid"='%s', "rtime"='%s', 
                         "ctms"='%s', "dsts"='%s', "status"='%s', "timerid"='%s' WHERE mess='%s';''' % (nick, jid, rtime, ctms, dsts, status, mess, timerid)
        
        rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), upd_sql)
        
        return rep

def recover_remind(gch, rem_handler, recover, reminds):
    curt = trunc(time.time()) 
    
    for rem in reminds:
        remj = rem[1]
        
        if is_groupchat(remj):
            type = 'public'
        else:
            type = 'private'
        
        rem2 = rem[2]
        rem3 = rem[3]
        rem4 = rem[4]
        rem8 = int(rem[8])
        
        nick = get_rem_nick(gch, remj)
        
        source = [gch + '/' + nick, gch, nick]
        
        if not ':' in rem2:
            rem2 = time.strftime('%H:%M:%S', time.localtime(int(rem4)))
        
        parameters = '%s %s' % (rem2, rem[5])
        
        rem_handler(type, source, parameters, recover, rem[1], rem3, rem[7], rem8, rem[9])

def show_reminds(gch, jid, reminds, pref='', suff='', cycle=False):
    cid = get_client_id()
    
    freml = [rel for rel in reminds if rel[1] == jid and rel[6] == 'run']
    
    nick = ''
    
    
    if is_groupchat(jid):
        freml = [rel for rel in reminds if rel[1] == jid and rel[6] == 'run']
    else:
        nick = get_rem_nick(gch, jid)

    sh_freml = []

    gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
    
    try:
        if is_groupchat(jid):
            sh_freml = [rel for rel in freml if rel[1] == jid]
        else:
            sh_freml = [rel for rel in freml if rel[1] == get_stripped(gch_dic[nick]['rjid'])]
    except Exception:
        log_exc_error()
        try:
            if is_groupchat(jid):
                sh_freml = [rel for rel in freml if rel[1] == jid]
            else:
                time.sleep(3)
                gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
                sh_freml = [rel for rel in freml if rel[1] == get_stripped(gch_dic[nick]['rjid'])]
        except Exception:
            log_exc_error()
            return []
    
    if sh_freml:
        rng = list(range(len(sh_freml)))
        
        if suff: 
            if not cycle: 
                nremli = [l('%s) %s%s%s:\n%s') % (li + 1, pref, time.strftime('%H:%M:%S', time.localtime(int(sh_freml[li][4]))), suff + timeElapsed(int(sh_freml[li][4]) - trunc(time.time())), sh_freml[li][5]) for li in rng]
            else:
                nremli = [l('%s) [%s] %s%s (each %s)%s:\n%s') % (li + 1, sh_freml[li][9],pref, time.strftime('%H:%M:%S', time.localtime(int(sh_freml[li][4]))), timeElapsed(int(sh_freml[li][2])*60, True), suff + timeElapsed(int(sh_freml[li][4]) - trunc(time.time())), sh_freml[li][5]) for li in rng]
        else:
            nremli = [l('%s) %s%s, %s ago:\n%s') % (li + 1, pref, time.strftime('%H:%M:%S', time.localtime(int(sh_freml[li][4]))), timeElapsed(trunc(time.time()) - int(sh_freml[li][4])), sh_freml[li][5]) for li in rng]
    
        return nremli
    else:
        return []

def exp_reminds(reminds, jid):
    ctm = trunc(time.time())
    chkreml = [rel for rel in reminds if int(rel[4]) <= ctm and rel[1] == jid and not int(rel[8])]
    return chkreml

def check_reminds(reminds, jid):
    ctm = trunc(time.time())
    chkreml = [rel for rel in reminds if int(rel[4]) > ctm and rel[1] == jid]
    return chkreml

def repair_ctasks(gch, rems):
    curt = trunc(time.time())
    
    nrems = []
    
    for rem in rems:
        rem = list(rem)
        rem8 = int(rem[8])
        rem2 = int(rem[2])
        rem4 = int(rem[4])
        rem7 = rem[7]
        
        if rem8:
            if rem4 < curt:
                rem[3] = str(curt)
                rem[4] = str(curt + (rem2 * 60))
                
                set_rem_cts(gch, rem[3], rem7) 
                set_rem_dts(gch, rem[4], rem7)
                
                nrems.append(rem)
            else:
                nrems.append(rem)
                
    return nrems
    
def del_remind(gch, jid, mess, timerid=''):
    cid = get_client_id()
    
    if timerid:
        del_sql = "DELETE FROM reminds WHERE jid='%s' AND mess='%s' AND timerid='%s';" % (jid, mess, timerid)
    else:
        del_sql = "DELETE FROM reminds WHERE jid='%s' AND mess='%s';" % (jid, mess)
    
    res = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), del_sql)
    
    return res

def get_reminds(gch):
    cid = get_client_id()

    del_sql = "DELETE FROM reminds WHERE status='done';"
    
    sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), del_sql)
    
    sql = "SELECT * FROM reminds WHERE status='run' ORDER BY dsts;"
    
    reminds = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
    
    return reminds

def get_dm_nicks(gch):
    cid = get_client_id()
    
    sql = 'SELECT nick FROM users ORDER BY uleave;'
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
    
    if qres:
        nicks = [nil[0].replace('&quot;', '"') for nil in qres]
        return nicks
    return []
    
def rmv_dm_nick(gch, body):
    cid = get_client_id()
    
    body = body.strip()
    
    if not body: 
        return body
    
    conf_nicks = list(get_dict_fatal_var(cid, 'gchrosters', gch))
    nicks = get_dm_nicks(gch)
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
        while body[:1] == ':' or body[:1] == ',':
            body = body[1:].strip()
    elif len(body) == 1 and body in [':', ',']:
        body = ''
        
    body = body.strip()
    
    return body

def get_hd_dm_nick(gch, body):
    nicks = get_dm_nicks(gch)
    delim = ''
    
    splbod = body.split(':', 1)
    splbod = [sbli for sbli in splbod if sbli]

    if len(splbod) == 2:
        prob_nick = splbod[0]
        
        if prob_nick in nicks:
            return (prob_nick, ':')
        else:
            delim = ':'

    splbod = body.split(',', 1)
    splbod = [sbli for sbli in splbod if sbli]

    if len(splbod) == 2:
        prob_nick = splbod[0]
        
        if prob_nick in nicks:
            return (prob_nick, ',')
        else:
            delim = ','            
    return ('', delim)

def del_dms(gch, jid):
    sql = "DELETE FROM dmess WHERE djid='%s'" % (jid)
    
    cid = get_client_id()
    
    qres = sqlquery('dynamic/%s/%s/dmess.db' % (cid, gch), sql)
    
    return qres

def get_sms(gch, jid):
    cid = get_client_id()
    
    sql = "SELECT * FROM dmess WHERE sjid='%s'" % (jid)
    qres = sqlquery('dynamic/%s/%s/dmess.db' % (cid, gch), sql)
    
    return qres

def get_dms(gch, jid):
    cid = get_client_id()
    
    sql = "SELECT * FROM dmess WHERE djid='%s'" % (jid)
    qres = sqlquery('dynamic/%s/%s/dmess.db' % (cid, gch), sql)
    
    return qres

def save_dm(gch, snick, sjid, dnick, djid, mess):
    date = time.time()
    mess = mess.replace('"', '&quot;')
    
    cid = get_client_id()
    
    sql = "SELECT mess FROM dmess WHERE mess='%s'" % (mess)
    qres = sqlquery('dynamic/%s/%s/dmess.db' % (cid, gch), sql)
    
    if not qres:
        sql = "INSERT INTO dmess (snick, sjid, dnick, djid, mess, date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (snick, sjid, dnick, djid, mess, date)
    else:
        sql = "UPDATE dmess SET \"snick\"='%s', \"sjid\"='%s', \"dnick\"='%s', \"djid\"='%s', \"date\"='%s' WHERE mess='%s';" % (snick, sjid, dnick, djid, date, mess)
    
    qres = sqlquery('dynamic/%s/%s/dmess.db' % (cid, gch), sql)
    
    return qres
    
def show_dms(dms):
    if dms:
        ndmsli = [l('%s) Sent by %s %s at %s:\n\n%s') % (dms.index(ndli) + 1, ndli[0], time.strftime('%d.%m.%Y', time.localtime(float(ndli[5]))), time.strftime('%H:%M:%S', time.localtime(float(ndli[5]))), ndli[4].replace('&quot;', '"')) for ndli in dms]
        return ndmsli
    
    return []
    
def handler_members(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    get_and_out_jids(type, source, groupchat, 'member', l('Members (total: %s):\n\n%s'), l('List of members is empty!'))
        
def handler_admins(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    get_and_out_jids(type, source, groupchat, 'admin', l('Admins (total: %s):\n\n%s'), l('List of admins is empty!'))
            
def handler_owners(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    get_and_out_jids(type, source, groupchat, 'owner', l('Owners (total: %s):\n\n%s'), l('List of owners is empty!'))
        
def handler_outcasts(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    get_and_out_jids(type, source, groupchat, 'outcast', l('Outcasts (total: %s):\n\n%s'), l('List of outcasts is empty!'))
    
def get_info_state(gch):
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/users.db' % (cid, gch)):
        sql = '''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 nick VARCHAR(30) NOT NULL, jid VARCHAR(30) NOT NULL, 
                 ujoin VARCHAR(20) NOT NULL, uleave VARCHAR(20) NOT NULL, 
                 reason VARCHAR, UNIQUE (nick));'''
        sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX iusers ON users (nick);'
        sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql) 
        
    if not is_db_exists('dynamic/%s/%s/reminds.db' % (cid, gch)):
        sql = '''CREATE TABLE reminds (nick VARCHAR(30) NOT NULL, 
                jid VARCHAR(30) NOT NULL, rtime VARCHAR(20) NOT NULL, 
                ctms VARCHAR(20) NOT NULL, dsts VARCHAR(20) NOT NULL, 
                mess VARCHAR NOT NULL, status VARCHAR(10) NOT NULL, 
                timerid VARCHAR(20) NOT NULL, ctask VARCHAR(1) NOT NULL, 
                mod VARCHAR(4) NOT NULL, cnt VARCHAR NOT NULL DEFAULT 0,
                UNIQUE (timerid));'''
        sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
        
        sql = 'CREATE INDEX ireminds ON reminds (nick, jid);'
        sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
        
    if not is_db_exists('dynamic/%s/%s/dmess.db' % (cid, gch)):
        sql = '''CREATE TABLE dmess (snick VARCHAR(30) NOT NULL, 
                sjid VARCHAR(30) NOT NULL, dnick VARCHAR(30) NOT NULL, 
                djid VARCHAR(30) NOT NULL, mess VARCHAR NOT NULL, 
                date VARCHAR(20) NOT NULL);'''
        sqlquery('dynamic/%s/%s/dmess.db' % (cid, gch), sql)
    
        sql = 'CREATE INDEX idmess ON dmess (sjid, djid);'
        sqlquery('dynamic/%s/%s/dmess.db' % (cid, gch), sql)
    
    if not param_exists(gch, 'dmess'):
        set_gch_param(gch, 'dmess', '0')

def handler_dmess_control(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))
        
        if int(parameters) > 1:
            return reply(type, source, l('Invalid syntax!'))
        
        if parameters == "1":
            set_gch_param(groupchat, 'dmess', '1')
            return reply(type, source, l('Automatic system of delayed messages has been turned on!'))
        else:
            set_gch_param(groupchat, 'dmess', '0')
            return reply(type, source, l('Automatic system of delayed messages has been turned off!'))
    else:
        dmess = int(get_gch_param(groupchat, 'dmess', '0'))
        
        if dmess:
            return reply(type, source, l('Automatic system of delayed messages is turned on in this groupchat!'))
        return reply(type, source, l('Automatic system of delayed messages is turned off in this groupchat!'))

def handler_dmess(type, source, body):
    cid = get_client_id()
    
    groupchat = source[1]
    snick = source[2]
    sjid = get_true_jid(source)
    bot_nick = get_bot_nick(groupchat)
    
    if snick == bot_nick:
        return
    
    dmess = int(get_gch_param(groupchat, 'dmess', '0'))
            
    if dmess and len(body) <= 1024:
        nicks = get_dm_nicks(groupchat)
        
        gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))
        conf_nicks = list(gch_dic)
        
        try:
            here_jids = [get_stripped(gch_dic[hli]['rjid']) for hli in conf_nicks]
        except Exception:
            try:
                time.sleep(3)
                gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))
                here_jids = [get_stripped(gch_dic[hli]['rjid']) for hli in conf_nicks]
            except Exception:
                return
        
        nickdl = get_hd_dm_nick(groupchat, body)
        dnick = nickdl[0] 
        
        if dnick and dnick in nicks or dnick in conf_nicks:
            djid = get_info_jid(groupchat, dnick)
            mess = rmv_dm_nick(groupchat, body)
            
            if djid and not djid in here_jids and mess:
                res = save_dm(groupchat, snick, sjid, dnick, djid, mess)
                
                if res != '':
                    reply(type, source, l('Message has been saved and will be send to the user!'))

def handler_tell(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    snick = source[2]
    sjid = get_true_jid(source)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))
        conf_nicks = list(gch_dic)
        here_jids = []
        
        for nki in conf_nicks:
            if not 'rjid' in gch_dic[nki]:
                continue

            here_jids.append(gch_dic[nki]['rjid'])
        
        nickdl = get_hd_dm_nick(groupchat, parameters)
        
        dnick = nickdl[0]
        delim = nickdl[1]
        
        if dnick:
            djid = get_info_jid(groupchat, dnick)
            mess = rmv_dm_nick(groupchat, parameters)
            
            if djid and not djid in here_jids and mess:
                res = save_dm(groupchat, snick, sjid, dnick, djid, mess)
                
                if res != '':
                    return reply(type, source, l('Message has been saved and will be send to the user!'))
            else:
                return reply(type, source, l('The user is present in this groupchat!'))
        else:
            if delim:
                rep = l('User not found!')
            else:
                rep = l('Invalid syntax!') 
                
            return reply(type, source, rep)
    else:
        dmsl = get_sms(groupchat, sjid)
        
        if dmsl:
            ndmsl = [l('%s) Sent to %s %s at %s:\n\n%s') % (dmsl.index(ndli) + 1, ndli[2], time.strftime('%d.%m.%Y', time.localtime(float(ndli[5]))), time.strftime('%H:%M:%S', time.localtime(float(ndli[5]))), ndli[4].replace('&quot;', '"')) for ndli in dmsl]

            rep = l('Delayed messages (total: %s):\n\n%s') % (len(ndmsl), '\n\n'.join(ndmsl))
        else:
            rep = l('There are no sent messages from you!')    
        
        if type == 'public':
            reply(type, source, l('Look in private!'))
            
        return reply('private', source, rep)
    
def handler_user_join(groupchat, nick, aff, role):
    jid = get_true_jid(groupchat + '/' + nick)

    qnick = nick.replace('"', '&quot;')
    
    cid = get_client_id()
    
    check_sql = "SELECT nick FROM users WHERE nick='%s'" % (qnick)
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), check_sql)
    
    if is_gch_user(groupchat, nick):
        ujoin = get_fatal_var(cid, 'gchrosters', groupchat, nick, 'joined')
    else:
        ujoin = time.time()
    
    if qres:
        upd_sql = "UPDATE users SET \"ujoin\"='%s', \"jid\"='%s' WHERE nick='%s';" % (ujoin, jid.strip(), qnick)
        
        sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), upd_sql)
    else:
        ins_sql = "INSERT INTO users (nick, jid, ujoin, uleave, reason) VALUES ('%s', '%s', '%s', '%s', '%s');" % (qnick, jid.strip(), ujoin, ujoin, '')
        
        sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), ins_sql)
        
    reminds = get_reminds(groupchat)
    
    reminds = repair_ctasks(groupchat, reminds)
    
    rems = check_reminds(reminds, jid)
    
    if jid == cid:
        prems = check_reminds(reminds, groupchat)
        
        if prems:
            rems.extend(prems)

    if rems:
        recover_remind(groupchat, handler_remind, True, rems)
    
    exp_rems = exp_reminds(reminds, jid)
    exp_prems = []
    
    if jid == cid:
        exp_prems = exp_reminds(reminds, groupchat)
    
    if exp_rems:
        for rel in exp_rems:
            del_remind(groupchat, rel[1], rel[5], rel[7])
            
    if exp_prems:
        for rel in exp_prems:
            del_remind(groupchat, rel[1], rel[5], rel[7])

    nexp_repl = show_reminds(groupchat, jid, exp_rems, pref=l('At') + ' ')
    nexp_repp = show_reminds(groupchat, groupchat, exp_prems, pref=l('At') + ' ')

    if nexp_repl:
        rep = l('Missed reminds (total: %s):\n\n%s') % (len(nexp_repl), '\n\n'.join(nexp_repl))
        msg(groupchat + '/' + nick, rep)
        
    if nexp_repp:
        rep = l('Missed public reminds (total: %s):\n\n%s') % (len(nexp_repp), '\n\n'.join(nexp_repp))
        msg(groupchat, rep)
        
    dmsl = get_dms(groupchat, jid)
    ndmsl = show_dms(dmsl)
    
    if ndmsl:
        rep = l('Delayed messages (total: %s):\n\n%s') % (len(ndmsl), '\n\n'.join(ndmsl))
        msg(groupchat + '/' + nick, rep)
        del_dms(groupchat, jid)
    
def handler_user_leave(groupchat, nick, reason, code):
    qnick = nick.replace('"', '&quot;')
    
    cid = get_client_id()
    
    check_sql = "SELECT nick FROM users WHERE nick='%s'" % (qnick)
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), check_sql)
    
    uleave = time.time()
    
    if not reason:
        reason = ''
    
    if qres:
        upd_sql = "UPDATE users SET \"uleave\"='%s', \"reason\"='%s'  WHERE nick='%s';" % (uleave, reason.strip(), qnick)
        
        sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), upd_sql)

def handler_user_presence(prs):
    ptype = prs.getType()
    groupchat = get_stripped(prs.getFrom())

    nick = get_resource(prs.getFrom())
    nick = nick.replace('"', '&quot;')
    
    jid = get_info_jid(groupchat, nick)
    
    scode = prs.getStatusCode()
    
    if scode == '303' and ptype == 'unavailable':
        newnick = prs.getNick()
                
        sjid = get_true_jid(groupchat + '/' + newnick)
                
        qnewnick = newnick.replace('"', '&quot;')
        
        cid = get_client_id()
        
        check_sql = "SELECT nick FROM users WHERE nick='%s'" % (qnewnick)
        qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), check_sql)
        
        ujoin = get_ujoin_time(groupchat, nick)
        set_fatal_var(cid, 'gchrosters', groupchat, newnick, 'joined', ujoin)
            
        if qres:
            upd_sql = "UPDATE users SET \"jid\"='%s', \"ujoin\"='%s' WHERE nick='%s';" % (sjid, ujoin, nick)
            
            sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), upd_sql)
        else:
            if jid and qnewnick:
                ins_sql = "INSERT INTO users (nick, jid, ujoin, uleave, reason) VALUES ('%s', '%s', '%s', '%s', '%s');" % (qnewnick, jid.strip(), ujoin, ujoin, '')
                
                sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), ins_sql)

def handler_seen(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    nick_jid = parameters
    curr_time = time.time()
    
    if not parameters:
        return reply(type, source, l('Invalid syntax!'))

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    jid = ''
    nick = ''
    
    if check_jid(nick_jid):
        jid = nick_jid
    else:
        nick = nick_jid
    
    qnick = nick.replace('"', '&quot;')
    
    gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))
    conf_nicks = list(gch_dic)
    
    if jid:
        qres = []
        
        for nkc in conf_nicks:
            if not 'rjid' in gch_dic[nkc]:
                continue

            rjid = get_stripped(gch_dic[nkc]['rjid'])
            
            if jid == rjid:
                if is_gch_user(groupchat, nkc):
                    nick = nkc
                    check_sql = "SELECT nick, ujoin, uleave FROM users WHERE nick='%s'" % (qnick)
                    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), check_sql)
                    break
        
        if not qres:
            check_sql = "SELECT nick, ujoin, uleave FROM users WHERE jid='%s' ORDER BY uleave" % (jid)
            qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), check_sql)

        if qres:
            qres = list(qres[-1])
            gnick = qres[0].replace('&quot;', '"')
            join_time = float(qres[1])
            leave_time = float(qres[2])
            
            if not is_gch_user(groupchat, gnick):
                seen_time = curr_time - leave_time
                here_time = leave_time - join_time
                rep = l('User %s was here %s ago and spent %s in this groupchat.') % (gnick, timeElapsed(seen_time), timeElapsed(here_time))
                return reply(type, source, rep)
            elif is_gch_user(groupchat, gnick):
                gjid = get_stripped(gch_dic[gnick]['rjid'])
                
                if gjid == jid:
                    rep = l('The user is present in this groupchat!')
                    return reply(type, source, rep)
            else:
                rep = l('The user %s has never been in this groupchat!') % (jid)
                return reply(type, source, rep)
        else:
            rep = l('The user %s has never been in this groupchat!') % (jid)
            return reply(type, source, rep)
    elif nick:
        check_sql = "SELECT nick, ujoin, uleave, jid FROM users WHERE nick='%s'" % (qnick)
        qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), check_sql)
        
        if qres:
            jid = list(qres[0])[3]
        
        gnick = ''
        
        for nkc in conf_nicks:
            if not 'rjid' in gch_dic[nkc]:
                continue

            rjid = get_stripped(gch_dic[nkc]['rjid'])
            
            if jid == rjid:
                if is_gch_user(groupchat, nkc):
                    gnick = nkc
                    break
    
        check_sql = "SELECT nick, ujoin, uleave, jid FROM users WHERE jid='%s' ORDER BY uleave" % (jid)
        qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), check_sql)
    
        if qres:
            qres = list(qres[-1])
            
            if not gnick:
                gnick = qres[0].replace('&quot;', '"')
            
            join_time = float(qres[1])
            leave_time = float(qres[2])
            
            if not is_gch_user(groupchat, gnick):
                seen_time = curr_time - leave_time
                here_time = leave_time - join_time
                rep = l('User %s was here %s ago and spent %s in this groupchat.') % (nick, timeElapsed(seen_time), timeElapsed(here_time))
                return reply(type, source, rep)
            elif is_gch_user(groupchat, gnick):
                rep = l('The user is present in this groupchat!')
                return reply(type, source, rep)
        else:
            rep = l('The user %s has never been in this groupchat!') % (nick)
            return reply(type, source, rep)
            
def handler_here(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    nick = source[2]
    here_nick = parameters
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))

    if parameters:
        if here_nick in list(gch_dic):
            join_time = gch_dic[here_nick]['joined']
            curr_time = time.time()
            here_time = timeElapsed(curr_time - join_time)
            
            if here_nick == nick:
                rep = l('Time spent in this groupchat: %s.') % (here_time)
            else:
                rep = l('Time spent by %s in this groupchat: %s.') % (here_nick, here_time)
            
            return reply(type, source, rep)
        else:
            return reply(type, source, l('User not found!'))
    else:
        join_time = gch_dic[nick]['joined']
        curr_time = time.time()
        here_time = timeElapsed(curr_time - join_time)
        rep = l('Time spent in this groupchat: %s.') % (here_time)
        return reply(type, source, rep)

def handler_nicks(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    cid = get_client_id()

    if parameters:
        prob_jid = parameters
        
        if check_jid(prob_jid):
            sql = "SELECT nick, ujoin FROM users WHERE jid='%s' ORDER BY ujoin DESC;" % (prob_jid)
            qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), sql)
            
            if qres:
                qres = [li[0].replace('&quot;', '"') for li in qres]
                rep = l('Nicks used by %s in this groupchat (total: %s):\n\n%s.') % (prob_jid, len(qres), ', '.join(qres))
            else:
                rep = l('The user %s has never been in this groupchat!') % (prob_jid)
        else:
            prob_nick = prob_jid
            jid = get_info_jid(groupchat, prob_nick)
            
            if jid:
                sql = "SELECT nick, ujoin FROM users WHERE jid='%s' ORDER BY ujoin DESC;" % (jid)
                qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), sql)
                
                if qres:
                    qres = [li[0].replace('&quot;', '"') for li in qres]
                    rep = l('Nicks used by %s in this groupchat (total: %s):\n\n%s.') % (prob_nick, len(qres), ', '.join(qres))
                else:
                    rep = l('Unknown error!')
            else:
                rep = l('The user %s has never been in this groupchat!') % (prob_nick)
    else:
        sql = 'SELECT nick, ujoin, uleave, jid FROM users ORDER BY nick;'
        qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), sql)
        ctm = time.time()
        
        if qres:
            qres = [li for li in qres if li[1] and li[1] != 'None' and li[3] != groupchat]
            nlst = []
            
            for li in qres:
                nick = li[0].replace('&quot;', '"')
                jotm = float(li[1])
                letm = float(li[2])
                jid = li[3].replace('&quot;', '"')
                
                if ctm - jotm <= 86400:
                    if is_gch_user(groupchat, nick):
                        jltms = l('Joined: %s') % (time.strftime('%d.%m.%Y, %H:%M:%S.', time.localtime(jotm)))
                    else:
                        jltms = l('Left: %s') % (time.strftime('%d.%m.%Y, %H:%M:%S.', time.localtime(letm)))
                    
                    nlst.append('%s / %s / %s' % (nick, jid, jltms))
            
            nlst = get_num_list(nlst)
            
            if nlst:
                rep = l('Users visited this groupchat (total: %s):\n\n%s') % (len(nlst), '\n'.join(nlst))
            else:
                rep = l('There were not users last twenty-four hours!')
        else:
            rep = l('Unknown error!')
        
        if type == 'public':
            reply(type, source, l('Look in private!'))
            
        return reply('private', source, rep)
        
    return reply(type, source, rep)

def handler_groupchats(type, source, parameters):
    cid = get_client_id()
    
    gchr = dict(get_dict_fatal_var(cid, 'gchrosters'))
    groupchats = list(gchr)
    groupchats.sort()
    
    chrml = ['%d) %s / %s [%s]' % (groupchats.index(chli) + 1, get_bot_nick(chli), chli, len(gchr[chli]) - 1) for chli in groupchats]
    
    if chrml:
        rep = l('Groupchats where bot was joined (total: %s):\n\n%s') % (len(groupchats), '\n'.join(chrml))
    else:
        rep = l('List of groupchats where bot was joined is empty!')

    return reply(type, source, rep)

def handler_getrealjid(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if not parameters:
        return reply(type, source, l('Invalid syntax!'))

    nick = parameters
    
    cid = get_client_id()
    
    sql = "SELECT jid FROM users WHERE nick='%s';" % (nick.replace('"', '&quot;'))
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, groupchat), sql)
    
    if not qres:
        return reply(type, source, l('User not found!'))
    else:
        truejid = qres[0][0]
        
        if type == 'public':
            reply(type, source, l('Look in private!'))

    rep = l('Real jid of %s: %s') % (nick, truejid)        
            
    if type == 'console':
        return reply(type, source, rep)
    else:
        return reply('private', source, rep)
        
def handler_total_in_muc(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))
    
    ulist = []

    for nki in list(gch_dic.keys()):
        if not 'rjid' in gch_dic[nki]:
            continue
        
        ulist.append(nki)

    ulist.sort()
    
    rep = l('Users joined in this groupchat (total: %s):\n\n%s.') % (len(ulist), ', '.join(ulist))
    return reply(type, source, rep)

def handler_bot_uptime(type, source, parameters):
    cid = get_client_id()
    
    bstart = get_fatal_var('info', 'start')
    
    if bstart:
        thrs = get_fatal_var('info', 'thr')
        ss = get_int_fatal_var(cid, 'info', 'ss')
        btraffic = get_fatal_var(cid, 'info', 'btraffic')
        pcycles = get_fatal_var(cid, 'info', 'pcycles')
        msgs = get_int_fatal_var(cid, 'info', 'msg')
        prss = get_int_fatal_var(cid, 'info', 'prs')
        iqs = get_int_fatal_var(cid, 'info', 'iq')
        cmds = get_int_fatal_var(cid, 'info', 'cmd')
        
        uptime = int(time.time() - bstart)
        
        rep = l('Bot run statistics:\n\n')
        rep += l('Runtime period: %s.\n') % (timeElapsed(uptime))
        rep += l('Sessions: %s.\n') % (ss)
        
        total_users = 0
        
        gchs = tuple(get_dict_fatal_var(cid, 'gchrosters'))
        
        for gch in gchs:
            tusers = tuple(get_dict_fatal_var(cid, 'gchrosters', gch))
            total_users += len(tusers)
            
        tot_traffic = round(float(btraffic) / 1024, 1)
            
        if total_users:
            rep += l('Groupchats: %s.\n') % (len(gchs))
            rep += l('\\Users: %s.\n') % (total_users)
            
        rep += l('Messages: %s.\n') % (msgs)
        rep += l('Presences: %s.\n') % (prss)
        rep += l('Iq-queries: %s.\n') % (iqs)
        rep += l('Commands: %s.\n') % (cmds + 1)
        rep += l('Parser cycles: %s.\n') % (pcycles)
        rep += l('Bot traffic: %s kB.\n') % (tot_traffic)
        
        mem = ''
        
        if os.name == 'posix':
            try:
                pr = os.popen('ps -o rss -p %s' % os.getpid())
                pr.readline()
                mem = pr.readline().strip()
                pr.close()
            except:
                pass
            
            if mem: 
                rep += l('Memory: %s kB.\n') % (mem)
            
        (user, system, qqq, www, eee, ) = os.times()
        
        rep += l('CPU time: %.2f sec.\n') % (user)
        rep += l('System time: %.2f sec.\n') % (system)
        rep += l('Created threads: %s.\n') % (thrs)
        rep += l('\Active threads: %s.') % (threading.activeCount())
    else:
        rep = l('Unknown error!')
        
    return reply(type, source, rep)

def handler_bot_sestime(type, source, parameters):
    cid = get_client_id()
    
    stime = get_fatal_var(cid, 'info', 'ses')
    
    if stime:
        sestime = int(time.time() - stime)
        rep = l('Bot session time: %s.') % (timeElapsed(sestime))
    else:
        rep = l('Unknown error!')
    
    return reply(type, source, rep)

def handler_thr_show(type, source, parameters):
    thr_list_get = get_thr_list()
    count = thr_list_get[0]
    thr_list = thr_list_get[1]
    rep = l('List of active threads (total: %s):\n\n%s') % (count, '\n'.join(thr_list))
    return reply(type, source, rep)
    
def handler_thr_dump(type, source, parameters):
    thr_list_get = get_thr_list()
    count = thr_list_get[0]
    thr_list = thr_list_get[1]
    dump = l('List of active threads (total: %s):\n\n%s') % (count, '\n'.join(thr_list))
    write_file('thr_list.dmp', dump.encode('utf-8'))
    return reply(type, source, l('Saved!'))

def handler_tasks(type, source, parameters):
    tlst = enum_fatal_tasks()
    curt = trunc(time.time())
    tols = []

    for li in tlst:
        tla = get_task_last(li)
        tnx = get_task_next(li)
        tiv = get_task_ival(li)
        tcn = get_task_count(li)
        trm = get_task_remns(li)
        
        tla = tla - tiv
        
        nnx = get_task_nnxt(li)
        
        nnx = time.strftime('%H:%M:%S', time.localtime(tnx + nnx))        
        tla = time.strftime('%H:%M:%S', time.localtime(tla))
        tnx = time.strftime('%H:%M:%S', time.localtime(tnx))
        
        trm = get_task_remns(li)
        
        tols.append('%s: %s, %s, %s, %s, %s (%s)' % (li, tiv, tcn, trm, tla, tnx, nnx))
        
    if parameters:
        tols = [li for li in tols if li.count(parameters)]
    
    tols = get_num_list(tols)
    
    miv = get_task_miv()
    
    evst = get_fatal_var(cid(), 'task_manager_event', 'start')
    
    if evst:
        evrm = curt - evst
    else:
        evrm = 0
    
    if tols:
        return reply(type, source, l('List of current tasks (total: %s; miv: %s; evel: %s):\n\n%s') % (len(tols), miv, evrm, '\n'.join(tols)))
    return reply(type, source, l('Tasks not found!'))

def handler_ctask(type, source, parameters):
    spar = parameters.split(' ', 1)
    
    spli = spar[0]
    
    if parameters:
        if spli.isdigit():
            handler_remind(type, source, parameters, cycle=True)
        elif len(spli) == 1 and spli == '-':
            handler_remind(type, source, parameters, cycle=True)
        elif len(spli) > 1 and spli[0] == '-':
            handler_remind(type, source, parameters, cycle=True)
        elif len(spli) >= 3 and spli[0] != '-' and spli.count(':') == 1:
            if spli[-1] != ':' and not spli[-1].isdigit():
                sppr = spli.split(':', 1)
                
                npar = ' '.join([sppr[0], spar[1]])
                
                if sppr[1] in ['q', 'Q']:
                    handler_remind(type, source, npar, cycle=True, mod=sppr[1])
                else:
                    return reply(type, source, l('Invalid syntax!'))
            elif spli[-1] != ':' and spli[-1].isdigit():
                sppr = spli.split(':', 1)
                
                npar = ' '.join([sppr[0], spar[1]])
            
                handler_remind(type, source, npar, cycle=True, mod=sppr[1])
            else:
                return reply(type, source, l('Invalid syntax!'))
        else:
            return reply(type, source, l('Invalid syntax!'))
    else:
        handler_remind(type, source, parameters, cycle=True)

def handler_remind(type, source, parameters, recover=False, jid='', rcts='', timerid='', cycle=False, mod='0'):
    groupchat = source[1]
    nick = source[2]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
    
    if not recover and not jid:
        jid = get_info_jid(groupchat, nick)
    
    if parameters:
        spltdp = parameters.split(' ', 1)
        
        if len(spltdp) == 2 and not '-' in spltdp[0]:
            rtime = spltdp[0]
            rtimes = rtime
            ctm = list(time.localtime())
            
            if ':' in rtime:
                rtime = rtime.split(':')
                rtime = [li for li in rtime if li != '']
                
                brtime = False
                
                for tli in rtime:
                    if not tli.isdigit():
                        brtime = True
                        break
                        
                if brtime:
                    return reply(type, source, l('Invalid syntax!'))
                
                if len(rtime) == 3:
                    sc = int(rtime[2])
                    mn = int(rtime[1])
                    hr = int(rtime[0])
                elif len(rtime) == 2:
                    sc = 0
                    mn = int(rtime[1])
                    hr = int(rtime[0])
                elif len(rtime) == 1:
                    sc = 0
                    mn = int(rtime[0])
                    hr = ctm[3]
                    
                if hr:
                    ctm[3] = hr
                    
                ctm[4] = mn
                ctm[5] = sc
                    
                dst = tuple(ctm)
                cts = trunc(time.time())
                dts = trunc(time.mktime(dst))
                
                secs = dts - cts
                
                if abs(secs) != secs and not recover:
                    return reply(type, source, l('Expired remind!'))
            else:
                rtimes = spltdp[0]
                
                if not rtimes.isdigit():
                    return reply(type, source, l('Invalid syntax!'))

                secs = int(rtimes) * 60
                cts = trunc(time.time())
                dts = trunc(cts + secs)
                
            mess = spltdp[1]
            
            if secs > 0:
                rep = ''
                
                if not recover:
                    rep = l('Saved!')
                    reply(type, source, rep)
                
                if recover:
                    cts = float(rcts)
                    nick = ''
                
                if not recover:
                    timerid = 'task%s' % (rand10())
                    chk_tmrid = check_timerid(groupchat, timerid)
                    
                    while not chk_tmrid:
                        timerid = 'task%s' % (rand10())
                        chk_tmrid = check_timerid(groupchat, timerid)
                
                if type == 'public':
                    jid = groupchat
                
                if not recover:
                    save_remind(groupchat, nick, jid, rtimes, cts, dts, mess, 'run', timerid, cycle, mod)
                
                if cycle:
                    tskn = 'cycle_%s' % (timerid)
                
                    if not recover:
                        add_fatal_task(tskn, rem_timer, (groupchat, cts, dts, nick, jid, mess, timerid, cycle, mod), secs, False)
                    else:
                        rtime = int(get_rem_rtime(groupchat, timerid))
                        
                        nsecs = rtime * 60
                        
                        ncts = int(get_rem_cts(groupchat, timerid))
                        
                        add_fatal_task(tskn, rem_timer, (groupchat, ncts, dts, nick, jid, mess, timerid, cycle, mod), nsecs, False)
                        
                        curt = time.time()
                        
                        tnxt = curt + secs
                        
                        set_task_last(tskn, ncts)
                        set_task_remns(tskn, secs)
                        set_task_next(tskn, tnxt) 
                else:
                    add_fatal_task('remind_%s' % (timerid), rem_timer, (groupchat, cts, dts, nick, jid, mess, timerid), secs, True)
                
                return rep
            else:
                if not recover:
                    return reply(type, source, l('Too short time interval!'))
        elif len(spltdp) == 1:
            nrem = spltdp[0]
            
            if '-' in nrem:
                nrem = nrem.split('-', 1)
                nrem = rmv_empty_items(nrem)
                
                if len(nrem) == 1:
                    nrem = nrem[0]
                    
                    if nrem.isdigit():
                        nrem = int(nrem)
                    else:
                        return reply(type, source, l('Invalid syntax!'))
                    
                    reminds = get_reminds(groupchat)
                    
                    if type == 'public':
                        rems = check_reminds(reminds, groupchat)
                    else:
                        rems = check_reminds(reminds, jid)
                    
                    if not cycle:
                        nrems = [li for li in rems if not int(li[8])]
                    else:
                        nrems = [li for li in rems if int(li[8])]
                    
                    if not nrems:
                        if type == 'public':
                            if not cycle:
                                return reply(type, source, l('List of public reminds is empty!'))
                            return reply(type, source, l('List of public cycle tasks is empty!'))
                        else:
                            if not cycle:
                                return reply(type, source, l('List of reminds is empty!'))
                            return reply(type, source, l('List of cycle tasks is empty!'))
                    elif nrem > len(nrems):
                        if not cycle:
                            return reply(type, source, l('Invalid remind number!'))
                        return reply(type, source, l('Invalid cycle task number!'))
                    
                    timerid = nrems[nrem - 1][7]
                    mess = nrems[nrem - 1][5]
                    jid = nrems[nrem - 1][1]

                    if not cycle:
                        tskn = 'remind_%s' % (timerid)
                    else:
                        tskn = 'cycle_%s' % (timerid)

                    rmv_fatal_task(tskn)

                    res = del_remind(groupchat, jid, mess, timerid)
                    
                    if res == '':
                        rep = l('Delete error!')
                    else:
                        if type == 'public':
                            if not cycle:
                                rep = l('Public remind number %s has been removed!') % (nrem)
                            else:
                                rep = l('Public cycle task number %s has been removed!') % (nrem)
                        else:
                            if not cycle:
                                rep = l('Remind number %s has been removed!') % (nrem)
                            else:
                                rep = l('Cycle task number %s has been removed!') % (nrem)
                        
                    return reply(type, source, rep)
                else:
                    reminds = get_reminds(groupchat)
                    
                    if type == 'public':
                        rems = check_reminds(reminds, groupchat)
                    else:
                        rems = check_reminds(reminds, jid)
                    
                    if not cycle:
                        nrems = [li for li in rems if not int(li[8])]
                    else:
                        nrems = [li for li in rems if int(li[8])]
                    
                    if not nrems:
                        if type == 'public':
                            if not cycle:
                                return reply(type, source, l('List of public reminds is empty!'))
                            return reply(type, source, l('List of public cycle tasks is empty!'))
                        else:
                            if not cycle:
                                return reply(type, source, l('List of reminds is empty!'))
                            return reply(type, source, l('List of cycle tasks is empty!'))
                    
                    for nrem in nrems:
                        timerid = nrem[7]
                        mess = nrem[5]
                        jid = nrem[1]
                        
                        if cycle:
                            tskn = 'cycle_%s' % (timerid)
                        else:    
                            tskn = 'remind_%s' % (timerid)

                        rmv_fatal_task(tskn)

                        del_remind(groupchat, jid, mess, timerid)
                  
                    if not cycle:
                        return reply(type, source, l('List of remind has been cleared!'))
                    return reply(type, source, l('List of cycle tasks has been cleared!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        else:
            return reply(type, source, l('Invalid syntax!'))
    else:
        reminds = get_reminds(groupchat)
        rems = check_reminds(reminds, jid)
        prems = check_reminds(reminds, groupchat)
        
        if not cycle:
            nrems = [rel for rel in rems if rel[6] == 'run' and not int(rel[8])]
            nprems = [rel for rel in prems if rel[6] == 'run' and not int(rel[8])]
        else:
            nrems = [rel for rel in rems if rel[6] == 'run' and int(rel[8])]
            nprems = [rel for rel in prems if rel[6] == 'run' and int(rel[8])]
        
        if not cycle:
            nrepl = show_reminds(groupchat, jid, nrems, pref=l('Assigned at') + ' ', suff=l(', remain') + ' ')
            nrepp = show_reminds(groupchat, groupchat, nprems, pref=l('Assigned at') + ' ', suff=l(', remain') + ' ')
        else:
            nrepl = show_reminds(groupchat, jid, nrems, pref=l('Next run at') + ' ', suff=l(', remain') + ' ', cycle=True)
            nrepp = show_reminds(groupchat, groupchat, nprems, pref=l('Next run at') + ' ', suff=l(', remain') + ' ', cycle=True)
        
        if type == 'public':
            if nrepp: 
                if not cycle:
                    rep = l('Public reminds (total: %s):\n\n%s') % (len(nrepp), '\n\n'.join(nrepp))
                else:
                    rep = l('Public cycle tasks (total: %s):\n\n%s') % (len(nrepp), '\n\n'.join(nrepp))
                
                return reply(type, source, rep)
            else:
                if not cycle:
                    return reply(type, source, l('There are no public reminds!'))
                return reply(type, source, l('There are no public cycle tasks!'))
        else:
            if nrepl:
                if not cycle:
                    rep = l('Reminds (total: %s):\n\n%s') % (len(nrepl), '\n\n'.join(nrepl))
                else:
                    rep = l('Cycle tasks (total: %s):\n\n%s') % (len(nrepl), '\n\n'.join(nrepl))
                
                return reply(type, source, rep)
            else:
                if not cycle:
                    return reply(type, source, l('There are no private reminds!'))
                return reply(type, source, l('There are no private cycle tasks!'))

register_stage1_init(get_info_state)
register_join_handler(handler_user_join)
register_leave_handler(handler_user_leave)
register_presence_handler(handler_user_presence)

register_command_handler(handler_getrealjid, 'realjid', 20)
register_command_handler(handler_total_in_muc, 'users', 10)
register_command_handler(handler_bot_uptime, 'botup', 20)
register_command_handler(handler_bot_sestime, 'sestime', 20)
register_command_handler(handler_groupchats, 'chatrooms', 20)
register_command_handler(handler_nicks, 'nicks', 20)
register_command_handler(handler_here, 'here', 10)
register_command_handler(handler_seen, 'seen', 10)
register_command_handler(handler_members, 'members', 20)
register_command_handler(handler_admins, 'admins', 20)
register_command_handler(handler_owners, 'owners', 20)
register_command_handler(handler_outcasts, 'banned', 20)
register_command_handler(handler_remind, 'remind', 11)
register_command_handler(handler_ctask, 'ctask', 20)
register_command_handler(handler_tasks, 'tasks', 100)
register_command_handler(handler_dmess_control, 'dmess', 20)
register_command_handler(handler_tell, 'tell', 11)
register_command_handler(handler_thr_show, 'thr_show', 100)
register_command_handler(handler_thr_dump, 'thr_dump', 100)

register_message_handler(handler_dmess)

