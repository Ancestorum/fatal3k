# -*- coding: utf-8 -*-

#  fatal plugin
#  xepfilter plugin

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

def get_mf_gch_nick(gch, jid):
    cid = get_client_id()
    
    nick = ''

    gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
    
    try:
        nickl = [li for li in gch_dic if jid == gch_dic[li]['rjid']]
    except Exception:
        try:
            time.sleep(3)
            gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
            nickl = [li for li in gch_dic if jid == gch_dic[li]['rjid']]
        except Exception:
            return nick

    if nickl:
        nick = nickl[-1]
    return nick

def get_mf_nick(mfnode):
    gch = get_mf_gch(mfnode)
    jid = '%s' % (get_mf_jid(mfnode))
    nick = get_mf_gch_nick(gch, jid)
    
    if nick:
        return nick
    return ''

def get_mf_gch_jid(mfnode):
    gch = get_mf_gch(mfnode)
    jid = '%s' % (get_mf_jid(mfnode))
    nick = get_mf_gch_nick(gch, jid)
    
    if nick:
        gch_jid = '%s/%s' % (gch, nick)
        return gch_jid
    return ''

def get_mf_target(mfnode):
    jid = get_mf_jid(mfnode)
    gch_jid = get_mf_gch_jid(mfnode)
    
    if gch_jid:
        return gch_jid
    return jid

def is_gch_target(mfnode):
    jid = get_mf_jid(mfnode)
    gch_jid = get_mf_gch_jid(mfnode)
    
    if gch_jid:
        return True
    return False

def check_mf_st_len(mfnode, stlen):
    stmsg = mfnode.getStatus()
    gch = get_mf_gch(mfnode)
    
    if stmsg:
        if len(stmsg) > stlen:
            if is_gch_target(mfnode):
                return l('Error: Your status message is too long!')
            else:
                return l('Error [%s]: Your status message is too long!') % (gch)
    return ''

def check_mf_prs_caps(mfnode):
    caps = mfnode.getTags('c', namespace=xmpp.NS_CAPS)
    gch = get_mf_gch(mfnode)
        
    if not caps:
        if is_gch_target(mfnode):
            return l('Error: Your client has empty presence caps!')
        else:
            return l('Error [%s]: Your client has empty presence caps!') % (gch)
    return ''

def check_mf_ak_ab(mfnode):
    cid = get_client_id()
    
    gch = get_mf_gch(mfnode)
    jid = get_mf_br_jid(mfnode)
    nick = get_mf_prs_nick(mfnode)

    akpat = ''
    abpat = ''
    
    akpat = get_fatal_var(cid, 'akick_comp_exp', gch)
    abpat = get_fatal_var(cid, 'aban_comp_exp', gch)

    if akpat:
        kbres = []
        fndj = []
        fndn = []
        
        for amli in akpat:
            exp = amli[0]
            
            if exp:
                if not fndj:
                    fndj = exp.findall(jid)
                
                if not fndn:
                    fndn = exp.findall(nick)
        
        if jid in fndj:
            kbres.append(l('Error [%s]: Your jid is prohibited in this groupchat!') % (gch))
        
        if nick in fndn:
            if is_gch_target(mfnode):
                kbres.append(l('Error: Selected nick is prohibited in this groupchat!'))
            else:
                kbres.append(l('Error [%s]: Selected nick is prohibited in this groupchat!') % (gch))
        
        if kbres: 
            return kbres
       
    if abpat:
        kbres = []
        fndj = []
        fndn = []
        
        for amli in abpat:
            exp = amli[0]
            
            if exp:
                if not fndj:
                    fndj = exp.findall(jid)
                    
                if not fndn:
                    fndn = exp.findall(nick)
        
        if jid in fndj: 
            kbres.append(l('Error [%s]: Your jid is prohibited in this groupchat!') % (gch))
            
        if nick in fndn: 
            if is_gch_target(mfnode):
                kbres.append(l('Error: Selected nick is prohibited in this groupchat!'))
            else:
                kbres.append(l('Error [%s]: Selected nick is prohibited in this groupchat!') % (gch))
            
        if kbres: 
            return kbres
    return ['']

def check_mf_nick_len(mfnode, nlen):
    nick = get_mf_prs_nick(mfnode)
    gch = get_mf_gch(mfnode)
    
    if len(nick) > nlen:
        if is_gch_target(mfnode):
            return l('Error: Nick is too long!')
        else:
            return l('Error [%s]: Nick is too long!') % (gch)
    return ''

def check_mf_nick_space(mfnode):
    nick = get_mf_prs_nick(mfnode)
    gch = get_mf_gch(mfnode)
    
    if has_edge_space(nick):
        if is_gch_target(mfnode):
            return l('Error: Nick with spaces by edges!')
        else:
            return l('Error [%s]: Nick with spaces by edges!') % (gch)
    return ''

