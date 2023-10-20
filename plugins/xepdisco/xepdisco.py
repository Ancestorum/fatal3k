# -*- coding: utf-8 -*-

#  fatal plugin
#  disco plugin

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>
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

def handler_disco(type, source, parameters):
    if parameters:
        parst = parameters.split(' ', 2)
        stop, srch, tojid = '', '', parst[0]
        
        if len(parst) == 1:
            if type == 'public': 
                stop = 10
            else: 
                stop = 50
            
            srch = None
        elif len(parst) > 1:
            try:
                stop = int(parst[1])
                
                try:
                    srch = parst[2]
                except Exception:
                    srch = None
            except Exception:
                srch = parst[1]
                
                if type == 'public': 
                    stop = 10
                else: 
                    stop = 50
            
            if type == 'public':
                if stop > 50: 
                    stop = '50'
            else:
                if stop > 250: 
                    stop = '250'
        
        iq = xmpp.Iq('get')
        Id = 'disco%s' % (time.time())
        iq.setID(Id)
        query = iq.addChild('query', {}, [], xmpp.NS_DISCO_ITEMS)
        
        if len(tojid.split('#')) == 2:
            query.setAttr('node', tojid.split('#')[1])
            iq.setTo(tojid.split('#')[0])
        else:
            iq.setTo(tojid)
        
        add_jid_to_privacy(tojid)

        jconn = get_client_conn()
        jconn.SendAndCallForResponse(iq, handler_disco_ext, {'type': type, 'source': source, 'stop': stop, 'srch': srch, 'tojid': tojid, 'sId': Id})
        
        return '[disco]'
    else:
        return reply(type, source, l('Invalid syntax!'))

@handle_xmpp_exc('Unknown error!')
def handler_disco_ext(coze, res, type, source, stop, srch, tojid, sId):
    disco = []
    rep, trig = '', 0
    
    if res:
        Id = res.getID()
        
        if Id != sId:
            return reply(type, source, l('Unknown error!'))
        
        if res.getType() == 'result':
            res = xmpp.Iq(node=res)
            props = res.getQueryChildren()
            
            if props:
                for x in props:
                    att = x.getAttrs()
                    
                    if 'name' in att:
                        try:
                            st = re.search('^(.*) \((.*)\)$', att['name'])
                            st = st.groups()
                            disco.append([st[0], att['jid'], st[1]])
                            
                            trig = 1
                        except Exception:
                            if not trig:
                                temp = []
                                
                                if 'name' in att:
                                    temp.append(att['name'])
                                if 'jid' in att and not tojid.count('@'):
                                    temp.append(att['jid'])
                                if 'node' in att:
                                    temp.append(att['node'])
                                
                                disco.append(temp)
                                
                            trig = 0    
                    else:
                        disco.append([att['jid']])
            else:
                return reply(type, source, l('Unable to execute query!'))
            
            disco_c = []
            
            for li in disco: 
                if li not in disco_c: 
                    disco_c.append(li)
            
            disco = disco_c
                                   
            if disco:
                return handler_disco_answ(type, source, stop, disco, srch)
            else:
                return reply(type, source, l('Not found!'))
        else:
            rep = l('Unable to execute query!')
    else:
        rep = l('Unknown error!')
    
    return reply(type, source, rep)
    
def handler_disco_answ(type, source, stop, disco, srch):
    total = 0
    
    if total == stop:
        return reply(type, source, l('Total %s items.') % (len(disco)))

    dis, disco = [], sortdis(disco)
    
    for item in disco:
        if len(item) == 3:
            if srch:
                if srch.endswith('@'):
                    if item[1].startswith(srch):
                    
                        dis.append('%s [%s]: %s' % (item[0], item[1], item[2]))
                        
                        break
                    else:
                        continue
                else:
                    if not item[0].count(srch) and not item[1].count(srch):
                        continue
            
            dis.append('%s [%s]: %s' % (item[0], item[1], item[2]))
            
            if len(dis) == stop:
                break
        elif len(item) == 2:
            if srch:
                if not item[0].count(srch) and not item[1].count(srch):
                    continue
            
            dis.append('%s [%s]' % (item[0], item[1]))
            
            if len(dis) == stop:
                break
        else:
            if srch:
                if not item[0].count(srch):
                    continue
            
            dis.append(item[0])
            
            if len(dis) == stop:
                break
    if dis:
        dis = get_num_list(dis)
        
        if len(disco) != len(dis):
            rep = l('Result of query (total: %s; displayed: %s):\n\n') % (len(disco), len(dis))
        else:
            rep = l('Result of query (total: %s):\n\n') % (len(dis))
    else:
        rep = l('Not found!')
    
    rep += '\n'.join(dis)
    return reply(type, source, rep)
    
def sortdis(dis):
    disd, diss, disr = [], [], []
    
    for x in dis:
        try:
            int(x[2])
            disd.append(x)
        except Exception:
            diss.append(x)
    
    disd.sort()
    disd.reverse()
    diss.sort()
    
    for x in disd:
        disr.append(x)
        
    for x in diss:
        disr.append(x)
        
    return disr

register_command_handler(handler_disco, 'disco', 10)
