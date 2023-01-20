# -*- coding: utf-8 -*-

#  fatal plugin
#  quotes plugin

#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Copyright © 2009-2023 Ancestors Soft

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

from fatalapi import *

import urllib3
import re

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')

def handler_borg_quotes_get(type, source, parameters):
    if parameters.strip() == '':
        url = 'http://www.bashorg.org/casual'
        http = urllib3.PoolManager()
        header = {'User-Agent': 'Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.18'}

        try:
            resp = http.request('GET', url, headers=header)
            resp = resp.data.decode('windows-1251')

            qn = re.search('<a href="javascript\:vote_quote\(\'rulez\', ', resp)
            q1 = resp[qn.end():] 
            q1 = q1[:re.search('\)">', q1).start()]

            od = re.search('<div>', resp)
            b1 = resp[od.end():]
            b1 = b1[:re.search(' </div>', b1).start()]
            message = escrep(b1)

            return reply(type, source, l('Quote №%s: \n\n%s') % (q1, message))
        except Exception:
            return reply(type, source, l('Unknown error!'))
    else:
        url = 'http://bashorg.org/quote/%s' %(parameters.strip())
        http = urllib3.PoolManager()
        headers = {'User-Agent': 'Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.18'}

        try:
            resp = http.request('GET', url, headers=headers)
            resp = resp.data.decode('windows-1251')

            qn = re.search('<a href="javascript\:vote_quote\(\'rulez\', ', resp)
            q1 = resp[qn.end():] 
            q1 = q1[:re.search('\)">', q1).start()]

            od = re.search('<div class="quote">', resp)
            b1 = resp[od.end():]
            b1 = b1[:re.search(' </div>', b1).start()]
            message = escrep(b1)

            return reply(type, source, l('Quote №%s: \n\n%s') % (q1, message))
        except Exception:
            return reply(type, source, l('Unknown error!'))

def handler_borg_pittop_get(type, source, parameters):
    if not parameters.strip():
        pind = random.randrange(1, 488)

        url = 'http://www.bashorg.org/pittop/page/%s' % (pind)
        http = urllib3.PoolManager()
        headers = {'User-Agent': 'Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.18'}

        try:
            resp = http.request('GET', url, headers=headers)
            resp = resp.data.decode('windows-1251')

            rlst = []
            qlst = []

            qser = resp

            ind = 35

            while ind > 0:
                qn = re.search('">Цитата #', qser)
                q1 = qser[qn.end():] 
                q1 = q1[:re.search('</a>', q1).start()]

                qlst.append(q1)

                q1 = '">Цитата #%s</a>' % (q1)
                qser = qser.replace(q1, '')

                od = re.search('<div class="quote">', resp)
                b1 = resp[od.end():]
                b1 = b1[:re.search(' </div>', b1).start()]

                rlst.append(b1)

                b1 = '<div class="quote">%s </div>' % (b1)

                resp = resp.replace(b1, '')

                ind -= 1

            rind = random.randrange(1, 35)
            message = rlst[rind]
            message = escrep(message)    

            return reply(type, source, l('Quote №%s <%s> [page№%s]: \n\n%s') % (qlst[rind], rind+1, pind, message))
        except Exception:
            return reply(type, source, l('Unknown error!'))
    else:
        return reply(type, source, l('This resource does not support quotes numbers!'))

