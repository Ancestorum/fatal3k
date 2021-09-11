# -*- coding: utf-8 -*-

#  fatal plugin
#  fact plugin

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

def get_tld_info(query):
    query = query.replace('"', '&quot;')
    query = query.lower()

    sql = "SELECT name FROM tlds WHERE tld='%s';" % (query)
    qres = sqlquery('static/tlds.db', sql)
    
    if not qres:
        sql = "SELECT tld FROM tlds WHERE name LIKE '%s%%';" % (query)
        qres = sqlquery('static/tlds.db', sql)
    
    if qres:
        info = qres[0][0]
        
        return info.replace('&quot;', '"')
    else:
        return ''

def handler_fact_tld(type, source, parameters):
    if parameters:
        result = get_tld_info(parameters.strip())
        
        if not result:
            result = l('Not found!')
        
        return reply(type, source, result)
    else:
        return reply(type, source, l('Invalid syntax!'))

register_command_handler(handler_fact_tld, 'tld', 10)
