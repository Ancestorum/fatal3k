# -*- coding: utf-8 -*-

#  fatal plugin
#  watcher plugin

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

def is_watcher_here(gch, jid):
    cid = get_client_id()
    
    if is_groupchat(gch):
        gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
            
        try:
            nickl = [li for li in gch_dic if jid == get_stripped(gch_dic[li]['rjid'])]
        except Exception:
            try:
                time.sleep(3)
                gch_dic = dict(get_dict_fatal_var(cid, 'gchrosters', gch))
                nickl = [li for li in gch_dic if jid == get_stripped(gch_dic[li]['rjid'])]
            except Exception:
                return False
        
        if nickl:
            return True
    return False

def handler_watcher_presence(prs):
    cid = get_client_id()
    
    ptype = prs.getType()
    groupchat = get_stripped(prs.getFrom())
    nick = get_resource(prs.getFrom())
    scode = prs.getStatusCode()

    if scode == '303' and ptype == 'unavailable':
        newnick = prs.getNick()
                
        jid = get_true_jid(groupchat + '/' + newnick)
                
        wgchs = list(get_dict_fatal_var(cid, 'watchers'))
        
        for wjid in wgchs:
            if not is_watcher_here(groupchat, wjid):
                if is_var_set(cid, 'watchers', wjid, 'gchs', groupchat):
                    sgch = groupchat.split('@', 1)[0]
                    rep = l('[%s]--- %s (%s) has changed nick to %s') % (sgch, nick, jid, newnick)
                    
                    return msg(wjid, rep)

def handler_watcher_leave(groupchat, nick, reason, code):
    cid = get_client_id()
    
    wgchs = list(get_dict_fatal_var(cid, 'watchers'))
    
    for wjid in wgchs:
        if not is_watcher_here(groupchat, wjid) and is_ruser_prsnt(wjid):
            if is_var_set(cid, 'watchers', wjid, 'gchs', groupchat):
                sgch = groupchat.split('@', 1)[0]
                
                rep = ''
                
                if code:
                    if code == '307':
                        rep = l('[%s]--- %s has been kicked') % (sgch, nick)
                    elif code == '301':
                        rep = l('[%s]--- %s has been banned') % (sgch, nick)
                else:
                    rep = l('[%s]--- %s has left') % (sgch, nick)
                
                if reason:
                    rep += ': %s' % (reason)

                return msg(wjid, rep)

def handler_watcher_join(groupchat, nick, aff, role):
    cid = get_client_id()
    
    jid = get_true_jid(groupchat + '/' + nick)
    
    wgchs = list(get_dict_fatal_var(cid, 'watchers'))
    
    waff = l(aff)
    wrole = l(role)
    
    for wjid in wgchs:
        if not is_watcher_here(groupchat, wjid):
            if is_var_set(cid, 'watchers', wjid, 'gchs', groupchat):
                sgch = groupchat.split('@', 1)[0]
                rep = l('[%s]--- %s (%s) has joined groupchat as %s/%s') % (sgch, nick, jid, waff, wrole)
                return msg(wjid, rep)

def handler_watcher_mess(type, source, body):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if type == 'private' and not is_groupchat(groupchat):
        return
    
    nick = source[2]
    wgchs = list(get_dict_fatal_var(cid, 'watchers'))
    
    for wjid in wgchs:
        if not is_watcher_here(groupchat, wjid):
            if is_var_set(cid, 'watchers', wjid, 'gchs', groupchat):
                sgch = groupchat.split('@', 1)[0]
                
                if nick:
                    rep = '[%s]<%s> %s' % (sgch, nick, body)
                else:
                    rep = '[%s] %s' % (sgch, body)
                
                splb = body.split(' ', 1)
                
                if splb:
                    if splb[0] == '/me':
                        rep = '[%s]* %s %s' % (sgch, nick, splb[1])
                
                return msg(wjid, rep)
    
def handler_watcher(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if type == 'console':
        jid = 'console'
    else:
        jid = get_true_jid(source)

    if is_groupchat(groupchat):
        return reply(type, source, l('This command can not be used in groupchat!'))

    if parameters:
        parameters = parameters.strip()
        
        if parameters[0] == '-' and len(parameters) == 1:
            rmv_fatal_var(cid, 'watchers', jid)
            return reply(type, source, l('List of watchers has been cleared!'))
        elif parameters[0] == '-' and len(parameters) > 1 and parameters[1:].isdigit():
            wgchn = int(parameters[1:])
            
            if not is_var_set(cid, 'watchers', jid):
                return reply(type, source, l('Watcher has not been set yet!'))
            else:
                wgchsl = get_list_fatal_var(cid, 'watchers', jid, 'gchs')
                
                if len(wgchsl) < wgchn:
                    return reply(type, source, l('Invalid number of groupchat!'))
                else:
                    wgch = wgchsl[wgchn - 1]
                    
                    gchs = get_fatal_var(cid, 'watchers', jid, 'gchs')
                    
                    if gchs:
                        gchs.remove(wgch)
                    
                    if not is_var_set(cid, 'watchers', jid, 'gchs'):
                        rmv_fatal_var(cid, 'watchers', jid)
                        
                    rep = l('Groupchat %s has been removed from list of watchers!') % (wgch)
                        
                    return reply(type, source, rep)
        else:
            wgch = parameters
            
            if not check_jid(wgch):
                return reply(type, source, l('Invalid syntax!'))

            if not is_var_set(cid, 'watchers', jid):
                set_fatal_var(cid, 'watchers', jid, 'gchs', [])
            
            if not is_var_set(cid, 'watchers', jid, 'gchs', wgch):
                if is_groupchat(wgch):
                    gchs = get_fatal_var(cid, 'watchers', jid, 'gchs')
                    
                    gchs.append(wgch)
                    
                    return reply(type, source, l('Watcher for %s has been set!') % (wgch))
                else:
                    if not is_var_set(cid, 'watchers', jid, 'gchs'):
                        rmv_fatal_var(cid, 'watchers', jid)

                    return reply(type, source, l('Unable to set watcher: bot is not present in tnis groupchat!'))
            else:
                return reply(type, source, l('Watcher has been already set!'))
    else:
        if is_var_set(cid, 'watchers', jid):
            rep = l('Groupchats with watchers (total: %s):\n\n%s')
            
            wgchsl = get_list_fatal_var(cid, 'watchers', jid, 'gchs')
            
            wgnli = get_num_list(wgchsl)
            
            return reply(type, source, rep % (len(wgchsl), '\n'.join(wgnli)))
        else:
            return reply(type, source, l('Watcher has not been set yet!'))

register_join_handler(handler_watcher_join)
register_leave_handler(handler_watcher_leave)
register_presence_handler(handler_watcher_presence)
register_message_handler(handler_watcher_mess)

register_command_handler(handler_watcher, 'watcher', 100)
