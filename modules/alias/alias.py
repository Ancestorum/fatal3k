# -*- coding: utf-8 -*-

#  fatal module
#  alias.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Copyright © 2009-2025 Ancestors Soft

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import os
import random
import re
import sqlite3 as db
import threading
from threading import Lock
from contextlib import contextmanager
import fatalapi as fapi

def rmv_empty_items(lst):
    if lst:
        lst = [li for li in lst if li and li.strip()]
        return lst
    return []

def alias_exists(alias, gch=''):
    sql = 'SELECT * FROM aliasdb WHERE alias=?;'
    
    cid = fapi.get_client_id()
    
    if gch:
        qres = fapi.sqlquery('dynamic/%s/%s/alias.db' % (cid, gch), sql, alias)
    else:
        qres = fapi.sqlquery('dynamic/%s/alias.db' % (cid), sql, alias)
    
    if qres:
        return True
    else:
        return False

def set_alias(alias, body, gch=''):
    if not alias_exists(alias, gch):
        sql = "INSERT INTO aliasdb (alias, body, access) VALUES (?, ?, '');"
        args = alias.strip(), body.strip()
    else:
        sql = "UPDATE aliasdb SET body=? WHERE alias=?;"
        args = body.strip(), alias.strip()
    
    cid = fapi.get_client_id()
    
    if gch:
        qres = fapi.sqlquery('dynamic/%s/%s/alias.db' % (cid, gch), sql, *args)
    else:
        qres = fapi.sqlquery('dynamic/%s/alias.db' % (cid), sql, *args)
    
    return qres
    
def set_access(alias, access, gch=''):
    access = str(access)
    
    if alias_exists(alias,gch):
        sql = "UPDATE aliasdb SET access=? WHERE alias=?;"
    else:
        return
    
    args = access.strip(), alias.strip()
    
    cid = fapi.get_client_id()
    
    if gch:
        qres = fapi.sqlquery('dynamic/%s/%s/alias.db' % (cid, gch), sql, *args)
    else:
        qres = fapi.sqlquery('dynamic/%s/alias.db' % (cid), sql, *args)
    
    return qres
    
def remove_alias(alias, gch=''):
    sql = "DELETE FROM aliasdb WHERE alias=?;"
    
    cid = fapi.get_client_id()
    
    if gch:
        rep = fapi.sqlquery('dynamic/%s/%s/alias.db' % (cid, gch), sql, alias)
    else:
        rep = fapi.sqlquery('dynamic/%s/alias.db' % (cid), sql, alias)
        
    return rep

def get_alias_list(gch='', oer={}):
    alias_list = {}
    
    sql = "SELECT alias, body FROM aliasdb;"
    
    cid = fapi.get_client_id()
    
    if gch:
        qres = fapi.sqlquery('dynamic/%s/%s/alias.db' % (cid, gch), sql)
    else:
        qres = fapi.sqlquery('dynamic/%s/alias.db' % (cid), sql)
    
    if qres == '':
        return oer
    else:
        if qres:
            for al in qres:
                alias = al[0]
                abody = al[1]
                alias_list[alias] = abody 
            return alias_list
        else:
            return oer

def get_access_list(gch='',oer={}):
    access_list = {}
    
    sql = "SELECT alias, access FROM aliasdb;"
    
    cid = fapi.get_client_id()
    
    if gch:
        qres = fapi.sqlquery('dynamic/%s/%s/alias.db' % (cid, gch), sql)
    else:
        qres = fapi.sqlquery('dynamic/%s/alias.db' % (cid), sql)
    
    if qres == '':
        return oer
    else:
        if qres:
            for acc in qres:
                acc = list(acc)
                if acc[1].isdigit():
                    acc[1] = int(acc[1])
                else:
                    acc[1] = -1
                access_list[acc[0]] = acc[1]
            return access_list
        else:
            return oer

def shell_esc(s):
    for c in [';', '&', '|', '`', '$']:
        s = s.replace(c, '#')
    return s

def xml_esc(s):
    s = s.replace('\'', '&apos;')
    s = s.replace('>', '&gt;')
    s = s.replace('<', '&lt;')
    s = s.replace('&', '&amp;')
    s = s.replace('\"', '&quot;')
    return s
    
def alias_get_rand(args, source):
    try:
        f = int(args[0])
        t = int(args[1])
        return str(random.randrange(f, t))
    except:
        return ''

def alias_def_val(args, source):
    try:
        val = args[0]
        dvl = args[1]
        
        if not val.strip():
            return dvl
        return val
    except:
        return ''

