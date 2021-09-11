# -*- coding: utf-8 -*-

#  fatal plugin
#  more plugin

#  Initial Copyright © 2009 Als <als-als@ya.ru>
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

def handler_more(type, source, parameters):
    cid = get_client_id()
    
    groupchat = source[1]

    if type == 'public':
        msg = get_fatal_var(cid, 'more', groupchat)
        
        if msg:
            rmv_fatal_var(cid, 'more', groupchat)
            rep = '...] %s' % (msg)
            
            return reply(type, source, rep)
    else:
        return reply(type, source, l('This command can be used only in public chat!'))
            
def handler_more_outmsg(target, body, obody):
    cid = get_client_id()
    
    if not is_groupchat(target):
        return

    msg = get_fatal_var(cid, 'more', target)
    
    if not msg or not obody.endswith(msg):
        mcrl = get_int_cfg_param('msg_chatroom_limit', 5000)
        
        if len(obody) > mcrl:
            tail = obody[mcrl:]
            set_fatal_var(cid, 'more', target, tail)

register_outgoing_message_handler(handler_more_outmsg)

register_command_handler(handler_more, 'more', 10)
