# -*- coding: utf-8 -*-

#  fatal plugin
#  isidabot plugin

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
from .isidacore import *

def load_isida_plugins():
    for params in executes:
        caccess = params[0]
        cmdname = params[1]
        cmdfunc = params[2]
        cmdtype = params[3]
        cmddesc = params[4]

        ncmname = '%s' % (cmdname)

        caccess = ftiacc[caccess]

        set_fatal_var('isida_help', ncmname, 'desc', cmddesc)

        func_str = "def %s(ctype, source, parameters):ctypes = {'public': \
            'groupchat', 'private': 'chat', 'console': 'console', 'null': 'null'}; \
                ctype = ctypes[ctype];jid = source[1];nick = source[2];%s"

        func_name = 'isida_%s_cmd_handler' % (cmdname)

        if cmdtype == 1:
            execstr = '%s(ctype, jid, nick)' % (cmdfunc.__name__)

            func_str = func_str % (func_name, execstr)

            exec(func_str, globals())
        elif cmdtype == 2:
            execstr = '%s(ctype, jid, nick, parameters)' % (cmdfunc.__name__)

            func_str = func_str % (func_name, execstr)

            exec(func_str, globals())

        gbvr = globals()
            
        register_command_handler(gbvr[func_name], ncmname, caccess)

    for param in msgs_hnd:
        msgfunc = param
        hndname = msgfunc.__name__
        
        func_name = 'isida_%s_msg_handler' % (hndname)

        func_str = "def %s(ctype, source, body):ctypes = {'public': \
            'groupchat', 'private': 'chat', 'console': 'console', 'null': 'null'}; \
                ctype = ctypes[ctype]; global selfjid; selfjid = get_client_id();jid = \
                    get_true_jid(source); room = source[1];nick = source[2];%s"

        execstr = '%s(room, jid, nick, ctype, body)' % (hndname)

        func_str = func_str % (func_name, execstr)

        exec(func_str, globals())

        gbvr = globals()

        register_message_handler(gbvr[func_name])

def load_isida_lc_strings():
    locale = get_sys_lang()
    locale = get_param('locale', locale)

    lcfn = '%s.txt' % (locale)

    lcfile = lcdir % (lcfn)

    isiLocale.msgsLoad(lcfile)

def load_isida_help():
    isihlp = get_fatal_var('isida_help')

    for hnam in isihlp:
        desc = isihlp[hnam]['desc']

        add_help_sect(hnam, 'desc', L(desc))
        add_help_sect(hnam, 'ccat', ('*', 'all', 'isida'))

def set_isida_cfg_params(gch):
    if not param_exists(gch, 'url_title'):
        set_gch_param(gch, 'url_title', '1')
    if not param_exists(gch, 'content_length'):
        set_gch_param(gch, 'content_length', '1')

load_isida_plugins()
load_isida_lc_strings()

register_stage0_init(load_isida_help)
register_stage1_init(set_isida_cfg_params)

