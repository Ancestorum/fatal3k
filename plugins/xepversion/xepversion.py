# -*- coding: utf-8 -*-

#  fatal plugin
#  xepversion plugin

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
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

def handler_version(ttype, source, parameters):
    gch_jid = source[1]
    nick = source[2]
    
    iq = xmpp.Iq('get')
    Id = 'ver%s' % (rand10())
    iq.setID(Id)
    iq.addChild('query', {}, [], 'jabber:iq:version')

    src = ''
    
    if parameters.strip():
        if is_groupchat(gch_jid):
            if is_gch_user(gch_jid, parameters):
                jid = gch_jid + '/' + parameters
            else:
                jid = parameters
                src = jid
        else:
            jid = parameters
            src = jid
    else:
        if is_groupchat(gch_jid):
            jid = gch_jid + '/' + nick
        else:
            jid = source[0]
        
    iq.setTo(jid)    
    
    if ttype != 'null':
        jconn = get_client_conn()
        jconn.SendAndCallForResponse(iq, handler_version_answ, {'ttype': ttype, 'source': source, 'src': src, 'jid': jid, 'sId': Id})
    else:
        xml = xmpp_nested_rtns(iq)
        node = xmpp.simplexml.XML2Node(xml)

        if node.getAttr('type') == 'result' and node.getAttr('id') == Id:
            qrtg = node.getTag('query')
            nmdt = qrtg.getTagData('name')
            vrdt = qrtg.getTagData('version')
            osdt = qrtg.getTagData('os')
            
            vrdc = {'name': nmdt, 'version': vrdt, 'os': osdt}
            
            return vrdc
        elif node.getAttr('type') == 'error' and node.getAttr('id') == Id:
            ertg = node.getTag('error')
            erco = ertg.getAttr('code')
            
            return '-%s' % (erco)
        return '-1'

@handle_xmpp_exc('Unknown error!')
def handler_version_answ(coze, res, ttype, source, src, jid, sId):
    rep = ''
    
    if res:
        Id = res.getID()
        
        if Id != sId:
            return reply(ttype, source, l('Unknown error!'))
            
        ptype = res.getType()
        
        if ptype == 'error':
            ecode = res.getErrorCode()
            
            if ecode == '404':
                return reply(ttype, source, l('User not found!'))
            elif ecode == '503':
                return reply(ttype, source, l('Service unavailable!'))
            else:
                return reply(ttype, source, l('Unknown error!'))
        elif ptype == 'result':
            name = '[no name]'
            version = '[no ver]'
            hos = '[no os]'
            res = xmpp.Iq(node=res)
            props = res.getQueryChildren()
            
            for p in props:
                if p.getName() == 'name':
                    name = p.getData()
                elif p.getName() == 'version':
                    version = p.getData()
                elif p.getName() == 'os':
                    hos = p.getData()
            
            if src:
                if check_jid(jid):
                    rep = l('Client version of %s:') % (src)
                    rep += ' '
                else:
                    rep = l('Server version of %s:') % (src)
                    rep += ' '
            else:
                rep = l('Client version:')
                rep += ' '
                
            if name:
                rep += name
            if version:
                rep += ' %s' % (version)
            if hos:
                rep += ' '
                rep += l('[OS: %s]') % (hos)
        elif ptype == 'get':
            name = '[no name]'
            version = '[no ver]'
            hos = '[no os]'
            
            rev = get_revision()
            
            set_fatal_var('ftver', 'rev', rev)
            
            name = get_fatal_var('ftver', 'botver', 'name')
            version = get_fatal_var('ftver', 'botver', 'ver') % (get_fatal_var('ftver', 'rev'))
            hos = get_fatal_var('ftver', 'botver', 'os')
            
            if not get_fatal_var('ftver', 'botver', 'os'):
                osver = ''
                
                if os.name == 'nt':
                    osname = os.popen("ver")
                    osver = codecs.decode(osname.read().strip().encode(), 'cp866') + ', '
                    osname.close()	
                else:
                    osname = os.popen("uname -sr", 'r')
                    osver = osname.read().strip() + ', '
                    osname.close()
                    
                pyver = sys.version.replace('\n', ' ')
                set_fatal_var('ftver', 'botver', 'os', '%s %s' % (osver, pyver))
            
            hos = get_fatal_var('ftver', 'botver', 'os')
            
            if name:
                rep = name
                
            if version:
                rep += ' %s' % (version)
                
            if hos:
                rep += ' '
                rep += l('[OS: %s]') % (hos)
        else:
            rep = l('Not supported by user client!')
    else:
        rep = l('Unknown error!')
        
    return reply(ttype, source, rep)
    
register_command_handler(handler_version, 'version')

