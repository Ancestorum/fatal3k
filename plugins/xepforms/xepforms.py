# -*- coding: utf-8 -*-

#  fatal plugin
#  xepforms plugin

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

def muc_filter_disco_hnd(conn, request, typ):
    title = l('Muc-filter room configurations')
    
    discofeatures = [xmpp.NS_COMMANDS, xmpp.NS_DATA]
    discoinfo = {'ids': [{'category': 'automation', 'type': 'command-node', 'name': title}], 'features': discofeatures}

    if typ == 'list':
        frmjid = request.getFrom()
        gch = get_stripped(frmjid)
        nick = get_resource(frmjid)
        uaff = get_gch_aff(gch, nick)
        
        if not is_groupchat(gch): 
            return
        
        if user_level(frmjid, gch) < 100 and not uaff == 'owner': 
            return
        
        bnick = get_bot_nick(gch)
        
        node = '%s/%s' % (gch, bnick)
        
        return (node, 'filter', title)
    elif typ == 'items':
        return []
    elif typ == 'info':
        frmjid = request.getFrom()
        gch = get_stripped(frmjid)
        nick = get_resource(frmjid)
        uaff = get_gch_aff(gch, nick)
        
        if not is_groupchat(gch): 
            return {'ids': [], 'features': []}
            
        if user_level(frmjid, gch) < 100 and not uaff == 'owner': 
            return {'ids': [], 'features': []}
        
        return discoinfo

def bot_config_disco_hnd(conn, request, typ):
    title = l('Bot configurations')
    
    discofeatures = [xmpp.NS_COMMANDS, xmpp.NS_DATA]
    discoinfo = {'ids': [{'category': 'automation', 'type': 'command-node', 'name': title}], 'features': discofeatures}

    if typ == 'list':
        frmjid = request.getFrom()
        strjid = get_stripped(frmjid)
        tojid = request.getTo()
        
        if not is_bot_admin(strjid):
            return
        
        return (tojid, 'config', title)
    elif typ == 'items':
        return []
    elif typ == 'info':
        frmjid = request.getFrom()
        strjid = get_stripped(frmjid)
        
        if not is_bot_admin(strjid):
            return {'ids': [], 'features': []}
        
        return discoinfo

def read_log_disco_hnd(conn, request, typ):
    title = l('Bot logs')
    
    discofeatures = [xmpp.NS_COMMANDS, xmpp.NS_DATA]
    discoinfo = {'ids': [{'category': 'automation', 'type': 'command-node', 'name': title}], 'features': discofeatures}

    if typ == 'list':
        frmjid = request.getFrom()
        strjid = get_stripped(frmjid)
        tojid = request.getTo()
        
        if not is_bot_admin(strjid):
            return
                
        return (tojid, 'logs', title)
    elif typ == 'items':
        return []
    elif typ == 'info':
        frmjid = request.getFrom()
        strjid = get_stripped(frmjid)
        
        if not is_bot_admin(strjid):
            return {'ids': [], 'features': []}
        
        return discoinfo

def bot_shutdown_disco_hnd(conn, request, typ):
    title = l('Bot shutdown')
    
    discofeatures = [xmpp.NS_COMMANDS, xmpp.NS_DATA]
    discoinfo = {'ids': [{'category': 'automation', 'type': 'command-node', 'name': title}], 'features': discofeatures}

    if typ == 'list':
        frmjid = request.getFrom()
        strjid = get_stripped(frmjid)
        tojid = request.getTo()
        
        if not is_bot_admin(strjid):
            return
        
        return (tojid, 'shutdown', title)
    elif typ == 'items':
        return []
    elif typ == 'info':
        frmjid = request.getFrom()
        strjid = get_stripped(frmjid)
        
        if not is_bot_admin(strjid):
            return {'ids': [], 'features': []}
        
        return discoinfo

def bot_shutdown_cmd(conn, request):
    action = request.getTagAttr('command', 'action')
    
    if action == 'execute':        
        interrupt('\n\nShutdown.', l('Shutdown.'))

