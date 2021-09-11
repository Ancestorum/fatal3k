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

from xml.dom.minidom import parseString

def flibusta(type, jid, nick, text):
    text = re.sub(' +', ' ', text).strip()
    msg = ''
    if text == 'new':
        c=urllib.request.urlopen('http://xpresslib.mobile-master.org/new').read()
        xml=parseString(c)
        nodes=xml.getElementsByTagName('book')
        for el in nodes:
            f=el.getAttribute('file')
            size=el.getAttribute('size')
            author=str(el.getAttribute('author'))
            title=str(el.firstChild.data)
            msg += '\n%s - %s, %s кБ, http://flibusta.net/b/%s' % (author,title,round(float(size)/1024,1),f.split('.')[0]+'/fb2')
        if not msg: msg = L('No news')
    else:
        opt = [i for i in (' ' + text).split(' -') if len(i)>2 and i[1]==' ']
        opt = dict([i.split(' ', 1) for i in opt])
        if 'n' in opt:
            if re.match('\d+$', opt['n']): a = b = int(opt['n'])
            elif re.match('\d+-\d+$', opt['n']): a, b = list(map(int,opt['n'].split('-')))
            else: a, b = 1, 5
        else: a, b = 1, 5
        if 't' in opt:
            i={}
            i['search']=opt['t'].encode('utf-8')
            d=urllib.parse.urlencode(i)
            s=urllib.request.urlopen('http://xpresslib.mobile-master.org/search',d).read()
            xml=parseString(s)
            nodes=xml.getElementsByTagName('book')
            t_book=[]
            for el in nodes:
                f0=el.getAttribute('file')
                size=el.getAttribute('size')
                author=str(el.getAttribute('author'))
                title=str(el.firstChild.data)
                t_book.append([author,title,size,f0])
            if 'a' in opt: t_book = [x for x in t_book if opt['a'].lower() in x[0].lower()]
            if t_book:
                c = len(t_book)
                if b > c:
                    if b != a:  b = c
                    else: a = b = c
                msg += L('Total found %s matches. Result(s) %s:\n') % (c, a if a == b else '%s-%s' % (a,b))
                for i in t_book[a-1:b]:
                    msg += '%s- %s, %s кБ, http://flibusta.net/b/%s\n' % (i[0],i[1],round(float(i[2])/1024,1),i[3].split('.')[0]+'/fb2')
        elif 'a' in opt:
            i={}
            i['search']=opt['a'].encode('utf-8')
            d=urllib.parse.urlencode(i)
            s=urllib.request.urlopen('http://xpresslib.mobile-master.org/authors',d).read()
            xml=parseString(s)
            nodes=xml.getElementsByTagName('author')
            a_book=[]
            for el in nodes:
                id=el.getAttribute('id')
                title=str(el.firstChild.data)
                a_book.append([id,title])
            if a_book:
                c = len(a_book)
                if b > c:
                    if b != a:  b = c
                    else: a = b = c
                msg += L('Total found %s matches. Result(s) %s:\n') % (c, a if a == b else '%s-%s' % (a,b))
                for i in a_book[a-1:b]:
                    msg += '%s- http://flibusta.net/a/%s\n' % (i[1], i[0])

    if not msg: msg = L('What?')
    send_msg(type, jid, nick, msg)



global execute

execute = [(3, 'flibusta', flibusta, 2, L('Search books and authors on flibusta.net.\nflibusta [-a author] [-t title] [-n number of result]'))]
