# -*- coding: utf-8 -*-

#  fatal plugin
#  xeppresence plugin

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Some portions of code © 2010 Quality <admin@qabber.ru>
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
from muc import kick

def handler_presence_ra_change(prs):
    frmsrc = prs.getFrom()
    groupchat = get_stripped(frmsrc)
    nick = get_resource(frmsrc)
    jid = get_true_jid(groupchat + '/' + nick)

    if user_access_exists(jid):
        return
    else:
        if user_access_exists(jid, groupchat):
            return
        else:
            if is_gch_user(groupchat, nick):
                role = get_gch_role(groupchat, nick)
                aff = get_gch_aff(groupchat, nick)
                
                accr = get_int_fatal_var('roles', role)
                acca = get_int_fatal_var('affiliations', aff)
                
                access = accr + acca
                
                change_access_temp(groupchat, jid, access)

def handler_presence_nickcommand(prs):
    cid = get_client_id()
    
    frmsrc = prs.getFrom()
    groupchat = get_stripped(frmsrc)
    
    if is_groupchat(groupchat):
        code = prs.getStatusCode()
        
        if code == '303':
            nick = prs.getNick()
        else:
            nick = get_resource(frmsrc)
        
        if nick:
            nickspl = safe_split(nick, ' ')
            nicksrc = nickspl[0]
            nicksrc = nicksrc.strip()
            nicksrc = nicksrc.lower()
        else:
            return
        
        aliaso = get_fatal_var(cid, 'alias')
        
        if is_var_set('commands', nicksrc) or nicksrc in aliaso.galiaslist or nicksrc in aliaso.aliaslist[groupchat]:
            kick(groupchat, nick, l('%s: invalid nick, choose another one!') % (get_bot_nick(groupchat)))

def start_gch_keepalive_check():
    check_time = 300
    
    keep_alive = get_int_cfg_param('keep_alive')

    if keep_alive:
        check_time = keep_alive

    add_fatal_task('gch_keep_alive_check', func=gch_keepalive_check, ival=check_time)

def gch_keepalive_check():
    cid = get_client_id()
    
    chats = list(get_dict_fatal_var(cid, 'gchrosters'))
    
    def_nick = get_cfg_param('default_nick', 'fatal-bot')
    
    for gch in chats:
        iq = xmpp.Iq()
        iq = xmpp.Iq('get')
        Id = 'gp%s' % (rand10())
        iq.setID(Id)
        iq.addChild('ping', {}, [], 'urn:xmpp:ping')
        iq.setTo(gch + '/' + get_chatroom_info(gch, 'nick', def_nick))
        
        jconn = get_client_conn()
        jconn.SendAndCallForResponse(iq, gch_keepalive_check_answ, {'sId': Id})
    
@handle_xmpp_exc(quiet=True)
def gch_keepalive_check_answ(coze, res, sId):
    if res:        
        Id = res.getID()
        
        coze.getFuncRes(sId)
        
        if not Id == sId:
            return
                
        gch, error = get_stripped(res.getFrom()), res.getErrorCode()
        
        if error in ['405', None]:
            pass
        elif error == '406':
            time.sleep(3)
            join_groupchat(gch, '', get_chatroom_info(gch, 'pass'))

def handler_presence_botresp(prs):
    frmsrc = prs.getFrom()
    groupchat = get_stripped(frmsrc)
    nick = get_resource(frmsrc)
    ptype = prs.getType()

    if ptype == 'unavailable':
        scode = prs.getStatusCode()
        superadmin = sadmin_jid()

        if nick == get_bot_nick(groupchat):
            if scode == '307':
                reason = prs.getReason()
                
                if reason:
                    msg(superadmin, l('Bot has been kicked in %s with reason: %s!') % (groupchat, reason))
                else:
                    msg(superadmin, l('Bot has been kicked in %s!') % (groupchat))
                    
                leave_groupchat(groupchat)
            elif scode == '301':
                reason = prs.getReason()
                
                if reason:
                    msg(superadmin, l('Bot has been banned in %s with reason: %s!') % (groupchat, reason))
                else:
                    msg(superadmin, l('Bot has been banned in %s!') % (groupchat))
                
                leave_groupchat(groupchat)

register_presence_handler(handler_presence_botresp)
register_presence_handler(handler_presence_ra_change)
register_presence_handler(handler_presence_nickcommand)
register_stage2_init(start_gch_keepalive_check)

