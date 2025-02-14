# -*- coding: utf-8 -*-

#  fatal plugin
#  aliases plugin

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
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

def handler_aliasadd(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    cprfx = get_comm_prefix(groupchat)

    access = 0
    
    spltdp = parameters.split('=', 1)
    
    if len(spltdp) == 2:
        alac = spltdp[0].strip()
        albo = spltdp[1].strip()
        
        splal = alac.split(':', 1)
        
        if len(splal) == 2:
            ali = splal[0].strip()
            acc = splal[1].strip()
            
            if acc:
                if acc.isdigit():
                    access = int(acc)
                    
                    if access > 100:
                        access = 100
                else:
                    ali = '%s:%s' % (ali, acc)
                    
            parameters = '%s = %s' % (ali, albo)
            
    aliaso = get_fatal_var(cid, 'alias')
    pl = aliaso.parse_cmd(parameters)
    
    if (len(pl) < 2):
        rep = l('Invalid syntax!')
    else:
        alnm = pl[0]
        cmal = pl[1].split()[0]
        
        if alnm.startswith(cprfx):
            alnm = alnm.replace(cprfx, '', 1)
        
        ralnm = get_real_cmd_name(alnm)
        
        if not ralnm:
            ralnm = alnm
        
        if get_fatal_var('command_handlers', ralnm):
            return reply(type, source, l('Invalid name for local alias!'))
        
        if cmd_name_exists(cmal):
            cmal = ''
        
        rcmal = get_real_cmd_name(cmal)
        
        if not rcmal:
            rcmal = cmal
        
        if is_var_set('command_handlers', rcmal) or rcmal in aliaso.galiaslist or rcmal in aliaso.aliaslist[groupchat]:
            command = pl[1].split(' ', 1)
            aliaso.add(pl[0], pl[1], groupchat)
            
            if access:
                aliaso.give_access(pl[0], access, groupchat)
            else:
                if is_var_set('command_handlers', command[0]):
                    cacc = get_int_fatal_var('commands', command[0], 'access')
                    
                    racc = int(get_cmd_access(command[0]))
                    
                    if racc < 0:
                        racc = cacc
                    
                    aliaso.give_access(pl[0], racc, groupchat)
                elif command[0] in aliaso.gaccesslist:
                    access = aliaso.gaccesslist[command[0]]
                    aliaso.give_access(pl[0], access, groupchat)
                elif command[0] in aliaso.accesslist[groupchat]:
                    access = aliaso.accesslist[groupchat][command[0]]
                    aliaso.give_access(pl[0], access, groupchat)
    
            rep = l('Local alias has been added!')
        else:
            rep = l("Alias body doesn't contain a command or another alias!")
    return reply(type, source, rep)
    
def handler_galiasadd(type, source, parameters):
    cid = get_client_id()
    
    gch_jid = source[1]
    
    gaccess = 0
    
    cprfx = get_comm_prefix(gch_jid)
    
    spltdp = parameters.split('=', 1)
    
    if len(spltdp) == 2:
        alac = spltdp[0].strip()
        albo = spltdp[1].strip()
        
        splal = alac.split(':', 1)
        
        if len(splal) == 2:
            ali = splal[0].strip()
            acc = splal[1].strip()
            
            if acc:
                if acc.isdigit():
                    gaccess = int(acc)
                    
                    if gaccess > 100:
                        gaccess = 100
                else:
                    ali = '%s:%s' % (ali, acc)
                    
            parameters = '%s = %s' % (ali, albo)
    
    aliaso = get_fatal_var(cid, 'alias')
    
    #pl = aliaso.parse_cmd(parameters)
    pl = spltdp
    
    if len(pl) < 2:
        rep = l('Invalid syntax!')
    else:
        alnm = pl[0]
        cmal = pl[1].split()[0]
        
        if alnm.startswith(cprfx):
            alnm = alnm.replace(cprfx, '', 1)
        
        ralnm = get_real_cmd_name(alnm)
        
        if not ralnm:
            ralnm = alnm        
        
        if is_var_set('command_handlers', ralnm):
            return reply(type, source, l('Invalid name for global alias!'))
        
        if cmd_name_exists(cmal):
            cmal = ''
        
        rcmal = get_real_cmd_name(cmal)
        
        if not rcmal:
            rcmal = cmal
        
        if is_var_set('command_handlers', rcmal) or rcmal in aliaso.galiaslist:
            command = pl[1].split(' ')
            aliaso.add(pl[0], pl[1])
            
            if gaccess:
                aliaso.give_access(pl[0], gaccess)
            else:
                if is_var_set('command_handlers', command[0]):
                    cacc = get_int_fatal_var('commands', command[0], 'access')
                    
                    racc = int(get_cmd_access(command[0]))
                    
                    if racc < 0:
                        racc = cacc
                    
                    aliaso.give_access(pl[0], racc)
                elif command[0] in aliaso.gaccesslist:
                    gaccess = aliaso.gaccesslist[command[0]]
                    aliaso.give_access(pl[0], gaccess)
            
            rep = l('Global alias has been added!')
        else:
            rep = l("Alias body doesn't contain a command or another alias!")
    return reply(type, source, rep)

def handler_aliasdel(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
    
    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        alias = parameters.strip()
        
        if alias in aliaso.aliaslist[groupchat]:
            res = aliaso.remove(alias, groupchat)
            aliaso.remove_access(alias, groupchat)
            
            if res == False:
                rep = l('Local alias has been removed!')
            else:
                rep = l('Delete error!')
        else:
            rep = l('Alias not found!')
    else:
        rep = l('Invalid syntax!')
    return reply(type, source, rep)
    
def handler_galiasdel(type, source, parameters):
    cid = get_client_id()
    
    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        alias = parameters.strip()
        
        if alias in aliaso.galiaslist:
            res = aliaso.remove(parameters)
            aliaso.remove_access(parameters)
            
            if res == False:
                rep = l('Global alias has been removed!')
            else:
                rep = l('Delete error!')
        else:
            rep = l('Alias not found!')
    else:
        rep = l('Invalid syntax!')
    return reply(type, source, rep)

def handler_aliasexpand(type, source, parameters):
    cid = get_client_id()
    
    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        alias = parameters.strip()
        alexp = aliaso.comexp(parameters, source)
        rep = '%s = %s' % (alias, alexp)
    else:
        rep = l('Invalid syntax!')
    return reply(type, source, rep)
    
def handler_galiasexpand(type, source, parameters):
    cid = get_client_id()
    
    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        galias = parameters.strip()
        galexp = aliaso.comexp(galias, source, '1')
        rep = '%s = %s' % (galias, galexp)
    else:
        rep = l('Invalid syntax!')
    return reply(type, source, rep)

def handler_aliasshow(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
    
    rep = ''
    aliaso = get_fatal_var(cid, 'alias')
    
    if parameters:
        if parameters in aliaso.aliaslist[groupchat]:
            rep = '%s = %s' % (parameters, aliaso.aliaslist[groupchat][parameters])
        else:
            rep = l('Alias not found!')
    else:
        lals = list(aliaso.aliaslist[groupchat].keys())
        
        if lals:
            rep = l('List of local aliases (total: %s):\n\n') % (len(lals))
            
            for la in lals:
                rep += '%d) %s = %s\n' % (lals.index(la) + 1, la, aliaso.aliaslist[groupchat][la])
        else:
            rep = l('List of local aliases is empty!')
            
    return reply(type, source, rep.strip())
    
def handler_galiasshow(type, source, parameters):
    cid = get_client_id()
    
    rep = ''
    
    aliaso = get_fatal_var(cid, 'alias')
    
    if parameters:
        if parameters in aliaso.galiaslist:
            rep = '%s = %s' % (parameters, aliaso.galiaslist[parameters])
        else:
            rep = l('Alias not found!')
    else:
        gals = list(aliaso.galiaslist.keys())
        
        if gals:
            rep = l('List of global aliases (total: %s):\n\n') % (len(gals))
            
            for ga in gals:
                rep += '%d) %s = %s\n' % (gals.index(ga) + 1, ga, aliaso.galiaslist[ga])
        else:
            rep = l('List of global aliases is empty!')

    return reply(type, source, rep.strip())
    
def handler_aliaslist(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    is_gch = True
    
    if not is_groupchat(groupchat):
        is_gch = False
    
    aliaso = get_fatal_var(cid, 'alias')
    
    rep, dsbll, dsblg, glist, llist = l('List of aliases:\n'), [], [], [], []
    tglist = list(aliaso.galiaslist.keys())
    
    if is_gch:
        if aliaso.aliaslist[groupchat]:
            for alias in list(aliaso.aliaslist[groupchat].keys()):
                if is_var_set(cid, 'commoff', groupchat, alias):
                    dsbll.append(alias)
                else:
                    llist.append(alias)
                    
            dsbll.sort()
            llist.sort()
            
            if llist:
                rep += l('\nLocal (total: %s):\n%s.\n') % (len(llist), ', '.join(llist))
                
            if dsbll:
                rep += l('\n\Following local aliases is currently turned off in this groupchat (total: %s):\n%s.\n') % (len(dsbll), ', '.join(dsbll))
        else:
            rep += ''
        
        for alias in tglist:
            if is_var_set(cid, 'commoff', groupchat, alias):
                dsblg.append(alias)
            else:
                glist.append(alias)
                
        dsblg.sort()
        glist.sort()
    else:
        dsblg = []
        tglist.sort()
        glist = tglist
    
    if glist:
        rep += l('\nGlobal (total: %s):\n%s.') % (len(glist), ', '.join(glist))
    else:
        rep += ''
    
    if dsblg:
        rep += l('\n\n\Following global aliases is currently turned off in this groupchat (total: %s):\n\n%s.') % (len(dsblg), ', '.join(dsblg))

    if type == 'public':
        reply(type, source, l('Look in private!'))

    if glist or llist:
        if type == 'console':
            return reply(type, source, rep.strip())
        else:
            return reply('private', source, rep.strip())
    elif not glist and not llist:
        rep = l('List of aliases is empty!')
        if type == 'console':
            return reply(type, source, rep.strip())
        else:
            return reply('private', source, rep.strip())
    
def handler_aliasaccess(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        args, access = parameters.split(' '), 10
        if len(args) == 2:
            alias = args[0].strip()
            access = args[1].strip()
            
            if access.isdigit():
                access = int(access)
            else:
                return reply(type, source, l('Invalid syntax!'))
            
            aliaso.give_access(alias, access, groupchat)
            rep = l('Access level to use local alias "%s" has been set to %s.') % (alias, access)
            return reply(type, source, rep)
        elif args[0] in aliaso.accesslist[groupchat]:
            alias = args[0]
            access = aliaso.accesslist[groupchat][alias]
            rep = l('Access level to use local alias "%s": %s.') % (alias, access)
            return reply(type, source, rep)
        elif not args[0] in aliaso.accesslist[groupchat]:
            return reply(type, source, l('Alias not found!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
            
def handler_galiasaccess(type, source, parameters):
    cid = get_client_id()
    
    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        args = parameters.split(' ')
        if len(args) == 2:
            alias = args[0].strip()
            access = args[1].strip()
            
            if access.isdigit():
                access = int(access)
            else:
                return reply(type, source, l('Invalid syntax!'))
            
            aliaso.give_access(alias, access)
            rep = l('Access level to use global alias "%s" has been set to %s.') % (alias, access)
            return reply(type, source, rep)
        elif args[0] in aliaso.gaccesslist:
            alias = args[0]
            access = aliaso.gaccesslist[alias]
            rep = l('Access level to use global alias "%s": %s.') % (alias, access)
            return reply(type, source, rep)
        elif not args[0] in aliaso.gaccesslist:
            return reply(type, source, l('Alias not found!'))
    else:
        return reply(type, source, l('Invalid syntax!'))

register_command_handler(handler_aliasadd, 'alias_add', 20)
register_command_handler(handler_galiasadd, 'galias_add', 100)
register_command_handler(handler_aliasdel, 'alias_del', 20)
register_command_handler(handler_galiasdel, 'galias_del', 100)
register_command_handler(handler_aliasexpand, 'alias_exp', 20)
register_command_handler(handler_galiasexpand, 'galias_exp', 100)
register_command_handler(handler_aliasshow, 'alias_show', 20)
register_command_handler(handler_galiasshow, 'galias_show', 100)
register_command_handler(handler_aliaslist, 'alias_list', 10)
register_command_handler(handler_aliasaccess, 'alias_acc', 20)
register_command_handler(handler_galiasaccess, 'galias_acc', 100)