def check_mf_msg_len(mfnode, mlen):
    body = mfnode.getBody()

    if body:
        if len(body) > mlen:
            return l('Error: Message is too long!')
    return ''

def check_mf_sw_ws(mfnode, ename='message'):
    mf_sw_ws = ['бляд', ' блят', ' бля ', ' блять ', ' плять ', ' хуй', ' ибал', ' ебал', 'нахуй', ' хуй', ' хуи', 'хуител', ' хуя', 'хуя', ' хую', ' хуе', ' ахуе', ' охуе', 'хуев', ' хер ', ' хер', 'хер', ' пох ', ' нах ', 'писд', 'пизд', 'рizd', ' пздц ', ' еб', ' епана ', ' епать ', ' ипать ', ' выепать ', ' ибаш', ' уеб', 'проеб', 'праеб', 'приеб', 'съеб', 'сьеб', 'взъеб', 'взьеб', 'въеб', 'вьеб', 'выебан', 'перееб', 'недоеб', 'долбоеб', 'долбаеб', ' ниибац', ' неебац', ' неебат', ' ниибат', ' пидар', ' рidаr', ' пидар', ' пидор', 'педор', 'пидор', 'пидарас', 'пидараз', ' педар', 'педри', 'пидри', ' заеп', ' заип', ' заеб', 'ебучий', 'ебучка ', 'епучий', 'епучка ', ' заиба', 'заебан', 'заебис', ' выеб', 'выебан', ' поеб', ' наеб', ' наеб', 'сьеб', 'взьеб', 'вьеб', ' гандон', ' гондон', 'пахуи', 'похуис', ' манда ', 'мандав', ' залупа', ' залупог']

    def check_sw_ws(strng):
        if strng:
            strng = strng.lower()
            strng = ' ' + strng + ' '
            
            for x in mf_sw_ws:
                if strng.count(x):
                    return True
        return False
    
    if ename == 'presence':
        gch = get_mf_gch(mfnode)
        
        pswres = []
        
        nick = get_mf_prs_nick(mfnode)
        
        if check_sw_ws(nick):
            if is_gch_target(mfnode):
                pswres.append(l('Error: Your nick contains obscene words!'))
            else:
                pswres.append(l('Error [%s]: Your nick contains obscene words!'))
        
        stmsg = mfnode.getStatus()
        
        if stmsg:
            if check_sw_ws(stmsg):
                if is_gch_target(mfnode):
                    pswres.append(l('Error: Your status message contains obscene words!'))
                else:
                    pswres.append(l('Error [%s]: Your status message contains obscene words!'))
                
        if pswres: 
            return pswres
        return ['']
    elif ename == 'message':
        body = mfnode.getBody()
        
        if body:
            if check_sw_ws(body):
                return l('Error: Your message contains obscene words!')
    return ''

