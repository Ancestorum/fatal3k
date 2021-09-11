# -*- coding: utf-8 -*-

#  fatal plugin
#  xepstanza plugin

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
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
from xml.parsers.expat import ExpatError

def handler_stanza(source, type, parameters):
    rep = l('Executed!')
    
    if parameters:
        try:
            node = xmpp.simplexml.XML2Node(str(parameters).encode('utf8'))
            jconn = get_client_conn()
            jconn.send(node)
        except ExpatError:
            rep = l('Parser error!')
    else:
        rep = l('Invalid syntax!')
        
    return reply(source, type, rep)

register_command_handler(handler_stanza, 'stanza', 100)
