#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 diSabler <dsy@dsy.name>                               #
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

last_urls_watch = []
url_watch_ignore = ['pdf','sig','spl','class','ps','torrent','dvi','gz','pac','swf','tar','tgz','tar','zip','mp3','m3u','wma',\
					'wax','ogg','wav','gif','jar','jpg','jpeg','png','xbm','xpm','xwd','css','asc','c','cpp','log','conf','text',\
					'txt','dtd','xml','mpeg','mpg','mov','qt','avi','asf','asx','wmv','bz2','tbz','tar','so','dll','exe','bin',\
					'img','usbimg','rar','deb','rpm','iso','ico','apk','patch','svg','7z','tcl']

def rss_search(type, jid, nick, text):
	if text:
		if not re.findall('^http(s?)://',text[:10]): text = 'http://%s' % text
		text = enidna(text)
		msg, result = get_opener(text)
		if result:
			msg = L('Bad url or rss/atom not found!')
			page = remove_sub_space(html_encode(load_page(text)))
			page = get_tag(page,'head')
			l = []
			while '<link' in page:
				lnk = get_tag_full(page,'link')
				page = page.replace(lnk,'')
				l.append(lnk)
			if l:
				m = []
				for t in l:
					rss_type = get_subtag(t,'type')
					if rss_type in ['application/rss+xml','application/atom+xml']:
						if rss_type == 'application/rss+xml': rss_type = 'RSS'
						else: rss_type = 'ATOM'
						rss_title = get_subtag(t,'title')
						rss_href = get_subtag(t,'href')
						if rss_href == '/': rss_href = '/'.join(text.split('/',3)[:3]) + rss_href
						m.append('[%s] %s - %s' % (rss_type,rss_href,rss_title))
				if m:
					m = '\n'.join(m)
					msg = L('Found feed(s):%s%s') % ([' ','\n']['\n' in m],unescape(m))
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

def www_isdown(type, jid, nick, text):
	text = text.strip().lower()
	if text:
		if not re.findall('^http(s?)://',text[:10]): text = 'http://%s' % text
		_,result = get_opener(enidna(text))
		if result: msg = L('It\'s just you. %s is up.') % text
		else: msg = L('It\'s not just you! %s looks down from here.') % text
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

def netheader(type, jid, nick, text):
	if text:
		try:
			regex = text.split('\n')[0].replace('*','*?')
			text = text.split('\n')[1]
		except: regex = None
		if not re.findall('^http(s?)://',text[:10]): text = 'http://%s' % text
		body, result = get_opener(enidna(text))
		if result: body = '%s\n%s' % (text,str(body.headers))
		if regex:
			try:
				mt = re.findall(regex, body, re.S+re.U+re.I)
				if mt != []: body = ''.join(mt[0])
				else: body = L('RegExp not found!')
			except: body = L('Error in RegExp!')
		body = deidna(body)
	else: body = L('What?')
	send_msg(type, jid, nick, body)

def netwww(type, jid, nick, text):
	if text:
		try:
			regex = text.split('\n')[0].replace('*','*?')
			text = text.split('\n')[1]
		except: regex = None
		if not re.findall('^http(s?)://',text[:10]): text = 'http://%s' % text
		text = enidna(text)
		msg, result = get_opener(text)
		if result:
			page = remove_sub_space(html_encode(load_page(text)))
			if regex:
				try:
					mt = re.findall(regex, page, re.S+re.U+re.I)
					if mt != []: msg = unhtml_hard(''.join(mt[0]))
					else: msg = L('RegExp not found!')
				except: msg = L('Error in RegExp!')
			else:
				msg = urllib.parse.unquote(unhtml_hard(page).encode('utf8')).decode('utf8', 'ignore')
				if '<title' in page: msg = '%s\n%s' % (rss_replace(get_tag(page,'title')), msg)
	else: msg = L('What?')
	send_msg(type, jid, nick, msg[:msg_limit])

def parse_url_in_message(room,jid,nick,type,text):
	global last_urls_watch
	urls_watch = []
	titleLoc = L('Title: %s')[:L('Title: %s').find(':')]
	message = ''
	if type != 'groupchat' or text == 'None' or nick == '' or getRoom(jid) == getRoom(selfjid): return
	#if get_level(room,nick)[0] < 4: return
	if '%%' in text: return
	if ' ' in text: return
	links = re.findall(r'(http[s]?://\S*)',text)
	
	urlCount = 0
	for link in links:
		was_shown = False
		urlCount += 1
		if get_config(getRoom(room),'url_title'):
			try:
				if link and link not in urls_watch and link not in last_urls_watch and pasteurl not in link:
					ll = link.lower()
					for t in url_watch_ignore:
						if ll.endswith('.%s' % t): raise
					link = enidna(link)
					urls_watch.append(link)
					for tries in range(3):
						original_page = load_page(urllib.request.Request(link))
						page = html_encode(original_page)
						if '<title' in page.lower(): break
						time.sleep(1)
					if '<title' in page: tag = 'title'
					elif '<TITLE' in page: tag = 'TITLE'
					else: raise
					text = remove_sub_space(get_tag(page,tag).replace('\n',' ').replace('\r',' ').replace('\t',' '))
					while '  ' in text: text = text.replace('  ',' ')
					if text:
						cnt = 0
						for tmp in text: cnt += int(ord(tmp) in [1056,1057])
						if cnt >= len(text)/3: text = remove_sub_space(html_encode(get_tag(original_page,tag)).replace('\n',' ').replace('\r',' ').replace('\t',' '))
					if text:
						was_shown = True
						if urlCount == 1:
							message += '%s: %s' % (titleLoc, rss_del_html(rss_replace(text)))
						else:
							message += '\n%s (%d): %s' % (titleLoc, urlCount, rss_del_html(rss_replace(text)))
						
			except: pass
			if not was_shown and get_config(getRoom(room),'content_length'):
				try:
					if link and link not in urls_watch and link not in last_urls_watch and pasteurl not in link:
						is_file = False
						ll = link.lower()
						for t in url_watch_ignore:
							if ll.endswith('.%s' % t):
								is_file = True
								break
						if is_file:
							urls_watch.append(enidna(link))
							body, result = get_opener(enidna(link))
							pprint('Show content length: %s in %s' % (link,room),'white')
							if result:
								body = str(body.headers)
								mt = float(re.findall('Content-Length.*?([0-9]+)', body, re.S+re.U+re.I)[0])

							if urlCount == 1:
								if mt: message += (L('Length of %s is %s') % ('…/%s' % urllib.parse.unquote(enidna(link).rsplit('/',1)[-1]).decode('utf-8'),get_size_human(mt)))
							else:
								if mt: message += ('\n' + L('Length (%d) of %s is %s') % (urlCount, '…/%s' % urllib.parse.unquote(enidna(link).rsplit('/',1)[-1]).decode('utf-8'),get_size_human(mt)))
				except: pass
	if message:
		send_msg(type, room, '', message)
		last_urls_watch = urls_watch
global execute

message_act_control = [parse_url_in_message]

execute = [(3, 'www', netwww, 2, L('Show web page.\nwww regexp\n[http://]url - page after regexp\nwww [http://]url - without html tags')),
		   (3, 'header', netheader, 2, L('Show net header')),
		   (3, 'isdown', www_isdown, 2, L('Check works site')),
		   (4, 'rss_search', rss_search, 2, L('Search RSS/ATOM feeds'))]