def alias_replace(args, source):
    try:
        rstr = args[0]
        sfro = args[1]
        srto = args[2]
        return rstr.replace(sfro, srto)
    except:
        return ''

def alias_eval_func(args, source):
    try:
        rstr = args[0].strip()
        sfro = args[1].strip()
        
        return str(eval(str("%s(%s)" % (rstr,sfro))))
    except:
        return '[error]'

def alias_shell_escape(args, source):
    return shell_esc(args[0])

def alias_xml_escape(args, source):
    return xml_esc(args[0])

def alias_context(args, source):
    arg = args[0]
    conf = source[1]
    nick = source[2]
    
    if arg == 'conf':
        return xml_esc(conf)
    elif arg == 'nick':
        return xml_esc(nick)
    elif arg == 'conf_jid':
        return xml_esc('%s/%s' % (conf, nick))
    else:
        return ''
        
class AliasCommands:
    commands = {'replace':      [3, alias_replace     ],
                'rand':         [2, alias_get_rand    ],
                'defval':       [2, alias_def_val     ],
                'func':         [2, alias_eval_func   ],
                'shell_escape': [1, alias_shell_escape],
                'xml_escape':   [1, alias_xml_escape  ],
                'context':      [1, alias_context     ]}
    
    def map_char(self, x, i):
        st = i['state']
        
        if i['esc']:
            i['esc'] = False
            ret = i['level']
        elif x == '\\':
            i['esc'] = True
            ret = 0
        elif x == '%':
            i['state'] = 'cmd_p'
            ret = 0
        elif x == '(':
            if i['state'] == 'cmd_p':
                i['level'] += 1
                i['state'] = 'args'
            ret = 0
        elif x == ')':
            if i['state'] == 'args':
                i['state'] = 'null'
            ret = 0
        else:
            if i['state'] == 'args':
                ret = i['level']
            else:
                i['state'] = 'null'
                ret = 0
        return ret

    def get_map(self, inp):
        i = {'level': 0, 'state': 'null', 'esc': False}
        return [self.map_char(x, i) for x in list(inp)]
    
    def parse_cmd(self, me):
        i = 0
        m = self.get_map(me)
        args = [''] * max(m)
        
        while i < len(m):
            if m[i] != 0:
                args[m[i]-1] += me[i]
            i += 1
        return args
        
    def execute_cmd(self, cmd, args, source):
        if cmd in self.commands:
            if self.commands[cmd][0] <= len(args):
                return self.commands[cmd][1](args, source)
        return ''
        
    def proccess(self, cmd, source):
        command = cmd[0]
        args = cmd[1:]
        return self.execute_cmd(command, args, source)

