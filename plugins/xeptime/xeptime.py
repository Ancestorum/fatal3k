# -*- coding: utf-8 -*-

#  fatal plugin
#  xeptime plugin

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>
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
    
def handler_gettime_xep_disco(type, source, parameters):
    gch_jid = source[1]
    nick = source[2]

    if parameters.strip():
        if is_groupchat(gch_jid):
            if is_gch_user(gch_jid, parameters):
                jid = '%s/%s' % (gch_jid, parameters)
            else:
                jid = parameters
        else:
            jid = parameters
    else:
        if is_groupchat(gch_jid):
            jid = '%s/%s' % (gch_jid, nick)
        else:
            jid = source[0]
    
    iq = xmpp.Iq('get')
    iq.setTo(jid)
    Id = 'info%s' % (time.time())
    iq.setID(Id)
    iq.addChild('query', {}, [], 'http://jabber.org/protocol/disco#info')
    jconn = get_client_conn()
    jconn.SendAndCallForResponse(iq, handler_gettime_xep_disco_answ, {'type': type, 'source': source, 'parameters': parameters, 'jid': jid, 'sId': Id})

@handle_xmpp_exc('Unknown error!')
def handler_gettime_xep_disco_answ(coze, res, type, source, parameters, jid, sId):
    groupchat = source[1]
    nick = source[2]
    rep = ''
    
    if res:
        Id = res.getID()
        
        if Id != sId:
            return reply(type, source, l('Unknown error!'))
        
        if not res.getType() == 'result':
            ecode = res.getErrorCode()
            
            if ecode == '404':
                return reply(type, source, l('User not found!'))
            else:
                return reply(type, source, l('Unknown error!'))
        
        res = xmpp.Iq(node=res)
        res = res.getQueryChildren()
        
        for x in res:
            att = x.getAttrs()
            
            if 'var' in att:
                att = att['var']
                
                if att == 'urn:xmpp:time':                            
                    gettime_xep0202(type, source, jid, parameters)
                    return
        
        gettime_xep0090(type, source, jid, parameters)
    else:
        return reply(type, source, l('Timeout has expired!'))

def gettime_xep0090(type, source, jid, param=''):
    nick = ''
    
    if param:
        nick = param
    else:
        nick = source[2]
        
    time_iq = xmpp.Iq('get')
    Id = 'time%s' % (time.time())
    time_iq.setID(Id)
    time_iq.addChild('query', {}, [], 'jabber:iq:time')
    time_iq.setTo(jid)
    jconn = get_client_conn()
    jconn.SendAndCallForResponse(time_iq, gettime_xep0090_answ, {'type': type, 'source': source, 'nick': nick, 'sId': Id})

@handle_xmpp_exc('Unknown error!')
def gettime_xep0090_answ(coze, res, nick, type, source, sId):
    Id = res.getID()
    
    if Id != sId:
        return reply(type, source, l('Unknown error!'))
    
    ptype = res.getType()
    
    if res:
        if ptype == 'error':
            return reply(type, source, l('Not supported by user client!'))
        elif ptype == 'result':
            time = ''
            res = xmpp.Iq(node=res)
            props = res.getQueryChildren()
            
            for p in props:
                if p.getName() == 'display':
                    time = p.getData()
            
            if time:
                if nick:
                    return reply(type, source, l('Current time of %s: %s.') % (nick, time))
                else:
                    return reply(type, source, l('Current time: %s.') % (time))
        else:
            return reply(type, source, l('Unknown error!'))

def gettime_xep0202(type, source, jid, param=''):
    nick = ''
    
    if param:
        nick = param
        
    time_iq = xmpp.Iq('get')
    Id = 'time%s' % (time.time())
    time_iq.setID(Id)
    time_iq.addChild('time', {}, [], 'urn:xmpp:time')
    time_iq.setTo(jid)
    jconn = get_client_conn()
    jconn.SendAndCallForResponse(time_iq, gettime_xep0202_answ, {'type': type, 'source': source, 'nick': nick, 'sId': Id})

@handle_xmpp_exc('Unknown error!')
def gettime_xep0202_answ(coze, res, nick, type, source, sId):
    if res:
        Id = res.getID()
        
        if Id != sId:
            return reply(type, source, l('Unknown error!'))
        
        ptype = res.getType()    
        
        if ptype == 'error':
            return reply(type, source, l('Not supported by user client!'))
        elif ptype == 'result':
            utc, tzo = '', ''
            props = res.getChildren()
            
            for p in props:
                tzo = p.getTagData('tzo')
                utc = p.getTagData('utc')
            
            if tzo and utc:
                tzss = int(tzo[:3]) * 3600
                
                pfmt = time.strptime(utc, '%Y-%m-%dT%H:%M:%SZ')
                
                gsec = time.mktime(pfmt)
                rsec = gsec + tzss
                
                rttm = time.strftime('%H:%M:%S', time.localtime(rsec))
                rtdt = time.strftime('%d.%m.%Y', time.localtime(rsec))
                
                if nick:
                    return reply(type, source, l('Current time of %s: %s (%s).') % (nick, rttm, rtdt))
                else:
                    return reply(type, source, l('Current time: %s (%s).') % (rttm, rtdt))
            else:
                return reply(type, source, l('Not supported by user client!'))
    else:
        return reply(type, source, l('Unknown error!'))

register_command_handler(handler_gettime_xep_disco, 'time', 10)
