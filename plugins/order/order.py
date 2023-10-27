# -*- coding: utf-8 -*-

#  fatal plugin
#  order plugin

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  First Version and Idea © 2007 dimichxp <dimichxp@gmail.com>
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

from fatalapi import *

def order_check_obscene_words(body):
    order_obscene_words = ['бляд', ' блят', ' бля ', ' блять ', ' плять ', ' хуй', ' ибал', ' ебал', 'нахуй', ' хуй', ' хуи', 'хуител', ' хуя', 'хуя', ' хую', ' хуе', ' ахуе', ' охуе', 'хуев', ' хер ', ' хер', 'хер', ' пох ', ' нах ', 'писд', 'пизд', 'рizd', ' пздц ', ' еб', ' епана ', ' епать ', ' ипать ', ' выепать ', ' ибаш', ' уеб', 'проеб', 'праеб', 'приеб', 'съеб', 'сьеб', 'взъеб', 'взьеб', 'въеб', 'вьеб', 'выебан', 'перееб', 'недоеб', 'долбоеб', 'долбаеб', ' ниибац', ' неебац', ' неебат', ' ниибат', ' пидар', ' рidаr', ' пидар', ' пидор', 'педор', 'пидор', 'пидарас', 'пидараз', ' педар', 'педри', 'пидри', ' заеп', ' заип', ' заеб', 'ебучий', 'ебучка ', 'епучий', 'епучка ', ' заиба', 'заебан', 'заебис', ' выеб', 'выебан', ' поеб', ' наеб', ' наеб', 'сьеб', 'взьеб', 'вьеб', ' гандон', ' гондон', 'пахуи', 'похуис', ' манда ', 'мандав', ' залупа', ' залупог']

    body = body.lower()
    body = ' ' + body + ' '
    
    for x in order_obscene_words:
        if body.count(x):
            return True
    return False

def order_check_space(mode, gch, jid, nick):
    if has_edge_space(nick):
        reason = l('Nicks with spaces by edges are not allowed!')
        
        if mode == 'kick':
            order_kick(gch, nick, reason)
        elif mode == 'ban':
            order_ban(gch, nick, reason)
        return True
    return False

def order_check_nick_len(nlen, mode, gch, jid, nick):
    if len(nick) > nlen:
        reason = l('Too long nick! Nicks longer than %s characters are not allowed!') % (nlen)
        
        if mode == 'kick':
            order_kick(gch, nick, reason)
        elif mode == 'ban':
            order_ban(gch, nick, reason)
        else:
            order_visitor(gch, nick, l('Too long nick!'))
            msg(gch + '/' + nick, l('Please change your nick, it must be no longer than %s characters!') % (nlen))
        return True
    return False

def order_check_prs_caps(prs, mode, gch, jid, nick):
    if isinstance(prs, xmpp.Presence):
        reason = l('Client has empty presence caps! Empty presence caps are not allowed!')
        
        if not prs.getTags('c', namespace=xmpp.NS_CAPS):
            if mode == 'kick':
                order_kick(gch, nick, reason)
            elif mode == 'ban':
                order_ban(gch, nick, reason)
            return True
    return False


def order_check_time_flood(gch, jid, nick):
    cid = get_client_id()
    
    lastmsg = get_int_fatal_var(cid, 'order_stats', gch, jid, 'msgtime')
    if lastmsg and time.time() - lastmsg <= 2.2:
        if inc_fatal_var(cid, 'order_stats', gch, jid, 'msg') > 3:
            set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'time', time.time())
            set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'cnd', 1)
            set_fatal_var(cid, 'order_stats', gch, jid, 'msg', 0)
            order_kick(gch, nick, l('You are sending messages too fast!'))
            return True
        return False

def order_check_len_flood(mlen, body, gch, jid, nick):
    cid = get_client_id()
    
    if len(body) > mlen:
        set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'time', time.time())
        set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'cnd', 1)
        order_kick(gch, nick, l('Flood!'))
        return True
    return False
                
def order_check_obscene(body, gch, jid, nick):
    cid = get_client_id()
    
    if order_check_obscene_words(body):
        set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'time', time.time())
        set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'cnd', 1)
        order_kick(gch, nick, l('Your message contains obscene words!'))
        return True
    return False
            
def order_check_caps(body, gch, jid, nick):
    cid = get_client_id()
    
    ccnt = 0
    nicks = list(get_dict_fatal_var(cid, 'gchrosters', gch))
    
    for x in nicks:
        if body.count(x):
            body = body.replace(x, '')
            
    for x in [x for x in body.replace(' ', '')]:
        if x.isupper():
            ccnt += 1
            
    if ccnt >= len(body) / 2 and ccnt > 9:
        set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'time', time.time())
        set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'cnd', 1)
        order_kick(gch, nick, l('Too much upper-case words!'))
        return True
    return False
        
