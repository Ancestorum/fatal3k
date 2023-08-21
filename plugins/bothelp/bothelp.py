# -*- coding: utf-8 -*-

#  fatal plugin
#  help plugin

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Copyright © 2009-2013 Ancestors Soft

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

def rmv_help_info(cmd):
    cmd = cmd.replace('"', '&quot;')
    
    sql = "DELETE FROM help WHERE command='%s';" % (cmd)
    
    cid = get_client_id()
    
    qres = sqlquery('dynamic/%s/help.db' % (cid), sql)
    
    return qres

def get_help_list(cmd, toi='ccat'):
    if not toi in ['ccat', 'exam']:
        toi = 'ccat'

    strng = get_help_info(cmd, toi)
    ilist = str_to_list(strng, '&comma;')
    
    return ilist

def set_help_list(cmd, lst, toi='ccat'):
    if not toi in ['ccat', 'exam']:
        toi = 'ccat'
    
    strng = list_to_str(lst, '&comma;')
    res = set_help_info(cmd, strng, toi)
    
    return res
    
def help_info_exists(cmd):
    cmd = cmd.replace('"', '&quot;')

    cid = get_client_id()
    
    sql = "SELECT * FROM help WHERE command='%s';" % (cmd)
    qres = sqlquery('dynamic/%s/help.db' % (cid), sql)
    
    if qres:
        return True
    return False

def get_help_info(cmd, toi='desc'):
    lc = get_param('locale', 'en')

    if not toi in ['ccat', 'desc', 'synt', 'exam']:
        toi = 'desc'
    
    cmd = cmd.replace('"', '&quot;')

    sql = "SELECT %s FROM help WHERE command='%s';" % (toi, cmd)
    
    cid = get_client_id()
    
    qdyn = sqlquery('dynamic/%s/help.db' % (cid), sql)
    qs = get_help_sect(cmd, toi)

    if qdyn and qs:
        qd = qdyn[0][0]
        
        if toi in ['ccat', 'exam']:
            ced = []
            ces = []
                
            if qd:
                ced = str_to_list(qd, '&comma;')
            
            ces = list(qs)

            ced.extend(ces)
            
            info = ''
            
            if ced:
                ced = sort_list_dist(ced)
                
                info = list_to_str(ced, '&comma;')
                info = info.replace('&quot;', '"')
                
            return info
        else:
            info = ''
            
            if qd:
                info = qd.replace('&quot;', '"')
                
                return info
            
            return '&comma;'.join(qs)
    elif qdyn and not qs:
        qd = qdyn[0][0]
        
        info = ''
        
        if qd:
            info = qd.replace('&quot;', '"')
            
            return info
        
        return info
    elif not qdyn and qs:       
        return '&comma;'.join(qs)
    
    return ''

def set_help_info(cmd, info, toi='desc'):
    if not toi in ['ccat', 'desc', 'synt', 'exam']:
        toi = 'desc'
    
    cmd = cmd.replace('"', '&quot;')
    info = info.replace('"', '&quot;')
    
    if not help_info_exists(cmd):
        sql = "INSERT INTO help (command, %s) VALUES ('%s', '%s');" % (toi.strip(), cmd.strip(), info.strip())
    else:
        sql = "UPDATE help SET \"%s\"='%s' WHERE command='%s';" % (toi.strip(), info.strip(), cmd.strip())
    
    cid = get_client_id()
    
    qres = sqlquery('dynamic/%s/help.db' % (cid), sql)
    
    return qres

def get_help_total_info(toi='ccat'):
    if not toi in ['ccat', 'exam']:
        toi = 'ccat'
    
    totli = []
    
    cmds = list(get_dict_fatal_var('commands'))
    
    for comm in cmds:
        heli = get_help_list(comm)
        
        if heli:
            totli.extend(heli)
    
    totli = sort_list_dist(totli)
    
    return totli

def get_help_cat_comms(cat):
    catcomms = []
    
    cmds = list(get_dict_fatal_var('commands'))
    
    for comm in cmds:
        cats = get_help_list(comm)
        
        if cat in cats:
            catcomms.append(comm)
    
    return catcomms

