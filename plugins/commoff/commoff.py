# -*- coding: utf-8 -*-

#  fatal plugin
#  commoff plugin

#  Initial Copyright © 2007 Als <Als@exploit.in>
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

def get_commoff_list(gch):
    commoff_list = get_gch_param(gch, 'commoff', '')
    commoff_list = str_to_list(commoff_list)
    return commoff_list

def set_commoff_list(gch, commoff_list):
    commoff_list = list_to_str(commoff_list)
    set_gch_param(gch, 'commoff', commoff_list)

def handler_commoff(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    cprfx = get_comm_prefix(groupchat)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    na = ['access', 'eval', 'login', 'logout', 'gaccess_set', 'leave', 'restart', 'commands', 'commoff', 'common']
    
    valcomm, notvalcomm, alrcomm, npcomm, vcnt, ncnt, acnt, nocnt, rep, commoff = '', '', '', '', 0, 0, 0, 0, '', []
    
    if not is_var_set(cid, 'commoff', groupchat):
        get_commoff(groupchat)
    
    commoff = get_fatal_var(cid, 'commoff', groupchat)
    
    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        params = parameters.split()
        
        for comm in params:
            acomm = get_real_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            if is_var_set('commands', rcomm) or rcomm in aliaso.aliaslist[groupchat] or rcomm in aliaso.galiaslist:
                if not rcomm in na:
                    if not rcomm in commoff:
                        commoff.append(rcomm)
                        vcnt += 1
                        valcomm += '%s) %s%s\n' % (vcnt, cprfx, comm)
                    else:
                        acnt += 1
                        alrcomm += '%s) %s%s\n' % (acnt, cprfx, comm)
                else:
                    ncnt += 1
                    npcomm += '%s) %s%s\n' % (ncnt, cprfx, comm)
            else:
                nocnt += 1
                notvalcomm += '%s) %s%s\n' % (nocnt, cprfx, comm)
        
        if valcomm:
            rep += l('Following commands have been turned off for this groupchat (total: %s):\n\n%s') % (vcnt, valcomm)
        
        if alrcomm:
            rep += l('\nFollowing commands have not been turned off, because they are already turned off (total: %s):\n\n%s') % (acnt, alrcomm)
        
        if notvalcomm:
            rep += l('\nFollowing commands are not commands (total: %s):\n\n%s') % (nocnt, notvalcomm)
        
        if npcomm:
            rep += l("\nFollowing commands you can't turn off (total: %s):\n\n%s") % (ncnt, npcomm)
        
        if not param_exists(groupchat, 'commoff'):
            set_gch_param(groupchat, 'commoff', '')
            
        set_commoff_list(groupchat, commoff)
        get_commoff(groupchat)
    else:
        for comm in commoff:
            acomm = get_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            vcnt += 1
            valcomm += '%s) %s%s\n' % (vcnt, cprfx, rcomm)
            
        if valcomm:
            rep = l('Following commands are turned off in this groupchat (total: %s):\n\n%s') % (vcnt, valcomm)
        else:
            rep = l('All commands are turned on in this groupchat!')
        
    return reply(type, source, rep.strip())
        
def handler_common(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    cprfx = get_comm_prefix(groupchat)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
    
    na = ['access', 'eval', 'login', 'logout', 'gaccess_set', 'leave', 'restart', 'commands', 'commoff', 'common']

    valcomm, notvalcomm, alrcomm, npcomm, vcnt, ncnt, acnt, nocnt, rep, commoff = '', '', '', '', 0, 0, 0, 0, '', []
    
    if not is_var_set(cid, 'commoff', groupchat):
        get_commoff(groupchat)
        
    commoff = get_fatal_var(cid, 'commoff', groupchat)
    
    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        params = parameters.split()
        
        for comm in params:
            acomm = get_real_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            if is_var_set('commands', rcomm) or rcomm in aliaso.aliaslist[groupchat] or rcomm in aliaso.galiaslist:
                if not rcomm in na:
                    if rcomm in commoff:
                        commoff.remove(rcomm)
                        vcnt += 1
                        valcomm += '%s) %s%s\n' % (vcnt, cprfx, comm)
                    else:
                        acnt += 1
                        alrcomm += '%s) %s%s\n' % (acnt, cprfx, comm)
                else:
                    ncnt += 1
                    npcomm += '%s) %s%s\n' % (ncnt, cprfx, comm)
            else:
                nocnt += 1
                notvalcomm += '%s) %s%s\n' % (nocnt, cprfx, comm)
                
        if valcomm:
            rep += l('Following commands have been turned on for this groupchat (total: %s):\n\n%s') % (vcnt, valcomm)
        
        if alrcomm:
            rep += l('\nFollowing commands have not been turned on, because they are already turned on (total: %s):\n\n%s') % (acnt, alrcomm)
        
        if notvalcomm:
            rep += l('\nFollowing commands are not commands (total: %s):\n\n%s') % (nocnt, notvalcomm)
        
        if npcomm:
            rep += l("\nFollowing commands you can't turn off (total: %s):\n\n%s") % (ncnt, npcomm)
        
        if not param_exists(groupchat, 'commoff'):
            set_gch_param(groupchat, 'commoff', '')
            
        set_commoff_list(groupchat, commoff)
        get_commoff(groupchat)
    else:
        rep = l('Invalid syntax!')
        
    return reply(type, source, rep.strip())
    
def get_commoff(gch):
    cid = get_client_id()
    
    if param_exists(gch, 'commoff'):
        commoff = get_commoff_list(gch)
        set_fatal_var(cid, 'commoff', gch, commoff)
    else:
        set_fatal_var(cid, 'commoff', gch, [])
    
register_command_handler(handler_commoff, 'commoff', 20)
register_command_handler(handler_common, 'common', 20)

register_stage1_init(get_commoff)
