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

__all__ = []

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
        pind = random.randrange(1, 444)

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
        pind = random.randrange(1, 2020)

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

def borg_pull_quotes(src, page=1):
    create_quotes_table()
    
    start = time.time() 
    
    fail = False
    
    qco = 0
    fco = 0
    tst = ''
        
    pind = int(page)

    http = urllib3.PoolManager()
    headers = {'User-Agent': 'Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.18'}
    
    num = pind * 35
    
    while pind <= 2021:
        try:
            url = 'http://www.bashorg.org/page/%s' % (pind) 
            resp = http.request('GET', url, headers=headers)
            resp = resp.data.decode('windows-1251')
            
            qser = resp
            
            ind = 35
            
            while ind > 0:
                qn = re.search('">Цитата #', qser)
                q1 = qser[qn.end():] 
                q1 = q1[:re.search('</a>', q1).start()]
                
                qid = q1
                
                q1 = '">Цитата #%s</a>' % (q1)
                qser = qser.replace(q1, '')
                
                od = re.search('<div class="quote">', resp)
                b1 = resp[od.end():]
                b1 = b1[:re.search(' </div>', b1).start()]
                
                b1 = '<div class="quote">%s </div>' % (b1)
                
                resp = resp.replace(b1, '')
          
                message = escrep(b1)
                
                res = add_bashorg_quote(qid, message)
                
                if res:
                    if qco >= 100:
                        reply('telegram', src, 'Succ: %s-%s' % (num, qid))
                        qco = 1 
                    
                    if fco >= 50:
                        fail = True
                    
                    fco += 1
                    
                    log_raw_stnzs('succ: %s-%s' % (num, qid), 'static/bashorg.log')
                else:
                    log_raw_stnzs('fail: %s-%s' % (num, qid), 'static/bashorg.log')
                    tst += 'Quote #%s was failed to dump!\n\n' % (qid)
                    
                if fail and tst:
                    reply('telegram', src, tst)
                    tst = ''
                    fail = False
                
                num += 1
                qco += 1
                ind -= 1
                
                time.sleep(0.5)
        except Exception:
            log_exc_error()
        
        pind += 1
    
    stop = time.time()
    elap = stop - start
    log_raw_stnzs('Dump time: %s sec.' % (elap), 'static/bashorg.log')
    reply('telegram', src, 'Dump time: %s sec.' % (elap)) 

def borg_pull_quotes_cmd(type, source, parameters):
    cid = get_client_id()
    
    call_in_sep_thr('%s/borg_dump_quotes' % (cid), borg_pull_quotes, source, parameters)

def create_quotes_table():
    if not is_db_exists('static/bashorg.db'):
        sql = 'CREATE TABLE quotes (idn INTEGER PRIMARY KEY AUTOINCREMENT, \
            id VARCHAR(30) NOT NULL, quote TEXT NOT NULL, UNIQUE (id));'
        sqlquery('static/bashorg.db', sql)
        
        sql = 'CREATE UNIQUE INDEX iquotes ON quotes (idn);'
        sqlquery('static/bashorg.db', sql)

def add_bashorg_quote(idc, quote):
    quote = quote.replace("'", '&quot;')
    
    sql = "INSERT INTO quotes (id, quote) VALUES ('%s', '%s');" % (idc, quote.strip())
    
    qres = sqlquery('static/bashorg.db', sql)
    
    if qres != '':
        return True
    return False

def escrep(text):
    return strip_tags.sub('', text.replace('<br />', '\n').replace('<br>', '\n'))\
        .replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')\
            .replace('&quot;', '"').replace('\t', '').replace('||||:]', '')\
                .replace('>[:\n', '')

def handler_borg_cycle_quote(type, source, parameters):
    cid = get_client_id()
    
    if parameters.strip():
        ival = int(parameters)
        
        ival = ival * 60
        
        add_fatal_task('%s/borc_cycle' % (cid), handler_borg_orgall_get,(type, source, ''), ival=ival)

        return reply(type, source, l('Cycle quote from bashorg.org has been turned on!'))
    else:
        rmv_fatal_task('%s/borc_cycle' % (cid))
        
        return reply(type, source, l('Cycle quote from bashorg.org has been turned off!'))

register_stage0_init(create_quotes_table)

register_command_handler(handler_borg_cycle_quote, 'borc', 20)
register_command_handler(handler_borg_quotes_get, 'borg', 10)
register_command_handler(handler_borg_orgall_get, 'bora', 10)
register_command_handler(handler_borg_pittop_get, 'bpit', 10)
