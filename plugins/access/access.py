# -*- coding: utf-8 -*-

#  fatal plugin
#  access plugin

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
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

def getacc_jid(gch, nick):
    cid = get_client_id()
    
    nick = nick.replace('"', '&quot;')
    sql = "SELECT jid FROM users WHERE nick='%s';" % (nick)
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
    
    if qres:
        jid = qres[0][0]
        return jid

def getacc_nicks(gch):
    cid = get_client_id()
    
    sql = 'SELECT nick FROM users ORDER BY uleave;'
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
    
    if qres:
        nicks = [nil[0].replace('&quot;', '"') for nil in qres]
        return nicks
    return []

def handler_access_login(type, source, parameters):
    jid = get_true_jid(source)
    
    admpass = get_cfg_param('admin_password').strip()
    
    if not admpass:
        return reply('private', source, l('Password not set yet!'))
    
    if parameters.strip() == admpass:
        set_user_access(jid, 100)
        
        add_fatal_task('auto_logout/%s' % (jid), handler_access_logout, ('null', source, parameters), ival=3600, once=True)
        
        return reply('private', source, l('Password adopted, a global full access has been granted!'))
    else:
        return reply('private', source, l('Incorrect password!'))

def handler_access_logout(type, source, parameters):
    jid = get_true_jid(source)
    
    adml = get_lst_cfg_param('admins')
    
    if adml:
        if adml[0] == jid:
            return reply(type, source, l('Superadmin can not be logout!'))
    
    set_user_access(jid)
    
    return reply(type, source, l('Logout!'))

def handler_access_view_access(type, source, parameters):
    accdesc = {'-100': l('(full ignoring)'), '-1': l('(blocked)'), '0': l('(none)'), '1': l('(low user)'), '10': l('(user)'), '11': l('(member)'), '15': l('(moderator)'), '16': l('(moderator)'), '20': l('(admin)'), '30': l('(owner)'), '40': l('(joiner)'), '100': l('(suderadmin)')}
    
    gch_jid = source[1]
    snick = source[2]
    sgch_jid = '%s/%s' % (gch_jid, snick)
    nick_jid = parameters
    cid = get_client_id()
    
    if not parameters:
        level = str(user_level(sgch_jid, gch_jid))
        
        if type == 'console':
            level = '100'
        
        if level in accdesc:
            levdesc = accdesc[level]
        else:
            levdesc = ''
        
        return reply(type, source, '%s %s' % (level, levdesc))
    else:
        if is_groupchat(gch_jid):
            nicks = get_fatal_var(cid, 'gchrosters', gch_jid)
            
            if nick_jid in nicks:
                dgch_jid = '%s/%s' % (gch_jid, nick_jid)
                level = str(user_level(dgch_jid, gch_jid))
                
                if level in list(accdesc.keys()):
                    levdesc = accdesc[level]
                else:
                    levdesc = ''
                
                return reply(type, source, '%s %s' % (level, levdesc))
            else:
                if check_jid(nick_jid):
                    level = str(user_level(nick_jid, gch_jid))
                    
                    if level in list(accdesc.keys()):
                        levdesc = accdesc[level]
                    else:
                        levdesc = ''
                    
                    return reply(type, source, '%s %s' % (level, levdesc))
                    
                return reply(type, source, l('User not found!'))
        else:
            if user_access_exists(nick_jid):
                level = str(user_level(nick_jid))
                
                if level in list(accdesc.keys()):
                    levdesc = accdesc[level]
                else:
                    levdesc = ''
                
                return reply(type, source, '%s %s' % (level, levdesc))
            
            return reply(type, source, l('User not found!'))

def handler_access_set_access(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))
    
    if parameters:
        spltdp = parameters.strip().split(':', 1)
        
        access = 0
        
        if len(spltdp) > 1:
            access = spltdp[1].strip()
            
            if access.isdigit() or (access[0] == '-' and access[1:].isdigit()):
                access = int(access)
            else:
                return reply(type, source, l('Invalid syntax!'))

            if access > 100 or access < -100:
                return reply(type, source, l('Invalid syntax!'))
                
        nicks = getacc_nicks(groupchat)
        nick = spltdp[0].strip()
        
        if not nick in nicks:
            return reply(type, source, l('User not found!'))
        
        tjidto = get_true_jid(groupchat + '/' + spltdp[0].strip())
        tjidsource = get_true_jid(source)
        jidacc = user_level(source, groupchat)
        toacc = user_level(tjidto, groupchat)
        
        if len(spltdp) > 1:
            if not is_bot_admin(tjidsource):
                if tjidto == tjidsource:
                    if int(spltdp[1]) > int(jidacc):
                        return reply(type, source, l('Too few rights!'))
                elif int(toacc) > int(jidacc):
                    return reply(type, source, l('Too few rights!'))
                elif int(spltdp[1]) >= int(jidacc):
                    return reply(type, source, l('Too few rights!'))
        else:
            if not is_bot_admin(tjidsource):
                if int(toacc) > int(jidacc):
                    return reply(type, source, l('Too few rights!'))
    
        if len(spltdp) == 1:
            set_user_access(tjidto, access, groupchat)
            return reply(type, source, l('Local access of user %s has been removed!') % (spltdp[0].strip()))
        elif len(spltdp) == 2:
            set_user_access(tjidto, access, groupchat)
            return reply(type, source, l('Local access of user %s has been set to %s!') % (spltdp[0].strip(), spltdp[1].strip()))
    else:
        return reply(type, source, l('Invalid syntax!'))
        
