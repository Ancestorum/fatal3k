# -*- coding: utf-8 -*-

#  fatal plugin
#  xepinvite plugin

#  Initial Copyright © 2008 Als <Als@exploit.in>
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

def get_invite_jid(gch, nick):
    cid = get_client_id()
    
    sql = "SELECT jid FROM users WHERE nick=?;"
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql, nick)
    
    if qres:
        return qres[0][0]
    else:
        return ''

def handler_invite_start(type, source, parameters):
    groupchat = source[1]
    nick = source[2]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    sparams = safe_split(parameters)
    
    nick_jid = sparams[0]
    reason = sparams[1]
    
    if parameters:
        if not check_jid(nick_jid):
            jid = get_invite_jid(groupchat, nick_jid)
            
            if not jid:
                return reply(type, source, l('User not found!'))
        else:
            jid = nick_jid
            
        msg = xmpp.Message(to=groupchat)
        
        Id = 'inv%s' % (time.time())
        
        msg.setID(Id)
        x = xmpp.Node('x')
        x.setNamespace('http://jabber.org/protocol/muc#user')
        inv = x.addChild('invite', {'to': jid})
        
        if reason:
            inv.setTagData('reason', '%s (%s)' % (reason, nick))
        else:
            inv.setTagData('reason', l('Invite from %s.') % (nick))
            
        msg.addChild(node=x)
        
        jconn = get_client_conn()
        resp = jconn.send(msg)
        
        if resp == Id:
            reply(type, source, l('Done!'))
    else:
        reply(type, source, l('Invalid syntax!'))

register_command_handler(handler_invite_start, 'invite', 11)
