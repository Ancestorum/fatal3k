# -*- coding: utf-8 -*-

#  fatal plugin
#  xepstatus plugin

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

def handler_status(type, source, parameters):
    groupchat = source[1]
    nick = source[2]
    
    if parameters:
        nick = parameters
        
        if is_gch_user(groupchat, nick):
            status = get_user_show(groupchat, nick)
            stmsg = get_user_status(groupchat, nick)
            
            if stmsg:
                rep = l('Current status of %s: %s (%s).') % (parameters, status, stmsg)
            else:
                rep = l('Current status of %s: %s.') % (parameters, status)
        else:
            rep = l('User not found!')
        
        return reply(type, source, rep)
    else:
        if is_gch_user(groupchat, nick):
            status = get_user_show(groupchat, nick)
            stmsg = get_user_status(groupchat, nick)
            
            if stmsg:
                rep = l('Current status: %s (%s).') % (status, stmsg)
            else: 
                rep = l('Current status: %s.') % (status)
        else:
            rep = l('User not found!')
        
        return reply(type, source, rep)

register_command_handler(handler_status, 'status')
