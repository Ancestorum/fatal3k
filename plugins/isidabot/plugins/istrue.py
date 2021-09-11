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

def is_valid(type, jid, nick, text):
	if text == '': text = nick
	ru_lit, en_lit, caps_lit = 0, 0, 0
	for tmp in text:
		if re.match('[a-z]|[A-Z]',tmp): en_lit+=1
		elif re.match('[а-яё]|[А-ЯЁ]',tmp): ru_lit+=1
		if re.match('[A-Z]|[А-ЯЁ]',tmp): caps_lit+=1
	lt = len(text)
	if ru_lit<en_lit: idx, hl = float(ru_lit)/en_lit, 1
	elif ru_lit>en_lit: idx, hl = float(en_lit)/ru_lit, 2
	else: idx, hl = 0.5, None
	if (ru_lit == lt or en_lit == lt) and float(caps_lit)/lt <= 0.5: msg = L('100% True-nick!')
	elif ru_lit+en_lit == 0: msg = L('Nicks without letters isn\'t true!')
	elif ru_lit+en_lit+text.count(' ')+text.count('.') == lt: msg = L('Valid of nick is - %s%s') % (100-int(idx*100), '%!')
	elif not ru_lit or not en_lit: msg = L('Normal nick, but left symbols in fireplace.')
	else: msg = L('Valid of nick is - %s%s') % (int(float(ru_lit+en_lit)/lt*100-int(idx*100)), '%!')
	if float(caps_lit)/lt > 0.5: msg += ' ' + L('Many caps - %s%s') % (int(float(caps_lit)/lt*100), '%!')
	if ru_lit+en_lit:
		msg += ' ' + L('Dominate letters:') + ' '
		if hl == 1: msg += L('Latin')
		elif hl == 2: msg += L('Cyrillic')
		else: msg += L('Equally')
	send_msg(type, jid, nick, msg)

def is_true(type, jid, nick, text):
	if text == '': msg = L('And?')
	else:
		idx = 0
		for tmp in text: idx += ord(tmp)
		msg = L('Expression is true for %s%s') % (idx % 100, '%')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'true', is_true, 2, L('Check truth of expession.')),
		   (3, 'valid', is_valid, 2, L('Check different languages symbols in nick.'))]
