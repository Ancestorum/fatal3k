# -*- coding: utf-8 -*-

#  fatal plugin
#  xepping plugin

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
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

def handler_ping(type, source, parameters):
    nick = parameters.strip()
    groupchat = source[1]
    param = ''
    
    iq = xmpp.Iq('get')
    Id = 'up%s' % (rand10())
    iq.setID(Id)
    iq.addChild('ping', {}, [], 'urn:xmpp:ping')
    
    if parameters:
        param = parameters.strip()
        
        if not is_gch_user(groupchat, nick):
            iq.setTo(param)
        else:
            param = nick
            jid = groupchat + '/' + nick
            iq.setTo(jid)
    else:
        jid = source[0]
        iq.setTo(jid)
        param = ''
    
    t0 = time.time()
    jconn = get_client_conn()
    jconn.SendAndCallForResponse(iq, handler_ping_answ, {'t0': t0, 'type': type, 'source': source, 'param': param, 'sId': Id})

@handle_xmpp_exc('Unknown error!')
def handler_ping_answ(coze, res, t0, type, source, param, sId):
    if res:
        Id = res.getID()
        
        if Id != sId:
            return reply(type, source, l('Unknown error!'))
        
        if res.getType() in ['result', 'get'] or res.getErrorCode() in ['503', '501']:
            t = time.time()
            ptime = round(t - t0, 3)
            
            if param:
                rep = l('Ping time for %s is %s seconds.') % (param, ptime)
            else:
                rep = l('Ping time is %s seconds.') % (ptime)
        elif res.getErrorCode() == '404':
            rep = l('Not found!')
        else:
            rep = l('Unknown error!')

    return reply(type, source, rep)
    
register_command_handler(handler_ping, 'ping')

