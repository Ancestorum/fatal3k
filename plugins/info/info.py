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

def check_timerid(gch, timerid):
    cid = get_client_id()
    
    sql = "SELECT * FROM reminds WHERE timerid='%s';" % (timerid)
    qres = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
    
    if qres:
        return False
    else:
        return True
    
def rem_timer(groupchat, cts, dts, nick, jid, mess, timerid=''):
    atime = time.strftime('%H:%M:%S', time.localtime(dts))
    rsecs = int(round(dts - cts))
    
    if not nick:
        nick = get_rem_nick(groupchat, jid)
    
    source = [groupchat + '/' + nick, groupchat, nick]
    
    if is_groupchat(jid):
        type = 'public'
    else:
        type = 'private'
    
    if is_gch_user(groupchat, nick) or is_groupchat(jid):
        del_remind(groupchat, jid, mess, timerid)
        
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

        if is_var_set('commands', pcmd):
            cmdacc = get_fatal_var('commands', pcmd, 'access')
            ulvl = user_level(source, groupchat)

            if ulvl >= cmdacc:
                cmdhnd = get_fatal_var('command_handlers', pcmd)
                cmdhnd(type, source, pars)
                return

        if type == 'public':
            rep = l('Public remind at %s after %s:\n\n%s') % (atime, timeElapsed(rsecs), mess)            
            msg(jid, rep)
        else:
            rep = l('Remind at %s after %s:\n\n%s') % (atime, timeElapsed(rsecs), mess)
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
        
def save_remind(gch, nick, jid, rtime, ctms, dsts, mess, status, timerid):
    mess = mess.replace(r'"', r'&quot;')
    sql = "INSERT INTO reminds (nick, jid, rtime, ctms, dsts, mess, status, timerid) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (nick, jid, rtime, ctms, dsts, mess, status, timerid)
    
    cid = get_client_id()
    
    rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
    
    if rep != '':
        return rep
    else:
        upd_sql = "UPDATE reminds SET \"nick\"='%s', \"jid\"='%s', \"rtime\"='%s', \"ctms\"='%s', \"dsts\"='%s', \"status\"='%s', \"timerid\"='%s' WHERE mess='%s';" % (nick, jid, rtime, ctms, dsts, status, mess, timerid)
        
        rep = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), upd_sql)
        
        return rep

def recover_remind(gch, rem_handler, recover, reminds):
    for rem in reminds:
        remj = rem[1]
        
        if is_groupchat(remj):
            type = 'public'
        else:
            type = 'private'
        
        nick = get_rem_nick(gch, remj)
        
        source = [gch + '/' + nick, gch, nick]
        rem2 = rem[2]
        
        if not ':' in rem2:
            rem2 = time.strftime('%H:%M:%S', time.localtime(float(rem[4])))
        
        parameters = rem2 + ' ' + rem[5]
        
        rem_handler(type, source, parameters, recover, rem[1], rem[3], rem[7])

def show_reminds(gch, jid, reminds, pref='', suff=''):
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
        try:
            if is_groupchat(jid):
                sh_freml = [rel for rel in freml if rel[1] == jid]
            else:
                time.sleep(3)
                gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
                sh_freml = [rel for rel in freml if rel[1] == get_stripped(gch_dic[nick]['rjid'])]
        except Exception:
            return []
    
    if sh_freml:
        rng = list(range(len(sh_freml)))
        
        if suff:
            nremli = ['%s) %s%s%s:\n%s' % (li + 1, pref, time.strftime('%H:%M:%S', time.localtime(float(sh_freml[li][4]))), suff + timeElapsed(float(sh_freml[li][4]) - time.time()), sh_freml[li][5]) for li in rng]
        else:
            nremli = [l('%s) %s%s, %s ago:\n%s') % (li + 1, pref, time.strftime('%H:%M:%S', time.localtime(float(sh_freml[li][4]))), timeElapsed(time.time() - float(sh_freml[li][4])), sh_freml[li][5]) for li in rng]
        
        return nremli
    else:
        return []

def exp_reminds(reminds, jid):
    ctm = time.time()
    chkreml = [rel for rel in reminds if float(rel[4]) <= ctm and rel[1] == jid]
    return chkreml

def check_reminds(reminds, jid):
    ctm = time.time()
    chkreml = [rel for rel in reminds if float(rel[4]) > ctm and rel[1] == jid]
    return chkreml

def del_remind(gch, jid, mess, timerid=''):
    if timerid:
        del_sql = "DELETE FROM reminds WHERE jid='%s' AND mess='%s' AND timerid='%s';" % (jid, mess, timerid)
    else:
        del_sql = "DELETE FROM reminds WHERE jid='%s' AND mess='%s';" % (jid, mess)
    
    cid = get_client_id()
    
    res = sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), del_sql)
    
    return res