def handler_muc_filter(conn, iq):
    cid = get_client_id()
    
    mfnode = get_mf_nodes(iq)
    
    if mfnode:
        ndname = mfnode.getName()
        
        riq = iq.buildReply('result')
        
        gch = get_mf_gch(mfnode)
        
        mfstate = int(get_gch_param(gch, 'muc_filter', '1'))
        
        mfnlenst = int(get_gch_param(gch, 'mf_nick_len', '1'))
        mfnlen = int(get_gch_param(gch, 'mf_nick_len_len', '30'))
        
        mfnspace = int(get_gch_param(gch, 'mf_nick_space', '1'))
        
        mfprsafl = int(get_gch_param(gch, 'mf_prs_aflood', '1'))
        
        mfmsgst = int(get_gch_param(gch, 'mf_msg', '1'))
        mfmsglen = int(get_gch_param(gch, 'mf_msg_len', '300'))
        
        mfswwst = int(get_gch_param(gch, 'mf_sww', '1'))
        
        mfmsgafl = int(get_gch_param(gch, 'mf_msg_aflood', '1'))
        
        mfpstlnst = int(get_gch_param(gch, 'mf_stmsg_len', '1'))
        mfpstlen = int(get_gch_param(gch, 'mf_stmsg_len_len', '100'))
        
        mfpcaps = int(get_gch_param(gch, 'mf_prscaps', '0'))
        
        mfakab = int(get_gch_param(gch, 'mf_akab', '1'))
        
        if mfstate:
            if ndname == 'presence':
                prsres = []
                
                if mfnlenst: 
                    prsres.append(check_mf_nick_len(mfnode, mfnlen))
                    
                if mfnspace: 
                    prsres.append(check_mf_nick_space(mfnode))
                    
                if mfakab: 
                    prsres.extend(check_mf_ak_ab(mfnode))
                    
                if mfswwst: 
                    prsres.extend(check_mf_sw_ws(mfnode, 'presence'))
                    
                if mfpstlnst: 
                    prsres.append(check_mf_st_len(mfnode, mfpstlen))
                
                if mfpcaps: 
                    prsres.append(check_mf_prs_caps(mfnode))
                
                prsres = rmv_empty_items(prsres)
                
                if prsres:
                    target = get_mf_target(mfnode)
                    
                    for pli in prsres:
                        msg(target, pli)
                    
                    raise xmpp.NodeProcessed
                    
                if mfprsafl:
                    nick = get_mf_prs_nick(mfnode)
                    
                    if not is_var_set(cid, 'uprs', gch, nick):
                        set_fatal_var(cid, 'uprs', gch, nick, '%s' % (mfnode))
                    else:
                        osprs = get_fatal_var(cid, 'uprs', gch, nick)
                        nsprs = '%s' % (mfnode)
                        
                        if osprs == nsprs:
                            raise xmpp.NodeProcessed
                        else:
                            set_fatal_var(cid, 'uprs', gch, nick, '%s' % (mfnode))
            elif ndname == 'message':
                msgres = []
                
                if mfmsgst: 
                    msgres.append(check_mf_msg_len(mfnode, mfmsglen))
                    
                if mfswwst: 
                    msgres.append(check_mf_sw_ws(mfnode))
                
                msgres = rmv_empty_items(msgres)
                
                if msgres:
                    gch_jid = get_mf_gch_jid(mfnode)
                    
                    for mli in msgres:
                        msg(gch_jid, mli)
                    
                    raise xmpp.NodeProcessed
                    
                if mfmsgafl:
                    mbody = mfnode.getBody()
                    
                    if not mbody: 
                        raise xmpp.NodeProcessed
                    
                    nick = get_mf_nick(mfnode)
                    
                    if not is_var_set(cid, 'umsg', gch, nick):
                        set_fatal_var(cid, 'umsg', gch, nick, '%s' % (mbody.strip()))
                    else:
                        omsg = get_fatal_var(cid, 'umsg', gch, nick)
                        nmsg = '%s' % (mbody.strip())
                        
                        if omsg == nmsg:
                            raise xmpp.NodeProcessed
                        else:
                            set_fatal_var(cid, 'umsg', gch, nick, '%s' % (mbody.strip()))
        
        query = riq.getTag('query')
        query.addChild(node=mfnode)
        conn.send(riq)
        raise xmpp.NodeProcessed

def handler_mf_leave(groupchat, nick, reason, code):
    cid = get_client_id()
    
    if is_var_set(cid, 'uprs', groupchat, nick):
        rmv_fatal_var(cid, 'uprs', groupchat, nick)

    if is_var_set(cid, 'umsg', groupchat, nick):
        rmv_fatal_var(cid, 'umsg', groupchat, nick)

def init_mfilter_process():
    register_raw_iq_handler(handler_muc_filter)

def get_muc_filter_state(gch):
    if not param_exists(gch, 'muc_filter'):
        set_gch_param(gch, 'muc_filter', '1')
        
    if not param_exists(gch, 'mf_nick_len'):
        set_gch_param(gch, 'mf_nick_len', '1')
    if not param_exists(gch, 'mf_nick_len_len'):
        set_gch_param(gch, 'mf_nick_len_len', '30')

    if not param_exists(gch, 'mf_nick_space'):
        set_gch_param(gch, 'mf_nick_space', '1')
        
    if not param_exists(gch, 'mf_prs_aflood'):
        set_gch_param(gch, 'mf_prs_aflood', '1')
        
    if not param_exists(gch, 'mf_msg'):
        set_gch_param(gch, 'mf_msg', '1')
    if not param_exists(gch, 'mf_msg_len'):
        set_gch_param(gch, 'mf_msg_len', '900')
        
    if not param_exists(gch, 'mf_sww'):
        set_gch_param(gch, 'mf_sww', '1')
        
    if not param_exists(gch, 'mf_msg_aflood'):
        set_gch_param(gch, 'mf_msg_aflood', '1')
        
    if not param_exists(gch, 'mf_stmsg_len'):
        set_gch_param(gch, 'mf_stmsg_len', '1')
    if not param_exists(gch, 'mf_stmsg_len_len'):
        set_gch_param(gch, 'mf_stmsg_len_len', '50')

    if not param_exists(gch, 'mf_prscaps'):
        set_gch_param(gch, 'mf_prscaps', '0')

    if not param_exists(gch, 'mf_akab'):
        set_gch_param(gch, 'mf_akab', '1')

register_stage0_init(init_mfilter_process)
register_stage1_init(get_muc_filter_state)
register_leave_handler(handler_mf_leave)
