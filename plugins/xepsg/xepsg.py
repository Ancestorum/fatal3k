# -*- coding: utf-8 -*-

#  fatal plugin
#  xepsg plugin

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Copyright © 2009-2023 Ancestors Soft

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

def handler_sg_get(ttype, source, parameters):
    iq = xmpp.Iq('get')
    Id = 'finf%s' % (rand10())
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
    
    if ttype != 'null':
        jconn.SendAndCallForResponse(iq, first_handler_sg, {'parameters': parameters, 'ttype': ttype, 'source': source, 'sId': Id})
    else:
        xml = xmpp_nested_rtns(iq)

        node = ''
        
        try:
            node = xmpp.simplexml.XML2Node(xml)
        except ExpatError:
            return -1
        
        if node.getAttr('type') == 'result' and node.getAttr('id') == Id:
            return first_handler_sg(jconn, node, parameters, ttype, source, Id)
        elif node.getAttr('type') == 'error' and node.getAttr('id') == Id:
            ertg = node.getTag('error')
            erco = ertg.getAttr('code')
            
            if not erco:
                erco = '503'
            
            return '-%s' % (erco)
        return '-1'

@handle_xmpp_exc('Unknown error!')
def first_handler_sg(coze, res, parameters, ttype, source, sId):
    qu = None
    
    if res:
        res = xmpp.Iq(node=res)
        qu = res.getQueryChildren()
        Id = res.getID()
        
        if Id != sId:
            return reply(ttype, source, l('Unknown error!'))
    else:
        return reply(ttype, source, l('Unknown error!'))
    
    ptype = res.getType()
    
    if ptype == 'error':
        return reply(ttype, source, l('Unknown error!'))
    elif ptype == 'result':
        iq = xmpp.Iq('get')
        Id = 'sinf%s' % (rand10())
        iq.setID(Id)
        iq.setQueryNS('http://jabber.org/protocol/stats')
        iq.setQueryPayload(qu)
        iq.setTo(parameters)

        if ttype != 'null':
            jconn = get_client_conn()
            jconn.SendAndCallForResponse(iq, second_handler_sg, {'parameters': parameters, 'ttype': ttype, 'source': source, 'sId': Id})
        else:
            xml = xmpp_nested_rtns(iq)

            node = ''
            
            try:
                node = xmpp.simplexml.XML2Node(xml)
            except ExpatError:
                pass

            if node:
                if node.getAttr('type') == 'result' and node.getAttr('id') == Id:
                    qrtg = node.getTag('query')
                    ndls = qrtg.getChildren()
                    idic = {}
                    
                    for nd in ndls:
                        name = nd.getAttr('name')
                        units = nd.getAttr('units')
                        value = nd.getAttr('value')
                        
                        idic[name] = {'units': units, 'value': value}
                        
                    return idic
                elif node.getAttr('type') == 'error' and node.getAttr('id') == Id:
                    ertg = node.getTag('error')
                    erco = ertg.getAttr('code')
                    
                    if not erco:
                        erco = '503'
                    
                    return '-%s' % (erco)
            return '-1'
    else:
        return reply(type, source, l('Timeout has expired!'))

@handle_xmpp_exc('Unknown error!')
def second_handler_sg(coze, stats, parameters, ttype, source, sId):
    if stats:
        Id = stats.getID()
        
        if Id != sId:
            return reply(ttype, source, l('Unknown error!'))
    else:
        return reply(ttype, source, l('Unknown error!'))
    
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
            
        return reply(ttype, source, result.strip())
    
register_command_handler(handler_sg_get, 'info', 10)
