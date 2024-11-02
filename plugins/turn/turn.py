# -*- coding: utf-8 -*-

#  fatal plugin
#  turn plugin

#  Initial Copyright © 2008 dimichxp <dimichxp@gmail.com>
#  Idea © 2008 Als <Als@exploit.in>
#  Copyright © 2024 GigaChat
#  Copyright © 2009-2024 Ancestors Soft

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
from functools import reduce

def fix_en_to_ru_layout(text):
    # Создаем словарь для замены символов
    replacements = {
        'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н',
        'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', 'a': 'ф', 's': 'ы',
        'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л',
        'l': 'д', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и',
        'n': 'т', 'm': 'ь', '[': 'х', ']': 'ъ', ';': 'ж', '\'': 'э',
        ',': 'б', '.': 'ю', '/': '.', '\\': '/', '~': 'Ё', '{': 'Х',
        '+': 'Ё', ':': 'Ж', '"': 'Э', '<': 'Б', '>': 'Ю', '?': ',', 
        '&': '?'
    }
    
    # Проходимся по каждому символу строки и заменяем его согласно словарю
    fixed_text = []
    for char in text:
        if char.lower() in replacements:
            replacement_char = replacements.get(char.lower())
            if char.isupper():
                replacement_char = replacement_char.upper()
            fixed_text.append(replacement_char)
        else:
            fixed_text.append(char)
            
    return ''.join(fixed_text)

def fix_ru_to_en_layout(text):
    # Создаем словарь для замены символов
    layout_map = {
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y',
        'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p', 'ф': 'a', 'ы': 's',
        'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k',
        'д': 'l', 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b',
        'т': 'n', 'ь': 'm', 'х': '[', 'ъ': ']', 'ж': ';', 'э': '\'',
        'ю': '.', 'б': ',', 'ё': '`'
    }
    
    fixed_text = []
    for char in text:
        if char in layout_map:
            fixed_char = layout_map.get(char)
            if char.isupper():
                fixed_char = fixed_char.upper()
            fixed_text.append(fixed_char)
        else:
            fixed_text.append(char)
            
    return ''.join(fixed_text)

def handler_turn_last(type, source, parameters):
    cid = get_client_id()
    
    nick = source[2]
    groupchat = source[1]
    jid = get_true_jid(source)
    
    nicks = tuple(get_fatal_var(cid, 'gchrosters', groupchat))
    
    if parameters:
        rep = fix_en_to_ru_layout(parameters)
        
        if rep == parameters:
            rep = fix_ru_to_en_layout(parameters)
        
        return reply(type, source, rep)
    else:
        if not is_var_set(cid, 'turn_msgs', groupchat, jid):
            return reply(type, source, l('Unable to perform this operation!'))

        tmsg = rmv_fatal_var(cid, 'turn_msgs', groupchat, jid)

        nck = ''
        dlm = ':'
        sst = ''

        for ni in nicks:
            if tmsg.startswith(ni):
                nck = ni
                
                mspl = tmsg.split(ni)
                
                sst = mspl[1].strip()
                
                if sst.startswith(',') or sst.startswith(':'):
                    dlm = sst[0]
                    sst = sst[1:].strip()

        if nck:
            rep = fix_en_to_ru_layout(sst)
            rep = '%s%s %s' % (nck, dlm, rep)
            
            if rep == tmsg:
                rep = fix_ru_to_en_layout(sst)
                rep = '%s%s %s' % (nck, dlm, rep)
        else:
            rep = fix_en_to_ru_layout(tmsg)
            
            if rep == tmsg:
                rep = fix_ru_to_en_layout(tmsg)
        
        return msg(groupchat, rep)

def handler_turn_save_msg(type, source, body):
    cid = get_client_id()
    
    nick = source[2]
    groupchat = source[1]
    jid = get_true_jid(source)
    bjid = get_client_id()
    cprfx = get_comm_prefix(groupchat)
    bsplt = body.split(' ', 1)
    
    if bsplt[0] != '%sturn' % (cprfx):
        if jid != groupchat and jid != bjid:
            set_fatal_var(cid, 'turn_msgs', groupchat, jid, body)

register_message_handler(handler_turn_save_msg)

register_command_handler(handler_turn_last, 'turn', 10)