def stat_cmd(conn, request):
    cid = get_client_id()
    
    action = request.getTagAttr('command', 'action')
    
    uptime = int(time.time() - get_int_fatal_var('info', 'start'))
    uptime = timeElapsed(uptime)

    sestime = int(time.time() - get_int_fatal_var(cid, 'info', 'ses'))
    sestime = timeElapsed(sestime)

    total_users = 0
        
    gchs = list(get_dict_fatal_var(cid, 'gchrosters'))
        
    for gch in gchs:
        gnicks = list(get_dict_fatal_var(cid, 'gchrosters', gch))
        total_users += len(gnicks)

    chtrs = len(gchs)

    bver = '[unknown]'
    
    ver = get_fatal_var('ftver', 'botver', 'ver')
    rev = get_fatal_var('ftver', 'rev')
    
    if not rev: 
        rev = ''
    
    if ver:
        bver = ver % (rev)

    dfdli = [l('Bot run statistics:'), '', l('Runtime period: %s.') % (uptime), l('Session time: %s.') % (sestime), l('Groupchats: %s.') % (chtrs), l('Users: %s.') % (total_users), '', '_' * (len(bver) + 3), l('Version: %s.') % (bver)]

    if action == 'execute':
        Iq = request.buildReply('result')
        
        command = Iq.addChild('command')
        command.setNamespace(xmpp.NS_COMMANDS)
        command.setAttr('node', 'stat')
        command.setAttr('status', 'completed')
        
        sesId = 'stat%s' % (time.time())
        command.setAttr('sessionid', sesId)
        
        dform = create_result_dform(l('Statistics'), dfdli)
        
        command.addChild(node=dform)
            
        conn.send(Iq)
        raise xmpp.NodeProcessed