def handler_borg_orgall_get(type, source, parameters):
    if not parameters.strip():
        pind = random.randrange(1, 2021)

        url = 'http://www.bashorg.org/page/%s' % (pind) 
        http = urllib3.PoolManager()
        headers = {'User-Agent': 'Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.18'}

        try:
            resp = http.request('GET', url, headers=headers)
            resp = resp.data.decode('windows-1251')

            rlst = []
            qlst = []

            qser = resp

            ind = 35

            while ind > 0:
                qn = re.search('">Цитата #', qser)
                q1 = qser[qn.end():] 
                q1 = q1[:re.search('</a>', q1).start()]

                qlst.append(q1)

                q1 = '">Цитата #%s</a>' % (q1)
                qser = qser.replace(q1, '')

                od = re.search('<div class="quote">', resp)
                b1 = resp[od.end():]
                b1 = b1[:re.search(' </div>', b1).start()]

                rlst.append(b1)

                b1 = '<div class="quote">%s </div>' % (b1)

                resp = resp.replace(b1, '')

                ind -= 1

            rind = random.randrange(1, 35)
            message = rlst[rind]
            message = escrep(message)    

            urlq = 'http://www.bashorg.org/quote/%s' % (qlst[rind])

            return reply(type, source, l('Quote №%s <%s> [page№%s]: \n\n%s\n\nLink: %s') % (qlst[rind], rind+1, pind, message, urlq))
        except Exception:
            return reply(type, source, l('Unknown error!'))
    else:
        return reply(type, source, l('This resource does not support quotes numbers!'))

def borg_pull_quotes(src, page=0):
    create_quotes_table()

    start = time.time() 

    fail = False
    succ = False

    qco = 0
    fco = 0
    tst = ''
    tsp = ''

    pind = int(page)

    num = 1

    while pind <= 488:
        try:
            pind += 1

            filename = 'static/pit_pages/page%s.html' % (str(pind).zfill(4))
            resp = read_file_ex(filename)

            qser = resp

            qdic = {}

            ind = 35

            while ind > 0:
                qn = re.search('">Цитата #', qser)
                q1 = qser[qn.end():] 
                q1 = q1[:re.search('</a>', q1).start()]

                qid = q1

                q1 = '">Цитата #%s</a>' % (q1)
                qser = qser.replace(q1, '', 1)

                od = re.search('<div class="quote">', resp)
                b1 = resp[od.end():]
                b1 = b1[:re.search(' </div>', b1).start()]

                b1 = '<div class="quote">%s </div>' % (b1)

                resp = resp.replace(b1, '', 1)

                message = escrep(b1)

                res = add_bashorg_quote(qid, pind, message)

                if res:
                    qco += 1
                    
                    if qco == 35:
                        qco = 0
                        succ = True     
                        
                    if fco >= 1:
                        fco = 0
                        fail = True

                    fco += 1

                    tsp += 'Succ: %s-%s-%s\n' % (pind, num, qid)
                    log_raw_stnzs('succ: %s-%s-%s' % (pind, num, qid), 'static/pit_pages/bashorg.log')
                else:
                    log_raw_stnzs('fail: %s-%s-%s' % (pind, num, qid), 'static/pit_pages/bashorg.log')
                    tst += 'Quote #%s was failed to dump!\n' % (qid)

                if succ and tsp:
                   reply('private', src, '\n'+tsp.strip()) 
                   tsp = ''
                   succ = False
                    
                if fail and tst:
                    reply('private', src, tst)
                    tst = ''
                    fail = False

                ind -= 1
                num += 1
        except Exception:
            tsp += 'Fail: %s-%s-%s\n' % (pind, num, qid)
            log_exc_error()

    stop = time.time()
    elap = stop - start
    log_raw_stnzs('Dump time: %s sec.' % (elap), 'static/pit_pages/bashorg.log')
    reply('private', src, 'Dump time: %s sec.' % (elap)) 

def create_quotes_table():
    if not is_db_exists('static/pit_pages/borpit.db'):
        sql = '''CREATE TABLE quotes (idn INTEGER PRIMARY KEY AUTOINCREMENT,
            page INTEGER NOT NULL, id VARCHAR(30) NOT NULL, quote TEXT, UNIQUE (id));'''
        sqlquery('static/pit_pages/borpit.db', sql)

        sql = 'CREATE UNIQUE INDEX iquotes ON quotes (idn);'
        sqlquery('static/pit_pages/borpit.db', sql)

def add_bashorg_quote(idc, page, quote):
    quote = quote.replace("'", '&quot;')

    sql = "INSERT INTO quotes (page, id, quote) VALUES ('%s', '%s', '%s');" % (page, idc, quote.strip())

    qres = sqlquery('static/pit_pages/borpit.db', sql)

    if qres != '':
        return True
    return False

