#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 diSabler <dsy@dsy.name>                               #
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

def jc(type, jid, nick, text):
	if not len(text): text = getName(jid)
	try:
		body = json.loads(html_encode(load_page('http://jc.jabber.ru/search.html?%s'.encode("utf-8") % (urllib.parse.urlencode({'json':'1', 'search':text.encode("utf-8")})))))
		if body['result']: msg = L('Found:') + ''.join(['\n%s. %s [%s] %s' % ([t['raiting'],'-'][t['raiting']==''],t['description'],t['jid'],t['current']) for t in body['result']])
		else: msg = L('Not found.')
	except: msg = L('Error!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'jc', jc, 2, L('Show information about conference from jc.jabber.ru.\njc [address]'))]