def muc_filter_cmd(conn, request):
    cid = get_client_id()
    
    if request:
        iqtype = request.getType()
        frmjid = request.getFrom()
        gch = get_stripped(frmjid)
        
        if iqtype == 'set':
            cmdtg = request.getChild()
            xtype = None
                    
            mfrtg = cmdtg.getTag('x')
            
            if mfrtg:
                xtype = mfrtg.getAttr('type')
            
            action = cmdtg.getAttr('action')
            
            if action == 'execute':
                mfstate = get_gch_param(gch, 'muc_filter', '1')
                
                mfnlenst = get_gch_param(gch, 'mf_nick_len', '1')
                mfnlen = get_gch_param(gch, 'mf_nick_len_len', '30')
                
                mfnspace = get_gch_param(gch, 'mf_nick_space', '1')
                
                mfprsafl = get_gch_param(gch, 'mf_prs_aflood', '1')
                
                mfmsgst = get_gch_param(gch, 'mf_msg', '1')
                mfmsglen = get_gch_param(gch, 'mf_msg_len', '300')
                
                mfswwst = get_gch_param(gch, 'mf_sww', '1')
                
                mfmsgafl = get_gch_param(gch, 'mf_msg_aflood', '1')
                
                mfpstlnst = get_gch_param(gch, 'mf_stmsg_len', '1')
                mfpstlen = get_gch_param(gch, 'mf_stmsg_len_len', '50')
                
                mfpcaps = get_gch_param(gch, 'mf_prscaps', '0')
                
                mfakab = get_gch_param(gch, 'mf_akab', '1')
                
                Iq = request.buildReply('result')
                
                command = Iq.addChild('command')
                command.setNamespace(xmpp.NS_COMMANDS)
                command.setAttr('node', 'filter')
                command.setAttr('status', 'executing')
                
                sesId = 'mf%s' % (time.time())
                
                set_fatal_var(cid, '_sesid:%s' % (frmjid), sesId)
                
                command.setAttr('sessionid', sesId)
                
                mfdform = fDataForm(l('Muc-filter room configurations'), l('Muc-filter options:'))
                
                mfdform.addBField('muc_filter', l('State of muc-filtering:'), mfstate)
                
                mfdform.addFField('::')
                
                mfdform.addBField('mf_nick_len', l('Nick length filter:'), mfnlenst)
                mfdform.addTSField('mf_nick_len_len', l('Maximum length of nick:'), mfnlen)
                
                mfdform.addFField('::')
                
                mfdform.addBField('mf_nick_space', l('Nick edge spaces filter:'), mfnspace)
                
                mfdform.addBField('mf_prs_aflood', l('Presence flood filter:'), mfprsafl)
                
                mfdform.addFField('::')
                
                mfdform.addBField('mf_msg', l('Message length filter:'), mfmsgst)
                mfdform.addTSField('mf_msg_len', l('Maximum length of message:'), mfmsglen)
                
                mfdform.addFField('::')
                
                mfdform.addBField('mf_sww', l('Obscene words filter:'), mfswwst)
                
                mfdform.addBField('mf_msg_aflood', l('Message flood filter:'), mfmsgst)
                
                mfdform.addFField('::')
                
                mfdform.addBField('mf_prscaps', l('Presence caps filter:'), mfpcaps)
                
                mfdform.addFField('::')
                
                mfdform.addBField('mf_stmsg_len', l('Status length filter:'), mfpstlnst)
                mfdform.addTSField('mf_stmsg_len_len', l('Maximum length of status:'), mfpstlen)
                
                mfdform.addFField('::')
                
                mfdform.addBField('mf_akab', l('Filter nicks and jids through amuc regexps:'), mfakab)
                
                mfdform.ProcessForm()
                
                command.addChild(node=mfdform)
                
                conn.send(Iq)
                raise xmpp.NodeProcessed
            elif action == 'complete':
                Iq = request.buildReply('result')
                
                command = Iq.addChild('command')
                command.setNamespace(xmpp.NS_COMMANDS)
                command.setAttr('node', 'filter')
                command.setAttr('status', 'completed')
                
                sesId = rmv_fatal_var(cid, '_sesid:%s' % (frmjid))
                
                command.setAttr('sessionid', sesId)
                
                dfdict = parse_result_dform(mfrtg)
                
                for var in dfdict:
                    defval = get_gch_param(gch, var, '')
                    
                    value = dfdict[var]
                    
                    if value != defval:
                        dvdict = {'mf_nick_len_len': 30, 'mf_msg_len': 900, 'mf_stmsg_len_len': 50}
                        
                        if var in dvdict:
                            if value.isdigit():
                                if int(value) < dvdict[var]:
                                    value = str(dvdict[var])
                                    dfdict[var] = value
                            else:
                                value = str(dvdict[var])
                                dfdict[var] = value
                                
                        res = set_gch_param(gch, var, value)
                        
                        if not res:
                            dfdict[var] = defval
                    
                    if value == '1':
                        dfdict[var] = l('On')
                    elif value == '0':
                        dfdict[var] = l('Off')
                
                dfdli = [l('Muc-filter options:'), '', l('State of muc-filtering: %s') % (dfdict['muc_filter']), '::', l('Nick length filter: %s') % (dfdict['mf_nick_len']), l('Maximum length of nick: %s') % (dfdict['mf_nick_len_len']), '::', l('Nick edge spaces filter: %s') % (dfdict['mf_nick_space']), l('Presence flood filter: %s') % (dfdict['mf_prs_aflood']), '::', l('Message length filter: %s') % (dfdict['mf_msg']), l('Maximum length of message: %s') % (dfdict['mf_msg_len']), '::', l('Obscene words filter: %s') % (dfdict['mf_sww']), l('Message flood filter: %s') % (dfdict['mf_msg_aflood']), '::', l('Presence caps filter: %s') % (dfdict['mf_prscaps']), '::', l('Status length filter: %s') % (dfdict['mf_stmsg_len']), l('Maximum length of status: %s') % (dfdict['mf_stmsg_len_len']), '::', l('Filter nicks and jids through amuc regexps: %s') % (dfdict['mf_akab'])]
                
                dform = create_result_dform(l('Muc-filter room configurations'), dfdli)
                
                command.addChild(node=dform)
                
                conn.send(Iq)
                raise xmpp.NodeProcessed
            elif action == 'cancel':
                Iq = request.buildReply('result')
                
                command = Iq.addChild('command')
                command.setNamespace(xmpp.NS_COMMANDS)
                command.setAttr('node', 'filter')
                command.setAttr('status', 'canceled')
                
                sesId = rmv_fatal_var(cid, '_sesid:%s' % (frmjid))
                
                command.setAttr('sessionid', sesId)
                
                conn.send(Iq)
                raise xmpp.NodeProcessed

