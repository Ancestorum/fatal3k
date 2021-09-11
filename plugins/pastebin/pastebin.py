# -*- coding: utf-8 -*-

#  fatal plugin
#  pastebin plugin

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

paste_private = ('0', '1')
paste_expire_date = ('N', '10M', '1H', '1D', '1M')
paste_format = ('text', 'abap', 'actionscript', 'actionscript3', 'ada', 'apache', 'applescript', 'apt_sources', 'asm', 'asp', 'autoit', 'avisynth', 'bash', 'basic4gl', 'blitzbasic', 'bnf', 'boo', 'bf', 'c', 'c_mac', 'cill', 'csharp', 'cpp', 'caddcl', 'cadlisp', 'cfdg', 'klonec', 'klonecpp', 'cmake', 'cobol', 'cfm', 'css', 'd', 'dcs', 'delphi', 'dff', 'div', 'dos', 'dot', 'eiffel', 'email', 'rlang', 'fo', 'fortran', 'freebasic', 'gml', 'genero', 'gettext', 'groovy', 'haskell', 'hq9plus', 'html4strict', 'idl', 'ini', 'inno', 'intercal', 'io', 'java', 'java5', 'javascript', 'kixtart', 'latex', 'lsl2', 'lisp', 'locobasic', 'lolcode', 'lotusformulas', 'lotusscript', 'lscript', 'lua', 'm68k', 'make', 'matlab', 'mirc', 'modula3', 'mpasm', 'mxml', 'mysql', 'nsis', 'oberon2', 'objc', 'ocaml-brief', 'ocaml', 'glsl', 'oobas', 'oracle8', 'oracle11', 'pascal', 'pawn', 'per', 'perl', 'php', 'php-brief', 'pic16', 'pixelbender', 'plsql', 'povray', 'powershell', 'progress', 'prolog', 'properties', 'providex', 'python', 'qbasic', 'rails', 'rebol', 'reg', 'robots', 'ruby', 'gnuplot', 'sas', 'scala', 'scheme', 'scilab', 'sdlbasic', 'smalltalk', 'smarty', 'sql', 'tsql', 'tcl', 'teraterm', 'thinbasic', 'typoscript', 'unreal', 'vbnet', 'verilog', 'vhdl', 'vim', 'visualprolog', 'vb', 'visualfoxpro', 'whitespace', 'whois', 'winbatch', 'xml', 'xorg_conf', 'xpp', 'z80')

def post_to_pastebin(paste_data):
    if paste_data:
        try:
            enc_paste_data = urllib.parse.urlencode(paste_data)
            
            fpst = urllib.request.urlopen('http://pastebin.com/api/api_post.php', enc_paste_data)
            pst_res = fpst.read()
            
            return pst_res
        except Exception:
            return ''
    else:
        return ''

def read_from_pastebin(pastid):
    if pastid:
        try:
            fpst = urllib.request.urlopen('http://pastebin.com/raw.php?i=%s' % (pastid))
            pst_res = fpst.read()
            
            return pst_res
        except Exception:
            return ''
    else:
        return ''

def handler_pastebin(type, source, parameters):
    def send_paste(paste_data, pst_cod, pst_priv, pst_expd, ppst_fmt):
        paste_data['api_paste_code'] = pst_cod.encode('utf-8')
        paste_data['api_paste_name'] = 'paste%s' % (time.time())
        paste_data['api_paste_private'] = pst_priv
        paste_data['api_paste_expire_date'] = pst_expd
        paste_data['api_paste_format'] = ppst_fmt
                
        pst_res = post_to_pastebin(paste_data)
                
        if pst_res:
            rep = l('Result of query from pastebin.com:\n\n%s') % (pst_res)
        else:
            rep = l('Unknown error!')
            
        return rep

    groupchat = source[1]
    
    if is_groupchat(groupchat):
        pst_priv = get_gch_param(groupchat, 'paste_private', '1')
        pst_expd = get_gch_param(groupchat, 'paste_expire_date', 'N')
        pst_fmt = get_gch_param(groupchat, 'paste_format', 'text')
    else:
        pst_priv = get_param('paste_private', '1')
        pst_expd = get_param('paste_expire_date', 'N')
        pst_fmt = get_param('paste_format', 'text')

    if parameters:
        paste_data = {'api_dev_key': '3c128b5d55e4522ea3bba0e8158ffe81', 'api_option': 'paste', 'api_paste_code': '', 'api_paste_name': '', 'paste_email': '', 'api_paste_expire_date': '', 'api_paste_format': ''}

        splp = safe_split(parameters)
        fsplp = [sli for sli in splp if sli]
        
        if len(fsplp) == 2:
            ppst_fmt = fsplp[0].strip()
            ppst_fmt = ppst_fmt.lower()
            
            pst_cod = fsplp[1].strip()
            
            if ppst_fmt in paste_format:
                rep = send_paste(paste_data, pst_cod, pst_priv, pst_expd, ppst_fmt)            
            else:
                pst_cod = parameters.strip()
                
                rep = send_paste(paste_data, pst_cod, pst_priv, pst_expd, ppst_fmt)        
        elif len(fsplp) == 1:
            pst_cod = fsplp[0].strip()
            
            rep = send_paste(paste_data, pst_cod, pst_priv, pst_expd, ppst_fmt)        
    else:
        pllist = ', '.join(paste_format)
        
        rep = l('Available programming languages for posting (total: %s):\n\n%s.') % (len(paste_format), pllist)

    return reply(type, source, rep)