def order_check_like(body, gch, jid, nick):
    cid = get_client_id()
    
    lcnt = 0
    lastmsg = get_int_fatal_var(cid, 'order_stats', gch, jid, 'msgtime')
    msgbody = get_list_fatal_var(cid, 'order_stats', gch, jid, 'msgbody')
    
    if lastmsg and msgbody:
        if time.time() - lastmsg > 60:
            set_fatal_var(cid, 'order_stats', gch, jid, 'msgbody', body.split())
        else:
            splb = body.split()
        
            for x in msgbody:
                for y in splb:
                    if x == y:
                        lcnt += 1
            
            if lcnt:
                lensrcmsgbody = len(splb)
                lenoldmsgbody = len(msgbody)
                avg = (lensrcmsgbody + lenoldmsgbody / 2) / 2
                
                if lcnt > avg:
                    if inc_fatal_var(cid, 'order_stats', gch, jid, 'msg') >= 2:
                        set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'time', time.time())
                        set_fatal_var(cid, 'order_stats', gch, jid, 'devoice', 'cnd', 1)
                        set_fatal_var(cid, 'order_stats', gch, jid, 'msg', 0)
                        order_kick(gch, nick, l('Too similar messages!'))
                        return True
            
            set_fatal_var(cid, 'order_stats', gch, jid, 'msgbody', body.split())
    else:
        set_fatal_var(cid, 'order_stats', gch, jid, 'msgbody', body.split())
    return False

#------------------------------------------------------------------------------