def bot_config_cmd(conn, request):
    cid = get_client_id()
    
    if request:
        iqtype = request.getType()
        frmjid = request.getFrom()
        
        if iqtype == 'set':
            cmdtg = request.getChild()
            
            mfrtg = cmdtg.getTag('x')
                       
            action = cmdtg.getAttr('action')
            
            if action == 'execute':
                bcjid = get_cfg_param('jid')
                bcport = get_cfg_param('port', '5222')
                bcpass = get_cfg_param('password')
                bcrsrc = get_cfg_param('resource', 'fatal')
                bctls = get_cfg_param('use_tls_ssl', '0')
                bcdnick = get_cfg_param('default_nick', 'fatal-bot')
                bckeepa = get_cfg_param('keep_alive', '300')
                bcadms = get_cfg_param('admins')
                bcapass = get_cfg_param('admin_password')
                bcadeli = get_cfg_param('admins_delivery', '0')
                bcasubs = get_cfg_param('auto_subscribe', '0')
                bcarecon = get_cfg_param('auto_reconnect', '1')
                bcshcon = get_cfg_param('show_console', '0')
                bcshall = get_cfg_param('shell_allowed', 'all')
                bccprfx = get_cfg_param('comm_prefix')
                bcmsgcl = get_cfg_param('msg_chatroom_limit', '5000')
                bcmsgpl = get_cfg_param('msg_private_limit', '10000')
                bcpuldir = get_cfg_param('public_log_dir', 'logs')
                bcprldir = get_cfg_param('private_log_dir', 'privlogs')
                bcrelc = get_cfg_param('reload_code', '0')
                bcmathr = get_cfg_param('max_active_threads', '50')
                bcmpstks = get_cfg_param('main_proc_stk_size', '1048576')
                bcdfstks = get_cfg_param('def_stk_size', '524288')
                
                Iq = request.buildReply('result')
                
                command = Iq.addChild('command')
                command.setNamespace(xmpp.NS_COMMANDS)
                command.setAttr('node', 'config')
                command.setAttr('status', 'executing')
                
                sesId = 'bcfg%s' % (time.time())
                
                set_fatal_var(cid, '_sesid:%s' % (frmjid), sesId)
                
                command.setAttr('sessionid', sesId)
                
                bcdform = fDataForm(l('Bot configurations'), l('Bot options:'))
                
                bcdform.addTSField('jid', l('Jabber Id (jid):'), bcjid)
                bcdform.addTPField('password', l('Account password:'), bcpass)
                bcdform.addTSField('port', l('Connection port:'), bcport)
                bcdform.addTSField('resource', l('Resource:'), bcrsrc)
                
                bcdform.addFField('::')
                
                bcdform.addBField('use_tls_ssl', l('Use TLS or SSL:'), bctls)
                bcdform.addTSField('default_nick', l('Default groupchat nick:'), bcdnick)
                bcdform.addTSField('keep_alive', l('Keep alive:'), bckeepa)
                
                bcdform.addFField('::')
                
                bcdform.addTSField('admins', l('Admins of bot:'), bcadms)
                bcdform.addTPField('admin_password', l('Admin password:'), bcapass)
                bcdform.addBField('admins_delivery', l('Deliver of messages to admins:'), bcadeli)
                
                bcdform.addFField('::')
                
                bcdform.addBField('auto_subscribe', l('Auto subscribe:'), bcasubs)
                bcdform.addBField('auto_reconnect', l('Auto reconnect:'), bcarecon)
                bcdform.addBField('show_console', l('Show bot console:'), bcshcon)
                bcdform.addTSField('shell_allowed', l('Allowed shell commands:'), bcshall)
                
                bcdform.addFField('::')
                
                bcdform.addTSField('comm_prefix', l('Commands prefix:'), bccprfx)
                
                bcdform.addFField('::')
                
                bcdform.addTSField('msg_chatroom_limit', l('Groupchats message limit:'), bcmsgcl)
                bcdform.addTSField('msg_private_limit', l('Privates message limit:'), bcmsgpl)
                
                bcdform.addFField('::')
                
                bcdform.addTSField('public_log_dir', l('Public logs directory:'), bcpuldir)
                bcdform.addTSField('private_log_dir', l('Private logs directory:'), bcprldir)
                
                bcdform.addFField('::')
                
                bcdform.addTSField('reload_code', l('Reload changed code:'), bcrelc)
                bcdform.addTSField('max_active_threads', l('Max active threads:'), bcmathr)
                bcdform.addTSField('main_proc_stk_size', l('Main xmpp thread stack size:'), bcmpstks)
                bcdform.addTSField('def_stk_size', l('Default threads stack size:'), bcdfstks)
                
                bcdform.ProcessForm()
                
                command.addChild(node=bcdform)
                
                conn.send(Iq)
                raise xmpp.NodeProcessed
            elif action == 'complete':
                Iq = request.buildReply('result')
                
                command = Iq.addChild('command')
                command.setNamespace(xmpp.NS_COMMANDS)
                command.setAttr('node', 'config')
                command.setAttr('status', 'completed')
                
                sesId = rmv_fatal_var(cid, '_sesid:%s' % (frmjid))
                
                command.setAttr('sessionid', sesId)
                
                dfdict = parse_result_dform(mfrtg)
                
                for var in dfdict:
                    defval = get_cfg_param(var)
                    
                    value = dfdict[var]
                    
                    if value != defval:
                        dvdict = {'port': '5222', 'keep_alive': '300', 'msg_chatroom_limit': '5000', 'msg_private_limit': '10000', 'max_active_threads': '50', 'main_proc_stk_size': '1048576', 'def_stk_size': '524288', 'reload_code': '0'}
                        
                        if var in dvdict:
                            if not value.isdigit():
                                value = dvdict[var]
                                dfdict[var] = value
                                
                        res = set_cfg_param(var, value)
                            
                        if not res:
                            dfdict[var] = defval
                            
                    if value == '1':
                        dfdict[var] = l('On')
                    elif value == '0':
                        dfdict[var] = l('Off')
                
                accp = dfdict['password']
                admp = dfdict['admin_password']

                accp = '*' * len(accp)
                admp = '*' * len(admp)

                dfdli = [l('Bot options:'), '', l('Jabber Id (jid): %s') % (dfdict['jid']), l('Account password: %s') % (accp), l('Connection port: %s') % (dfdict['port']), l('Resource: %s') % (dfdict['resource']), '::', l('Use TLS or SSL: %s') % (dfdict['use_tls_ssl']), l('Default groupchat nick: %s') % (dfdict['default_nick']), l('Keep alive: %s') % (dfdict['keep_alive']), '::', l('Admins of bot: %s') % (dfdict['admins']), l('Admin password: %s') % (admp), l('Deliver of messages to admins: %s') % (dfdict['admins_delivery']), '::', l('Auto subscribe: %s') % (dfdict['auto_subscribe']), l('Auto reconnect: %s') % (dfdict['auto_reconnect']), l('Show bot console: %s') % (dfdict['show_console']), l('Allowed shell commands: %s') % (dfdict['shell_allowed']), '::', l('Commands prefix: %s') % (dfdict['comm_prefix']), '::', l('Groupchats message limit: %s') % (dfdict['msg_chatroom_limit']), l('Privates message limit: %s') % (dfdict['msg_private_limit']), '::', l('Public logs directory: %s') % (dfdict['public_log_dir']), l('Private logs directory: %s') % (dfdict['private_log_dir']), '::', l('Reload changed code: %s') % (dfdict['reload_code']), l('Max active threads: %s') % (dfdict['max_active_threads']), l('Main xmpp thread stack size: %s') % (dfdict['main_proc_stk_size']), l('Default threads stack size: %s') % (dfdict['def_stk_size'])]
                
                dform = create_result_dform(l('Bot configurations'), dfdli)
                
                command.addChild(node=dform)
                
                conn.send(Iq)
                raise xmpp.NodeProcessed
            elif action == 'cancel':
                Iq = request.buildReply('result')
                
                command = Iq.addChild('command')
                command.setNamespace(xmpp.NS_COMMANDS)
                command.setAttr('node', 'config')
                command.setAttr('status', 'canceled')
                
                sesId = rmv_fatal_var(cid, '_sesid:%s' % (frmjid))
                
                command.setAttr('sessionid', sesId)
                
                conn.send(Iq)
                raise xmpp.NodeProcessed

