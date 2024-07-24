# -*- coding: utf-8 -*-

#  fatal plugin
#  muc plugin

#  Copyright © 2009-2024 Ancestors Soft

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

from fatalapi import *

def compile_re_patt(gch, amuc):
    qli = show_amuc(gch, amuc)
    
    if qli != '':
        patts = []
        
        for rexp in qli:
            exp = '^%s$' % (rexp[0])
            
            if len(rexp) == 2:
                reason = rexp[1]
            else:
                reason = ''
        
            try:
                exp = re.compile(exp)
            except Exception:
                exp = None
            
            patts.append((exp, reason))
            
        if patts:
            return patts

def muc_set_role(func, type, source, parameters):
    groupchat = source[1]
    
    sparams = safe_split(parameters)
    nick = sparams[0]
    reason = sparams[1]
    
    if check_jid(nick):
        nick = get_muc_nick(groupchat, nick)

    if is_gch_user(groupchat, nick):
        resp = func(groupchat, nick, reason)
        
        if resp:
            return reply(type, source, l('Done!'))
        else:
            return reply(type, source, l('Unable to perform this operation!'))
    else:
        return reply(type, source, l('User not found!'))

def muc_set_aff(func, type, source, parameters):
    groupchat = source[1]
    
    sparams = safe_split(parameters)
    nick_jid = sparams[0]
    reason = sparams[1]
    
    if is_gch_user(groupchat, nick_jid):
        if func.__name__ == 'none' and reason == 'unban':
            return reply(type, source, l('Unable to perform this operation!'))
        
        resp = func(groupchat, nick_jid, reason)
        
        if func.__name__ == 'ban':
            del_banned(groupchat, nick_jid)
        
        if resp:
            return reply(type, source, l('Done!'))
        else:
            return reply(type, source, l('Unable to perform this operation!'))
    elif check_jid(nick_jid):
        resp = func(groupchat, nick_jid, reason)
            
        if resp:
            reply(type, source, l('Done!'))
        else:
            reply(type, source, l('Unable to perform this operation!'))
    else:
        reply(type, source, l('User not found!')) 


def del_banned(gch, nick):
    if not nick:
        nick = ''
    
    sql = "DELETE FROM users WHERE nick=?;"
    
    cid = get_client_id()
    
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql, nick)
    
    if qres == []:
        return True

def get_join_nick(gch, jid):
    cid = get_client_id()
    
    nick = ''
    
    gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
    
    try:
        nickl = [li for li in gch_dic if jid in gch_dic[li]['rjid']]
    except Exception:
        try:
            time.sleep(3)
            gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
            nickl = [li for li in gch_dic if jid in gch_dic[li]['rjid']]
        except Exception:
            return nick
    
    if nickl:
        nick = nickl[-1]
        
    return nick
    
def get_muc_nick(gch, jid):
    cid = get_client_id()
    
    sql = "SELECT nick FROM users WHERE jid=? ORDER BY ujoin;"
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql, jid)
    
    if qres:
        nick = qres[-1][0]
        return nick

def get_muc_jid(gch, nick):
    cid = get_client_id()

    sql = "SELECT jid FROM users WHERE nick=?;"
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql, nick)
    
    if qres:
        jid = qres[0][0]
        return jid

def set_subject(groupchat, subject):
    msg = xmpp.Message(groupchat)
    msg.setID('topic%s' % (time.time()))
    msg.setType('groupchat')
    msg.setTagData('subject', subject)
    
    jconn = get_client_conn()
    resp = jconn.send(msg)
    
    if resp:
        return True

