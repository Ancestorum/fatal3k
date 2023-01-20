# -*- coding: utf-8 -*-

#  fatal plugin
#  admin plugin

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
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

def handler_remote(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    nick = source[2]

    groupchats = list(get_fatal_var(cid, 'gchrosters'))
    groupchats.sort()

    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        spltdp = parameters.split(' ', 2)
        dest_gch = spltdp[0]
        
        if len(spltdp) >= 2:
            dest_comm = spltdp[1]
        else:
            return reply(type, source, l('Invalid syntax!'))
        
        dest_params = ''
        
        if dest_gch.isdigit():
            if int(dest_gch) <= len(groupchats) and int(dest_gch) != 0:
                dest_gch = groupchats[int(dest_gch) - 1]
            else:
                return reply(type, source, l('Groupchat not found!'))
        else:
            if not dest_gch in groupchats:
                return reply(type, source, l('Groupchat not found!'))
        
        if len(spltdp) >= 3:
            dest_params = spltdp[2]
        
        bot_nick = get_bot_nick(dest_gch)
        
        dest_source = [groupchat + '/' + nick, dest_gch, bot_nick]
                
        acomm = get_real_cmd_name(dest_comm)
        dest_rcomm = dest_comm
        
        if acomm:
            dest_rcomm = acomm
        
        if cmd_name_exists(dest_comm):
            dest_rcomm = ''

        if is_var_set('command_handlers', dest_rcomm):
            comm_hnd = get_fatal_var('command_handlers', dest_rcomm)
        elif dest_rcomm in aliaso.aliaslist[dest_gch]:
            exp_alias = aliaso.expand(dest_rcomm, dest_source)
            
            spl_comm_par = exp_alias.split(' ', 1)
            dest_comm = spl_comm_par[0]
            
            if len(spl_comm_par) >= 2:
                alias_par = spl_comm_par[1]
                dest_params = '%s %s' % (alias_par, dest_params)
                dest_params = dest_params.strip()
            
            acomm = get_real_cmd_name(dest_comm)
            dest_rcomm = dest_comm
            
            if acomm:
                dest_rcomm = acomm
            
            if is_var_set('command_handlers', dest_rcomm):
                comm_hnd = get_fatal_var('command_handlers', dest_rcomm)
            else:
                return reply(type, source, l('Unknown command!'))
        elif dest_rcomm in aliaso.galiaslist:
            exp_alias = aliaso.expand(dest_rcomm, dest_source)
            
            spl_comm_par = exp_alias.split(' ', 1)
            dest_comm = spl_comm_par[0]
            
            if len(spl_comm_par) >= 2:
                alias_par = spl_comm_par[1]
                dest_params = '%s %s' % (alias_par, dest_params)
                dest_params = dest_params.strip()
            
            acomm = get_real_cmd_name(dest_comm)
            dest_rcomm = dest_comm
            
            if acomm:
                dest_rcomm = acomm
            
            if is_var_set('command_handlers', dest_rcomm):
                comm_hnd = get_fatal_var('command_handlers', dest_rcomm)
            else:
                return reply(type, source, l('Unknown command!'))
        else:
            return reply(type, source, l('Unknown command!'))
        
        if type == 'public':
            reply(type, source, l('Look in private!'))
            
        if type == 'console':
            return comm_hnd('console', dest_source, dest_params)
        else:
            return comm_hnd('private', dest_source, dest_params)
    else:
        gchli = get_num_list(groupchats)
        
        if gchli:
            rep = l('Available groupchats (total: %s):\n\n%s') % (len(gchli), '\n'.join(gchli))
        else:
            rep = l('There are no available groupchats!')
            
        return reply(type, source, rep)

def handler_redirect(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]
    nick = source[2]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if ':' in parameters:
            aliaso = get_fatal_var(cid, 'alias')
            spltdp = parameters.split(':', 1)
            dest_nick = spltdp[0]
            
            if len(spltdp) >= 2:
                mess = spltdp[1]
                comm_par = spltdp[1].strip()
                comm_par = comm_par.split(' ', 1)
                comm = comm_par[0].strip()
                params = ''
                
                if len(comm_par) >= 2:
                    params = comm_par[1].strip()
            else:
                return reply(type, source, l('Invalid syntax!'))
            
            bot_nick = get_bot_nick(groupchat)
            
            dest_source = [groupchat + '/' + dest_nick, groupchat, bot_nick]
            
            acomm = get_real_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            if cmd_name_exists(comm):
                rcomm = ''
            
            if is_var_set('command_handlers', rcomm):
                comm_hnd = get_fatal_var('command_handlers', rcomm)
            elif rcomm in aliaso.aliaslist[groupchat]:
                exp_alias = aliaso.expand(comm, dest_source)
                
                spl_comm_par = exp_alias.split(' ', 1)
                comm = spl_comm_par[0]
                
                if len(spl_comm_par) >= 2:
                    alias_par = spl_comm_par[1]
                    params = '%s %s' % (alias_par, params)
                    params = params.strip()
                
                acomm = get_real_cmd_name(comm)
                rcomm = comm
                
                if acomm:
                    rcomm = acomm
                
                if is_var_set('command_handlers', rcomm):
                    comm_hnd = get_fatal_var('command_handlers', rcomm)
                else:
                    rep = reply('private', [groupchat + '/' + dest_nick, groupchat, dest_nick], mess)
                    reply(type, source, l('Sent!'))
                    return rep
            elif comm in aliaso.galiaslist:
                exp_alias = aliaso.expand(comm, dest_source)
                
                spl_comm_par = exp_alias.split(' ', 1)
                comm = spl_comm_par[0]
                
                if len(spl_comm_par) >= 2:
                    alias_par = spl_comm_par[1]
                    params = '%s %s' % (alias_par, params)
                    params = params.strip()
                
                acomm = get_real_cmd_name(comm)
                rcomm = comm
                
                if acomm:
                    rcomm = acomm
                
                if is_var_set('command_handlers', rcomm):
                    comm_hnd = get_fatal_var('command_handlers', rcomm)
                else:
                    rep = reply('private', [groupchat + '/' + dest_nick, groupchat, dest_nick], mess)
                    reply(type, source, l('Sent!'))
                    return rep
            else:
                rep = reply('private', [groupchat + '/' + dest_nick, groupchat, dest_nick], mess)
                reply(type, source, l('Sent!'))
                return rep
            
            res = comm_hnd('private', dest_source, params)
            reply(type, source, l('Sent!'))
            return res
        else:
            return reply(type, source, l('Invalid syntax!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_set_nick(type, source, parameters):
    if parameters:
        groupchat = source[1]
        nick = parameters
        join_groupchat(groupchat, nick)
        return reply(type, source, l('Saved!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_admin_rejoin(type, source, parameters):
    cid = get_client_id()
    
    join_count = 0
    succ_join = 0
    fail_join = 0
    rejoin_rooms = []
    groupchats = get_chatrooms_list()
    aliaso = get_fatal_var(cid, 'alias')
    dnick = get_cfg_param('default_nick', 'fatal-bot')
    
    if not groupchats:
        return reply(type, source, l('There are no groupchats to rejoin!')) 

    for groupchat in groupchats:
        cprfx = get_comm_prefix(groupchat)
        stmsg = get_gch_param(groupchat, 'status_text', l('Type %shelp and follow instructions of the bot to understand how to work with me!') % (cprfx))
        status = get_gch_param(groupchat, 'status_show', 'online')

        add_gch_config(groupchat)
        aliaso.init(groupchat)
        
        call_stage1_init_handlers(groupchat)

        gch_nick = get_chatroom_info(groupchat, 'nick', dnick)
        gch_pass = get_chatroom_info(groupchat, 'pass')
        
        try:
            join_groupchat(groupchat, gch_nick, gch_pass)
            change_bot_status(groupchat, stmsg, status)

            join_count += 1
            succ_join += 1
            
            rejoin_rooms.append('+%d) %s' % (join_count, groupchat))
        except:
            join_count += 1
            fail_join += 1
            
            rejoin_rooms.append('-%d) %s' % (join_count, groupchat))

    rep = l('Rejoin groupchats (total: %s, successfull: %s, fail: %s):\n\n%s') % (join_count, succ_join, fail_join, '\n'.join(rejoin_rooms))
    return reply(type, source, rep.strip())

def handler_admin_join(type, source, parameters):
    cid = get_client_id()
    
    if parameters:
        aliaso = get_fatal_var(cid, 'alias')
        def_nick = get_cfg_param('default_nick')
        
        passw = ''
        
        args = parameters.split()
        
        if len(args) > 1:
            groupchat = args[0].lower()
            argstr = ' '.join(args[1:])
            passw_nick = safe_split(argstr)
            
            if not passw_nick[0]:
                bot_nick = def_nick
            else:
                bot_nick = passw_nick[0]
                
            passw = passw_nick[1]
        else:
            groupchat = parameters.lower()
            bot_nick = ''
        
        bjid = get_client_id()
        cuser = get_domain(bjid)
            
        if not check_jid(groupchat):
            groupchat = '%s@conference.%s' % (groupchat, cuser)
        
        gch_serv = safe_split(groupchat, '@')[1]
        
        reply(type, source, l('Waiting for groupchat join query result...'))
        
        if get_int_cfg_param('privacy_lists', 1):
            add_jid_to_privacy(gch_serv)
        
        if not dis_service_exists(gch_serv):
            return reply(type, source, l('Service not found!'))
        
        add_gch_config(groupchat)
        
        call_stage1_init_handlers(groupchat)

        if not passw:
            if not bot_nick:
                join_groupchat(groupchat, def_nick)
            else:
                join_groupchat(groupchat, bot_nick)
        else:
            if not bot_nick:
                join_groupchat(groupchat, def_nick, passw)
            else:
                join_groupchat(groupchat, bot_nick, passw)

        aliaso.load(groupchat)

        if bot_nick:
            return reply(type, source, l('Bot has joined %s with nick %s.') % (groupchat, bot_nick))
        else:
            return reply(type, source, l('Bot has joined %s with nick %s.') % (groupchat, def_nick))
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_admin_leave(type, source, parameters):
    gch = source[1]
    groupchat = gch
    nick = source[2]
    gch_jid = '%s/%s' % (groupchat, nick)

    args = parameters.split()

    if len(args) > 1:
        level = int(user_level(gch_jid, groupchat))
        
        if level < 40 and args[0] != groupchat and not type == 'console':
            return reply(type, source, l('Too few rights!'))
        
        reason = ' '.join(args[1:]).strip()
        groupchat = args[0]
    elif len(args) == 1:
        level = int(user_level(gch_jid, groupchat))
        
        if level < 40 and args[0] != groupchat and not type == 'console':
            return reply(type, source, l('Too few rights!'))
        
        reason = ''
        groupchat = args[0]
    else:
        if not is_groupchat(groupchat):
            return reply(type, source, l('It is possible only in groupchat!'))
        reason = ''

    bjid = get_client_id()
    cuser = get_domain(bjid)

    if not check_jid(groupchat):
        groupchat = '%s@conference.%s' % (groupchat, cuser)

    if not is_groupchat(groupchat):
        return reply(type, source, l('Bot is not present in this groupchat!'))
    
    rep = ''
    
    if not groupchat.count(gch):
        rep = l('Bot has left %s.') % (groupchat)
        reply(type, source, rep)

    if reason:
        leave_groupchat(groupchat, l('Exit from groupchat %s.') % (reason))
    else:
        leave_groupchat(groupchat, l('Exit from groupchat.'))
    
    return rep

def handler_admin_msg(type, source, parameters):
    if parameters:
        tojid = safe_split(parameters, ' ')[0]
        mess = safe_split(parameters, ' ')[1]
        
        msg(tojid, mess)
        
        return reply(type, source, l('Message has sent!'))
        
    return reply(type, source, l('Invalid syntax!'))
            
def handler_glob_msg(type, source, parameters):
    cid = get_client_id()
    
    total = 0
    
    if parameters:
        gchs = list(get_fatal_var(cid, 'gchrosters'))
        
        if not gchs:
            return reply(type, source, l('There are no groupchats to send message!'))
        
        for gch in gchs:
            msg(gch, l("Message from bot's admin:\n\n%s") % (parameters))
            total += 1

        return reply(type, source, l('Message has been sent in %s groupchats!') % (total))
    else:
        return reply(type, source, l('Invalid syntax!'))
    
def handler_admin_say(type, source, parameters):
    groupchat = source[1]
    
    if parameters:
        return msg(groupchat, parameters.strip())
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_admin_echo(type, source, parameters):
    if parameters:
        if type == 'private':
            return reply(type, source, parameters.strip())
        elif type == 'console':
            return msg('console', parameters.strip())
        elif type == 'public':
            return reply(type, source, parameters.strip())
        else:
            return msg('null', parameters.strip())
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_admin_restart(type, source, parameters):
    if parameters:
        reason = parameters
    else:
        reason = ''
    
    prs = xmpp.Presence(typ='unavailable')
    
    if reason:
        prs.setStatus(l('Restart: %s') % (reason))
    else:
        prs.setStatus(l('Restart.'))

    cids = dict(get_dict_fatal_var('clconns'))
    
    for cid in cids:
        jconn = cids[cid]
        
        try:
            jconn.send(prs)
        except Exception:
            pass        
    
    sprint('\nGot restart command.')
    time.sleep(3)
    sprint('\Restarting...')
    restart_bot()

def handler_admin_exit(type, source, parameters):
    if parameters:
        reason = parameters
    else:
        reason = ''
        
    prs = xmpp.Presence(typ='unavailable')
    
    if reason:
        prs.setStatus(l('Shutdown: %s') % (reason))
    else:
        prs.setStatus(l('Shutdown.'))
    
    cids = dict(get_dict_fatal_var('clconns'))
    
    for cid in cids:
        jconn = cids[cid]
        
        try:
            jconn.send(prs)
        except Exception:
            pass        
    
    sprint('\nDisconnected.')
    sprint('\n...---===BOT STOPPED===---...\n')
    time.sleep(2)
    rmv_pid_file()
    os._exit(0)
    
def handler_changebotstatus(type, source, parameters):
    gch_jid = source[1]

    if parameters:
        args, show, status = safe_split(parameters, ' '), '', ''
        
        args = rmv_empty_items(args)
        
        if args[0] in ['online', 'away', 'xa', 'dnd', 'chat']:
            show = args[0]
        else:
            show = get_gch_param(gch_jid, 'status_show', 'online')
            status = parameters
            
        if not status:
            if len(args) >= 2:
                status = args[1]
        
        if show != 'online':        
            change_bot_status(gch_jid, status, show)
        else:
            change_bot_status(gch_jid, status)   
        
        if is_groupchat(gch_jid):
            set_gch_param(gch_jid, 'status_text', status)
            set_gch_param(gch_jid, 'status_show', show)
        else:
            set_param('status_text', status)
            set_param('status_show', show)
            
        return reply(type, source, l('Status has set.'))
    else:
        cid = get_client_id()
        
        cprfx = get_comm_prefix(gch_jid)
        bot_nick = get_bot_nick(gch_jid)
        
        if is_groupchat(gch_jid):
            stmsg = get_fatal_var(cid, 'gchrosters', gch_jid, bot_nick, 'status')
            status = get_fatal_var(cid, 'gchrosters', gch_jid, bot_nick, 'show')
        else:
            stmsg = get_param('status_text', l('Type %shelp and follow instructions of the bot to understand how to work with me!') % (cprfx))
            status = get_param('status_show', 'online')
            
        if stmsg:
            return reply(type, source, l('Current status of bot is %s (%s).') % (status, stmsg))
        else:
            return reply(type, source, l('Current status of bot is %s.') % (status))

def handler_cmd_names(type, source, parameters):
    cid = get_client_id()
    
    gch_jid = source[1]
    
    cprfx = get_comm_prefix(gch_jid)
    
    comms = list(get_dict_fatal_var('commands'))
    comms.sort()
    
    if parameters:
        spltdp = parameters.split()
        rep = ''
        
        if len(spltdp) == 1:
            if spltdp[0][0] != "-":
                comm = parameters.strip()
                pcomm = cprfx + comm
                
                rcomm = get_real_cmd_name(comm)
                
                if rcomm in comms:
                    if cmd_name_exists(rcomm):
                        rep = l('Real name of command "%s": %s.') % (pcomm, rcomm)
                    else:
                        rep = l('Name of command "%s" has not been changed yet.') % (pcomm)
                else:
                    rep = l('Unknown command!')
            else:
                spltdp = spltdp[0].split('-', 1)
                
                spltdp = [spli for spli in spltdp if spli != '']
                
                if not spltdp:                    
                    res = rmv_cmd_name()
                    
                    if res != '':
                        rep = l('List of changed command names has been cleared, default command names has been restored!')
                    else:
                        rep = l('Unknown error!')
                elif len(spltdp) == 1:
                    if spltdp[0].isdigit():
                        commlst = get_cmd_name_list()
                        
                        if commlst:
                            anamelst = [anli[1].strip() for anli in commlst]
                            delind = int(spltdp[0])
                            
                            if delind <= len(anamelst) and delind != 0:
                                aname = anamelst[delind - 1]
                                panam = cprfx + aname
                                
                                res = rmv_cmd_name(aname)
                                
                                if res != '':
                                    rep = l('Changed name of command "%s" has been removed from list, default name has been restored!') % (panam)
                                else:
                                    rep = l('Unknown error!')
                            else:
                                rep = l('Invalid number!')
                        else:
                            if commlst != '':
                                rep = l('List of changed command names is empty!')
                            else:
                                rep = l('Unknown error!')
                    else:
                        comm = parameters.strip()
                        pcomm = cprfx + comm
                        rcomm = get_real_cmd_name(comm)
                       
                        if rcomm in comms:
                            if cmd_name_exists(rcomm):
                                rep = l('Real name of command "%s": %s.') % (pcomm, rcomm)
                            else:
                                rep = l('Name of command "%s" has not been changed yet.') % (pcomm)
                        else:
                            rep = l('Unknown command!')
        elif len(spltdp) >= 2:
            comm = spltdp[0]
            name = spltdp[1]
            pcomm = cprfx + comm
            
            aliaso = get_fatal_var(cid, 'alias')
            
            acomm = get_real_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            if rcomm in comms and not cmd_name_exists(comm):
                if name:                    
                    lali = []
                    
                    if is_groupchat(gch_jid):
                        lali = aliaso.aliaslist[gch_jid]
                    
                    if name in aliaso.galiaslist or name in lali or get_real_cmd_name(name):
                        return reply(type, source, l('Invalid new name of command, choose another one!'))
                    
                    if not name in comms:
                        if comm != rcomm:
                            set_cmd_name(rcomm, name)
                        else:
                            set_cmd_name(comm, name)
                    else:
                        rmv_cmd_name(comm)
                else:
                    return reply(type, source, l('Invalid syntax!'))
                
                rep = l('Name of command "%s" has been changed to "%s"!') % (pcomm, name)
            else:
                rep = l('Unknown command!')
        else:
            rep = l('Invalid syntax!')
                
        return reply(type, source, rep.strip())
    else:
        cmd_names = get_cmd_name_list()
        
        if cmd_names:
            count = len(cmd_names)
            rep = l('List of changed command names (total: %s):\n\n') % (count)
            cmdnsli = ['%d) %s = %s' % (cmd_names.index(cnli) + 1, cnli[0], cnli[1]) for cnli in cmd_names]
            rep += '\n'.join(cmdnsli)
            return reply(type, source, rep.strip())
        else:
            return reply(type, source, l('List of changed command names is empty!'))

def handler_cblock_control(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
    
    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))
        
        if int(parameters) > 1:
            return reply(type, source, l('Invalid syntax!'))
        
        if parameters == "1":
            set_gch_param(groupchat, 'conf_lock', '1')
            return reply(type, source, l('Local bot lock has been turned on!'))
        else:
            set_gch_param(groupchat, 'conf_lock', '0')
            return reply(type, source, l('Local bot lock has been turned off!'))
    else:
        conf_lock = int(get_gch_param(groupchat, 'conf_lock', '0'))
        
        if conf_lock:
            return reply(type, source, l('Local bot lock is turned on in this groupchat!'))
        else:
            return reply(type, source, l('Local bot lock is turned off in this groupchat!'))

def handler_gblock_control(type, source, parameters):
    if parameters:
        if not parameters.isdigit():
            return reply(type, source, l('Invalid syntax!'))
        
        if int(parameters) > 1:
            return reply(type, source, l('Invalid syntax!'))
        
        if parameters == "1":
            set_param('global_lock', '1')
            return reply(type, source, l('Global bot lock has been turned on!'))
        else:
            set_param('global_lock', '0')
            return reply(type, source, l('Global bot lock has been turned off!'))
    else:
        conf_lock = int(get_param('global_lock', '0'))
        
        if conf_lock:
            return reply(type, source, l('Global bot lock is turned on!'))
        else:
            return reply(type, source, l('Global bot lock is turned off!'))

def init_gblock_param():
    if not param_exists('', 'global_lock'):
        set_param('global_lock', '0')

def set_default_gch_status(gch):
    cprfx = get_comm_prefix(gch)
    
    if not param_exists(gch, 'conf_lock'):
        set_gch_param(gch, 'conf_lock', '0')

    if not param_exists(gch, 'status_text'):
        set_gch_param(gch, 'status_text', l('Type %shelp and follow instructions of the bot to understand how to work with me!') % (cprfx))
    if not param_exists(gch, 'status_show'):
        set_gch_param(gch, 'status_show', 'online')
    
def handler_delivery(type, source, body):
    cid = get_client_id()
    
    sender_jid = source[1]
    
    if is_groupchat(sender_jid): 
        return

    if get_int_cfg_param('admins_delivery'):
        admins = get_lst_cfg_param('admins')
        
        if not sender_jid in admins:
            aliaso = get_fatal_var(cid, 'alias')
            rostero = get_fatal_var(cid, 'roster')
            
            icomm = safe_split(body, ' ')[0]
            icomm = icomm.lower()

            prefix = get_comm_prefix()

            pcomm = icomm

            if prefix and icomm.startswith(prefix):
                pcomm = icomm.replace(prefix, '', 1)

            cname = get_real_cmd_name(pcomm)
    
            if not cname:
                cname = pcomm

            uname = ''
            
            if sender_jid in rostero.getItems():
                uname = rostero.getName(sender_jid)
                subs = rostero.getSubscription(sender_jid)

                if subs in ('none', None, ''):
                    return
            else:
                return
            
            if not uname:
                uname = sender_jid
            
            if not is_var_set('commands', cname) and not icomm in aliaso.galiaslist:
                if uname != sender_jid:
                    rep = l('Message from %s (%s):\n\n%s') % (uname, sender_jid, body)
                else:
                    rep = l('Message from %s:\n\n%s') % (uname, body)
                
                for adli in admins:
                    msg(adli, rep)
    
def handler_admin_subscription():
    cid = get_client_id()
    
    admins = get_lst_cfg_param('admins')
    
    for adli in admins:
        rostero = get_fatal_var(cid, 'roster')
        
        gsubs = ''
        
        if adli in rostero.getItems():
            gsubs = rostero.getSubscription(adli)
        
        admin_id = 'admin' + str(random.randrange(1000, 9999))
        
        if not gsubs or gsubs == 'none':
            rostero.setItem(adli, admin_id, ['bot-admins'])
            
        if gsubs != 'both':
            rostero.Subscribe(adli)

def handler_bot_lang(type, source, parameters):
    if parameters:
        locale = parameters.strip()
        
        if len(locale) == 2:
            locale = locale.lower()
            
            res = set_param('locale', locale)
            
            if res != '':
                change_locale(locale)
                set_help_locale(locale)
                
                rep = l('Bot locale has been set!')
            else:
                rep = l('Unknown error!')
        else:
            rep = l('Invalid syntax!')
    else:
        locale = get_param('locale', 'en')
        
        rep = l('Current bot locale is "%s"!') % (locale)
        
    return reply(type, source, rep)          

def handler_prefix_control(type, source, parameters):
    gch_jid = source[1] 
    
    isgch = is_groupchat(gch_jid)
    
    if parameters:
        ulvl = user_level(source, gch_jid)
        prefix = parameters.strip()
        
        if len(prefix) == 1:
            prefix = prefix.lower()
            
            fwr = l('Too few rights!')
            
            if isgch and ulvl < 30:
                return reply(type, source, fwr)
            elif not isgch and ulvl < 100:
                return reply(type, source, fwr)
            
            res = set_comm_prefix(gch_jid, prefix)
            
            if res != '':
                if isgch:
                    rep = l('Command prefix for this groupchat has been set!')
                else:
                    rep = l('Command prefix has been set!')
            else:
                rep = l('Unknown error!')
        else:
            rep = l('Invalid syntax!')
    else:
        prefix = get_comm_prefix(gch_jid)
        
        if isgch:
            rep = l('Current command prefix for this groupchat: %s') % (prefix)
        else:
            rep = l('Current command prefix: %s') % (prefix)
    
    return reply(type, source, rep)

def handler_connect(type, source, parameters):
    if parameters:
        splp = parameters.split(':')
        fspp = [spi.strip() for spi in splp if spi]
        
        if len(fspp) >= 2 and len(fspp) <= 3:
            crs = ''
            
            cid = fspp[0]
            psw = fspp[1]
            
            if len(fspp) == 3:
                crs = fspp[2]
            
            cids = get_lst_cfg_param('jid')
            psws = get_lst_cfg_param('password')
            
            if cid in cids:
                return reply(type, source, l('Client %s is already connected!') % (cid))
            
            if check_jid(cid):
                init_clients_vars([cid])
                
                call_in_sep_thr(cid + '/connect', connect_client, cid, psw, crs)
                
                reply(type, source, l('Waiting for connect...'))
                
                res = read_client_state()
                
                if res == 'suc':
                    cids.append(cid)
                    psws.append(psw)
                    
                    cstr = ', '.join(cids)
                    pstr = ', '.join(psws)
                    
                    set_cfg_param('jid', cstr)
                    set_cfg_param('password', pstr)
                    
                    clients = get_int_fatal_var('clients')
                    clients += 1
                    set_fatal_var('clients', clients)
                    
                    cows = get_fatal_var('console_owners')
                    
                    if 'fatal-bot' in cows or get_fatal_var('curr_cons_owner') == 'fatal-bot':
                        if 'fatal-bot' in cows:
                            cows.remove('fatal-bot')
                        
                        set_fatal_var('curr_cons_owner', cid)
                        
                    locale = get_sys_lang()

                    locale = get_param('locale', locale)
                        
                    reld_acc_lc_msgs(locale, cid)
                    reld_acc_hlp_msgs(locale, cid)
                    
                    cows.append(cid)
                    
                    rep = l('Client %s has been successfully connected!') % (cid)
                else:
                    rep = l('Unable to connect client %s due to errors!') % (cid)
                    
                close_state_pipes()
            else:
                rep = l('Invalid jid!')
        else:
            rep = l('Invalid syntax!')
    else:
        rep = l('Invalid syntax!')
        
    return reply(type, source, rep)

def handler_disconnect(type, source, parameters):
    def disconnect(cid):
        jconn = get_client_conn(cid)
        
        prs = xmpp.Presence()
        prs['type'] = 'unavailable'
        prs.setStatus(l('Client has been got disconnect command!'))
        
        jconn.send(prs)
        
        set_fatal_var(cid, 'disconnected', True)
        
        stop_scheduler()
                
        call_in_sep_thr(cid + '/disconnect', jconn.disconnect)
        
        dec_fatal_var('clients')
        
        cows = get_fatal_var('console_owners')
        
        if cid in cows:
            cows.remove(cid)
        
        cids = get_lst_cfg_param('jid')
        psws = get_lst_cfg_param('password')
        
        if cid in cids:
            pidx = cids.index(cid)
            
            cids.pop(pidx)
            psws.pop(pidx)
        
        cstr = ', '.join(cids)
        pstr = ', '.join(psws)
        
        set_cfg_param('jid', cstr)
        set_cfg_param('password', pstr)
        
        rmv_fatal_var(cid)
        
        return l('Client %s has been disconnected!') % (cid)
    
    cids = get_lst_cfg_param('jid')
    cids.sort()
    
    cids = [cid for cid in cids if is_var_set(cid)]
    
    ccid = get_client_id()
    
    if ccid in cids:
        cids.remove(ccid)
    
    if parameters:
        cid = parameters.strip()
        
        if check_jid(cid):
            if cid in cids:
                rep = disconnect(cid)
            else:
                rep = l('Client not in list of connected accounts!') 
        elif cid.isdigit():
            cin = int(cid)
            
            if cin <= len(cids) and cin > 0:
                cid = cids[cin - 1]
                
                rep = disconnect(cid)
            else:
                rep = l('Client not in list of connected accounts!')
        else:
            rep = l('Invalid syntax!')
    else:
        if cids:
            ncids = get_num_list(cids)
            
            rep = l('Connected clients for disconnect (total: %s):\n\n%s') % (len(ncids), '\n'.join(ncids))
        else:
            rep = l('List of connected clients for disconnect is empty!')
    
    return reply(type, source, rep)

def handler_syslog(type, source, parameters):
    syslogs = os.listdir('syslogs')
    syslogs = [lli.split('.')[0] for lli in syslogs if lli.endswith('.log')]
    syslogs.sort()
    rep = ''
    
    if parameters:
        stprms = parameters.strip()
        splp = stprms.split()
        
        if len(splp) <= 2:
            lines = '20'
            
            if len(splp) == 2:
                lines = splp[1]
                lines = lines.strip()
            
            logf = splp[0]
            
            if logf.isdigit():
                logn = int(logf)
                
                if logn <= len(syslogs):
                    logf = syslogs[logn - 1]
                else:
                    rep = l('Invalid syntax!')
            
            logf = 'syslogs/%s.log' % (logf)
            
            if not rep and lines.isdigit():
                lnsdt = read_file(logf, True)
                lines = int(lines)
                
                if lnsdt:
                    slns = lnsdt[-lines:]
                    
                    olns = ''.join(slns)
                    olns = olns.decode('utf-8')

                    rep = l('System bot logfile "%s" (lines: %s; displayed: %s):\n\n%s') % (logf, len(lnsdt), len(slns), olns.strip())
                else:
                    rep = l('System bot logfile "%s" is empty or not found!') % (logf)
            elif not rep and lines == '-':
                if os.path.exists(logf):
                    write_file(logf, '')
                    
                    rep = l('System bot logfile "%s" has been cleared!') % (logf)
                else:
                   rep = l('System bot logfile "%s" is empty or not found!') % (logf) 
            else:
                rep = l('Invalid syntax!')
        else:
            rep = l('Invalid syntax!')
    else:
        ollist = []
        
        for lfi in syslogs:
            lsz = os.path.getsize('syslogs/%s.log' % (lfi))
            ollist.append('%s [%s]' % (lfi, lsz))
        
        nmolst = get_num_list(ollist)
        
        rep = l('List of bot system logs is empty!')
        
        if nmolst:
            rep = l('List of bot system logs (total: %s):\n\n%s') % (len(nmolst), '\n'.join(nmolst))
    
    return reply(type, source, rep)

def handler_admin_config(type, source, parameters):

    def process_params(pars, group):
        parl = []

        pars.sort()

        for pmi in pars:
            par = pmi[0]
            val = pmi[1]
            val = val.replace('&quot;', '"')

            parl.append('%s = %s' % (par, val))

        nprs = get_num_list(parl)

        if nprs:
            return l('Parameters of group "%s" (total: %s):\n\n%s') % (group, len(nprs), '\n'.join(nprs))

        return l('Unknown error!')

    gch_jid = source[1]
    locus = 'glob'
    grps = ('bot', 'glob', 'room')

    if is_groupchat(gch_jid):
        locus = 'room'

    if parameters:
        pstrp = parameters.strip()

        psplt = pstrp.split(' ', 2)

        if len(psplt) == 1:
            loc_par = psplt[0]

            if not loc_par in grps:
                param = loc_par
                group = locus

                if group == 'glob':
                    value = get_param(param)
                else:
                    value = get_gch_param(gch_jid, param)
                
                if value:
                    rep = l('Value of parameter (name: %s, group: %s): %s') % (param, group, value)
                else:
                    rep = l('Not found!')
            else:
                group = loc_par

                if group == 'bot':
                    parl = []

                    pars = enum_cfg_params()
                    
                    for pmi in pars:
                        par = pmi
                        val = get_cfg_param(par)
                        
                        parl.append('%s = %s' % (par, val))

                    nprs = get_num_list(parl)

                    if nprs:
                        rep = l('Parameters of group "%s" (total: %s):\n\n%s') % (group, len(nprs), '\n'.join(nprs))
                    else:
                        rep = l('Unknown error!')
                elif group == 'glob':
                    pars = get_params()
                    
                    rep = process_params(pars, group)
                elif group == 'room':
                    if locus == 'room':
                        pars = get_gch_params(gch_jid)

                        rep = process_params(pars, group)
                    else:
                        rep = l('This command can be used only in groupchat!')
        elif len(psplt) == 2:
            loc_par = psplt[0]
            par_val = psplt[1]

            if not loc_par in grps:
                param = loc_par
                group = locus
                value = par_val

                if group == 'glob':
                    res = set_param(param, value)
                else:
                    res = set_gch_param(gch_jid, param, value)
                
                if res != '':
                    rep = l('Set value of parameter (name: %s, group: %s): %s') % (param, group, value)
                else:
                    rep = l('Not found!')
            else:
                group = loc_par
                param = par_val

                rpstr = l('Value of parameter (name: %s, group: %s): %s')

                if group == 'bot':
                    value = get_cfg_param(param)                    

                    if value:
                        rep = rpstr % (param, group, value)
                    else:
                        rep = l('Not found!')
                elif group == 'glob':
                    value = get_param(param)
                    
                    if value:
                        rep = rpstr % (param, group, value)
                    else:
                        rep = l('Not found!')
                elif group == 'room':
                    if locus == 'room':
                        value = get_gch_param(gch_jid, param)

                        if value:
                            rep = rpstr % (param, group, value)
                        else:
                            rep = l('Not found!')
                    else:
                        rep = l('This command can be used only in groupchat!')
        elif len(psplt) == 3:
            group = psplt[0]
            param = psplt[1]
            value = psplt[2]

            rpstr = l('Set value of parameter (name: %s, group: %s): %s')

            if group == 'bot':
                if is_param_set(param):
                    res = set_cfg_param(param, value)

                    if res:
                        rep = rpstr % (param, group, value)
                    else:
                        rep = l('Unknown error!')
                else:
                    rep = l('Not found!')
            elif group == 'glob':
                res = set_param(param, value)

                if res:
                    rep = rpstr % (param, group, value)
                else:
                    rep = l('Unknown error!')
            elif group == 'room':
                if locus == 'room':
                    res = set_gch_param(gch_jid, param, value)

                    if res:
                        rep = rpstr % (param, group, value)
                    else:
                        rep = l('Unknown error!')
                else:
                    rep = l('This command can be used only in groupchat!')
            else:
                rep = l('Invalid syntax!')
        else:
            rep = l('Invalid syntax!')
    else:
        grnl = get_num_list(grps)

        rep = l('Configure groups (total: %s):\n\n%s') % (len(grnl), '\n'.join(grnl))

    if type == 'public':
        reply(type, source, l('Look in private!'))

    return reply('private', source, rep)

register_command_handler(handler_admin_join, 'join', 40)
register_command_handler(handler_admin_leave, 'leave', 20)
register_command_handler(handler_admin_msg, 'message', 20)
register_command_handler(handler_admin_say, 'say', 20)
register_command_handler(handler_admin_echo, 'echo', 20)
register_command_handler(handler_admin_restart, 'restart', 100)
register_command_handler(handler_admin_exit, 'halt', 100)
register_command_handler(handler_glob_msg, 'globmsg', 100)
register_command_handler(handler_changebotstatus, 'set_status', 20)
register_command_handler(handler_set_nick, 'set_nick', 20)
register_command_handler(handler_remote, 'remote', 100)
register_command_handler(handler_redirect, 'redirect', 20)
register_command_handler(handler_admin_rejoin, 'rejoin', 100)
register_command_handler(handler_cmd_names, 'cmd_name', 100)
register_command_handler(handler_cblock_control, 'cblock', 100)
register_command_handler(handler_gblock_control, 'gblock', 100)
register_command_handler(handler_bot_lang, 'bot_lang', 100)
register_command_handler(handler_connect, 'connect', 100)
register_command_handler(handler_disconnect, 'disconnect', 100)
register_command_handler(handler_syslog, 'syslog', 100)
register_command_handler(handler_prefix_control, 'prefix', 0)
register_command_handler(handler_admin_config, 'config', 100)

register_stage0_init(init_gblock_param)
register_stage1_init(set_default_gch_status)
register_message_handler(handler_delivery)
register_stage2_init(handler_admin_subscription)