def escrep(text):
    return strip_tags.sub('', text.replace('<br />', '\n').replace('<br>', '\n'))\
        .replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')\
            .replace('&quot;', '"').replace('\t', '').replace('||||:]', '')\
                .replace('>[:\n', '')

def handler_borg_cycle_quote(type, source, parameters):
    taskn = 'borc.%s' % (source[1])
    sparam = parameters.strip()
    
    if sparam and sparam != '-':
        if not is_task_exists(taskn):
            ival = int(sparam)

            ival = ival * 60

            newsrc = [source[1], source[1], '']
            
            add_fatal_task(taskn, handler_borg_orgall_get, ('public', newsrc, ''), ival)

            return reply(type, source, l('Cycle quote from bashorg.org has been turned on!'))
        else:
            tlast = get_task_last(taskn)
            nquote = time.strftime('%H:%M:%S', time.localtime(tlast))
            tival = get_task_ival(taskn)
            return reply(type, source, l('Cycle quote from bashorg.org has been already turned on!'))
    else:
        if sparam == '-':
            if is_task_exists(taskn):  
                rmv_fatal_task(taskn)
                return reply(type, source, l('Cycle quote from bashorg.org has been turned off!'))
            else:    
                return reply(type, source, l('Cycle quote from bashorg.org has not been turned on yet!'))
        else:
            if is_task_exists(taskn):
                tlast = get_task_last(taskn)
                nquote = time.strftime('%H:%M:%S', time.localtime(tlast))
                tival = get_task_ival(taskn)
                qina = timeElapsed(tlast-time.time())
                each = timeElapsed(tival)
                return reply(type, source, l('Next quote at %s (in %s/each %s)!') % (nquote, qina, each))
            else:
                return reply(type, source, l('Cycle quote from bashorg.org has not been turned on yet!')) 

def borg_pull_pages(dest, page=1):
    start = time.time() 

    pind = int(page)

    http = urllib3.PoolManager()
    headers = {'User-Agent': 'Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.18'}

    while pind <= 488:
        try:
            url = 'http://www.bashorg.org/pit/page/%s' % (pind) 
            resp = http.request('GET', url, headers=headers)
            resp = resp.data.decode('windows-1251')

            res = write_file('static/pit_pages/page%s.html' % (str(pind).zfill(4)), resp)

            if res:
                msg(dest, 'succ: %s' % (pind))
                log_raw_stnzs('succ: %s' % (pind), 'static/pit_pages/bpit_pages.log')
            else:
                log_raw_stnzs('fail: %s' % (pind), 'static/pit_pages/bpit_pages.log')
                msg(dest, 'fail: %s' % (pind))
        except Exception:
            log_exc_error()

        pind += 1

    stop = time.time()
    elap = stop - start
    log_raw_stnzs('Dump time: %d sec.' % (elap), 'static/pit_pages/bpit_pages.log')
    msg(dest, 'Dump time: %d sec.' % (elap))

def borg_pull_quotes_cmd(type, source, parameters):
    cid = get_client_id()
    call_in_sep_thr('%s/dump_borg_quotes' % (cid), borg_pull_quotes, source)
    
def borg_pull_pages_cmd(type, source, parameters):
    cid = get_client_id()
    dest = '%s/%s' % (source[1].strip(), source[2].strip())
    call_in_sep_thr('%s/dump_pit_pages' % (cid), borg_pull_pages, dest)    

register_stage0_init(create_quotes_table)

register_command_handler(borg_pull_quotes_cmd, 'pqdb', 100)
register_command_handler(borg_pull_pages_cmd, 'bopp', 100)

register_command_handler(handler_borg_cycle_quote, 'borc', 20)
register_command_handler(handler_borg_quotes_get, 'borg', 10)
register_command_handler(handler_borg_orgall_get, 'bora', 10)
register_command_handler(handler_borg_pittop_get, 'bpit', 10)