def handler_access_set_access_glob(type, source, parameters):
    gch_jid = source[1]
    
    if parameters:
        spltdp = parameters.strip().split(':', 1)
        access = 0
        
        nick_jid = spltdp[0]
        
        tjidto = nick_jid
        
        if len(spltdp) == 2:
            access = spltdp[1].strip()
            
            if access:
                if access.isdigit() or (access[0] == '-' and access[1:].isdigit()):
                    access = int(access)
                else:
                    return reply(type, source, l('Invalid syntax!'))
            else:
                spltdp.remove(access)
        
        if is_groupchat(gch_jid):        
            nicks = getacc_nicks(gch_jid)
            
            if not nick_jid in nicks and not check_jid(nick_jid):
                return reply(type, source, l('User %s has never been here!') % (nick_jid))
            
            tjidto = getacc_jid(gch_jid, nick_jid)
        else:
            if not check_jid(nick_jid):
                return reply(type, source, l('Invalid syntax!'))
        
        if len(spltdp) == 2:
            if access <= 100 and access >= -100:
                set_user_access(tjidto, access)
                return reply(type, source, l('Global access of user %s has been set to %s!') % (nick_jid, access))
            else:
                return reply(type, source, l('Invalid syntax!'))
        else:
            set_user_access(tjidto)
            return reply(type, source, l('Global access of user %s has been removed!') % (nick_jid))
    else:
        return reply(type, source, l('Invalid syntax!'))
        
def handler_cmd_access(type, source, parameters):
    groupchat = source[1]
    comms = list(get_dict_fatal_var('commands'))
    cprfx = get_comm_prefix(groupchat)
    comms.sort()
    
    if parameters:
        spltdp = parameters.split(' ', 1)
        
        if len(spltdp) == 1:
            comm = parameters.strip()
            ocomm = cprfx + comm
            
            acomm = get_real_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            if rcomm in comms:
                cacc = get_int_fatal_var('commands', rcomm, 'access')
                
                racc = int(get_cmd_access(rcomm))
                
                if racc < 0:
                    racc = cacc
                
                rep = l('Access level for use of command "%s": %s.') % (ocomm, racc)
            else:
                rep = l('Unknown command!')
        elif len(spltdp) == 2:
            comm = spltdp[0]
            access = spltdp[1]
            ocomm = cprfx + comm
            
            acomm = get_real_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            if rcomm in comms:
                if access.isdigit():
                    set_cmd_access(rcomm, access)
                else:
                    return reply(type, source, l('Invalid syntax!'))
                
                rep = l('Access level for use of command "%s" has been set to %s.') % (ocomm, access)
            else:
                rep = l('Unknown command!')
        else:
            rep = l('Invalid syntax!')
        
        return reply(type, source, rep)
    else:
        cmds = ''
        rep = l('Access levels for use of commands (total: %s):\n\n%s')
        
        for comm in comms:
            acomm = get_cmd_name(comm)
            rcomm = comm
            
            if acomm:
                rcomm = acomm
            
            cacc = get_int_fatal_var('commands', comm, 'access')
            
            racc = int(get_cmd_access(comm))
            
            if racc < 0:
                racc = cacc
            
            cmds += '%s = %d\n' % (cprfx + rcomm, cacc)
        
        rep = rep % (len(comms), cmds)
        
        return reply(type, source, rep.strip())

def get_access_state(gch):
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/access.db' % (cid, gch)):
        sql = 'CREATE TABLE access(jid VARCHAR(50) NOT NULL, access VARCHAR(4) NOT NULL, UNIQUE(jid))'
        qres = sqlquery('dynamic/%s/%s/access.db' % (cid, gch), sql)

register_command_handler(handler_access_login, 'login')
register_command_handler(handler_access_logout, 'logout', 100)
register_command_handler(handler_access_view_access, 'access')
register_command_handler(handler_access_set_access, 'access_set', 15)
register_command_handler(handler_access_set_access_glob, 'gaccess_set', 100)
register_command_handler(handler_cmd_access, 'cmd_access', 100)

register_stage1_init(get_access_state)
