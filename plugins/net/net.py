# -*- coding: utf-8 -*-

#  fatal plugin
#  net plugin

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
from urllib.parse import urlsplit

def download_file(url, file):
    try:
        resp = urllib.request.urlretrieve(url, file)
    except:
        return 0
    
    if resp and len(resp) == 2:
        return resp[1].get('Content-Length')
    else:
        return 0

def si_gf_request(frm, fjid, sid, name, size, site):
    iq = xmpp.Protocol(name='iq', to=fjid, typ='set')
    ID = 'si%s' % (time.time())
    iq.setID(ID)
    si = iq.setTag('si')
    si.setNamespace(xmpp.NS_SI)
    si.setAttr('profile', xmpp.NS_FILE)
    si.setAttr('id', sid)
    file_tag = si.setTag('file')
    file_tag.setNamespace(xmpp.NS_FILE)
    file_tag.setAttr('name', name)
    file_tag.setAttr('size', size)
    desc = file_tag.setTag('desc')
    desc.setData(l('File from "%s".') % (site))
    file_tag.setTag('range')
    feature = si.setTag('feature')
    feature.setNamespace(xmpp.NS_FEATURE)
    _feature = xmpp.DataForm(typ='form')
    feature.addChild(node=_feature)
    field = _feature.setField('stream-method')
    field.setAttr('type', 'list-single')
    field.addOption(xmpp.NS_IBB)
    field.addOption('jabber:iq:oob')
    return iq

def check_gf_stream(gch, nick, to, sid):
    try:
        cid = get_client_id()
        
        st_time = time.strftime('%H.%M.%S', time.localtime(time.time()))
        thrc = inc_fatal_var('info', 'thr')
        tmr_name = '%s/check%d.%s.%s' % (cid, thrc, 'check_gf_stream', st_time)
        tmr = threading.Timer(1, check_gf_stream, (gch, nick, to, sid))
        tmr.setName(tmr_name)
        tmr.start()
    except:
        return
    
    jconn = get_client_conn()
    
    if not sid in jconn.IBB._streams:
        tmr.cancel()
        return
    
    if not is_gch_user(groupchat, nick):
        Iq = xmpp.Protocol('iq', to, 'set', payload=[xmpp.Node(xmpp.NS_IBB + ' close', {'sid': sid})])
        jconn.send(Iq)
        del jconn.IBB._streams[sid]
        tmr.cancel()

def handler_get_file(type, source, parameters):
    groupchat = source[1]
    nick = source[2]

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        url = parameters.strip()
        
        to = get_user_jid(groupchat, nick)
        
        if not to:
            return reply(type, source, l('Internal error, unable to perform operation!'))
        
        cid = get_client_id()
        
        sid = 'file%s' % (time.time())
        name = sid
        path = 'dynamic/%s/%s' % (cid, name)
        site = 'unknown'
        
        spurl = urlsplit(url)
        
        if spurl[2] != '':
            spname = spurl[2].split('/')
            name = spname[-1]
                
        if spurl[1] != '':
            site = spurl[1]
            
            if spurl[0] != '':
                site = spurl[0] + '://' + site		
        
        dlsize = download_file(url.encode('utf-8'), path)
        
        if not dlsize or dlsize > 1048576:
            if os.path.exists(path):
                os.remove(path)
            
            return reply(type, source, l('Unable to get this file!'))
        
        try:
            fp = open(path, 'rb')
        except Exception:
            if os.path.exists(path):
                os.remove(path)
            
            return reply(type, source, l('Unable to get this file!'))
        
        bjid = get_client_id()
        resource = get_cfg_param('resource')
        
        frm = '%s/%s' % (bjid, resource)
        
        sireq = si_gf_request(frm, to, sid, name, dlsize, site)
        
        jconn = get_client_conn()
        jconn.SendAndCallForResponse(sireq, handler_get_file_answ, args={'type': type, 'source': source, 'sid': sid, 'to': to, 'fp': fp})
    else:
        return reply(type, source, l('Invalid syntax!'))
        
def handler_get_file_answ(coze, resp, type, source, sid, to, fp):
    try:
        rtype = resp.getType()
        nick = source[2]
        groupchat = source[1]
        
        jconn = get_client_conn()
        
        if rtype == 'result':
            jconn.IBB.OpenStream(sid, to, fp, 1024)
            check_gf_stream(groupchat, nick, to, sid)
            
            name = fp.name
            os.remove(name)
        else:
            name = fp.name
            fp.close()
            os.remove(name)
            reply(type, source, l('File transfer has failed!'))
    except:
        reply(type, source, l('Unknown error!'))
        log_exc_error()

register_command_handler(handler_get_file, 'get_file', 11)