def handler_help_del(type, source, parameters):
    if parameters:
        comm = parameters.strip()
        
        comms = list(get_dict_fatal_var('commands'))
        
        if cmd_name_exists(comm):
            comm = ''
        
        acomm = get_real_cmd_name(comm)
        rcomm = comm
        
        if acomm:
            rcomm = acomm
        
        if rcomm in comms:
            if not help_info_exists(rcomm):
                rep = l('User-defined help for "%s" not found!') % (comm)
                return reply(type, source, rep)
            
            rmv_help_info(rcomm)
            
            if not help_info_exists(rcomm):
                rep = l('User-defined help for "%s" has been removed!') % (comm)
            else:
                rep = l('Delete error!')
            
            return reply(type, source, rep)
        else:
            return reply(type, source, l('Unknown command!'))
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_help_cat(type, source, parameters):
    groupchat = source[1]
    
    if parameters:
        cprfx = get_comm_prefix()
        splp = safe_split(parameters)
        cdel = splp[0].split()
        
        if len(cdel) > 1 and not splp[1]:
            if len(cdel) == 2:
                comm = cdel[0].strip()
                dnum = cdel[1].strip()
                pcomm = cprfx + comm
                
                if cmd_name_exists(comm):
                    comm = ''
                
                acomm = get_real_cmd_name(comm)
                
                if acomm:
                    comm = acomm
                
                if '-' in dnum[0] and dnum[1:].isdigit():
                    lidnum = int(dnum[1:])
                    
                    cats = get_help_list(comm)
                    
                    if not cats:
                        rep = l('List of categories for "%s" is empty!') % (pcomm.strip())
                        return reply(type, source, rep)
                    
                    cats.sort()
                    
                    if lidnum <= len(cats) and lidnum != 0:
                        dcat = cats.pop(lidnum - 1)
                        
                        res = set_help_list(comm, cats)
                        
                        if res == '':
                            rep = l('Unable to remove command "%s" from category "%s"!') % (pcomm.strip(), dcat.strip())
                            return reply(type, source, rep)
                        
                        if cats:
                            rep = l('Command "%s" has been removed from category "%s"!') % (pcomm.strip(), dcat.strip())
                            return reply(type, source, rep)
                        else:
                            rep = l('List of categories for "%s" has been cleared!') % (pcomm.strip())
                            return reply(type, source, rep)
                    else:
                        return reply(type, source, l('Invalid number!'))
                elif '-' in dnum[0] and not dnum[1:]:
                    cats = []
                    res = set_help_list(comm, cats)
                    
                    if res != '':
                        rep = l('List of categories for "%s" has been cleared!') % (pcomm.strip())
                        return reply(type, source, rep)
                    else:
                        rep = l('Unable to clear list of categories for "%s"!') % (pcomm.strip())
                        return reply(type, source, rep)
                else:
                    return reply(type, source, l('Invalid syntax!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
            return
        
        spltdp = rmv_empty_items(splp)
        
        if len(spltdp) == 1:
            comm = spltdp[0]
            pcomm = cprfx + comm
            
            if cmd_name_exists(comm):
                comm = ''
            
            acomm = get_real_cmd_name(comm)
            
            if acomm:
                comm = acomm
            
            if is_var_set('commands', comm):
                cats = get_help_list(comm)
                    
                if cats:
                    cats.sort()
                    cats = get_num_list(cats)
                    rep = l('List of categories for "%s" (total %s):\n\n%s') % (pcomm.strip(), len(cats), '\n'.join(cats))
                else:
                    rep = l('List of categories for "%s" is empty!') % (pcomm.strip())
                    
                return reply(type, source, rep)
            else:
                return reply(type, source, l('Unknown command!'))
        else:
            comm = spltdp[0]
            pcomm = cprfx + comm
            
            if cmd_name_exists(comm):
                comm = ''
            
            acomm = get_real_cmd_name(comm)
            
            if acomm:
                comm = acomm
            
            if is_var_set('commands', comm):
                if ',' in spltdp[1]:
                    return reply(type, source, l('Invalid syntax!'))
                
                extli = spltdp[1].split()
                cats = get_help_list(comm)
                fextli = [feli for feli in extli if not feli in cats]
                cats.extend(fextli)
                
                res = set_help_list(comm, cats)
                
                if fextli and res != '':
                    rep = l('Command "%s" has been added in new categories (total %s):\n\n%s.') % (pcomm.strip(), len(fextli), ', '.join(fextli))
                else:
                    rep = l('Command "%s" has not been added in new categories!') % (pcomm.strip())
                    
                return reply(type, source, rep)
            else:
                return reply(type, source, l('Unknown command!'))
    else:
        cats = get_help_total_info()
        
        if cats:
            rep = l('Full list of command categories (total %s):\n\n%s.') % (len(cats), ', '.join(cats))
        else:
            rep = l('List of command categories is empty!')
        
        return reply(type, source, rep)

def handler_help_ex(type, source, parameters):
    groupchat = source[1]
    
    if parameters:
        cprfx = get_comm_prefix(groupchat)
        splp = safe_split(parameters)
        cdel = splp[0].split()
        
        if len(cdel) > 1 and not splp[1]:
            if len(cdel) == 2:
                comm = cdel[0].strip()
                dnum = cdel[1].strip()
                pcomm = cprfx + comm
                
                if cmd_name_exists(comm):
                    comm = ''
                
                acomm = get_real_cmd_name(comm)
                
                if acomm:
                    comm = acomm
                
                if '-' in dnum[0] and dnum[1:].isdigit():
                    lidnum = int(dnum[1:])
                    
                    exs = get_help_list(comm, 'exam')
                    
                    if not exs:
                        rep = l('List of examples for "%s" is empty!') % (pcomm.strip())
                        return reply(type, source, rep)
                    
                    exs.sort()
                    
                    if lidnum <= len(exs) and lidnum != 0:
                        exs.pop(lidnum - 1)
                        
                        res = set_help_list(comm, exs, 'exam')
                        
                        if res == '':
                            rep = l('Unable to remove example for "%s"!') % (pcomm.strip())
                            return reply(type, source, rep)
                        
                        if exs:
                            rep = l('Example for "%s" has been removed!') % (pcomm.strip())
                            return reply(type, source, rep)
                        else:
                            rep = l('List of examples for "%s" has been cleared!') % (pcomm.strip())
                            return reply(type, source, rep)
                    else:
                        return reply(type, source, l('Invalid number!'))
                elif '-' in dnum[0] and not dnum[1:]:
                    exs = []
                    res = set_help_list(comm, exs, 'exam')
                    
                    if res != '':
                        rep = l('List of examples for "%s" has been cleared!') % (pcomm.strip())
                        return reply(type, source, rep)
                    else:
                        rep = l('Unable to clear list of examples for "%s"!') % (pcomm.strip())
                        return reply(type, source, rep)
                else:
                    return reply(type, source, l('Invalid syntax!'))
            else:
                return reply(type, source, l('Invalid syntax!'))
            return
        
        spltdp = [fspli for fspli in splp if fspli]
        
        if len(spltdp) == 1:
            comm = spltdp[0]
            pcomm = cprfx + comm
            
            if cmd_name_exists(comm):
                comm = ''
            
            acomm = get_real_cmd_name(comm)
            
            if acomm:
                comm = acomm
            
            if is_var_set('commands', comm):
                exs = get_help_list(comm, 'exam')
                
                if exs:
                    exs.sort()
                    exs = get_num_list(exs)
                    rep = l('List of examples for "%s" (total %s):\n\n%s') % (pcomm.strip(), len(exs), '\n'.join(exs))
                    rep = rep.replace('%prefix%', cprfx)
                else:
                    rep = l('List of examples for "%s" is empty!') % (pcomm.strip())
                    
                return reply(type, source, rep)
            else:
                return reply(type, source, l('Unknown command!'))
        else:
            comm = spltdp[0]
            pcomm = cprfx + comm
            
            if cmd_name_exists(comm):
                comm = ''
            
            acomm = get_real_cmd_name(comm)
            
            if acomm:
                comm = acomm
            
            if is_var_set('commands', comm):
                extstr = spltdp[1]
                exs = get_help_list(comm, 'exam')
                
                if extstr in exs: 
                    extstr = ''
                
                if extstr: 
                    exs.append(extstr)
                
                res = set_help_list(comm, exs, 'exam')
                    
                if extstr and res != '':
                    rep = l('New example for "%s" has been added!') % (pcomm.strip())
                else:
                    rep = l('New example for "%s" has not been added!') % (pcomm.strip())
                    
                return reply(type, source, rep)
            else:
                return reply(type, source, l('Unknown command!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_help_syn(type, source, parameters):
    groupchat = source[1]
    
    if parameters:
        cprfx = get_comm_prefix(groupchat)
        splp = safe_split(parameters)
        cdel = splp[0].split()
        
        if len(cdel) > 1:
            return reply(type, source, l('Invalid syntax!'))
        
        spltdp = rmv_empty_items(splp)
        
        if len(spltdp) == 1:
            comm = spltdp[0]
            pcomm = cprfx + comm
            
            if cmd_name_exists(comm):
                comm = ''
            
            acomm = get_real_cmd_name(comm)
            
            if acomm:
                comm = acomm
            
            if is_var_set('commands', comm):
                syn = get_help_info(comm, 'synt')
                
                if syn:
                    rep = l('Command syntax for "%s": %s') % (pcomm.strip(), syn.strip())
                    rep = rep.replace('%prefix%', cprfx)
                else:
                    rep = l('Command syntax for "%s" has not been set yet!') % (pcomm.strip())
                
                return reply(type, source, rep)
            else:
                return reply(type, source, l('Unknown command!'))
        else:
            comm = spltdp[0]
            pcomm = cprfx + comm
            
            if cmd_name_exists(comm):
                comm = ''
            
            acomm = get_real_cmd_name(comm)
            
            if acomm:
                comm = acomm
            
            if is_var_set('commands', comm):
                synstr = spltdp[1].strip()
                
                res = set_help_info(comm, synstr, 'synt')
                
                if res != '':
                    rep = l('Command syntax for "%s" has been set!') % (pcomm.strip())
                else:
                    rep = l('Command syntax for "%s" has not been set!') % (pcomm.strip())
                    
                return reply(type, source, rep)
            else:
                return reply(type, source, l('Unknown command!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
        
def handler_help_desc(type, source, parameters):
    groupchat = source[1]
    
    if parameters:
        cprfx = get_comm_prefix(groupchat)
        splp = safe_split(parameters)
        cdel = splp[0].split()
        
        if len(cdel) > 1:
            return reply(type, source, l('Invalid syntax!'))
        
        spltdp = rmv_empty_items(splp)
        
        if len(spltdp) == 1:
            comm = spltdp[0]
            pcomm = cprfx + comm
            
            if cmd_name_exists(comm):
                comm = ''
            
            acomm = get_real_cmd_name(comm)
            
            if acomm:
                comm = acomm
            
            if is_var_set('commands', comm):
                desc = get_help_info(comm, 'desc')
                    
                if desc:
                    rep = l('Description for "%s": %s') % (pcomm.strip(), desc.strip())
                    rep = rep.replace('%prefix%', cprfx)
                else:
                    rep = l('Description for "%s" has not been set yet!') % (pcomm.strip())
                    
                return reply(type, source, rep)
            else:
                return reply(type, source, l('Unknown command!'))
        else:
            comm = spltdp[0]
            pcomm = cprfx + comm
            
            if cmd_name_exists(comm):
                comm = ''
            
            acomm = get_real_cmd_name(comm)
            
            if acomm:
                comm = acomm
            
            if is_var_set('commands', comm):
                desc = spltdp[1].strip()
                
                res = set_help_info(comm, desc, 'desc')
                    
                if res != '':
                    rep = l('Description for "%s" has been set!') % (pcomm.strip())
                else:
                    rep = l('Description for "%s" has not been set!') % (pcomm.strip())
                    
                return reply(type, source, rep)
            else:
                return reply(type, source, l('Unknown command!'))
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_help_help(type, source, parameters):
    groupchat = source[1]
    cprfx = get_comm_prefix(groupchat)
    
    comm = parameters.strip()
    acomm = get_real_cmd_name(comm)
    rcomm = comm
    
    if acomm:
        rcomm = acomm
    
    if cmd_name_exists(comm):
        rcomm = ''
    
    if parameters and is_var_set('commands', rcomm):  
        desc = get_help_sect(rcomm, 'desc')

        if not desc:
            desc = get_help_info(rcomm, 'desc')

        desc = desc.replace('%prefix%', cprfx)
        
        cats = get_help_sect(rcomm, 'ccat')

        if not cats:
            cats = get_help_list(rcomm)

        syn = get_help_sect(rcomm, 'synt')

        if not syn:
            syn = get_help_info(rcomm, 'synt')

        syn = syn.replace('%prefix%', cprfx)
        
        exs = get_help_sect(rcomm, 'exam')

        if not exs:
            exs = get_help_list(rcomm, 'exam')

        exs = [exli.replace('%prefix%', cprfx) for exli in exs]
        
        cacc = get_int_fatal_var('commands', rcomm, 'access')
        
        racc = int(get_cmd_access(rcomm))
        
        if racc < 0:
            racc = cacc
        
        if not desc:
            return reply(type, source, l('Help not found!'))
        
        if acomm:
            syn = syn.replace(rcomm, comm)
            exs = [exli.replace(rcomm, comm) for exli in exs]
            exs.sort()
        
        rep = '%s\n' % (desc)

        if cats:
            rep += l('Categories: %s.\n') % (', '.join(cats))
        
        if syn:
            rep += l('Syntax: %s\n') % (syn)
        
        if exs:
            rep += l('Examples:\n  >  %s\n') % ('\n  >  '.join(exs))
        
        rep += l('Required access: %s') % (racc)
        
        if is_groupchat(groupchat):
            if is_var_set('commoff', groupchat, rcomm):
                rep += l('\n\nCommand is turned off in this groupchat!')
    else:
        comm_comm = get_cmd_name('commands')
        help_comm = get_cmd_name('help')
        alias_list_comm = get_cmd_name('alias_list')
        alias_acc_comm = get_cmd_name('alias_acc')
        galias_acc_comm = get_cmd_name('galias_acc')
        
        if not comm_comm:
            comm_comm = 'commands'
        if not help_comm:
            help_comm = 'help'
        if not alias_list_comm:
            alias_list_comm = 'alias_list'
        if not alias_acc_comm:
            alias_acc_comm = 'alias_acc'
        if not galias_acc_comm:
            galias_acc_comm = 'galias_acc'
        
        rep = l('Type "%s%s" (without quotes), to get list of commands, "%s%s <command without prefix>" to get help for command, "%s%s" to get list of aliases, and also "%s%s <alias>" to get access level for local alias and "%s%s" to get access level for global alias.') % (cprfx, comm_comm, cprfx, help_comm, cprfx, alias_list_comm, cprfx, alias_acc_comm, cprfx, galias_acc_comm)
                
    return reply(type, source, rep)

def handler_help_commands(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    cprfx = get_comm_prefix(groupchat)
    parameters = parameters.strip()
    
    if parameters:
        rep, dsbl = [], []
        total = 0
        
        catcom = get_help_cat_comms(parameters)
        
        if not catcom:
            return reply(type, source, l('Unknown category!'))
        
        for cat in catcom:
            cacc = get_int_fatal_var('commands', cat, 'access')
            
            racc = int(get_cmd_access(cat))
            
            if racc < 0:
                racc = cacc
            
            cname = get_cmd_name(cat)
            pcname = cprfx + cname
            
            if not cname:
                pcname = cprfx + cat
            
            if has_access(source, racc, groupchat) or type in ['console', 'telegram']:
                if is_var_set(cid, 'commoff', groupchat):
                    if is_var_set(cid, 'commoff', groupchat, cat):
                        dsbl.append(pcname)
                    else:
                        rep.append(pcname)
                        total += 1
                else:
                    rep.append(pcname)
                    total += 1
        
        if rep:
            if type == 'public':
                reply(type, source, l('Look in private!'))
                
            rep.sort()
            answ = l('List of commands in category "%s" (total: %s):\n\n%s.') % (parameters, total, ', '.join(rep))
            
            if dsbl:
                dsbl.sort()
                answ += l('\n\nFollowing commands are turned off in this groupchat (total: %s):\n\n%s.') % (len(dsbl), ', '.join(dsbl))
                
            if type in ['console', 'telegram']:
                return reply(type, source, answ)
            else:
                return reply('private', source, answ)
        else:
            return reply(type, source, l('Too few rights!'))
    else:
        cats = get_help_total_info()
            
        qcats = len(cats)
        cats = ', '.join(cats)
        
        if type == 'public':
            reply(type, source, l('Look in private!'))
            
        comm_comm = get_cmd_name('commands')
        
        if not comm_comm:
            comm_comm = 'commands'
            
        rep = l('List of categories (total: %s):\n\n%s.\n\nTo view list of commands in category type "%s%s <category>" without quotes, for example "%s%s *"') % (qcats, cats, cprfx, comm_comm, cprfx, comm_comm)

        if type in ['console', 'telegram']:
            return reply(type, source, rep)
        else:
            return reply('private', source, rep)
        
def init_help_db():
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/help.db' % (cid)):
        sql = 'CREATE TABLE help (command VARCHAR NOT NULL, ccat VARCHAR, desc VARCHAR, synt VARCHAR, exam VARCHAR, UNIQUE(command));'
        sqlquery('dynamic/%s/help.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX ihelp ON help (command);'
        sqlquery('dynamic/%s/help.db' % (cid), sql)

register_command_handler(handler_help_help, 'help')
register_command_handler(handler_help_commands, 'commands')
register_command_handler(handler_help_cat, 'help_cat', 100)
register_command_handler(handler_help_ex, 'help_ex', 100)
register_command_handler(handler_help_syn, 'help_syn', 100)
register_command_handler(handler_help_desc, 'help_desc', 100)
register_command_handler(handler_help_del, 'help_del', 100)

register_stage2_init(init_help_db)
