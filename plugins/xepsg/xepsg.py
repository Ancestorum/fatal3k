# -*- coding: utf-8 -*-

#  fatal plugin
#  xepsg plugin

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
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

def handler_sg_get(type, source, parameters):
    iq = xmpp.Iq('get')
    Id = 'finf%s' % (time.time())
    iq.setID(Id)
    iq.setQueryNS('http://jabber.org/protocol/stats')
    
    if parameters != '':
        iq.setTo(parameters.strip())
    else:
        jid = get_client_id()
        conser = get_domain(jid)

        iq.setTo(conser)
        parameters = conser
        
    jconn = get_client_conn()
    jconn.SendAndCallForResponse(iq, first_handler_sg, {'parameters': parameters, 'type': type, 'source': source, 'sId': Id})

@handle_xmpp_exc('Unknown error!')
def first_handler_sg(coze, res, parameters, type, source, sId):
    qu = None
    
    if res:
        res = xmpp.Iq(node=res)
        qu = res.getQueryChildren()
        Id = res.getID()
        
        if Id != sId:
            return reply(type, source, l('Unknown error!'))
    else:
        return reply(type, source, l('Unknown error!'))
    
    ptype = res.getType()
    
    if ptype == 'error':
        return reply(type, source, l('Unknown error!'))
    elif ptype == 'result':
        iq = xmpp.Iq('get')
        Id = 'sinf%s' % (time.time())
        iq.setID(Id)
        iq.setQueryNS('http://jabber.org/protocol/stats')
        iq.setQueryPayload(qu)
        iq.setTo(parameters)
        
        jconn = get_client_conn()
        jconn.SendAndCallForResponse(iq, second_handler_sg, {'parameters': parameters, 'type': type, 'source': source, 'sId': Id})
    else:
        return reply(type, source, l('Timeout has expired!'))

@handle_xmpp_exc('Unknown error!')
def second_handler_sg(coze, stats, parameters, type, source, sId):
    if stats:
        Id = stats.getID()
        
        if Id != sId:
            return reply(type, source, l('Unknown error!'))
    else:
        return reply(type, source, l('Unknown error!'))
    
    stats = xmpp.Iq(node=stats)
    pay = stats.getQueryPayload()
    
    if stats.getType() == 'result':
        result = l('Statistics of %s:\n\n') % (parameters.strip())
        
        for stat in pay:
            name = stat.getAttrs()['name']
            value = stat.getAttrs()['value']
            units = stat.getAttrs()['units']
            
            if not name: 
                name = ''
            
            result += '%s: %s %s.\n' % (name.capitalize(), value, units) 
            
        return reply(type, source, result.strip())
    
register_command_handler(handler_sg_get, 'info', 10)
