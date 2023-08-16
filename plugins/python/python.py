# -*- coding: utf-8 -*-

#  fatal plugin
#  python plugin

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Parts of code Copyright © Bohdan Turkynewych aka Gh0st <tb0hdan[at]gmail.com>
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

import string

from fatalapi import *

def shell_del_specs_sym(s):
    for c in [';', '&', '|', '`', '$', '\\', '>', '<', '\n']:
        s = s.replace(c, ' #')
    return s

def parse_shells(shells):
    if shells:
        parsed = shells.split('&&')
        parsed = strip_list_items(parsed)
        
        for tkn in ['||', '|', ';', '$(', '`']:
            sparsed = []
            for prsd in parsed:
                if tkn == '`':
                    spp = prsd.split(tkn, 1)
                else:
                    spp = prsd.split(tkn)
                
                spp = strip_list_items(spp)
                sparsed.extend(spp)
            parsed = sparsed
        return parsed
    return []

def check_allowed(shells):
    allowed = get_lst_cfg_param('shell_allowed')

    if not allowed:
        return False

    if 'all' in allowed:
        return True

    prsd = parse_shells(shells)
    apro = list(prsd)
    
    for ald in allowed:
        for pr in prsd:
            if pr.startswith(ald):
                apro.remove(pr)

    if not apro:
        return True
        
    return False

def handler_python_ssh(type, source, parameters):
    parameters = shell_del_specs_sym(parameters)
    handler_python_sh(type, source, parameters)

def handler_python_eval(type, source, parameters):
    cid = get_client_id()
    gch = source[1]
    
    try:
        return_value = '%s' % (eval(parameters))
    except:
        return_value = '%s - %s.' % (sys.exc_info()[0], sys.exc_info()[1])
    return reply(type, source, return_value.strip())

def handler_python_exec(type, source, parameters):
    cid = get_client_id()
    gch = source[1]
    
    if '\n' in parameters and parameters[-1] != '\n':
        parameters += '\n'
    try:
        exec(str(parameters), globals())
        return reply(type, source, l('Executed!'))
    except:
        rep = '%s - %s' % (sys.exc_info()[0], sys.exc_info()[1])
        return reply(type, source, rep.strip())

def handler_python_sh(type, source, parameters):
    return_value = ''
    
    start = time.time()
    
    if not check_allowed(parameters):
        return reply(type, source, l('Some of requested operations in your shell-statement are not allowed by administrator!'))
    
    if os.name == 'posix':
        pipe = os.popen('sh -c "%s" 2>&1' % (parameters))
        return_value = pipe.read()
        pipe.close()
    elif os.name == 'nt':
        pipe = os.popen('%s' % (parameters))
        return_value = pipe.read().encode('cp1251').decode('cp866')
        pipe.close()
    
    stop = time.time()
    
    return reply(type, source, l('Shell output result (in: %s sec.):\n\n%s') % (round(stop-start, 3), return_value.strip()))
    
def handler_python_calc(type, source, parameters):
    parameters = parameters.strip()
    
    if '**' in parameters:
        return reply(type, source, l('Invalid operation!'))

    if re.sub('([' + string.digits + ']|[\+\-\/\*\^\.\%\(\)])', '', parameters).strip() == '':
        try:
            return_value = str(eval(parameters))
        except:
            return_value = l('Syntax error!')
    else:
        return_value = l('Invalid syntax!')
    
    return reply(type, source, return_value.strip())

register_command_handler(handler_python_eval, 'eval', 100)
register_command_handler(handler_python_exec, 'exec', 100)
register_command_handler(handler_python_sh, 'sh', 100)
register_command_handler(handler_python_ssh, 'ssh', 100)
register_command_handler(handler_python_calc, 'calc', 11)
