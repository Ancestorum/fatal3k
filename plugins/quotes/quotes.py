# -*- coding: utf-8 -*-

#  fatal plugin
#  quotes plugin

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

from fatalapi import *

import urllib.request, urllib.error, urllib.parse
import re

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')

def handler_bashorgru_get(type, source, parameters):
    if parameters.strip() == '':
        req = urllib.request.Request('http://bash.im/random')
    else:
        req = urllib.request.Request('http://bash.im/quote/%s' % (parameters.strip()))
        req.add_header = ('User-agent', 'Mozilla/5.0')
        
    try:
        r = urllib.request.urlopen(req)
        target = r.read()
        """link to the quote"""
        od = re.search(r'class="id">', target)
        b1 = target[od.end():]
        b1 = b1[:re.search(r'</a>', b1).start()]
        b1 = strip_tags.sub('', b1.replace('\n', ''))
        b1 = b1.replace('#', '')
        b1 = 'http://bash.im/quote/' + b1 + '\n\n'
        """quote"""
        od = re.search(r'class="id">.*?</a>.*?</div>.*?<div class="text">(.*?)</div>', target, re.DOTALL)
        message = b1 + od.group(1)
        message = decode(message)
        message = message.strip()
        
        return reply(type, source, str(message, 'windows-1251'))
    except Exception:
        return reply(type, source, l('Unknown error!'))

def handler_bashorgru_abyss_get(type, source, parameters):
    if parameters.strip() == '':
        req = urllib.request.Request('http://bash.im/abysstop')
    else:
        return reply(type, source, l('This resource does not support quotes numbers!'))
        
    req.add_header = ('User-agent', 'Mozilla/5.0')
    
    try:
        r = urllib.request.urlopen(req)
        target = r.read()
        aqid = str(random.randrange(1, 25))
        b1 = 'http://bash.im/abysstop\n\n'
        od = re.search('class="abysstop">#' + aqid + '</span>', target)
        q1 = target[od.end():]
        od = re.search(r'<div class="text">(.*?)</div>', q1, re.DOTALL)
        message = b1 + od.group(1)
        message = decode(message)

        return reply(type, source, str(message, 'windows-1251'))
    except Exception:
        return reply(type, source, l('Unknown error!'))

def decode(text):
    return strip_tags.sub('', text.replace('<br />', '\n').replace('<br>', '\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t', '').replace('||||:]', '').replace('>[:\n', '')

register_command_handler(handler_bashorgru_get, 'bor', 10)
register_command_handler(handler_bashorgru_abyss_get, 'borb', 10)
