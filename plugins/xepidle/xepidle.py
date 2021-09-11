# -*- coding: utf-8 -*-

#  fatal plugin
#  xepidle plugin

#  Initial Copyright © 2007 Als <Als@exploit.in>
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

def handler_idle(type, source, parameters):
    idle_iq = xmpp.Iq('get')
    Id = 'idle%s' % (time.time())
    idle_iq.setID(Id)
    idle_iq.setNamespace('')
    idle_ch = idle_iq.addChild('query')
    idle_ch.setNamespace('jabber:iq:last')
    
    if parameters:
        param = parameters.strip()
        idle_iq.setTo(param)
    else:
        jid = get_client_id()
        param = get_domain(jid)
        idle_iq.setTo(param)
    
    add_jid_to_privacy(param)

    jconn = get_client_conn()
    jconn.SendAndCallForResponse(idle_iq, handler_idle_answ, {'type': type, 'source': source, 'param': param, 'sId': Id})

@handle_xmpp_exc('Unknown error!')
def handler_idle_answ(coze, res, type, source, param, sId):
    rep = ''
    
    if res:
        Id = res.getID()
        
        if Id != sId:
            return reply(type, source, l('Unknown error!'))
        
        if res.getType() == 'error':
            return reply(type, source, l('Not found!'))
        elif res.getType() == 'result':
            sec = ''
            props = res.getPayload()
            
            if not props:
                return reply(type, source, l('Not found!'))
            
            for p in props:
                sec = p.getAttrs()['seconds']
                
                if not sec == '0':
                    rep = l('Resource run statistics: %s works %s.') % (param, timeElapsed(int(sec)))
    else:
        rep = l('Unknown error!')
        
    return reply(type, source, rep)

def handler_userinfo_idle(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    gnick = source[2]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if not parameters:
        return reply(type, source, l('Active!'))
        
    nick = parameters.strip()
        
    if nick == gnick:
        return reply(type, source, l('Active!'))
            
    if is_gch_user(groupchat, nick):
        idtm = get_int_fatal_var(cid, 'gchrosters', groupchat, nick, 'idle')
        
        if idtm:
            idletime = int(time.time() - idtm)
        else:
            idletime = 0
            
        return reply(type, source, l('User %s is idling about already for %s!') % (nick, timeElapsed(idletime)))
    else:
        return reply(type, source, l('User not found!'))

register_command_handler(handler_idle, 'uptime', 10)
register_command_handler(handler_userinfo_idle, 'idle', 10)