class Alias:
    def __init__(self):
        self.galiaslist = {}
        self.gaccesslist = {}
        
        self.aliaslist = {}
        self.accesslist = {}
        self.aliascmds = AliasCommands()

    def init(self, gch=''):
        self.galiaslist = get_alias_list()
        self.gaccesslist = get_access_list()
        
        ali = get_alias_list(gch = gch)
        
        if ali:
            self.aliaslist[gch] = ali
        else:
            self.aliaslist[gch] = {}
        
        aliac = get_access_list(gch = gch)
        
        if aliac:
            self.accesslist[gch] = aliac
        else:
            self.accesslist[gch] = {}

    def load(self, gch):
        ali = get_alias_list(gch=gch)
        
        if ali:
            self.aliaslist[gch] = ali
        else:
            self.aliaslist[gch] = {}

        aliac = get_access_list(gch=gch)
        
        if aliac:
            self.accesslist[gch] = aliac
        else:
            self.accesslist[gch] = {}
                
    def add(self, alias, body, gch=''):
        if gch:
            res = set_alias(alias, body, gch)
            
            if res == '':
                return False
            
            if gch not in self.aliaslist:
                self.aliaslist[gch] = {}
                
            self.aliaslist[gch][alias] = body
            
            return True
        else:
            res = set_alias(alias,body)
            
            if res == '':
                return False
            
            self.galiaslist[alias] = body
            
            return True
        
    def remove(self, alias, gch=''):
        if gch:
            res = remove_alias(alias, gch)
            
            if res == '':
                return False
            
            if alias in self.aliaslist[gch]:
                del self.aliaslist[gch][alias]
            
            return alias_exists(alias,gch)
        else:
            res = remove_alias(alias)
            
            if res == '':
                return False
            
            if alias in self.galiaslist:
                del self.galiaslist[alias]
                
            return alias_exists(alias)

    def map_char(self, x, i):
        ret = i['level']
        
        if i['esc']:
            i['esc'] = False
        elif x == '\\':
            i['esc'] = True
            ret = 0
        elif x == '=':
            if ret < 3:
                i['larg'] = not i['larg']
                i['level'] += 1
                ret = 0
        elif x == ' ':
            if not i['larg']:
                i['level'] += 1
        return ret

    def get_map(self, inp):
        i = {'larg': False, 'level': 1, 'esc': False}
        return [self.map_char(x, i) for x in list(inp)]
    
    def parse_cmd(self, me):
        i = 0
        m = self.get_map(me)
        
        if not m: 
            return []
        
        args = [''] * max(m)
        
        while i < len(m):
            if m[i] != 0:
                args[m[i] - 1] += me[i]
                
            i += 1
            
        if args:
            args = [arli.strip() for arli in args if arli]
            
        return args

    def expand(self, cmd, source):
        if type(cmd) is None:
            return ''
            
        exp = ''
        cl = self.parse_cmd(cmd)
        cl = rmv_empty_items(cl)
        
        if (len(cl) < 1):
            return cmd
        
        command = cl[0].split()
        command = command[0]
        args = cl[1:]
        
        try:
            for alias in self.aliaslist[source[1]]:
                if len(command) <= len(alias) and command == alias[:len(alias)]:
                    if self.aliaslist[source[1]][alias]:
                        exp = self.apply(self.aliaslist[source[1]][alias], args, source)
        except:
            pass
        
        try:
            for alias in self.galiaslist:
                if len(command) <= len(alias) and command == alias[:len(alias)]:
                    if self.galiaslist[alias]:
                        exp = self.apply(self.galiaslist[alias], args, source)
        except:
            pass
        
        if not exp:
            return cmd
        
        rexp = self.expand(exp, source)
        
        return rexp
        
    def comexp(self, cmd, source, key=''):
        if type(cmd) is None:
            return ''
            
        cl = self.parse_cmd(cmd)
        
        if (len(cl)<1):
            return cmd
            
        command = cl[0].split(' ')[0]
        args = cl[1:]
        exp = ''
        
        try:
            for alias in self.aliaslist[source[1]]:
                if len(command) <= len(alias) and command == alias[0:len(alias)]:
                    if self.aliaslist[source[1]][alias]:
                        exp = self.apply(self.aliaslist[source[1]][alias], args, source)
        except:
            pass
        
        try:
            for alias in self.galiaslist:
                if len(command) <= len(alias) and command == alias[0:len(alias)]:
                    if self.galiaslist[alias]:
                        exp = self.apply(self.galiaslist[alias], args, source)
        except:
            pass
        
        if not exp:
            return cmd
            
        rexp = self.comexp(exp, source, key)
        
        return rexp
        
    def apply(self, alias, args, source):
        expanded = alias
        expanded = expanded.replace('$*', ' '.join(args));
        m = self.aliascmds.parse_cmd(expanded)
        
        for i in m:
            cmd = [x.strip() for x in i.split(',')]
            
            for j in re.findall('\$[0-9]+', i):
                index = int(j[1:]) - 1
                
                if len(args) <= index:
                    return expanded
                    
                cmd = [x.replace(j, args[index]) for x in cmd]
                
            res = self.aliascmds.proccess(cmd, source)
            
            if res:
                expanded = expanded.replace('%(' + i + ')', res)
        
        for j in re.findall('\$[0-9]+', expanded):
            index = int(j[1:]) - 1
            
            if len(args) <= index:
                return expanded
                
            expanded = expanded.replace(j, args[index])
        
        return expanded
        
    def get_access(self, alias, gch=''):
        if gch in self.accesslist:
            if alias in self.accesslist[gch]:
                return self.accesslist[gch][alias]
            elif alias in self.gaccesslist:
                return self.gaccesslist[alias]
            else:
                return -1
        elif alias in self.gaccesslist:
            return self.gaccesslist[alias]
        else:
            return -1

    def give_access(self, alias, access, gch=''):
        if gch:
            res = set_access(alias, access, gch)
            
            if res == '':
                return False
            
            if gch not in self.accesslist:
                self.accesslist[gch] = {}
            
            self.accesslist[gch][alias] = access
            
            return True
        else:
            res = set_access(alias, access)
            
            if res == '':
                return False
            
            if alias not in self.gaccesslist:
                self.gaccesslist[alias] = alias
                
            self.gaccesslist[alias] = access
            
            return True
            
    def remove_access(self, alias, gch=None):
        if gch:
            if alias in self.accesslist[gch]:
                del self.accesslist[gch][alias]
        else:
            if alias in self.gaccesslist:
                del self.gaccesslist[alias]