def handler_pastebin_opt(type, source, parameters):
    groupchat = source[1]

    if parameters:
        splp = safe_split(parameters)
        fsplp = [sli for sli in splp if sli]
        
        if len(fsplp) == 2:
            param = fsplp[0].lower().strip()
            value = fsplp[1].strip()
            
            if param in ['paste_private', 'paste_expire_date', 'paste_format']:
                if param == 'paste_private':
                    if value in paste_private:
                        if is_groupchat(groupchat):
                            set_gch_param(groupchat, 'paste_private', value)
                        else:
                            set_param('paste_private', value)
                        
                        rep = l('Value of option "%s" has been set successfully!') % (param)
                    else:
                        rep = l('Invalid syntax!')
                elif param == 'paste_expire_date':
                    value = value.upper()
                    
                    if value in paste_expire_date:
                        if is_groupchat(groupchat):
                            set_gch_param(groupchat, 'paste_expire_date', value)
                        else:
                            set_param('paste_expire_date', value)
                            
                        rep = l('Value of option "%s" has been set successfully!') % (param)
                    else:
                        rep = l('Invalid syntax!')
                elif param == 'paste_format':
                    value = value.lower()
                    
                    if value in paste_format:
                        if is_groupchat(groupchat):
                            set_gch_param(groupchat, 'paste_format', value)
                        else:
                            set_param('paste_format', value)
                            
                        rep = l('Value of option "%s" has been set successfully!') % (param)
                    else:
                        rep = l('Invalid syntax!')
            else:
                rep = l('Invalid syntax!')
        elif len(fsplp) == 1:
            param = fsplp[0].lower().strip()
            
            if param in ['paste_private', 'paste_expire_date', 'paste_format']:
                if param == 'paste_private':
                    if is_groupchat(groupchat):
                        value = get_gch_param(groupchat, 'paste_private', '1')
                    else:
                        value = get_param('paste_private', '1')
                    
                    rep = l('Value of option "%s" is set to "%s"!') % (param, value)
                elif param == 'paste_expire_date':
                    if is_groupchat(groupchat):
                        value = get_gch_param(groupchat, 'paste_expire_date', 'N')
                    else:
                        value = get_param('paste_expire_date', 'N')
                        
                    rep = l('Value of option "%s" is set to "%s"!') % (param, value)
                elif param == 'paste_format':
                    if is_groupchat(groupchat):
                        value = get_gch_param(groupchat, 'paste_format', 'text')
                    else:
                        value = get_param('paste_format', 'text')
                        
                    rep = l('Value of option "%s" is set to "%s"!') % (param, value)
            else:
                rep = l('Invalid syntax!')
    else:
        pllist = ', '.join(['paste_private', 'paste_expire_date', 'paste_format'])
        
        rep = l('Available options to set up (total: 3):\n\n%s.') % (pllist)

    return reply(type, source, rep)

def handler_pastebin_read(type, source, parameters):
    if parameters:
        spurl = parameters.split('/')
        pstid = spurl[-1]
        res = read_from_pastebin(pstid)
        
        if len(spurl) > 1 and not 'pastebin.com' in spurl:
            rep = l('Unknown URL!')
        else:
            if res:
                if res.count('Unknown Paste ID'):
                    rep = l('Unknown paste Id!')
                else:
                    rep = l('Result of query from pastebin.com:\n\n%s') % (res)
            else:
                rep = l('Unknown error!')
    else:
        rep = l('Invalid syntax!')
        
    return reply(type, source, rep)
        

def init_pastebin_params():
    if not param_exists('', 'paste_private'):
        set_param('paste_private', '1')
    if not param_exists('', 'paste_expire_date'):
        set_param('paste_expire_date', 'N')
    if not param_exists('', 'paste_format'):
        set_param('paste_format', 'text')

def get_pastebin_state(gch):
    if not param_exists(gch, 'paste_private'):
        set_gch_param(gch, 'paste_private', '1')
    if not param_exists(gch, 'paste_expire_date'):
        set_gch_param(gch, 'paste_expire_date', 'N')
    if not param_exists(gch, 'paste_format'):
        set_gch_param(gch, 'paste_format', 'text')

register_command_handler(handler_pastebin_read, 'pstget', 11)
register_command_handler(handler_pastebin, 'paste', 11)
register_command_handler(handler_pastebin_opt, 'pstopt', 20)

register_stage0_init(init_pastebin_params)
register_stage1_init(get_pastebin_state)
