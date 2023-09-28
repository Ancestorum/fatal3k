# -*- coding: utf-8 -*-

#  fatal plugin
#  xeproster plugin

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

def parse_subs_par(params):
    jid = ''
    name = ''
    access = ''
    
    if params:
        spltdp = params.strip().split(':', 1)
        
        if len(spltdp) == 1:
            spltdp = spltdp[0].strip().split(' ', 1)
            
            if len(spltdp) == 1:
                jid = spltdp[0]
            elif len(spltdp) == 2:
                jid = spltdp[0]
                name = spltdp[1]
        elif len(spltdp) == 2:
            jid_name = spltdp[0].strip()
            access = spltdp[1]
            spltdp = jid_name.split(' ', 1)
            
            if len(spltdp) == 1:
                jid = spltdp[0]
            elif len(spltdp) == 2:
                jid = spltdp[0]
                name = spltdp[1]

    return (jid.strip(), name.strip(), access.strip())
        
def handler_subscribe(type, source, parameters):
    cid = get_client_id()
    
    rostero = get_fatal_var(cid, 'roster')
    cont_jids = rostero.getItems()
    
    set_fatal_var(cid, 'msubs_query', 1)
    set_fatal_var(cid, 'gtemp_subs_name', '')
    set_fatal_var(cid, 'manual_subscribe', 1)
    
    if parameters:
        parsed_par = parse_subs_par(parameters)
        jid = parsed_par[0]
        name = parsed_par[1]
        access = parsed_par[2]
        
        if check_jid(jid):
            if jid in cont_jids:
                gsubs = rostero.getSubscription(jid)
                
                if gsubs != 'both':
                    if not name:
                        name = jid.split('@', 1)[0]
                    
                    set_fatal_var(cid, 'gtemp_subs_name', name)
                    rostero.Subscribe(jid)
                    
                    if access and access.isdigit():
                        set_user_access(jid, int(access))
                    else:
                        set_user_access(jid, 11)
                        
                    rep = l('Authorization request has been sent to %s!') % (jid)
                    return reply(type, source, rep)
                else:
                    cont_groups = rostero.getGroups(jid)
                    
                    if not 'bot-users' in cont_groups:
                        old_name = rostero.getName(jid)
                        
                        if old_name:
                            name = old_name
                        elif not name:
                            name = jid.split('@', 1)[0]
                            
                        set_fatal_var(cid, 'gtemp_subs_name', name)	
                        rostero.setItem(jid, name, ['bot-users'])
                        
                        if access and access.isdigit():
                            set_user_access(jid, int(access))
                        else:
                            set_user_access(jid, 11)
                        
                        rep = l('Account %s already is in the roster, but has been moved to bot-users group!') % (jid)
                        return reply(type, source, rep)
                    else:
                        rep = l('Account %s already is in the roster and authorized!') % (jid)
                        return reply(type, source, rep)
            else:
                if not name:
                    name = jid.split('@', 1)[0]
                
                if access and access.isdigit():
                    set_user_access(jid, int(access))
                else:
                    set_user_access(jid, 11)
                
                set_fatal_var(cid, 'gtemp_subs_name', name)
                rostero.Subscribe(jid)
                            
                rep = l('Account %s has been added in the roster, authorization request has been sent!') % (jid)
                return reply(type, source, rep)
        else:
            return reply(type, source, l('Invalid syntax!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
        
def handler_usubscribe(type, source, parameters):
    cid = get_client_id()
    
    rostero = get_fatal_var(cid, 'roster')
    cont_jids = rostero.getItems()
    
    set_fatal_var(cid, 'manual_usubscribe', 1)
    
    if parameters:
        if check_jid(parameters):
            ajid = parameters
            
            if ajid in cont_jids:
                gsubs = rostero.getSubscription(ajid)
                
                if gsubs == 'both':
                    if 'bot-users' in rostero.getGroups(ajid):
                        set_user_access(ajid)
                    
                    rostero.Unsubscribe(ajid)
                    rostero.delItem(ajid)
                else:
                    rostero.delItem(ajid)
                    
                rep = l('Subscription and account %s has been removed from the roster!') % (ajid)
                return reply(type, source, rep)	
            else:
                rep = l('Account %s not found in the roster!') % (ajid)
                return reply(type, source, rep)
        else:
            return reply(type, source, l('Invalid syntax!'))
    else:
        return reply(type, source, l('Invalid syntax!'))	
        
def handler_auto_subscribe(conn, iq):
    cid = get_client_id()
    
    if iq.getTags('query', {}, 'jabber:iq:roster'):
        iqtype = iq.getType()
        
        fromjid = ''
        subs = ''
        sadmin = ''
        
        admins = get_lst_cfg_param('admins')
        
        if admins: 
            sadmin = admins[0]
        
        if iqtype == 'set':
            rostero = get_fatal_var(cid, 'roster')
            query = iq.getTag('query')
            itmtg = query.getTag('item')
            fromjid = itmtg.getAttr('jid')
            subs = itmtg.getAttr('subscription')
            
            if subs and fromjid:
                if subs == 'both':
                    if get_fatal_var(cid, 'msubs_query'):
                        set_fatal_var(cid, 'msubs_query', 0)
                    else:
                        if not fromjid in admins:
                            if rostero.getSubscription(fromjid) != 'both':
                                msg(sadmin, l('New account %s has been authorized and added in the roster!') % (fromjid))
                
                if subs == 'none':
                    if fromjid in rostero.getItems() and not fromjid in admins:
                        rostero.delItem(fromjid)
                elif subs == 'from' and not get_int_cfg_param('auto_subscribe'):
                    if fromjid in rostero.getItems() and not fromjid in admins:
                        rostero.delItem(fromjid)
                elif subs == 'remove': 
                    if get_int_fatal_var(cid, 'msubs_query'):
                        msg(sadmin, l('Account %s has rejected subscription and has not been added!') % (fromjid))
                        set_fatal_var(cid, 'msubs_query', 0)
            
            if fromjid in admins or get_int_cfg_param('auto_subscribe') and not get_int_fatal_var(cid, 'manual_usubscribe'):
                if subs and fromjid:
                    if subs == 'from':
                        sname = get_fatal_var(cid, 'gtemp_subs_name')
                        rostero.Subscribe(fromjid)
                        
                        if fromjid in admins:
                            if get_int_cfg_param('auto_subscribe'):
                                set_user_access(fromjid, 100)
                                rostero.setItem(fromjid, sname, ['bot-admins'])
                            else:
                                set_user_access(fromjid, 100)
                        else:
                            rostero.setItem(fromjid, sname, ['bot-users'])
                            set_user_access(fromjid, 11)
                        
                        set_fatal_var(cid, 'manual_usubscribe', 0)

def init_roster_subs_process():
    register_raw_iq_handler(handler_auto_subscribe)

def handler_list_roster(type, source, parameters):
    cid = get_client_id()
    
    rostero = get_fatal_var(cid, 'roster')
    rstjds = rostero.getItems()

    fjwg = [li for li in rstjds if not is_groupchat(li) and cid != li]

    if parameters:
        jid = parameters.strip()

        if not jid in fjwg:
            return reply(type, source, l('Not found!'))

        fjwg = [jid]

    usrlst = []

    for jdi in fjwg:
        usrln = l('User: %s\n     \Group(s): %s\n     \Subscription: %s\n     \Status: %s\n     \Access: %s\n')
        name = rostero.getName(jdi)
        groups = rostero.getGroups(jdi)
        show = rostero.getShow(jdi)
        status = rostero.getStatus(jdi)
        resrcs = rostero.getResources(jdi)
        access = user_level(jdi)

        if resrcs:
            usrln = l('User: %s\n     \Group(s): %s\n     \Subscription: %s\n     \Status: %s\n     \Resources: %s\n     \Access: %s\n')

        if not is_ruser_prsnt(jdi):
            status = 'offline'
        else:
            if show == None:
                show = 'online'
            
            if status != None:
                status = '%s <%s>' % (show, status)
            else:
                status = show

        if name != None:
            user = '%s <%s>' % (name, jdi)
        else:
            user = jdi

        if groups:
            grpln = ', '.join(groups)
        else:
            grpln = l('None')

        subs = rostero.getSubscription(jdi)
        
        if resrcs:
            resrcs = ', '.join(resrcs)
            usrlst.append(usrln % (user, grpln, subs, status, resrcs, access))
        else:    
            usrlst.append(usrln % (user, grpln, subs, status, access))

    nusrls = get_num_list(usrlst)

    rep = l('Roster users (total: %s):\n\n%s') % (len(nusrls), '\n'.join(nusrls))
    
    if type == 'public':
        reply(type, source, l('Look in private!'))

    if type in ('console', 'null', 'telegram'):
        return reply(type, source, rep.strip())
    else:
        return reply('private', source, rep.strip())

register_stage2_init(init_roster_subs_process)

register_command_handler(handler_subscribe, 'subscribe', 100)
register_command_handler(handler_usubscribe, 'usubscribe', 100)
register_command_handler(handler_list_roster, 'roster', 100)