def read_log_cmd(conn, request):
    cid = get_client_id()
    
    if request:
        iqtype = request.getType()
        frmjid = request.getFrom()
            
        if iqtype == 'set':
            cmdtg = request.getChild()
            
            mfrtg = cmdtg.getTag('x')
            
            action = cmdtg.getAttr('action')
            
            if action == 'execute':
                log_list = os.listdir('syslogs')
                loptv = []
                lopts = []
                
                for lli in log_list:
                    lsize = os.path.getsize('syslogs/%s' % (lli))
                    
                    optl = '%s [%s bytes]' % (lli, lsize)
                    
                    loptv.append(lli)
                    lopts.append((optl, lli))
                
                Iq = request.buildReply('result')
                
                command = Iq.addChild('command')
                command.setNamespace(xmpp.NS_COMMANDS)
                command.setAttr('node', 'logs')
                command.setAttr('status', 'executing')
                
                sesId = 'rlog%s' % (time.time())
                
                set_fatal_var(cid, '_sesid:%s' % (frmjid), sesId)
                
                command.setAttr('sessionid', sesId)
                
                rldform = fDataForm(l('Bot logs'), l('Output log options:'))
                
                rldform.addFField('')
                
                rldform.addLSField('log', l('Choose log:'), loptv[0], lopts)
                
                rldform.addFField('::')
                
                rldform.addTSField('lines', l('Lines:'), '17')
                
                rldform.addFField('::')
                
                rldform.addBField('clrlog', l('Clear log:'), '0')
                
                rldform.ProcessForm()
                
                command.addChild(node=rldform)
                
                conn.send(Iq)
                raise xmpp.NodeProcessed
            elif action == 'complete':
                Iq = request.buildReply('result')
                
                command = Iq.addChild('command')
                command.setNamespace(xmpp.NS_COMMANDS)
                command.setAttr('node', 'logs')
                command.setAttr('status', 'completed')
                
                sesId = rmv_fatal_var(cid, '_sesid:%s' % (frmjid))
                
                command.setAttr('sessionid', sesId)
                
                dfdict = parse_result_dform(mfrtg)
                
                clg = dfdict['log']
                lines = dfdict['lines']
                
                if not lines.isdigit():
                    lines = 17
                else:
                    lines = int(lines)
                
                clrl = int(dfdict['clrlog'])
                
                logb = read_file('syslogs/%s' % (clg))
                llns = logb.splitlines()
                
                if clrl:
                    write_file('syslogs/%s' % (clg), '')
                
                if lines < len(llns):
                    llns = llns[-lines:]
                
                ollns = '\n'.join(llns)
                
                rldform = fDataForm(l('Bot logs'), '')
                
                rldform.setType('result')
                
                rldform.addTMField('log', l('Choosed log "%s":') % (clg), ollns)
                
                rldform.addFField('::')
                
                for lli in llns:
                    rldform.addFField(lli)
                
                rldform.ProcessForm()
                
                command.addChild(node=rldform)
                
                conn.send(Iq)
                raise xmpp.NodeProcessed
            elif action == 'cancel':
                Iq = request.buildReply('result')
                
                command = Iq.addChild('command')
                command.setNamespace(xmpp.NS_COMMANDS)
                command.setAttr('node', 'logs')
                command.setAttr('status', 'canceled')
                
                sesId = rmv_fatal_var(cid, '_sesid:%s' % (frmjid))
                
                command.setAttr('sessionid', sesId)
                
                conn.send(Iq)
                raise xmpp.NodeProcessed

def init_dform_adhoccmd():
    register_adhoc_command('stat', l('Statistics'), cmdhnd=stat_cmd)
    register_adhoc_command('filter', l('Muc-filter room configurations'), muc_filter_disco_hnd, muc_filter_cmd)
    register_adhoc_command('config', l('Bot configurations'), bot_config_disco_hnd, bot_config_cmd)
    register_adhoc_command('logs', l('Bot logs'), read_log_disco_hnd, read_log_cmd)
    register_adhoc_command('shutdown', l('Bot shutdown'), bot_shutdown_disco_hnd, bot_shutdown_cmd)
    
register_stage0_init(init_dform_adhoccmd)
