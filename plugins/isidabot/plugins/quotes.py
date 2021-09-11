#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 Vit@liy <vitaliy@root.ua>                             #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

try: quotes_list = json.loads(readfile(data_folder % 'quotes.txt'),encoding='utf-8')
except:
    raise
    quotes_list = {'bash':
        {'title': 'bash.org.ru - Цитатник Рунета',
        'random': ['http://bash.org.ru/random', '<div\ class="text">((?:.|\\s)+?)</div>'],
        'number': ['http://bash.org.ru/quote/%s', '<div\ class="text">((?:.|\\s)+?)</div>']}}

def quote(type, jid, nick, text):
    global quotes_list
    tmp = text.strip().split()
    if not tmp: tmp =[random.choice([q for q in list(quotes_list.keys()) if 'random' in quotes_list[q]])]
    if len(tmp) == 1 and tmp[0] == 'list':
        msg = (L('Quotes:\n') + '\n'.join(['%s - %s (%s)' % (q, quotes_list[q]['title'],
        ', '.join(k for k  in list(quotes_list[q].keys()) if k != 'title').replace('random', L('rand')).replace('number', L('by number')).replace('search', L('search')))
        for q in list(quotes_list.keys())]))
    elif len(tmp) == 1 and tmp[0] in quotes_list and 'random' in quotes_list[tmp[0]]:
        try:
            url = quotes_list[tmp[0]]['random'][0]
            body = html_encode(load_page(url))
            message = re.search(unescape(quotes_list[tmp[0]]['random'][1]), body).group(1)
            msg = unhtml(message)
        except:
            msg = L('Can\'t searching random quote!')
    elif len(tmp) > 1 and tmp[0] in quotes_list and 'number' in quotes_list[tmp[0]] and re.match('\d+\Z', tmp[1]):
        try:
            url = quotes_list[tmp[0]]['number'][0] % tmp[1]
            body = html_encode(load_page(url))
            message = re.search(unescape(quotes_list[tmp[0]]['number'][1]), body).group(1)
            msg = unhtml(message)
            if not msg:
                msg = L('Can\'t searching quote by number!')
        except:
            msg = L('Can\'t searching quote by number!')
    elif len(tmp) > 1 and tmp[0] in quotes_list and 'search' in quotes_list[tmp[0]]:
        try:
            url = quotes_list[tmp[0]]['search'][0] % urllib.parse.quote(tmp[1].encode(quotes_list[tmp[0]]['search'][2]))
            body = html_encode(load_page(url))
            message = re.search(unescape(quotes_list[tmp[0]]['search'][1]), body).group(1)
            msg = unhtml(message)
        except:
            msg = L('Quote not found!')
    else:
        msg = L('What?')
    send_msg(type, jid, nick, msg)


def ithap(type, jid, nick, text): quote(type, jid, nick, 'ithap %s' % text)

def afor(type, jid, nick): quote(type, jid, nick, 'afor')
	
global execute

execute = [(3, 'quote', quote, 2, L('Quote from Internet. Exaples:\nquote list - list of resources\nquote [<key> [number|text]]')),
		(3, 'ithap', ithap, 2, L('Quote from ithappens.ru\nithap [number]')),
		(3, 'afor', afor, 1, L('Show random aphorism from skio.ru'))]
