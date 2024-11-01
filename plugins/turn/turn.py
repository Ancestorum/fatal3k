# -*- coding: utf-8 -*-

#  fatal plugin
#  turn plugin

#  Initial Copyright © 2008 dimichxp <dimichxp@gmail.com>
#  Idea © 2008 Als <Als@exploit.in>
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
        '+': 'Ё', ':': 'Ж', '"': 'Э', '<': 'Б', '>': 'Ю', '?': '.'
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

def handler_turn_last(type, source, parameters):
    cid = get_client_id()
    
    global_en2ru_table = dict(list(zip("qwertyuiop[]asdfghjkl;'zxcvbnm,./`йцукенгшщзхъфывапролджэячсмитьбю.ёQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё", "йцукенгшщзхъфывапролджэячсмитьбю.ёqwertyuiop[]asdfghjkl;'zxcvbnm,./`ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ЁQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~")))

    nick = source[2]
    groupchat = source[1]
    jid = get_true_jid(source)
    
    if parameters:
        rep = fix_en_to_ru_layout(parameters)
        
        return reply(type, source, rep)
    else:
        if not is_var_set(cid, 'turn_msgs', groupchat, jid):
            return reply(type, source, l('Unable to perform this operation!'))

        tmsg = rmv_fatal_var(cid, 'turn_msgs', groupchat, jid)

        rep = fix_en_to_ru_layout(tmsg)
        
        return reply(type, source, rep)

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