def order_kick(groupchat, nick, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    iq.setID('kick%s' % (time.time()))
    query = xmpp.Node('query')
    query.setNamespace('http://jabber.org/protocol/muc#admin')
    kick = query.addChild('item', {'nick': nick, 'role': 'none'})
    kick.setTagData('reason', get_bot_nick(groupchat) + ': ' + reason)
    iq.addChild(node=query)
    jconn = get_client_conn()
    jconn.send(iq)
    
def order_visitor(groupchat, nick, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    iq.setID('visitor%s' % (time.time()))
    query = xmpp.Node('query')
    query.setNamespace('http://jabber.org/protocol/muc#admin')
    visitor = query.addChild('item', {'nick': nick, 'role': 'visitor'})
    visitor.setTagData('reason', get_bot_nick(groupchat) + ': ' + reason)
    iq.addChild(node=query)
    jconn = get_client_conn()
    jconn.send(iq)
    
def order_ban(groupchat, nick, reason):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    iq.setID('ban%s' % (time.time()))
    query = xmpp.Node('query')
    query.setNamespace('http://jabber.org/protocol/muc#admin')
    ban = query.addChild('item', {'nick': nick, 'affiliation': 'outcast'})
    ban.setTagData('reason', get_bot_nick(groupchat) + ': ' + reason)
    iq.addChild(node=query)
    jconn = get_client_conn()
    jconn.send(iq)
    
def order_unban(groupchat, jid):
    iq = xmpp.Iq('set')
    iq.setTo(groupchat)
    iq.setID('uban%s' % (time.time()))
    query = xmpp.Node('query')
    query.setNamespace('http://jabber.org/protocol/muc#admin')
    query.addChild('item', {'jid': jid, 'affiliation': 'none'})
    iq.addChild(node=query)
    jconn = get_client_conn()
    jconn.send(iq)

def start_check_idle():
    gchs = []
    
    if is_cvar_set('gchrosters'):
        gchs = tuple(get_client_var('gchrosters'))
    
    idle_cond = False
    
    for gch in gchs:
        flidco = int(get_gch_param(gch, 'filt_idle_cond', '0'))
        
        if flidco:
            idle_cond = True
            break
    
    if idle_cond:
        add_fatal_task('order_check_idle', func=order_check_idle, ival=120, inthr=False)

def order_check_idle():
    cid = get_client_id()
    
    gchs = list(get_fatal_var(cid, 'gchrosters'))
    
    for gch in gchs:
        nicks = list(get_dict_fatal_var(cid, 'gchrosters', gch))
        
        flidco = int(get_gch_param(gch, 'filt_idle_cond', '0'))
        if flidco:
            timee = int(get_gch_param(gch, 'filt_idle_time', '3500'))
            now = time.time()
            
            for nick in nicks:
                if user_level(gch + '/' + nick, gch) < 11:
                    tidl = get_int_fatal_var(cid, 'gchrosters', gch, nick, 'idle')
                    idle = now - tidl
                    
                    if idle > timee:
                        order_kick(gch, nick, l('Silence more than %s!') % (timeElapsed(idle)))
        else:
            rmv_fatal_task('order_check_idle')

#------------------------------------------------------------------------------

def handler_order_message(type, source, body):
    cid = get_client_id()
    
    nick = source[2]
    groupchat = source[1]
    
    strict = int(get_gch_param(groupchat, 'filt_strict_cond', '0'))
    strlev = 10
    
    if strict:
        strlev = 11

    if is_groupchat(groupchat) and user_level(source, groupchat) <= strlev:
        if get_bot_nick(groupchat) != nick:
            jid = get_true_jid(source)
            
            if is_var_set('order_stats', groupchat, jid):
                fltm = int(get_gch_param(groupchat, 'filt_time', '1'))
                flln = int(get_gch_param(groupchat, 'filt_len', '1'))
                mlen = int(get_gch_param(groupchat, 'filt_msg_len', '900'))
                flob = int(get_gch_param(groupchat, 'filt_obscene', '1'))
                flca = int(get_gch_param(groupchat, 'filt_caps', '1'))
                flli = int(get_gch_param(groupchat, 'filt_like', '1'))
                
                if fltm:
                    if order_check_time_flood(groupchat, jid, nick):
                        return
                        
                if flln:
                    if order_check_len_flood(mlen, body, groupchat, jid, nick):
                        return
                        
                if flob:
                    if order_check_obscene(body, groupchat, jid, nick):
                        return
                        
                if flca:
                    if order_check_caps(body, groupchat, jid, nick):
                        return
                        
                if flli:
                    if order_check_like(body, groupchat, jid, nick):
                        return
                
                set_fatal_var(cid, 'order_stats', groupchat, jid, 'msgtime', time.time())

def handler_order_join(groupchat, nick, aff, role):
    cid = get_client_id()
    
    jid = get_true_jid(groupchat + '/' + nick)

    time.sleep(1)

    strict = int(get_gch_param(groupchat, 'filt_strict_cond', '0'))
    strlev = 10
    
    if strict:
        strlev = 11

    if is_gch_user(groupchat, nick) and user_level(groupchat + '/' + nick, groupchat) <= strlev:
        fnickl = int(get_gch_param(groupchat, 'filt_nickl_cond', '1'))
        
        if fnickl:
            mode = get_gch_param(groupchat, 'filt_nickl_mode', 'kick')
            nlen = int(get_gch_param(groupchat, 'filt_nickl_len', '30'))
            
            if order_check_nick_len(nlen, mode, groupchat, jid, nick):	
                return
        
        now = time.time()
            
        if is_var_set(cid, 'order_stats', groupchat, jid):
            if is_var_set(cid, 'order_stats', groupchat, jid, 'devoice', 'cnd'):
                if now - get_int_fatal_var(cid, 'order_stats', groupchat, jid, 'devoice', 'time') > 300:
                    set_fatal_var(cid, 'order_stats', groupchat, jid, 'devoice', 'cnd', 0)
                else:
                    order_visitor(groupchat, nick, l('You have been devoiced due to previous violations!'))
            
            flkico = int(get_gch_param(groupchat, 'filt_kicks_cond', '1'))
            
            if flkico:
                kcnt = int(get_gch_param(groupchat, 'filt_kicks_cnt', '2'))
                
                if get_int_fatal_var(cid, 'order_stats', groupchat, jid, 'kicks') > kcnt:
                    order_ban(groupchat, nick, l('Too much kicks!'))
                    return
            
            flflco = int(get_gch_param(groupchat, 'filt_fly_cond', '1'))
            
            if flflco and is_var_set(cid, 'order_stats', groupchat, jid):
                lastprs = get_int_fatal_var(cid, 'order_stats', groupchat, jid, 'prstime', 'fly')
                set_fatal_var(cid, 'order_stats', groupchat, jid, 'prstime', 'fly', time.time())
                
                if now - lastprs <= 70:
                    if inc_fatal_var(cid, 'order_stats', groupchat, jid, 'prs', 'fly') > 4:
                        set_fatal_var(cid, 'order_stats', groupchat, jid, 'prs', 'fly', 0)
                        fmode = get_gch_param(groupchat, 'filt_fly_mode', 'ban')
                        ftime = int(get_gch_param(groupchat, 'filt_fly_time', '60'))
                        
                        if fmode == 'ban':
                            order_ban(groupchat, nick, l('Too much rejoins!'))
                            time.sleep(ftime)
                            order_unban(groupchat, jid)
                        else:
                            order_kick(groupchat, nick, l('Too much rejoins!'))
                            return
                else:
                    set_fatal_var(cid, 'order_stats', groupchat, jid, 'prs', 'fly', 0)
            
            flob = int(get_gch_param(groupchat, 'filt_obscene', '1'))
            
            if flob:
                if order_check_obscene(nick, groupchat, jid, nick):
                    return
        elif is_gch_user(groupchat, nick):
            set_fatal_var(cid, 'order_stats', groupchat, jid, {'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0})
    elif is_var_set(cid, 'order_stats', groupchat, jid):
        rmv_fatal_var(cid, 'order_stats', groupchat, jid)

def handler_order_presence(prs):
    cid = get_client_id()
    
    ptype = prs.getType()

    if ptype == 'unavailable' or ptype == 'error':
        return

    groupchat = get_stripped(prs.getFrom())
    nick = get_resource(prs.getFrom())
    stmsg = prs.getStatus()
    jid = get_true_jid(groupchat + '/' + nick)
    
    fprsc = int(get_gch_param(groupchat, 'filt_prscaps_cond', '0'))
            
    if fprsc:
        mode = get_gch_param(groupchat, 'filt_prscaps_mode', 'kick')
        
        if order_check_prs_caps(prs, mode, groupchat, jid, nick):
            return
    
    fnickl = int(get_gch_param(groupchat, 'filt_nickl_cond', '1'))
            
    if fnickl:
        mode = get_gch_param(groupchat, 'filt_nickl_mode', 'kick')
        nlen = int(get_gch_param(groupchat, 'filt_nickl_len', '30'))
        
        if order_check_nick_len(nlen, mode, groupchat, jid, nick):
            return
    
    fspace = int(get_gch_param(groupchat, 'filt_space_cond', '1'))
            
    if fspace:
        mode = get_gch_param(groupchat, 'filt_space_mode', 'kick')
        
        if order_check_space(mode, groupchat, jid, nick):
            return

    if is_var_set(cid, 'order_stats', groupchat, jid):
        if get_gch_aff(groupchat, nick) in ['admin', 'owner']:
            rmv_fatal_var(cid, 'order_stats', groupchat, jid)
            return
    else:
        if get_gch_aff(groupchat, nick) in ['none', 'member']:
            set_fatal_var(cid, 'order_stats', groupchat, jid, {'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0})
    
    strict = int(get_gch_param(groupchat, 'filt_strict_cond', '0'))
    strlev = 10
    
    if strict:
        strlev = 11

    if is_gch_user(groupchat, nick) and user_level(groupchat + '/' + nick, groupchat) <= strlev:
        if is_var_set(cid, 'order_stats', groupchat, jid):
            now = time.time()
            
            if now - get_int_fatal_var(cid, 'gchrosters', groupchat, nick, 'joined') > 1:
                if get_gch_role(groupchat, nick) == 'participant':
                    set_fatal_var(cid, 'order_stats', groupchat, jid, 'devoice', 'cnd', 0)
                    
                lastprs = get_int_fatal_var(cid, 'order_stats', groupchat, jid, 'prstime', 'status')
                set_fatal_var(cid, 'order_stats', groupchat, jid, 'prstime', 'status', now)
                
                flpr = int(get_gch_param(groupchat, 'filt_presence', '1'))
                
                if flpr:
                    if now - lastprs > 300:
                        set_fatal_var(cid, 'order_stats', groupchat, jid, 'prs', 'status', 0)
                    else:
                        if inc_fatal_var(cid, 'order_stats', groupchat, jid, 'prs', 'status') > 5:
                            set_fatal_var(cid, 'order_stats', groupchat, jid, 'prs', 'status', 0)
                            order_kick(groupchat, nick, l('Presence-flood!'))
                            return
                
                flob = int(get_gch_param(groupchat, 'filt_obscene', '1'))
                
                if flob:
                    if order_check_obscene(nick, groupchat, jid, nick):
                        return
                
                flpl = int(get_gch_param(groupchat, 'filt_prsstlen', '1'))
                plen = int(get_gch_param(groupchat, 'filt_prsstlen_len', '200'))
                
                if flpl and stmsg:
                    if order_check_len_flood(plen, stmsg, groupchat, jid, nick):
                        return

def handler_order_leave(groupchat, nick, reason, code):
    cid = get_client_id()
    
    jid = get_true_jid(groupchat + '/' + nick)
    
    strict = int(get_gch_param(groupchat, 'filt_strict_cond', '0'))
    strlev = 10
    
    if strict:
        strlev = 11
    
    if is_gch_user(groupchat, nick) and user_level(groupchat + '/' + nick, groupchat) <= strlev:
        if is_var_set(cid, 'order_stats', groupchat, jid):
            flpr = int(get_gch_param(groupchat, 'filt_presence', '1'))
            
            if flpr:
                if reason == 'Replaced by new connection':
                    return
                    
                if code:
                    if code == '307':  # kick
                        inc_fatal_var(cid, 'order_stats', groupchat, jid, 'kicks')
                        return
                    elif code == '301':  # ban
                        rmv_fatal_var(cid, 'order_stats', groupchat, jid)
                        return
                    elif code == '407':  # members-only
                        return
            
            flflco = int(get_gch_param(groupchat, 'filt_fly_cond', '1'))
            
            if flflco:
                now = time.time()
                lastprs = get_int_fatal_var(cid, 'order_stats', groupchat, jid, 'prstime', 'fly')
                set_fatal_var(cid, 'order_stats', groupchat, jid, 'prstime', 'fly', now)
                
                if now - lastprs <= 70:
                    inc_fatal_var(cid, 'order_stats', groupchat, jid, 'prs', 'fly')
                else:
                    set_fatal_var(cid, 'order_stats', groupchat, jid, 'prs', 'fly', 0)

#------------------------------------------------------------------------------

def handler_order_filt(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        parameters = parameters.split()
        
        if parameters[0] == 'time':
            if len(parameters) == 1:
                time = int(get_gch_param(groupchat, 'filt_time', '1'))
                
                if time:
                    return reply(type, source, l('Message time filter is turned on!'))
                else:
                    return reply(type, source, l('Message time filter is turned off!'))
            
            if parameters[1] == '0':
                set_gch_param(groupchat, 'filt_time', '0')
                return reply(type, source, l('Message time filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_time', '1')
                return reply(type, source, l('Message time filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'presence':
            if len(parameters) == 1:
                prs = int(get_gch_param(groupchat, 'filt_presence', '1'))
                
                if prs:
                    return reply(type, source, l('Presence time filter is turned on!'))
                else:
                    return reply(type, source, l('Presence time filter is turned off!'))
            
            if parameters[1] == '0':
                set_gch_param(groupchat, 'filt_presence', '0')
                return reply(type, source, l('Presence time filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_presence', '1')
                return reply(type, source, l('Presence time filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'len':
            if len(parameters) == 1:
                flen = int(get_gch_param(groupchat, 'filt_len', '1'))
                
                if flen:
                    return reply(type, source, l('Message length filter is turned on!'))
                else:
                    return reply(type, source, l('Message length filter is turned off!'))
            
            if parameters[1] == 'len':
                if len(parameters) == 2:
                    mlen = get_gch_param(groupchat, 'filt_msg_len', '900')
                    
                    return reply(type, source, l('Max message length is set to %s!') % (mlen))
                
                if not parameters[2].isdigit():
                    return reply(type, source, l('Invalid syntax!'))
                
                if int(parameters[2]) >= 80:
                    set_gch_param(groupchat, 'filt_msg_len', parameters[2])
                    return reply(type, source, l('Max message length has been set to %s!') % (parameters[2]))
                else:
                    return reply(type, source, l('Value must not be less than 80 characters!'))
            elif parameters[1] == '0':
                set_gch_param(groupchat, 'filt_len', '0')
                return reply(type, source, l('Message length filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_len', '1')
                return reply(type, source, l('Message length filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'like':
            if len(parameters) == 1:
                like = int(get_gch_param(groupchat, 'filt_like', '1'))
                
                if like:
                    return reply(type, source, l('Similar messages filter is turned on!'))
                else:
                    return reply(type, source, l('Similar messages filter is turned off!'))
            
            if parameters[1] == '0':
                set_gch_param(groupchat, 'filt_like', '0')
                return reply(type, source, l('Similar messages filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_like', '1')
                return reply(type, source, l('Similar messages filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'caps':
            if len(parameters) == 1:
                caps = int(get_gch_param(groupchat, 'filt_caps', '1'))
                
                if caps:
                    return reply(type, source, l('Caps filter is turned on!'))
                else:
                    return reply(type, source, l('Caps filter is turned off!'))

            if parameters[1] == '0':
                set_gch_param(groupchat, 'filt_caps', '0')
                return reply(type, source, l('Caps filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_caps', '1')
                return reply(type, source, l('Caps filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'prsstlen':
            if len(parameters) == 1:
                prsstlen = int(get_gch_param(groupchat, 'filt_prsstlen', '1'))
                
                if prsstlen:
                    return reply(type, source, l('Status message length filter is turned on!'))
                else:
                    return reply(type, source, l('Status message length filter is turned off!'))
            
            if parameters[1] == 'len':
                if len(parameters) == 2:
                    plen = get_gch_param(groupchat, 'filt_prsstlen_len', '200')
                    
                    return reply(type, source, l('Max status message length is set to %s!') % (plen))

                if not parameters[2].isdigit():
                    return reply(type, source, l('Invalid syntax!'))

                if int(parameters[2]) >= 40:
                    set_gch_param(groupchat, 'filt_prsstlen_len', parameters[2])
                    return reply(type, source, l('Max status message length has been set to %s!') % (parameters[2]))
                else:
                    return reply(type, source, l('Value must not be less than 40 characters!'))
            elif parameters[1] == '0':
                set_gch_param(groupchat, 'filt_prsstlen', '0')
                return reply(type, source, l('Status message length filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_prsstlen', '1')
                return reply(type, source, l('Status message length filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'prscaps':
            if len(parameters) == 1:
                prsc = int(get_gch_param(groupchat, 'filt_prscaps_cond', '1'))
                
                if prsc:
                    return reply(type, source, l('Presence caps filter is turned on!'))
                else:
                    return reply(type, source, l('Presence caps filter is turned off!'))
            
            if parameters[1] == 'mode':
                if len(parameters) == 2:
                    pcmode = get_gch_param(groupchat, 'filt_prscaps_mode', 'kick')
                    return reply(type, source, l('Reaction on empty presence caps is set to %s!') % (pcmode))
                
                if parameters[2] in ['kick', 'ban']:
                    set_gch_param(groupchat, 'filt_prscaps_mode', parameters[2])
                    return reply(type, source, l('Reaction on empty presence caps has been set to %s!') % (parameters[2]))
                else:
                    return reply(type, source, l('Invalid syntax!'))
            elif parameters[1] == '0':
                set_gch_param(groupchat, 'filt_prscaps_cond', '0')
                return reply(type, source, l('Presence caps filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_prscaps_cond', '1')
                return reply(type, source, l('Presence caps filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'obscene':
            if len(parameters) == 1:
                obscene = int(get_gch_param(groupchat, 'filt_obscene', '1'))
                
                if obscene:
                    return reply(type, source, l('Obscene words filter is turned on!'))
                else:
                    return reply(type, source, l('Obscene words filter is turned on!'))
            
            if parameters[1] == '0':
                set_gch_param(groupchat, 'filt_obscene', '0')
                return reply(type, source, l('Obscene words filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_obscene', '1')
                return reply(type, source, l('Obscene words filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'fly':
            if len(parameters) == 1:
                fly = int(get_gch_param(groupchat, 'filt_fly_cond', '1'))
                
                if fly:
                    return reply(type, source, l('Fly (rejoins) filter is turned on!'))
                else:
                    return reply(type, source, l('Fly (rejoins) filter is turned off!'))
            
            if parameters[1] == 'cnt':
                if len(parameters) == 2:
                    flytime = get_gch_param(groupchat, 'filt_fly_time', '60')
                    
                    return reply(type, source, l('Auto-voice timeout is set to %s seconds!') % (flytime))
                
                if not parameters[2].isdigit():
                    return reply(type, source, l('Invalid syntax!'))
                
                if int(parameters[2]) in range(0, 121):
                    set_gch_param(groupchat, 'filt_fly_time', parameters[2])
                    return reply(type, source, l('Auto-voice timeout has been set to %s seconds!') % (parameters[2]))
                else:
                    return reply(type, source, l('No more than two minutes (120 seconds)!'))
            elif parameters[1] == 'mode':
                if len(parameters) == 2:
                    flymode = get_gch_param(groupchat, 'filt_fly_mode', 'ban')
                        
                    return reply(type, source, l('Reaction on flies (rejoins) is set to %s!') % (flymode))
                
                if parameters[2] in ['kick', 'ban']:
                    set_gch_param(groupchat, 'filt_fly_mode', parameters[2])
                    return reply(type, source, l('Reaction on flies (rejoins) has been set to %s!') % (parameters[2]))
                else:
                    return reply(type, source, l('Invalid syntax!'))
            elif parameters[1] == '0':
                set_gch_param(groupchat, 'filt_fly_cond', '0')
                return reply(type, source, l('Fly (rejoins) filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_fly_cond', '1')
                return reply(type, source, l('Fly (rejoins) filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'kicks':
            if len(parameters) == 1:
                kicks = int(get_gch_param(groupchat, 'filt_kicks_cond', '1'))
                
                if kicks:
                    return reply(type, source, l('Auto-ban after multiple kicks filter is turned on!'))
                else:
                    return reply(type, source, l('Auto-ban after multiple kicks filter is turned off!'))
            
            if parameters[1] == 'cnt':
                if len(parameters) == 2:
                    kickscnt = get_gch_param(groupchat, 'filt_kicks_cnt', '2')
                        
                    return reply(type, source, l('Auto-ban is set after %s kicks!') % (kickscnt))
                
                if not parameters[2].isdigit():
                    return reply(type, source, l('Invalid syntax!'))
                
                if int(parameters[2]) in range(3, 10):
                    set_gch_param(groupchat, 'filt_kicks_cnt', parameters[2])
                    return reply(type, source, l('Auto-ban has been set after %s kicks!') % (parameters[2]))
                else:
                    return reply(type, source, l('Value must be from 3 to 10 kicks!'))
            elif parameters[1] == '0':
                set_gch_param(groupchat, 'filt_kicks_cond', '0')
                return reply(type, source, l('Auto-ban after multiple kicks filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_kicks_cond', '1')
                return reply(type, source, l('Auto-ban after multiple kicks filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'idle':
            if len(parameters) == 1:
                idle = int(get_gch_param(groupchat, 'filt_idle_cond', '1'))
                
                if idle:
                    return reply(type, source, l('Kick for silence filter is turned on!'))
                else:
                    return reply(type, source, l('Kick for silence filter is turned off!'))
                
            if parameters[1] == 'time':
                if len(parameters) == 2:
                    idletime = int(get_gch_param(groupchat, 'filt_idle_time', '3500'))
                        
                    return reply(type, source, l('Kick for silence is set after %s seconds (%s)!') % (idletime, timeElapsed(idletime)))
                
                if not parameters[2].isdigit():
                    return reply(type, source, l('Invalid syntax!'))

                set_gch_param(groupchat, 'filt_idle_time', parameters[2])    
                    
                return reply(type, source, l('Kick for silence has been set after %s seconds (%s)!') % (parameters[2], timeElapsed(int(parameters[2]))))
            elif parameters[1] == '0':
                set_gch_param(groupchat, 'filt_idle_cond', '0')
                rmv_fatal_task('order_check_idle')
                return reply(type, source, l('Kick for silence filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_idle_cond', '1')
                add_fatal_task('order_check_idle', func=order_check_idle, ival=120, inthr=False)
                return reply(type, source, l('Kick for silence filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'nick':
            if len(parameters) == 1:
                nickl = int(get_gch_param(groupchat, 'filt_nickl_cond', '1'))
                
                if nickl:
                    return reply(type, source, l('Nick length filter is turned on!'))
                else:
                    return reply(type, source, l('Nick length filter is turned off!'))

            if parameters[1] == 'len':
                if len(parameters) == 2:
                    nickl_len = get_gch_param(groupchat, 'filt_nickl_len', '30')
                    
                    return reply(type, source, l('Max nick length is set to %s characters!') % (nickl_len))

                if not parameters[2].isdigit():
                    return reply(type, source, l('Invalid syntax!'))

                set_gch_param(groupchat, 'filt_nickl_len', parameters[2])
                
                return reply(type, source, l('Max nick length has been set to %s characters!') % (parameters[2]))
            elif parameters[1] == 'mode':
                if len(parameters) == 2:
                    nickl_mode = get_gch_param(groupchat, 'filt_nickl_mode', 'kick')
                    
                    return reply(type, source, l('Reaction on max nick length excess is set to %s!') % (nickl_mode))

                if parameters[2] in ['kick', 'ban', 'visitor']:
                    set_gch_param(groupchat, 'filt_nickl_mode', parameters[2])
                    return reply(type, source, l('Reaction on max nick length excess has been set to %s!') % (parameters[2]))
                else:
                    return reply(type, source, l('Invalid syntax!'))
            elif parameters[1] == '0':
                set_gch_param(groupchat, 'filt_nickl_cond', '0')
                return reply(type, source, l('Nick length filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_nickl_cond', '1')
                return reply(type, source, l('Nick length filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'space':
            if len(parameters) == 1:
                space = int(get_gch_param(groupchat, 'filt_space_cond', '1'))
                
                if space:
                    return reply(type, source, l('Nick edge spaces filter is turned on!'))
                else:
                    return reply(type, source, l('Nick edge spaces filter is turned off!'))

            if parameters[1] == 'mode':
                if len(parameters) == 2:
                    spacemode = get_gch_param(groupchat, 'filt_space_mode', 'kick')
                    
                    return reply(type, source, l('Reaction on nicks with spaces by edges is set to %s!') % (spacemode))

                if parameters[2] in ['kick', 'ban']:
                    set_gch_param(groupchat, 'filt_space_mode', parameters[2])
                    return reply(type, source, l('Reaction on nicks with spaces by edges has been set to %s!') % (parameters[2]))
                else:
                    return reply(type, source, l('Invalid syntax!'))
            elif parameters[1] == '0':
                set_gch_param(groupchat, 'filt_space_cond', '0')
                return reply(type, source, l('Nick edge spaces filter has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_space_cond', '1')
                return reply(type, source, l('Nick edge spaces filter has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        elif parameters[0] == 'strict':
            if len(parameters) == 1:
                strict = int(get_gch_param(groupchat, 'filt_strict_cond', '1'))
                
                if strict:
                    return reply(type, source, l('Strict filtration mode is turned on!'))
                else:
                    return reply(type, source, l('Strict filtration mode is turned off!'))
            
            if parameters[1] == '0':
                set_gch_param(groupchat, 'filt_strict_cond', '0')
                return reply(type, source, l('Strict filtration mode has been turned off!'))
            elif parameters[1] == '1':
                set_gch_param(groupchat, 'filt_strict_cond', '1')
                return reply(type, source, l('Strict filtration mode has been turned on!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
        else:
            return reply(type, source, l('Invalid syntax!'))
    else:
        flts = []
        fin = 1
        rep, foff, fon = '', [], []
        time = int(get_gch_param(groupchat, 'filt_time', '1'))
        prs = int(get_gch_param(groupchat, 'filt_presence', '1'))
        flen = int(get_gch_param(groupchat, 'filt_len', '1'))
        fmln = int(get_gch_param(groupchat, 'filt_msg_len', '900'))
        like = int(get_gch_param(groupchat, 'filt_like', '1'))
        caps = int(get_gch_param(groupchat, 'filt_caps', '1'))
        prsstlen = int(get_gch_param(groupchat, 'filt_prsstlen', '1'))
        fprsl = int(get_gch_param(groupchat, 'filt_prsstlen_len', '200'))
        obscene = int(get_gch_param(groupchat, 'filt_obscene', '1'))
        prsc = int(get_gch_param(groupchat, 'filt_prscaps_cond', '0'))
        pcmode = get_gch_param(groupchat, 'filt_prscaps_mode', 'kick')
        fly = int(get_gch_param(groupchat, 'filt_fly_cond', '1'))
        flytime = get_gch_param(groupchat, 'filt_fly_time', '60')
        flymode = get_gch_param(groupchat, 'filt_fly_mode', 'ban')
        kicks = int(get_gch_param(groupchat, 'filt_kicks_cond', '1'))
        kickscnt = get_gch_param(groupchat, 'filt_kicks_cnt', '2')
        idle = int(get_gch_param(groupchat, 'filt_idle_cond', '1'))
        idletime = int(get_gch_param(groupchat, 'filt_idle_time', '3500'))
        nickl = int(get_gch_param(groupchat, 'filt_nickl_cond', '1'))
        nickl_len = int(get_gch_param(groupchat, 'filt_nickl_len', '30'))
        nickl_mode = get_gch_param(groupchat, 'filt_nickl_mode', 'kick')
        space = int(get_gch_param(groupchat, 'filt_space_cond', '1'))
        spacemode = get_gch_param(groupchat, 'filt_space_mode', 'kick')
        strict = int(get_gch_param(groupchat, 'filt_strict_cond', '0'))
        
        if time:
            flts.append('+' + l('%s) Name: time. Description: Message time filter.') % (fin))
        else:
            flts.append('-' + l('%s) Name: time. Description: Message time filter.') % (fin))
        
        fin += 1
        
        if prs:
            flts.append('+' + l('%s) Name: presence. Description: Presence time filter.') % (fin))
        else:
            flts.append('-' + l('%s) Name: presence. Description: Presence time filter.') % (fin))
            
        fin += 1
            
        if flen:
            flts.append(l('+%s) Name: len. Description: Message length filter. Max length: %s.') % (fin, fmln))
        else:
            flts.append(l('-%s) Name: len. Description: Message length filter.') % (fin))
            
        fin += 1
            
        if like:
            flts.append('+' + l('%s) Name: like. Description: Similar messages filter.') % (fin))
        else:
            flts.append('-' + l('%s) Name: like. Description: Similar messages filter.') % (fin))
            
        fin += 1
            
        if caps:
            flts.append('+' + l('%s) Name: caps. Description: Caps filter.') % (fin))
        else:
            flts.append('-' + l('%s) Name: caps. Description: Caps filter.') % (fin))
            
        fin += 1
            
        if prsstlen:
            flts.append(l('+%s) Name: prsstlen. Description: Status message length filter. Max length: %s.') % (fin, fprsl))
        else:
            flts.append(l('-%s) Name: prsstlen. Description: Status message length filter.') % (fin))

        fin += 1
            
        if prsc:
            flts.append(l('+%s) Name: prscaps. Description: Presence caps filter (reaction: %s).') % (fin, pcmode))
        else:
            flts.append(l('-%s) Name: prscaps. Description: Presence caps filter.') % (fin))

        fin += 1
            
        if obscene:
            flts.append('+' + l('%s) Name: obscene. Description: Obscene words filter.') % (fin))
        else:
            flts.append('-' + l('%s) Name: obscene. Description: Obscene words filter.') % (fin))
            
        fin += 1
            
        if fly:
            flts.append(l('+%s) Name: fly. Description: Fly (rejoins) filter (reaction: %s; time: %s seconds).') % (fin, flymode, flytime))
        else:
            flts.append(l('-%s) Name: fly. Description: Fly (rejoins) filter.') % (fin))
            
        fin += 1
            
        if kicks:
            flts.append(l('+%s) Name: kicks. Description: Auto-ban after %s kicks filter.') % (fin, kickscnt))
        else:
            flts.append(l('-%s) Name: kicks. Description: Auto-ban after multiple kicks filter.') % (fin))
            
        fin += 1
            
        if idle:
            flts.append(l('+%s) Name: idle. Description: Kick for silence filter after %s (%s).') % (fin, idletime, timeElapsed(idletime)))
        else:
            flts.append(l('-%s) Name: idle. Description: Kick for silence filter.') % (fin))
            
        fin += 1
            
        if nickl:
            flts.append(l('+%s) Name: nick. Description: Nick length filter. Max length: %s characters. Reaction: %s.') % (fin, nickl_len, nickl_mode))
        else:
            flts.append(l('-%s) Name: nick. Description: Nick length filter.') % (fin))
        
        fin += 1
        
        if space:
            flts.append(l('+%s) Name: space. Description: Nick edge spaces filter. Reaction: %s.') % (fin, spacemode))
        else:
            flts.append(l('-%s) Name: space. Description: Nick edge spaces filter.') % (fin))
        
        fin += 1
        
        if strict:
            flts.append('+' + l('%s) Name: strict. Description: Strict filtration mode: apply filters also for members.') % (fin))
        else:
            flts.append('-' + l('%s) Name: strict. Description: Strict filtration mode: apply filters also for members.') % (fin))
        
        if flts:
            rep = l('Filters (total: %s; on: (+); off: (-)):\n\n%s') % (len(flts), '\n'.join(flts))
        else:
            rep = l('There are no available filters!')
            
        return reply(type, source, rep.strip())

def get_order_cfg(gch):
    if not param_exists(gch, 'filt_like'):
        set_gch_param(gch, 'filt_like', '1')
    if not param_exists(gch, 'filt_presence'):
        set_gch_param(gch, 'filt_presence', '1')
    if not param_exists(gch, 'filt_len'):
        set_gch_param(gch, 'filt_len', '1')
    if not param_exists(gch, 'filt_msg_len'):
        set_gch_param(gch, 'filt_msg_len', '900')
    if not param_exists(gch, 'filt_caps'):
        set_gch_param(gch, 'filt_caps', '1')
    if not param_exists(gch, 'filt_obscene'):
        set_gch_param(gch, 'filt_obscene', '1')
    if not param_exists(gch, 'filt_time'):
        set_gch_param(gch, 'filt_time', '1')
    if not param_exists(gch, 'filt_prsstlen'):
        set_gch_param(gch, 'filt_prsstlen', '1')
    if not param_exists(gch, 'filt_prsstlen_len'):
        set_gch_param(gch, 'filt_prsstlen_len', '200')

    if not param_exists(gch, 'filt_fly_cond'):
        set_gch_param(gch, 'filt_fly_cond', '1')
    if not param_exists(gch, 'filt_fly_mode'):
        set_gch_param(gch, 'filt_fly_mode', 'ban')
    if not param_exists(gch, 'filt_fly_time'):
        set_gch_param(gch, 'filt_fly_time', '60')
        
    if not param_exists(gch, 'filt_idle_cond'):
        set_gch_param(gch, 'filt_idle_cond', '0')
    if not param_exists(gch, 'filt_idle_time'):
        set_gch_param(gch, 'filt_idle_time', '3500')
        
    if not param_exists(gch, 'filt_kicks_cond'):
        set_gch_param(gch, 'filt_kicks_cond', '1')
    if not param_exists(gch, 'filt_kicks_cnt'):
        set_gch_param(gch, 'filt_kicks_cnt', '2')
            
    if not param_exists(gch, 'filt_nickl_cond'):
        set_gch_param(gch, 'filt_nickl_cond', '1')
    if not param_exists(gch, 'filt_nickl_len'):
        set_gch_param(gch, 'filt_nickl_len', '30')
    if not param_exists(gch, 'filt_nickl_mode'):
        set_gch_param(gch, 'filt_nickl_mode', 'kick')

    if not param_exists(gch, 'filt_prscaps_cond'):
        set_gch_param(gch, 'filt_prscaps_cond', '0')
    if not param_exists(gch, 'filt_prscaps_mode'):
        set_gch_param(gch, 'filt_prscaps_mode', 'kick')

    if not param_exists(gch, 'filt_space_cond'):
        set_gch_param(gch, 'filt_space_cond', '1')
    if not param_exists(gch, 'filt_space_mode'):
        set_gch_param(gch, 'filt_space_mode', 'kick')
        
    if not param_exists(gch, 'filt_strict_cond'):
        set_gch_param(gch, 'filt_strict_cond', '0')

register_message_handler(handler_order_message)
register_join_handler(handler_order_join)
register_leave_handler(handler_order_leave)
register_presence_handler(handler_order_presence)

register_command_handler(handler_order_filt, 'filt', 20)

register_stage1_init(get_order_cfg)
register_stage2_init(start_check_idle)