def kick(groupchat, nick, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    Id = 'kick%s' % (time.time())
    iq.setID(Id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    kick = query.addChild('item', {'nick': nick, 'role': 'none'})
    kick.setTagData('reason', reason.strip())
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    resp = jconn.send(iq)
    
    if Id == resp:
        return True

def ban(groupchat, nick_jid, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    Id = 'ban%s' % (time.time())
    iq.setID(Id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    
    if check_jid(nick_jid):
        ban = query.addChild('item', {'jid': nick_jid, 'affiliation': 'outcast'})
    else:
        ban = query.addChild('item', {'nick': nick_jid, 'affiliation': 'outcast'})
    
    ban.setTagData('reason', reason.strip())
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    resp = jconn.send(iq)
    
    if Id == resp:
        return True

def none(groupchat, nick_jid, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    Id = 'none%s' % (time.time())
    iq.setID(Id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    
    if check_jid(nick_jid):
        none = query.addChild('item', {'jid': nick_jid, 'affiliation': 'none'})
    else:
        none = query.addChild('item', {'nick': nick_jid, 'affiliation': 'none'})
    
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    resp = jconn.send(iq)
    
    if Id == resp:
        return True

def visitor(groupchat, nick, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    Id = 'devoice%s' % (time.time())
    iq.setID(Id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    visitor = query.addChild('item', {'nick': nick, 'role': 'visitor'})
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    resp = jconn.send(iq)
    
    if Id == resp:
        return True

def participant(groupchat, nick, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    Id = 'voice%s' % (time.time())
    iq.setID(Id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    participant = query.addChild('item', {'nick': nick, 'role': 'participant'})
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    resp = jconn.send(iq)
    
    if Id == resp:
        return True
    
def member(groupchat, nick_jid, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    Id = 'member%s' % (time.time())
    iq.setID(Id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    
    if check_jid(nick_jid):
        member = query.addChild('item', {'jid': nick_jid, 'affiliation': 'member'})
    else:
        member = query.addChild('item', {'nick': nick_jid, 'affiliation': 'member'})
    
    member.setTagData('reason', reason.strip())
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    resp = jconn.send(iq)
    
    if Id == resp:
        return True
    
def moderator(groupchat, nick, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    Id = 'moder%s' % (time.time())
    iq.setID(Id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    moderator = query.addChild('item', {'nick': nick, 'role': 'moderator'})
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    resp = jconn.send(iq)
    
    if Id == resp:
        return True

def admin(groupchat, nick_jid, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    Id = 'admin%s' % (time.time())
    iq.setID(Id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    
    if check_jid(nick_jid):
        admin = query.addChild('item', {'jid': nick_jid, 'affiliation': 'admin'})
    else:
        admin = query.addChild('item', {'nick': nick_jid, 'affiliation': 'admin'})
    
    admin.setTagData('reason', reason.strip())
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    resp = jconn.send(iq)
    
    if Id == resp:
        return True

def owner(groupchat, nick_jid, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    Id = 'owner%s' % (time.time())
    iq.setID(Id)
    query = xmpp.Node('query')
    query.setNamespace(xmpp.NS_MUC_ADMIN)
    
    if check_jid(nick_jid):
        owner = query.addChild('item', {'jid': nick_jid, 'affiliation': 'owner'})
    else:
        owner = query.addChild('item', {'nick': nick_jid, 'affiliation': 'owner'})
    
    owner.setTagData('reason', reason.strip())
    iq.addChild(node=query)
    
    jconn = get_client_conn()
    resp = jconn.send(iq)
    
    if Id == resp:
        return True

def save_amuc(gch, amuc, exp, reason=''):
    if amuc == 'akick' or amuc == 'aban':
        sql = "INSERT INTO %s (exp,reason) VALUES (?, ?);" % (amuc)
        args = exp.strip(), reason.strip()
    else:
        sql = "INSERT INTO %s (exp) VALUES (?);" % (amuc)
        args = (exp.strip(),)
    
    cid = get_client_id()
    
    rep = sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql, *args)
        
    return rep
    
def show_amuc(gch, amuc):
    if amuc == 'akick' or amuc == 'aban':
        sql = 'SELECT exp,reason FROM %s;' % (amuc)
    else:
        sql = 'SELECT exp FROM %s;' % (amuc)
    
    cid = get_client_id()
    
    rep = sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)
    return rep

def del_amuc(gch, amuc, amucre):
    sql = "DELETE FROM %s WHERE exp=?;" % (amuc)
    
    cid = get_client_id()
    
    rep = sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql, amucre)
        
    return rep

def clear_amuc(gch, amuc):
    sql = 'DELETE FROM %s;' % (amuc)
    
    cid = get_client_id()
    
    rep = sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)
        
    return rep

def set_amuc(gch, amfunc, cpatt, nick, jid):
    amucnifi = []
    reason = ''
    
    if cpatt:
        for amli in cpatt:
            exp = amli[0]

            if exp:
                amucnifi = exp.findall(nick)
            
            if amucnifi:
                reason = amli[1]
                break
        
    if amucnifi:
        if amfunc.__name__ != 'moderator' and user_level(gch + '/' + nick, gch) <= 10:
            amfunc(gch, amucnifi[-1], reason)
            return amfunc.__name__
        elif amfunc.__name__ == 'moderator':
            amfunc(gch, amucnifi[-1], reason)
            return amfunc.__name__

    amucjifi = []

    if cpatt:
        for amli in cpatt:
            exp = amli[0]

            if exp:
                amucjifi = exp.findall(jid)
            
            if amucjifi:
                reason = amli[1]
                break
    
    if amucjifi:
        if amfunc.__name__ != 'ban':
            nick = get_join_nick(gch, amucjifi[-1])
            
            if nick:
                if amfunc.__name__ != 'moderator' and user_level(gch + '/' + nick, gch) <= 10:
                    amfunc(gch, nick, reason)
                    return amfunc.__name__
                elif amfunc.__name__ == 'moderator':
                    amfunc(gch, nick, reason)
                    return amfunc.__name__
        else:
            if user_level(gch + '/' + nick, gch) <= 10:
                amfunc(gch, jid, reason)

def process_avoice(gch, nick):
    avtm = int(get_gch_param(gch, 'av_time', '15'))
    time.sleep(avtm)
    
    if is_gch_user(gch, nick):
        participant(gch, nick, '')

def process_regvoice(gch, nick, jid):
    rvquest = get_gch_param(gch, 'rv_quest', '2+2*2 = ?')
    rvmess = get_gch_param(gch, 'rv_mess', l('Hi, %nick%, you have joined in %conf%, one of the best groupchats of this jabber server! ;) If you want to chat with us, please answer on simple question below, you have %tries% tries. If answer will be right you get voice automatically:'))
    rvtries = int(get_gch_param(gch, 'rv_tries', '3'))
    
    rvmess = rvmess.replace('%nick%', nick).replace('%conf%', gch).replace('%tries%', str(rvtries)) + '\n\n' + l('Question: %s') % (rvquest)
    
    if is_gch_user(gch, nick):
        msg(jid, rvmess)

def handler_muc_join(groupchat, nick, aff, role):
    cid = get_client_id()
    
    #jid = get_true_jid(groupchat + '/' + nick)
    jid = get_fatal_var(cid, 'gchrosters', groupchat, nick, 'rjid')
    
    res = ''
    
    avon = int(get_gch_param(groupchat, 'av_on', '0'))
    rvon = int(get_gch_param(groupchat, 'rv_on', '0'))

    amexp = get_fatal_var(cid, 'amoder_comp_exp', groupchat)
    
    if amexp:
        res = set_amuc(groupchat, moderator, amexp, nick, jid)
        
        if res == 'moderator':
            return
    
    avexp = get_fatal_var(cid, 'avisitor_comp_exp', groupchat)
    
    if avexp and aff == 'none':
        res = set_amuc(groupchat, visitor, avexp, nick, jid)
            
    if (role == 'visitor' and aff == 'none') or res == 'visitor':
        if rvon:
            time.sleep(10)
            racc = user_level(groupchat + '/' + nick, groupchat)
            
            if racc == 0:
                set_fatal_var(cid, 'regvoice', jid, {groupchat: {'tries': 0, 'nick': nick}})
                
                gchs = get_fatal_var(cid, 'regvoice', jid, 'gchs')
                
                if not gchs:
                    gchs = []
                    set_fatal_var(cid, 'regvoice', jid, 'gchs', gchs)
                
                gchs.append(groupchat)
                
                add_jid_to_privacy(jid, active=False)
                
                process_regvoice(groupchat, nick, jid)
                return

        if avon:
            process_avoice(groupchat, nick)
            return
    
    akexp = get_fatal_var(cid, 'akick_comp_exp', groupchat)
    
    if akexp and aff == 'none':
        res = set_amuc(groupchat, kick, akexp, nick, jid)
        
        if res == 'kick':
            return
    
    abexp = get_fatal_var(cid, 'aban_comp_exp', groupchat)
    
    if abexp and aff == 'none':
        set_amuc(groupchat, ban, abexp, nick, jid)

def handler_muc_leave(groupchat, nick, reason, code):
    cid = get_client_id()
    
    jid = get_muc_jid(groupchat, nick)
    rmv_fatal_var(cid, 'regvoice', jid)

def handler_regvoice_processansw(type, source, body):
    cid = get_client_id()
    
    gch_jid = source[1]
    
    if is_groupchat(gch_jid):
        return
    
    jid = gch_jid
    
    if is_var_set(cid, 'regvoice', jid):
        groupchat = get_list_fatal_var(cid, 'regvoice', jid, 'gchs')[-1]
        vitries = get_int_fatal_var(cid, 'regvoice', jid, groupchat, 'tries')
        rvtries = int(get_gch_param(groupchat, 'rv_tries', '3'))
        
        if vitries <= rvtries:
            rvquest = get_gch_param(groupchat, 'rv_quest', '2+2*2 = ?')
            viansw = body.lower().strip()
            rvansw = get_gch_param(groupchat, 'rv_answ', '6').lower().strip()
            
            if viansw == rvansw:
                rep = l('Your answer is right! You are welcome in %s and have a good chat! You will get voice automatically after 10 seconds!') % (groupchat)
                nick = get_fatal_var('regvoice', jid, groupchat, 'nick')
                
                msg(jid, rep)
                
                gchs = get_fatal_var(cid, 'regvoice', jid, 'gchs')
                
                rmv_fatal_var(cid, 'regvoice', jid, groupchat)
                
                gchs.remove(groupchat)
                
                if not is_var_set(cid, 'regvoice', jid, 'gchs'):
                    rmv_fatal_var(cid, 'regvoice', jid)
                    
                time.sleep(10)
                
                participant(groupchat, nick, '')
                
                rmv_jid_from_privacy(jid, active=False)
            else:
                if vitries + 2 > rvtries:
                    if rvtries:
                        rep = l('Your answer is incorrect! You have exhausted all your tries, to get voice ask moderators of %s!') % (groupchat)
                        
                        msg(jid, rep)
                        
                        gchs = get_fatal_var(cid, 'regvoice', jid, 'gchs')
                        
                        rmv_fatal_var(cid, 'regvoice', jid, groupchat)
                        
                        gchs.remove(groupchat)
                        
                        if not is_var_set(cid, 'regvoice', jid, 'gchs'):
                            rmv_fatal_var(cid, 'regvoice', jid)
                     
                        rmv_jid_from_privacy(jid, active=False)
                     
                        return
                
                rep = l('Your answer is incorrect! Try again! Question will be repeated after 3 seconds!')
                
                msg(jid, rep)
                
                if rvtries:
                    inc_fatal_var(cid, 'regvoice', jid, groupchat, 'tries')
                
                time.sleep(3)
                
                rep = l('Question: %s') % (rvquest)
                
                msg(jid, rep)
    
def handler_muc_presence(prs):
    cid = get_client_id()
    
    ptype = prs.getType()
    pfrom = prs.getFrom()
    groupchat = get_stripped(pfrom)
    nick = get_resource(pfrom)
    #jid = get_true_jid(groupchat + '/' + nick)
    jid = get_fatal_var(cid, 'gchrosters', groupchat, nick, 'rjid')
    scode = prs.getStatusCode()

    if scode == '303' and ptype == 'unavailable':
        newnick = prs.getNick()
        
        amexp = get_fatal_var(cid, 'amoder_comp_exp', groupchat)
        
        if amexp:
            set_amuc(groupchat, moderator, amexp, newnick, jid)
        
        avexp = get_fatal_var(cid, 'avisitor_comp_exp', groupchat)
        
        if avexp:
            set_amuc(groupchat, visitor, avexp, newnick, jid)
        
        akexp = get_fatal_var(cid, 'akick_comp_exp', groupchat)
        
        if akexp:
            set_amuc(groupchat, kick, akexp, newnick, jid)
        
        abexp = get_fatal_var(cid, 'aban_comp_exp', groupchat)
        
        if abexp:
            set_amuc(groupchat, ban, abexp, newnick, jid)
    
    if is_var_set(cid, 'regvoice', jid):
        racc = user_level(pfrom, groupchat)
        
        if racc >= 10:
            rep = l('Voice has been given by moderator, it means that no need to answer the question. You are welcome in %s and have a good chat!') % (groupchat)
            
            msg(jid, rep)
            
            gchs = get_fatal_var(cid, 'regvoice', jid, 'gchs')
            
            rmv_fatal_var(cid, 'regvoice', jid, groupchat)
            
            gchs.remove(groupchat)
            
            if not is_var_set(cid, 'regvoice', jid, 'gchs'):
                rmv_fatal_var(cid, 'regvoice', jid)
    
def get_muc_state(gch):
    if not param_exists(gch, 'av_on'):
        set_gch_param(gch, 'av_on', '0')
    if not param_exists(gch, 'av_time'):
        set_gch_param(gch, 'av_time', '15')
        
    if not param_exists(gch, 'rv_on'):
        set_gch_param(gch, 'rv_on', '0')
    if not param_exists(gch, 'rv_mess'):
        set_gch_param(gch, 'rv_mess', l('Hi, %nick%, you have joined in %conf%, one of the best groupchats of this jabber server! ;) If you want to chat with us, please answer on simple question below, you have %tries% tries. If answer will be right you get voice automatically:'))
    if not param_exists(gch, 'rv_quest'):
        set_gch_param(gch, 'rv_quest', '2+2*2 = ?')
    if not param_exists(gch, 'rv_answ'):
        set_gch_param(gch, 'rv_answ', '6')
    if not param_exists(gch, 'rv_tries'):
        set_gch_param(gch, 'rv_tries', '3')
    
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/amuc.db' % (cid, gch)):
        sql = 'CREATE TABLE avisitor(id INTEGER PRIMARY KEY AUTOINCREMENT, exp VARCHAR, UNIQUE (exp));'
        sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX iavisitor ON avisitor (exp);'
        sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)

        sql = 'CREATE TABLE akick(id INTEGER PRIMARY KEY AUTOINCREMENT, exp VARCHAR, reason VARCHAR, UNIQUE (exp));'
        sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX iakick ON akick (exp);'
        sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)

        sql = 'CREATE TABLE amoderator(id INTEGER PRIMARY KEY AUTOINCREMENT, exp VARCHAR, UNIQUE (exp));'
        sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX iamoderator ON amoderator (exp);'
        sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)

        sql = 'CREATE TABLE aban(id INTEGER PRIMARY KEY AUTOINCREMENT, exp VARCHAR, reason VARCHAR, UNIQUE (exp));'
        sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX iaban ON aban (exp);'
        sqlquery('dynamic/%s/%s/amuc.db' % (cid, gch), sql)
    else:
        set_fatal_var(cid, 'akick_comp_exp', gch, compile_re_patt(gch, 'akick'))
        set_fatal_var(cid, 'amoder_comp_exp', gch, compile_re_patt(gch, 'amoderator'))
        set_fatal_var(cid, 'avisitor_comp_exp', gch, compile_re_patt(gch, 'avisitor'))
        set_fatal_var(cid, 'aban_comp_exp', gch, compile_re_patt(gch, 'aban'))

def handler_regvoice_control(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))
        
        if int(parameters) > 1:
            return reply(type, source, l('Invalid syntax!'))
        
        if parameters == '1':
            set_gch_param(groupchat, 'rv_on', '1')
            return reply(type, source, l('Voice registration has been turned on!'))
        else:
            set_gch_param(groupchat, 'rv_on', '0')
            return reply(type, source, l('Voice registration has been turned off!'))
    else:
        rvon = int(get_gch_param(groupchat, 'rv_on', '0'))
        
        if rvon:
            return reply(type, source, l('Voice registration is turned on!'))
        else:
            return reply(type, source, l('Voice registration is turned off!'))

def handler_regvoice_rvquest(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        set_gch_param(groupchat, 'rv_quest', parameters.strip())
        return reply(type, source, l('Question for voice registration has been set!'))
    else:
        rvquest = get_gch_param(groupchat, 'rv_quest', '2+2*2 = ?')
        return reply(type, source, l('Question for voice registration in this groupchat: %s') % (rvquest))

def handler_regvoice_rvansw(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        set_gch_param(groupchat, 'rv_answ', parameters.strip())
        return reply(type, source, l('Answer for voice registration has been set!'))
    else:
        rvansw = get_gch_param(groupchat, 'rv_answ', '6')
        return reply(type, source, l('Answer for voice registration in this groupchat: %s') % (rvansw))

def handler_regvoice_rvmess(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        set_gch_param(groupchat, 'rv_mess', parameters.strip())
        return reply(type, source, l('Query message for voice registration has been set!'))
    else:
        rvmess = get_gch_param(groupchat, 'rv_mess', l('Hi, %nick%, you have joined in %conf%, one of the best groupchats of this jabber server! ;) If you want to chat with us, please answer on simple question below, you have %tries% tries. If answer will be right you get voice automatically:'))
        return reply(type, source, l('Query message for voice registration in this groupchat: %s') % (rvmess))

def handler_regvoice_rvtries(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    parameters = parameters.strip()
    
    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))

        if int(parameters) < 0:
            return reply(type, source, l('Invalid syntax!'))

        set_gch_param(groupchat, 'rv_tries', parameters)
        return reply(type, source, l('Tries for voice registration has been set to %s!') % (parameters))
    else:
        rvtries = get_gch_param(groupchat, 'rv_tries', '3')
        return reply(type, source, l('Tries for voice registration in this groupchat %s!') % (rvtries))

def handler_avoice_control(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))

        if int(parameters) > 1:
            return reply(type, source, l('Invalid syntax!'))

        if parameters == '1':
            set_gch_param(groupchat, 'av_on', '1')
            return reply(type, source, l('Auto-voice has been turned on!'))
        else:
            set_gch_param(groupchat, 'av_on', '0')
            return reply(type, source, l('Auto-voice has been turned off!'))
    else:
        avon = int(get_gch_param(groupchat, 'av_on', '0'))
        
        if avon:
            return reply(type, source, l('Auto-voice is turned on!'))
        else:
            return reply(type, source, l('Auto-voice is turned off!'))

def handler_avoice_avtime(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    parameters = parameters.strip()
    
    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))

        if int(parameters) > 300 or int(parameters) < 3:
            return reply(type, source, l('Invalid syntax!'))

        set_gch_param(groupchat, 'av_time', parameters)
        return reply(type, source, l('Auto-voice timeout has been set to %s seconds!') % (parameters))
    else:
        avtime = get_gch_param(groupchat, 'av_time', '15')
        return reply(type, source, l('Auto-voice timeout is set to %s seconds!') % (avtime))

def handler_akick(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    spltd = safe_split(parameters)
    exp = spltd[0]
    reason = spltd[1]
    
    if parameters and not parameters[1:].isdigit() and len(parameters) != 1:
        res = save_amuc(groupchat, 'akick', exp, reason)
        
        if res != '':
            akexp = compile_re_patt(groupchat, 'akick')
            
            set_fatal_var(cid, 'akick_comp_exp', groupchat, akexp)
           
            gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))
            
            for nick in gch_dic:
                if not 'rjid' in gch_dic[nick]:
                    continue

                jid = gch_dic[nick]['rjid'] #get_stripped(gch_dic[nick]['rjid'])
                
                if is_gch_user(groupchat, nick):
                    set_amuc(groupchat, kick, akexp, nick, jid)
            
            return reply(type, source, l('Rule has been added!'))
        else:
            return reply(type, source, l('Insert error!'))
    elif parameters and parameters[1:].isdigit() and parameters.startswith('-'):
        parameters = parameters[1:]
        akreli = show_amuc(groupchat, 'akick')
        renum = int(parameters)
        
        if renum > len(akreli) or renum <= 0:
            return reply(type, source, l('Invalid number of rule!'))

        amucre = akreli[renum - 1][0]
        dres = del_amuc(groupchat, 'akick', amucre)
        
        if dres != '':
            akexp = compile_re_patt(groupchat, 'akick')
            set_fatal_var(cid, 'akick_comp_exp', groupchat, akexp)
            return reply(type, source, l('Rule has been removed!'))
        else:
            return reply(type, source, l('Delete error!'))
    elif parameters and parameters.strip() == '-' and len(parameters) == 1:
        qres = clear_amuc(groupchat, 'akick')
        
        if qres != '':
            rmv_fatal_var(cid, 'akick_comp_exp', groupchat)
            rep = l('List of auto-kick rules has been cleared!')
        else:
            rep = l('Unable to clear auto-kick rules!')
        
        return reply(type, source, rep)
    else:
        akreli = show_amuc(groupchat, 'akick')
        fakreli = []
        
        for rexp in akreli:
            exp = rexp[0]
            reason = rexp[1]
            
            if reason:
                fakreli.append(l('%s / Reason: %s') % (exp, reason))
            else:
                fakreli.append(exp)
        
        nakreli = get_num_list(fakreli)
        
        if akreli:
            rep = l('List of auto-kick rules (total: %s):\n\n%s') % (len(nakreli), '\n'.join(nakreli))
        else:
            rep = l('List of auto-kick rules is empty!')
            
        if type == 'public':
            reply(type, source, l('Look in private!'))
            
        if type == 'console':
            return reply(type, source, rep)
        else:
            return reply('private', source, rep)

def handler_amoderator(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    spltd = safe_split(parameters)
    exp = spltd[0]
    
    if parameters and not parameters[1:].isdigit() and len(parameters) != 1:
        res = save_amuc(groupchat, 'amoderator', exp)
        
        if res != '':
            amexp = compile_re_patt(groupchat, 'amoderator')
            
            set_fatal_var(cid, 'amoder_comp_exp', groupchat, amexp)
           
            gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))
            
            for nick in gch_dic:
                if not 'rjid' in gch_dic[nick]:
                    continue

                jid = gch_dic[nick]['rjid'] #get_stripped(gch_dic[nick]['rjid'])
                
                if is_gch_user(groupchat, nick):
                    set_amuc(groupchat, moderator, amexp, nick, jid)
            
            return reply(type, source, l('Rule has been added!'))
        else:
            return reply(type, source, l('Insert error!'))
    elif parameters and parameters[1:].isdigit() and parameters.startswith('-'):
        parameters = parameters[1:]
        amreli = show_amuc(groupchat, 'amoderator')
        renum = int(parameters)
        
        if renum > len(amreli) or renum <= 0:
            return reply(type, source, l('Invalid number of rule!'))

        amucre = amreli[renum - 1][0]
        dres = del_amuc(groupchat, 'amoderator', amucre)
        
        if dres != '':
            amexp = compile_re_patt(groupchat, 'amoderator')
            set_fatal_var(cid, 'amoder_comp_exp', groupchat, amexp)
            return reply(type, source, l('Rule has been removed!'))
        else:
            return reply(type, source, l('Delete error!'))
    elif parameters and parameters.strip() == '-' and len(parameters) == 1:
        qres = clear_amuc(groupchat, 'amoderator')
        
        if qres != '':
            rmv_fatal_var(cid, 'amoder_comp_exp', groupchat)
            rep = l('List of auto-moderator rules has been cleared!')
        else:
            rep = l('Unable to clear auto-moderator rules!')
        
        return reply(type, source, rep)
    else:
        amreli = show_amuc(groupchat, 'amoderator')
        
        famreli = [li[0] for li in amreli]
        namreli = get_num_list(famreli)
        
        if amreli:
            rep = l('List of auto-moderator rules (total: %s):\n\n%s') % (len(namreli), '\n'.join(namreli))
        else:
            rep = l('List of auto-moderator rules is empty!')
        
        if type == 'public':
            reply(type, source, l('Look in private!'))
            
        if type == 'console':
            return reply(type, source, rep)
        else:
            return reply('private', source, rep)

def handler_avisitor(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    spltd = safe_split(parameters)
    exp = spltd[0]
    reason = spltd[1]
    
    if parameters and not parameters[1:].isdigit() and len(parameters) != 1:
        res = save_amuc(groupchat, 'avisitor', exp)
        
        if res != '':
            avexp = compile_re_patt(groupchat, 'avisitor')
            
            set_fatal_var(cid, 'avisitor_comp_exp', groupchat, avexp)
           
            gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))
            
            for nick in gch_dic:
                if not 'rjid' in gch_dic[nick]:
                    continue

                jid = gch_dic[nick]['rjid'] #get_stripped(gch_dic[nick]['rjid'])
                
                if is_gch_user(groupchat, nick):
                    set_amuc(groupchat, visitor, avexp, nick, jid)
            
            return reply(type, source, l('Rule has been added!'))
        else:
            return reply(type, source, l('Insert error!'))
    elif parameters and parameters[1:].isdigit() and parameters.startswith('-'):
        parameters = parameters[1:]
        avreli = show_amuc(groupchat, 'avisitor')
        renum = int(parameters)
        
        if renum > len(avreli) or renum <= 0:
            return reply(type, source, l('Invalid number of rule!'))
        
        amucre = avreli[renum - 1][0]
        dres = del_amuc(groupchat, 'avisitor', amucre)
        
        if dres != '':
            avexp = compile_re_patt(groupchat, 'avisitor')
            set_fatal_var(cid, 'avisitor_comp_exp', groupchat, avexp)
            return reply(type, source, l('Rule has been removed!'))
        else:
            return reply(type, source, l('Delete error!'))
    elif parameters and parameters.strip() == '-' and len(parameters) == 1:
        qres = clear_amuc(groupchat, 'avisitor')
        
        if qres != '':
            rmv_fatal_var(cid, 'avisitor_comp_exp', groupchat)
            rep = l('List of auto-visitor rules has been cleared!')
        else:
            rep = l('Unable to clear auto-visitor rules!')
        
        return reply(type, source, rep)
    else:
        avreli = show_amuc(groupchat, 'avisitor')
        
        favreli = [li[0] for li in avreli]
        navreli = get_num_list(favreli)
        
        if avreli:
            rep = l('List of auto-visitor rules (total: %s):\n\n%s') % (len(navreli), '\n'.join(navreli))
        else:
            rep = l('List of auto-visitor rules is empty!')
        
        if type == 'public':
            reply(type, source, l('Look in private!'))
            
        if type == 'console':
            return reply(type, source, rep)
        else:
            return reply('private', source, rep)

def handler_aban(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
    
    spltd = safe_split(parameters)
    exp = spltd[0]
    reason = spltd[1]
    
    if parameters and not parameters[1:].isdigit() and len(parameters) != 1:
        res = save_amuc(groupchat, 'aban', exp, reason)
        
        if res != '':
            abexp = compile_re_patt(groupchat, 'aban')
            
            set_fatal_var(cid, 'aban_comp_exp', groupchat, abexp)
           
            gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', groupchat))
            
            for nick in gch_dic:
                if not 'rjid' in gch_dic[nick]:
                    continue

                jid = gch_dic[nick]['rjid'] #get_stripped(gch_dic[nick]['rjid'])
                
                if is_gch_user(groupchat, nick):
                    set_amuc(groupchat, ban, abexp, nick, jid)
            
            return reply(type, source, l('Rule has been added!'))
        else:
            return reply(type, source, l('Insert error!'))
    elif parameters and parameters[1:].isdigit() and parameters.startswith('-'):
        parameters = parameters[1:]
        abreli = show_amuc(groupchat, 'aban')
        renum = int(parameters)
        
        if renum > len(abreli) or renum <= 0:
            return reply(type, source, l('Invalid number of rule!'))
        
        amucre = abreli[renum - 1][0]
        dres = del_amuc(groupchat, 'aban', amucre)
        
        if dres != '':
            abexp = compile_re_patt(groupchat, 'aban')
            set_fatal_var(cid, 'aban_comp_exp', groupchat, abexp)
            return reply(type, source, l('Rule has been removed!'))            
        else:
            return reply(type, source, l('Delete error!'))
    elif parameters and parameters.strip() == '-' and len(parameters) == 1:
        qres = clear_amuc(groupchat, 'aban')
        
        if qres != '':
            rmv_fatal_var(cid, 'aban_comp_exp', groupchat)
            rep = l('List of auto-ban rules has been cleared!')            
        else:
            rep = l('Unable to clear auto-ban rules!')
        
        return reply(type, source, rep)
    else:
        abreli = show_amuc(groupchat, 'aban')
        fabreli = []
        
        for rexp in abreli:
            exp = rexp[0]
            reason = rexp[1]
            
            if reason:
                fabreli.append(l('%s / Reason: %s') % (exp, reason))
            else:
                fabreli.append(exp)

        nabreli = get_num_list(fabreli)

        if abreli:
            rep = l('List of auto-ban rules (total: %s):\n\n%s') % (len(nabreli), '\n'.join(nabreli))
        else:
            rep = l('List of auto-ban rules is empty!')
        
        if type == 'public':
            reply(type, source, l('Look in private!'))
            
        if type == 'console':
            return reply(type, source, rep)
        else:
            return reply('private', source, rep)

def handler_set_subject(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        resp = set_subject(groupchat, parameters)
        
        if resp:
            return reply(type, source, l('Done!'))
        else:
            return reply(type, source, l('Unable to set topic!'))
    else:
        subject = get_fatal_var(cid, 'gch_subjs', groupchat)
        
        if subject:
            rep = l('Current topic in this groupchat:\n\n%s') % (subject)
        else:
            rep = l('Topic has not been set yet!')
        
        return reply(type, source, rep)
    
def handler_kick(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_role(kick, type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_global_ban(type, source, parameters):
    cid = get_client_id()
    
    gchs = list(get_fatal_var(cid, 'gchrosters'))
    
    if parameters:
        for gch in gchs:
            nsrc = [gch, gch, '']
            
            handler_ban('null', nsrc, parameters)
            
        return reply(type, source, l('Done!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_ban(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_aff(ban, type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_none(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_aff(none, type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_member(type, source, parameters):
    groupchat = source[1]

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_aff(member, type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_admin(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_aff(admin, type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_owner(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_aff(owner, type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_moderator(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_role(moderator, type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_visitor(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_role(visitor, type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_participant(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_role(participant, type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_unban(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        muc_set_aff(none, type, source, parameters + ':unban')
    else:
        return reply(type, source, l('Invalid syntax!'))
    
register_command_handler(handler_kick, 'kick', 16)
register_command_handler(handler_ban, 'ban', 20)
register_command_handler(handler_global_ban, 'gban', 100)
register_command_handler(handler_visitor, 'visitor', 16)
register_command_handler(handler_participant, 'participant', 16)
register_command_handler(handler_unban, 'unban', 20)
register_command_handler(handler_none, 'none', 20)
register_command_handler(handler_member, 'member', 20)
register_command_handler(handler_moderator, 'moderator', 20)
register_command_handler(handler_admin, 'admin', 30)
register_command_handler(handler_owner, 'owner', 30)
register_command_handler(handler_set_subject, 'subject', 16)
register_command_handler(handler_akick, 'akick', 20)
register_command_handler(handler_amoderator, 'amoderator', 20)
register_command_handler(handler_avisitor, 'avisitor', 20)
register_command_handler(handler_aban, 'aban', 20)
register_command_handler(handler_avoice_control, 'avoice', 20)
register_command_handler(handler_avoice_avtime, 'avtime', 20)
register_command_handler(handler_regvoice_control, 'regvoice', 20)
register_command_handler(handler_regvoice_rvquest, 'rvquest', 20)
register_command_handler(handler_regvoice_rvansw, 'rvansw', 20)
register_command_handler(handler_regvoice_rvmess, 'rvmess', 20)
register_command_handler(handler_regvoice_rvtries, 'rvtries', 20)

register_stage1_init(get_muc_state)
register_join_handler(handler_muc_join)
register_leave_handler(handler_muc_leave)
register_presence_handler(handler_muc_presence)
register_message_handler(handler_regvoice_processansw)