def get_reminds(gch):
    del_sql = "DELETE FROM reminds WHERE status='done';"
    
    cid = get_client_id()
    
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
        sql = 'CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, nick VARCHAR(30) NOT NULL, jid VARCHAR(30) NOT NULL, ujoin VARCHAR(20) NOT NULL, uleave VARCHAR(20) NOT NULL, reason VARCHAR, UNIQUE (nick));'
        sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX iusers ON users (nick);'
        sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
        
    if not is_db_exists('dynamic/%s/%s/reminds.db' % (cid, gch)):
        sql = 'CREATE TABLE reminds (nick VARCHAR(30) NOT NULL, jid VARCHAR(30) NOT NULL, rtime VARCHAR(20) NOT NULL, ctms VARCHAR(20) NOT NULL, dsts VARCHAR(20) NOT NULL, mess VARCHAR NOT NULL, status VARCHAR(10) NOT NULL, timerid VARCHAR(20) NOT NULL, UNIQUE (timerid));'
        sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
        
        sql = 'CREATE INDEX ireminds ON reminds (nick, jid);'
        sqlquery('dynamic/%s/%s/reminds.db' % (cid, gch), sql)
        
    if not is_db_exists('dynamic/%s/%s/dmess.db' % (cid, gch)):
        sql = 'CREATE TABLE dmess (snick VARCHAR(30) NOT NULL, sjid VARCHAR(30) NOT NULL, dnick VARCHAR(30) NOT NULL, djid VARCHAR(30) NOT NULL, mess VARCHAR NOT NULL, date VARCHAR(20) NOT NULL);'
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
        else:
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

def handler_remind(type, source, parameters, recover=False, jid='', rcts='', timerid=''):
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
                cts = time.time()
                dts = time.mktime(dst)
                
                secs = int(round(dts - cts))
                
                if abs(secs) != secs and not recover:
                    return reply(type, source, l('Expired remind!'))
            else:
                rtimes = spltdp[0]
                secs = int(rtimes) * 60
                cts = time.time()
                dts = cts + secs
            
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
                    timerid = 'task' + str(random.randrange(10000000, 99999999))
                    chk_tmrid = check_timerid(groupchat, timerid)
                    
                    while not chk_tmrid:
                        timerid = 'task' + str(random.randrange(10000000, 99999999))
                        chk_tmrid = check_timerid(groupchat, timerid)
                
                if type == 'public':
                    jid = groupchat
                
                if not recover:
                    save_remind(groupchat, nick, jid, rtimes, cts, dts, mess, 'run', timerid)
                
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
                    
                    if not rems:
                        if type == 'public':
                            return reply(type, source, l('List of public reminds is empty!'))
                        else:    
                            return reply(type, source, l('List of reminds is empty!'))
                    elif nrem > len(rems):
                        return reply(type, source, l('Invalid remind number!'))
                    
                    timerid = rems[nrem - 1][7]
                    mess = rems[nrem - 1][5]
                    jid = rems[nrem - 1][1]

                    tskn = 'remind_%s' % (timerid)

                    rmv_fatal_task(tskn)

                    res = del_remind(groupchat, jid, mess, timerid)
                    
                    if res == '':
                        rep = l('Delete error!')
                    else:
                        if type == 'public':
                            rep = l('Public remind number %s has been removed!') % (nrem)
                        else:
                            rep = l('Remind number %s has been removed!') % (nrem)
                        
                    return reply(type, source, rep)
                else:
                    reminds = get_reminds(groupchat)
                    
                    if type == 'public':
                        rems = check_reminds(reminds, groupchat)
                    else:
                        rems = check_reminds(reminds, jid)
                    
                    if not rems:
                        if type == 'public':
                            return reply(type, source, l('List of public reminds is empty!'))
                        else:    
                            return reply(type, source, l('List of reminds is empty!'))
                    
                    for nrem in rems:
                        timerid = nrem[7]
                        mess = nrem[5]
                        jid = nrem[1]
                        
                        tskn = 'remind_%s' % (timerid)

                        rmv_fatal_task(tskn)

                        del_remind(groupchat, jid, mess, timerid)
                  
                    return reply(type, source, l('List of remind has been cleared!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        else:
            return reply(type, source, l('Invalid syntax!'))
    else:
        reminds = get_reminds(groupchat)
        rems = check_reminds(reminds, jid)
        prems = check_reminds(reminds, groupchat)
        
        nrepl = show_reminds(groupchat, jid, rems, pref=l('Assigned at') + ' ', suff=l(', remain') + ' ')
        nrepp = show_reminds(groupchat, groupchat, prems, pref=l('Assigned at') + ' ', suff=l(', remain') + ' ')
        
        if type == 'public':
            if nrepp:
                rep = l('Public reminds (total: %s):\n\n%s') % (len(nrepp), '\n\n'.join(nrepp))
                
                return reply(type, source, rep)
            else:
                return reply(type, source, l('There are no public reminds!'))
        else:
            if nrepl:
                rep = l('Reminds (total: %s):\n\n%s') % (len(nrepl), '\n\n'.join(nrepl))
                
                return reply(type, source, rep)
            else:
                return reply(type, source, l('There are no private reminds!'))

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
register_command_handler(handler_dmess_control, 'dmess', 20)
register_command_handler(handler_tell, 'tell', 11)
register_command_handler(handler_thr_show, 'thr_show', 100)
register_command_handler(handler_thr_dump, 'thr_dump', 100)

register_message_handler(handler_dmess)

