# -*- coding: utf-8 -*-

#  fatal plugin
#  dns_plugin.py

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

import socket

from fatalapi import *

def dns_query(query):
    try:
        int(query[-1])
    except ValueError:
        try:
            (hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex(query)
            return ', '.join(ipaddrlist)
        except socket.gaierror:
            return l('Not found!')
    else:
        try:
            (hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(query)
        except socket.herror:
            return l('Not found!')
        return '%s %s %s' % (hostname, ' '.join(aliaslist), ' '.join(aliaslist))

def handler_dns_dns(type, source, parameters):
    if parameters.strip():
        result = dns_query(parameters)
        return reply(type, source, result)
    else:
        return reply(type, source, l('Invalid syntax!'))

register_command_handler(handler_dns_dns, 'dns', 10)
