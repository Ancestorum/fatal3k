# -*- coding: utf-8 -*-

#  fatal API module
#  fatalapi.py

#  Copyright © 2009-2025 Ancestors Soft
#  Some useful ideas © 2010 Quality <admin@qabber.ru>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime as dt
import os
import subprocess
import sys
import atexit
import threading
import traceback
import time
import heapq
import types
import locale
import re
import random
import importlib
import socket
import select
import urllib.request, urllib.parse, urllib.error
import hashlib
import base64
import codecs

import sqlite3 as db

import xmpp
from xmpp import features
from xmpp import simplexml
from xml.parsers.expat import ExpatError
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import ParseError
from typing import Union

from fatalvar import *
from fataldmn import *

#-----------------------------------------------------------------------------

try:
    import readline
except ImportError:
    readline = None
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

    if os.path.exists('.fatalhst'):
        readline.read_history_file('.fatalhst')
    
    readline.set_history_length(80)

    import __main__

    rlcomp = rlcompleter.Completer(__main__.__dict__)

#-----------------------------------------------------------------------------

stk_size = get_int_cfg_param('def_stk_size', 524288)
threading.stack_size(stk_size)

#sys.setcheckinterval(17)

mtx = threading.Lock()
dmtx = threading.Lock()
wsmph = threading.BoundedSemaphore(value=1)
smph = threading.BoundedSemaphore(value=100)
smph3 = threading.BoundedSemaphore(value=3)

st0_prt = 1.1
st1_prt = 1.2
st2_prt = 1.3
joi_prt = 2.0
lev_prt = 2.1
iq_prt = 2.2
prs_prt = 2.3
msg_prt = 3.0
oms_prt = 3.1

def sprint(*args):
    color = ''
    ncolor = ''
    
    if args:
        tp = args[-1]
        
        if tp == True and len(args) > 2:
            args = list(args)
            args.pop()
            
            if is_var_set('cle'):
                color = args.pop()
                ncolor = cl_none
            else:
                args.pop()

    try:
        for arg in args:
            print(color + arg + ncolor)
            sys.stdout.flush()

        if not args:
            print()
            sys.stdout.flush()
    except Exception:
        log_exc_error()
        log_error(str(args), 'syslogs/output.log')

def dc(file=''):
    curr_thrn = get_curr_thr_name()
    gch = cgv(curr_thrn, 'called_from')

    if gch:
        return d('%s/%s' % (gch, file))
    return ''

def d(file=''):
    cid = get_client_id()
    
    if file:
        return 'dynamic/%s/%s' % (cid, file)
    return 'dynamic/%s/' % (cid)

def copyright():
    fatal_copy_head = ' ' + '=' * 41
    fatal_copy_mid = '< Copyright (c) 2009-2025 Ancestors Soft  >'
    fatal_copy_foot = ' ' + '=' * 41

    sprint()
    
    if is_var_set('cle'):
        sprint(fatal_copy_head, fatal_copy_mid, fatal_copy_foot, cl_yellow, True)
    else:
        sprint(fatal_copy_head, fatal_copy_mid, fatal_copy_foot)

def _get_full_ver():
    ver = get_fatal_var('ftver', 'botver', 'ver')
    rev = get_fatal_var('ftver', 'rev')
    
    if not rev:
        rev = ' [Neutrino]'
    
    fver = ver % (rev)
    return fver

def fatal_version():
    fver = _get_full_ver()
    
    vstr = '\n+----------------------------------------------------+\n'
    vstr += '+fatal-bot %s,   free   jabber(XMPP)   bot.+\n' % (fver)
    vstr += '+----> Copyright (c) 2009-2025 Ancestors Soft. <-----+\n'
    
    sprint(vstr, cl_bgreen, True)

def fatal_help():
    fver = _get_full_ver()
    
    hstr = 'fatal-bot %s, free jabber (XMPP) bot.\n\n' % (fver)
    hstr += 'Usage: ./fatal.py [options]\n\n'
    hstr += 'Options:\n'
    hstr += "  -v,  --version  show program's version number and exit.\n"
    hstr += '  -h,  --help     show this help message and exit.\n'
    hstr += '  -d,  --daemon   daemonize bot after startup.\n'
    hstr += '  -k,  --kill     kill the currently running bot.\n'
    hstr += '\nPlease send bug reports and questions to <alt.ancestor@gmail.com>.'

    sprint(hstr)

def equalize_lists(lsto=[], lstt=[], dfvl='fatal3k'):
    if (len(lsto) != len(lstt)) and (len(lsto) != 0):
        dlt = len(lsto) - len(lstt)

        while dlt >= 1:
            lstt.append(dfvl)
            dlt -= 1
            
    return lsto, lstt

def read_file(filename, lines=False):
    try:
        fp = open(filename, encoding='utf-8')
        
        if lines:
            data = fp.readlines()
        else:    
            data = fp.read()
        
        fp.close()
        
        return data
    except Exception:
        return False

def read_file_ex(filename, lines=False):
    try:
        fp = open(filename, encoding='windows-1251')
        
        if lines:
            data = fp.readlines()
        else:    
            data = fp.read()
        
        fp.close()
        
        return data
    except Exception:
        return False

def write_file(filename, data):
    try:
        fp = open(filename, 'w', encoding='windows-1251')
        fp.write(data)
        fp.close()
        return True
    except Exception:
        return False

def _app_file(filename, data):
    try:
        if os.path.exists(filename):
            if os.path.getsize(filename) >= 512000:
                os.remove(filename)

        fp = open(filename, 'a', encoding='utf-8')

        fp.write(data)
        fp.close()
    except Exception:
        log_exc_error()

def get_ldc_tms(utm=0):
    ldctm = utm 
    
    if not utm:
        ldctm = time.time()
    
    ldctm = time.strftime('%d.%m.%Y, %H:%M:%S', time.localtime(ldctm))
    return ldctm

def tms_to_str(tmstm=None, pat='%d.%m.%Y/%H:%M:%S'):
    if not tmstm:
        tmstm = time.time()
        
    return time.strftime(pat, time.localtime(tmstm))

def iso_to_tms(isof):
    try:
        return dt.fromisoformat(isof).timestamp()
    except ValueError:
        try:
            return dt.fromisoformat(isof[:-1]).timestamp()
        except Exception:
            return time.time()

def log_null_cmdr(data, file='syslogs/ncmdr.log'):    
    stm = time.time()
    
    sstm = str(stm)
    sptl = sstm.split('.', 1)
    stim = sptl[1]
    stim = stim[:3]

    stz_time = '[%s.' % (tms_to_str())
    stz_time = '%s%s]: '% (stz_time, stim) 
    _app_file(file, '%s%s\n' % (stz_time, data))
    return '%s%s\n' % (stz_time, data)

def log_exc_error(file='syslogs/error.log'):
    exc_err = traceback.format_exc()
    exc_time = '[%s]: ' % (tms_to_str())
    _app_file(file, '%s%s\n' % (exc_time, exc_err))
    
    if is_var_set('cle'):
        outs = '%s%s' % (exc_time, exc_err)
        return cl_bred + outs + cl_none
    return '%s%s' % (exc_time, exc_err)

def log_error(err, file='syslogs/error.log'):
    err_time = '[%s]: ' % (tms_to_str())
    _app_file(file, '%s%s\n' % (err_time, err))
    
    if is_var_set('cle'):
        outs = '%s%s\n' % (err_time, err)
        return cl_bred + outs + cl_none
    return '%s%s\n' % (err_time, err)

def log_raw_stnzs(stanza, file='syslogs/xmpp.log'):
    stz_time = '[%s]: ' % (tms_to_str())
    _app_file(file, '\n%s%s\n' % (stz_time, stanza))
    return '%s%s\n' % (stz_time, stanza)

def log_cmd_run(cmd, params, guser, user, file='syslogs/cmdruns.log'):
    run_time = '[%s]' % (tms_to_str())
    
    if len(params) > 255:
        params = '%s [...]' % (params[:254])
    
    if guser:
        comp_str = '%s<%s>(%s): %s %s' % (run_time, guser, user, cmd, params)
    else:
        comp_str = '%s(%s): %s %s' % (run_time, user, cmd, params)
    
    _app_file(file, '%s\n' % (comp_str))
    
    return '%s\n' % (comp_str)

def log_ddos_act(guser, user, status, file='syslogs/ddos.log'):
    run_time = '[%s]' % (tms_to_str())
    
    if guser:
        comp_str = '%s<%s>(%s): %s' % (run_time, guser, user, status)
    else:
        comp_str = '%s(%s): %s' % (run_time, user, status)

    _app_file(file, '%s\n' % (comp_str))
    
    return '%s\n' % (comp_str)

def get_md5(txt):
    md5t = hashlib.md5(txt.encode())
    md5t = md5t.hexdigest()
    return md5t

def _md5hash(plbody):
    md5s = hashlib.md5()
    md5s.update(plbody)
    return md5s.hexdigest()

def _sha1hash(text):
    sha1s = hashlib.sha1()
    sha1s.update(text.encode())
    return sha1s.hexdigest()

def _get_core_body():
    cpath = 'fatal.py'
    if os.path.exists(cpath):
        crbody = read_file(cpath)
        
        crblines = crbody.splitlines()
        
        if crblines:
            crblines.pop(0)
        
        crbody = '\n'.join(crblines)
        return crbody
    else:
        return ''

def rand10(ln=10):
    random.seed()
    
    rstr = str(random.randrange(1, 10))
    
    for i in range(ln-1):
        rstr += str(random.randrange(0, 10))
    
    return rstr

def interrupt(clmess='\nInterrupt (Ctrl+C)', prmess='Got Ctrl+C --> Shutdown!'):
    sprint(clmess)
    prs = xmpp.Presence(typ='unavailable')
    prs.setStatus(prmess)
    
    cids = dict(get_dict_fatal_var('clconns'))
    
    for cid in cids:
        jconn = cids[cid]
        
        set_fatal_var(cid, 'disconnected', True)
        
        try:
            jconn.send(prs)
        except Exception:
            pass        
    
    time.sleep(2)
    
    dctm = get_ldc_tms()
   
    sprint('\nDisconnected: %s' % (dctm))
    sprint('\n...---===FATAL-BOT STOPPED===---...\n')
    rmv_pid_file()
    os._exit(0)

def interrupt_dmn():
    prs = xmpp.Presence(typ='unavailable')
    prs.setStatus('Restarting...')
    
    cids = dict(get_dict_fatal_var('clconns'))
    
    for cid in cids:
        jconn = cids[cid]
        
        set_fatal_var(cid, 'disconnected', True)
        
        try:
            jconn.send(prs)
        except Exception:
            pass        

#---------------------------- Decorator routines -----------------------------

def print_exception(func):
    def wrapper(*ar, **kw):
        try:
            func(*ar, **kw)
        except Exception:
            sprint(log_exc_error())
    return wrapper

def handle_exception(message='', quiet=False):
    def ewrapper(func):
        def iwrapper(*ar, **kw):
            try:
                return func(*ar, **kw)
            except Exception:
                log_exc_error()
                
                if not quiet or message:
                    return l(message)
        return iwrapper
    return ewrapper

def handle_xmpp_exc(message='', quiet=False):
    def ewrapper(func):
        def iwrapper(*ar, **kw):
            try:
                return func(*ar, **kw)
            except xmpp.NodeProcessed:
                raise
            except Exception:
                log_exc_error()
                
                if not quiet or message:
                    if 'type' in kw and 'source' in kw:
                        return reply(kw['type'], kw['source'], l(message))
                    return l(message)
        return iwrapper
    return ewrapper

@contextmanager
def semph(sem):
    sem.acquire()
    try:
        yield
    finally:
        sem.release()

#------------------------------- fatal GUI routines ---------------------------

def fatal_gui():
    try:
        import _tkinter.ttk
        #wlib = ttk
    except ImportError:
        wlib = _tkinter
    
    ftk = _tkinter.Tk()
    
    fmn_frame = wlib.Frame(ftk)
    fmn_frame.pack()
    
    set_fatal_var('ftk', '.', 'tw', ftk)
    set_fatal_var('ftk', '.', 'mframe', 'frame', fmn_frame)
    
    ftk.wm_title('fatal-bot v2.0')
    
    mxs = ftk.maxsize()
    
    swidth = mxs[0]
    sheight = mxs[1]
    dxpos = int(swidth / 2) - 100
    dypos = int(sheight / 2) - 40
    
    ftk.wm_geometry('200x80+%s+%s' % (dxpos, dypos))
    ftk.wm_resizable(0, 0)
    ftk.iconbitmap('@fatal.xbm')
    
    label = wlib.Label(fmn_frame, text='[fatal-bot control panel]')
    label.pack()
    
    set_fatal_var('ftk', '.', 'mframe', 'tlbl', label)
    
    stop_bot = wlib.Button(fmn_frame, text='Stop fatal-bot', command=interrupt)
    close_panel = wlib.Button(fmn_frame, text=' Close panel ', command=ftk.destroy)
    
    stop_bot.pack()
    close_panel.pack()
    
    set_fatal_var('ftk', '.', 'mframe', 'sbtn', stop_bot)
    set_fatal_var('ftk', '.', 'mframe', 'cbtn', close_panel)
    
    ftk.iconify()
    ftk.update()
    ftk.deiconify()
    ftk.mainloop()

#------------------------------- Locale routines ------------------------------

def load_help(cid):
    locale = get_sys_lang()
    locale = get_param('locale', locale)
    set_help_locale(locale, cid)

def load_locale(cid):
    locale = get_sys_lang()
    locale = get_param('locale', locale)
    load_lc_msgs(locale, cid=cid)

def set_client_locale():
    locale = get_param('locale', 'en')
    change_locale(locale)

def get_sys_lang():
    lang = os.getenv('LANG')
    
    if lang is None:
        def_lang = locale.getdefaultlocale()[0]
        
        if def_lang:
            lang = def_lang
        else:
            return 'en'
    
    sys_lang = lang[:2]
    
    if sys_lang:
        return sys_lang

    return 'en'

def l(orig):
    if orig:
        ls = get_lc_str(orig)
        
        if orig.count('%s') != ls.count('%s') or not ls:
            return orig
        return ls
    else:
        return ''

#------------------------------------------------------------------------------

def init_anti_ddos(conf, gch_jid, jid):
    cid = get_client_id()
    
    if conf:
        if gch_jid == jid: 
            return
        
        if not is_var_set(cid, 'last', gch_jid, jid):
            set_fatal_var(cid, 'last', gch_jid, jid, {'t': time.time(), 'c': 0, 'b': False, 'df': 0})
        else:
            set_fatal_var(cid, 'last', gch_jid, jid, 't', time.time())
    else:
        if not is_var_set(cid, 'last', gch_jid):
            set_fatal_var(cid, 'last', gch_jid, {'t': time.time(), 'c': 0, 'b': False, 'df': 0})
        else:
            set_fatal_var(cid, 'last', gch_jid, 't', time.time())

def ddos_detect(conf, gch_jid, guser, jid):
    cid = get_client_id()
    
    if conf:
        if gch_jid == jid: 
            return
        
        if is_var_set(cid, 'last', gch_jid, jid):
            stime = get_int_fatal_var(cid, 'last', gch_jid, jid, 't')
            isbl = get_int_fatal_var(cid, 'last', gch_jid, jid, 'b')
            
            if isbl:
                if time.time() - stime >= 600:
                    set_fatal_var(cid, 'last', gch_jid, jid, 'b', False)
                    set_fatal_var(cid, 'last', gch_jid, jid, 'c', 0)
                else:
                    return True
            
            if time.time() - stime <= 1.7:
                set_fatal_var(cid, 'last', gch_jid, jid, 't', time.time())
                count = get_int_fatal_var(cid, 'last', gch_jid, jid, 'c')
                ddos_flag = get_int_fatal_var(cid, 'last', gch_jid, jid, 'df')
                
                set_fatal_var(cid, 'last', gch_jid, jid, 'df', 1)
                
                if count >= 5:                    
                    if get_int_cfg_param('privacy_lists', 1):
                        add_jid_to_privacy(gch_jid, act='deny')
                        log_ddos_act(guser, jid, 'User has been blocked by privacy list!')
                    else:
                        log_ddos_act(guser, jid, 'User has been blocked for 10 minutes!')
                    
                    set_fatal_var(cid, 'last', gch_jid, jid, 'b', True)
                    set_fatal_var(cid, 'last', gch_jid, jid, 'df', 0)
                return True
            
            if time.time() - stime >= 8:
                set_fatal_var(cid, 'last', gch_jid, jid, 'c', 0)
            
            ddos_flag = get_int_fatal_var(cid, 'last', gch_jid, jid, 'df')
            
            if ddos_flag:
                log_ddos_act(guser, jid, 'Message sending limit has been exceeded!')
                inc_fatal_var(cid, 'last', gch_jid, jid, 'c')
                set_fatal_var(cid, 'last', gch_jid, jid, 'df', 0)
    else:
        if is_var_set(cid, 'last', gch_jid):
            stime = get_int_fatal_var(cid, 'last', gch_jid, 't')
            isbl = get_int_fatal_var(cid, 'last', gch_jid, 'b')
            
            if isbl:
                if time.time() - stime >= 600:
                    set_fatal_var(cid, 'last', gch_jid, 'b', False)
                    set_fatal_var(cid, 'last', gch_jid, 'c', 0)
                else:
                    return True
            
            if time.time() - stime <= 1.7:
                set_fatal_var(cid, 'last', gch_jid, 't', time.time())
                count = get_int_fatal_var(cid, 'last', gch_jid, 'c')
                ddos_flag = get_int_fatal_var(cid, 'last', gch_jid, 'df')
                
                set_fatal_var(cid, 'last', gch_jid, 'df', 1)
                
                if count >= 5:
                    if get_int_cfg_param('privacy_lists', 1):
                        rmv_jid_from_privacy(jid)
                        add_jid_to_privacy(jid, act='deny')
                        log_ddos_act(guser, jid, 'User has been blocked by privacy list!')
                    else:
                        log_ddos_act(guser, jid, 'User has been blocked for 10 minutes!')
                    
                    set_fatal_var(cid, 'last', gch_jid, 'b', True)
                    set_fatal_var(cid, 'last', gch_jid, 'df', 0)
                return True
            
            if time.time() - stime >= 8:
                set_fatal_var(cid, 'last', gch_jid, 'c', 0)
            
            ddos_flag = get_int_fatal_var(cid, 'last', gch_jid, 'df')
            
            if ddos_flag:
                log_ddos_act(guser, jid, 'Message sending limit has been exceeded!')
                inc_fatal_var(cid, 'last', gch_jid, 'c')
                set_fatal_var(cid, 'last', gch_jid, 'df', 0)

def _thr_counter():
    ac, ma = 0, 0
    actcnt = 0

    if os.path.exists('counter.log'):
        os.remove('counter.log')

    while True:
        if get_int_fatal_var('info', 'thr'):
            ac = actcnt
            
            totcnt = get_int_fatal_var('info', 'thr')
            actcnt = threading.activeCount()
            
            ma = max(actcnt, ma)
            
            if ac != actcnt:
                if ma == actcnt:
                    _app_file('counter.log', '\n%s/%s\n' % (actcnt, totcnt))

def craiot(coro):
    return create_and_run_asyncio_task(coro)

def handle_task_done(task):
    evn = task.get_name()
    set_fatal_event(evn)

def _executor_func(coro, evn):
    loop = cgv('tgram_loop')
    task = loop.create_task(coro)
    task.set_name(evn)
    task.add_done_callback(handle_task_done)
    return task

def create_and_run_asyncio_task(coro):
    loop = cgv('tgram_loop')
    
    res = None
    
    evn = 'tgram_task_%s' % (rand10())
    
    with ThreadPoolExecutor() as executor:
        res = loop.run_in_executor(executor, _executor_func, coro, evn)
        iawt_fatal_event(evn)
        res = res.result()
        res = res.result()
        return res

def make_thr_name(cid, frm, name):
    thrc = inc_fatal_var('info', 'thr')
    st_time = time.strftime('%H.%M.%S', time.localtime(time.time()))
    return '%s/%s.%s%d.%s' % (cid, frm, name, thrc, st_time)

def init_fatal_thr(*args):
    frm, func = '', None
    dfunc = lambda *largs: largs
    
    if not args:
        frm = 'empty'
        func = dfunc
    elif len(args) == 1:
        frm = 'unnamed_func'
        args = list(args)
        func = args.pop()
        
        if type(func) != type(dfunc):
            func = dfunc
    elif len(args) >= 2:
        frm = args[0]
        
        if type(frm) == type(dfunc):
            frm = 'unnamed_func'
            args = list(args)
            func = args.pop(0)
        elif type(frm) in (str, str):
            args = list(args)
            frm = args.pop(0)
            func = args.pop(0)
            
            if type(func) != type(dfunc):
                func = dfunc

    thrc = inc_fatal_var('info', 'thr')
    st_time = time.strftime('%H.%M.%S', time.localtime(time.time()))
    thr_name = '%s.%s%d.%s' % (frm, func.__name__, thrc, st_time)
    init_thr = fThread(None, func, thr_name, args)
    init_thr.ttype = 'otr'
    return init_thr

def call_in_sep_thr(*args):
    try:        
        sep_thr = init_fatal_thr(*args)
        sep_thr.start()
    except Exception:
        dec_fatal_var('info', 'thr')
        log_exc_error()

def cid():
    return get_client_id()

def get_client_id():
    curr_thr = threading.currentThread()
    thr_name = curr_thr.getName()
    sptnm = thr_name.split('/', 1)
    cid = sptnm[0]
    
    if cid == 'all' or not thr_name.count('/'):
        cid = get_fatal_var('curr_cons_owner')
    
    return cid

def get_client_conn(cid=''):
    if not cid:
        cid = get_client_id()
    
    return get_fatal_var(cid, 'jconn')

def _get_pooled_thr_id():
    thrid = get_int_fatal_var('info', 'pld_thr_id')
    
    if thrid >= 999:
        set_fatal_var('info', 'pld_thr_id', 0)

    return inc_fatal_var('info', 'pld_thr_id')

def put_in_thr_pool(prt, thr):
    thrid = _get_pooled_thr_id()
    thread_pool = get_fatal_var('thread_pool')
    thread_pool.put((prt, thrid, thr))

def start_win_dmn(stdout=None, stderr=None):
    subprocess.Popen("py fatal.py", creationflags=subprocess.CREATE_NO_WINDOW, stdout=stdout, stderr=stderr)

def start_nix_dmn(pidfile, wfunc, stdout='/dev/null', stderr='/dev/null'):
    drun = fDaemon(pidfile)
    drun.worker = wfunc
    drun.stderr = stderr
    drun.stdout = stdout
    set_fatal_var('daemon', drun)
    drun.start()

def start_thr_disp():
    max_thrs = get_int_cfg_param('max_active_threads', 50)
    
    get_and_start_thr = init_fatal_thr('all/start_thr_disp', _thr_pool_get_and_start, max_thrs)
    
    try:
        get_and_start_thr.ttype = 'sys'
        get_and_start_thr.start()
    except Exception:
        log_exc_error()

def _thr_pool_get_and_start(max_thrs):
    psmph = threading.BoundedSemaphore(max_thrs)
    thread_pool = get_fatal_var('thread_pool')
    thr_st_del = get_flt_cfg_param('thread_start_delay', 0.1)

    while True:
        try:
            with semph(psmph):
                if threading.activeCount() < max_thrs:
                    thr = thread_pool.get()
                    
                    time.sleep(abs(thr_st_del))
                    
                    thr.start()
        except Exception:
            dec_fatal_var('info', 'thr')
            log_exc_error()

def cancel_waited_tmrs(cid=''):
    enu_list = list(threading.enumerate())
    
    if not cid:
        cid = get_client_id()
    
    enu_list = [tmi for tmi in enu_list if tmi.getName().startswith(cid)]
    
    try:
        for thr in enu_list:
            if type(thr) is threading._Timer:
                thr.cancel()
    except Exception:
        log_exc_error()

def get_thrs_rtime():
    enu_list = list(threading.enumerate())
    
    rtms = []

    for thr in enu_list:
        if type(thr) is fThread:
            ttype = thr.ttype
            strtd = thr.strtd
            tname = thr.getName()

            curt = time.time()
            rntm = curt - strtd

            rtms.append((tname, ttype, int(rntm)))

    return rtms

def kill_thrs_by_type(ttype='otr'):
    enu_list = list(threading.enumerate())
    
    for thr in enu_list:
        if type(thr) is fThread:
            if thr.ttype == ttype:
                thr.kill()

def kill_thr_by_name(tname):
    enu_list = list(threading.enumerate())
    
    for thr in enu_list:
        if type(thr) is fThread:
            if thr.getName == tname:
                thr.kill()

def kill_hung_thrs():
    cid = get_client_id()

    thrl = get_thrs_rtime()
    ttps = ('stg', 'msg', 'joi', 'lev', 'prs', 'otr', 'iq')

    fthl = [thi for thi in thrl if thi[1] in ttps and thi[0].startswith(cid) and thi[2] >= 60]

    killc = 0

    for thi in fthl:
        tname = thi[0]

        try:
            kill_thr_by_name(tname)
            killc += 1
        except Exception:
            log_exc_error()

    return killc

def get_cmd_thr_prt(access):
    cmd_prts = 0
    
    if isinstance(access, int):
        cmd_prts = (float(100) - access) / 100
        return cmd_prts
    else:
        return cmd_prts

def is_pid_alive(pid):
    if os.name == 'posix':
        cmdstr = 'sh -c "ps -p %s" 2>&1' % (pid) 
        
        pipe = os.popen(cmdstr)
        ret = pipe.read()
        pipe.close()
        
        if ret.count(pid):
            return True
        return False
    elif os.name == 'nt':
        cmdstr =  'tasklist /fi "pid eq %s" /fo csv' % (pid)
        
        pipe = os.popen(cmdstr)
        ret = pipe.read().encode('cp1251').decode('cp866')
        pipe.close()

        if ret.count(pid):
            return True
        return False
    else:
        return True

def create_pid_file():
    try:
        write_file('fatal.pid', str(os.getpid()))            
    except Exception:
        pass
    
def read_pid_file():
    if os.path.exists('fatal.pid'):
        pid = read_file('fatal.pid')
        return pid.strip()
    else:
        return ''
    
def rmv_pid_file():
    try:
        if os.path.exists('fatal.pid'):
            os.remove('fatal.pid')
    except Exception:
        pass

def get_os_uname(orig=False):
    osver = ''
    
    if os.name == 'posix':
        osname = os.popen("uname", 'r')
        osver = osname.read().strip() + '\n'
        osname.close()
        
        if orig:
            osver = osver.strip()
        else:
            osver = osver.lower().strip()
            
        return osver
    elif os.name == 'nt':
        osname = os.popen("ver")
        osver = codecs.decode(osname.read().strip().encode(), 'cp866') + '\n'
        osname.close()
        
        if orig:
            osver = osver.strip()
        else:
            osver = osver.lower().strip()
            
        return osver
    else:
        return os.name

def is_cycle_overload(cparam='cspeed'):
    if not is_var_set(cparam):
        set_fatal_var(cparam, 1)
    
    if time.time() - get_fatal_var(cparam) <= 0.001:
        rmv_fatal_var(cparam)
        
        log_error('Error: Overloaded cycle detected in "%s". Break cycle!' % (cparam))
        
        return True
    
    set_fatal_var(cparam, time.time())
    
    return False

def restart_bot():
    cid = get_client_id()

    drun = get_fatal_var('daemon') 
    
    if not drun:
        rmv_pid_file()
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        interrupt_dmn()
        rmv_fatal_var(cid, 'tgbot')
        drun.restart()

def get_last_rev(url):
    try:
        fhtml = urllib.request.urlopen(url)
        raw_html = fhtml.read(71)
        fhtml.close()
        revl = raw_html.splitlines(1)[0]
        last_rev = revl.split()[3].replace(':', '').strip()
        return ' [last rev. in repos: r%s]' % (last_rev)
    except Exception:
        return ''

def initialize_file(filename, data=''):
    if not os.access(filename, os.F_OK):
        fp = open(filename, 'w')
        if data:
            fp.write(data)
        fp.close()

def sfr_dic_val(dic, oer, *args):
    for dar in args:
        if type(dic) == dict:
            if dar in dic:
                dic = dic[dar]
            else:
                return oer
        else:
            return oer
    return dic

def get_num_list(lst: list, bra: str=')') -> list:
    if lst:
        nlst = ['%d%c %s' % (lst.index(li) + 1, bra, li) for li in lst]
        return nlst
    return []

def str_to_list(strng, spltr=','):
    if strng:
        lst = strng.split(spltr)
        lst = [li.strip() for li in lst]
        return lst
    return []

def list_to_str(lst, spltr=','):
    if type(lst) == list and lst:
        strng = spltr.join(lst)
        return strng
    return ''

def sort_list_dist(lst, rv=False):
    if lst:
        sili = set(lst)
        sili = list(sili)

        sili.sort(reverse=rv)
             
        return sili
    return []

def strip_list_items(lst):
    if lst:
        lst = rmv_empty_items(lst)
        lst = [li.strip() for li in lst]
        return lst
    return []

def rmv_empty_items(lst):
    if lst:
        lst = [li for li in lst if li and li.strip()]
        return lst
    return []

def parse_cmd_params(params):
    fgroup = ''
    sgroup = ''
    tgroup = ''
    
    if params.count(':') <= 1:
        if ':=' in params:
            params = ':%s' % (params)
    
    splp = safe_split(params)
    
    if not splp[0] and not splp[1]:
        return fgroup, sgroup, tgroup
    elif splp[0] and not splp[1]:
        fgroup = splp[0].strip()
        return fgroup, sgroup, tgroup
    elif not splp[0] and splp[1]:
        ssplp = safe_split(splp[1], ':=')
        
        if ssplp[0] and not ssplp[1]:
            sgroup = ssplp[0].strip()
            return fgroup, sgroup, tgroup
        elif not ssplp[0] and ssplp[1]:
            tgroup = ssplp[1].strip()
            return fgroup, sgroup, tgroup
        elif ssplp[0] and ssplp[1]:
            sgroup = ssplp[0].strip()
            tgroup = ssplp[1].strip()
            return fgroup, sgroup, tgroup
        elif not ssplp[0] and not ssplp[1]:
            return fgroup, sgroup, tgroup
    elif splp[0] and splp[1]:
        fgroup = splp[0].strip()
        
        ssplp = safe_split(splp[1], ':=')
        
        if ssplp[0] and not ssplp[1]:
            sgroup = ssplp[0].strip()
            return fgroup, sgroup, tgroup
        elif not ssplp[0] and ssplp[1]:
            tgroup = ssplp[1].strip()
            return fgroup, sgroup, tgroup
        elif ssplp[0] and ssplp[1]:
            sgroup = ssplp[0].strip()
            tgroup = ssplp[1].strip()
            return fgroup, sgroup, tgroup
        elif not ssplp[0] and not ssplp[1]:
            return fgroup, sgroup, tgroup

def is_db_exists(dbpath):
    if isinstance(dbpath, str):
        dbpath = dbpath.encode('utf-8')
    
    if os.path.exists(dbpath):
        dbsize = os.path.getsize(dbpath)
        
        if dbsize == 1:
            return False
        return True
    return False

def sqlquery(dbpath, query, *args, qer=False):
    if query:
        cursor, connection = None, None
        
        chkq = query.lower()
        spls = chkq.split()
        hdcmd = spls[0]
        
        if not is_db_exists(dbpath):
            if hdcmd != 'create':
                return ''
        
        try:
            connection = db.connect(dbpath)
            cursor = connection.cursor()
            
            if query.count(';') > 1:
                cursor.executescript(query)
            else:
                if args:
                    cursor.execute(query, args)
                else:
                    cursor.execute(query)
            
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            
            return result
        except db.Error as e:
            if not qer:
                log_error('SQLite3 error (%s) [%s] ---> %s' % (dbpath, query, e.args[0]))
            
            if cursor:
               cursor.close()
                
            if connection:
                connection.commit()
                connection.close()
        except Exception:
            log_exc_error()
    return ''
        
def core_md5(path):
    try:
        fp = open(path, 'r')
        ccbody = fp.read()
        fp.close()
        return _md5hash(ccbody.encode())
    except Exception:
        return ''

def is_fl_domain(domain):
    domain = domain.strip()
    
    if domain:
        sql = "SELECT COUNT(tld) FROM tlds WHERE tld=?;" 
        qres = sqlquery('static/tlds.db', sql, domain)

        if qres:
            tldc = qres[0][0]

            if tldc:
                return True
    return False

def check_jid(jid: str, mdl: int=3) -> bool:
    def check_domain(dmnpart):
        if dmnpart:
            sdmnp = dmnpart.split('.')
            sdmnp = rmv_empty_items(sdmnp)

            if len(sdmnp) >= 2 and len(sdmnp) <= mdl:
                fldmn = sdmnp[-1]

                if is_fl_domain(fldmn):
                    return True
        return False

    jid = jid.strip()
    prsdjid = jid.split('@')
    
    prsdjid = rmv_empty_items(prsdjid)

    if len(prsdjid) == 2:
        locpart = prsdjid[0]
        dmnpart = prsdjid[1]

        if locpart:
            return check_domain(dmnpart)
    elif len(prsdjid) == 1:
        dmnpart = prsdjid[0]
        
        return check_domain(dmnpart)
    
    return False
    
def has_edge_space(strng):
    fstrng = strng.strip()
    
    if fstrng != strng:
        return True
    return False

def cnt_edge_spaces(strng, side=0):
    def returner(leds, reds, side):
        if side == -1:
            return leds
        elif side == 1:
            return reds
        return (leds, reds)

    if strng:
        splts = strng.split(' ')
        leds, reds = 0, 0
        
        if strng.isspace():
            return returner(leds, reds, side)
        
        while not splts[0]:
            leds += 1
            splts.pop(0)
            
        while not splts[-1]:
            reds += 1
            splts.pop()
            
        return returner(leds, reds, side)
    return returner(0, 0, side)
    
def rmv_tgs_esc(text):
    rep_src_frst = ['&quot;', '&amp;', '&lt;', '&gt;', '&trade;', '&nbsp;', '&cent;', '&pound;', '&curren;', '&yen;', '&brvbar;', '&sect;', '&copy;', '&laquo;', '&not;', '&reg;', '&deg;', '&plusmn;', '&sup2;', '&sup3;', '&micro;', '&para;', '&middot;', '&sup1;', '&raquo;', '&frac14;', '&frac12;', '&times;', '&divide;']
    rep_src_sec = ['&#34;', '&#38;', '&#60;', '&#62;', '&#153;', '&#160;', '&#162;', '&#163;', '&#164;', '&#165;', '&#166;', '&#167;', '&#169;', '&#171;', '&#172;', '&#174;', '&#176;', '&#177;', '&#178;', '&#179;', '&#181;', '&#182;', '&#183;', '&#185;', '&#187;', '&#188;', '&#189;', '&#215;', '&#247;']
    rep_dest = ['"', '&', '<', '>', '™', ' ', '¢', '£', '¤', '¥', '¦', '§', '©', '«', '¬', '®', '°', '±', '²', '³', 'µ', '¶', '·', '¹', '»', '¼', '½', '×', '÷']
    
    nobold = text.replace('<b>', '').replace('</b>', '')
    nobreaks = nobold.replace('<br>', ' ')
    noescape = nobreaks.replace('&#39;', "'").replace('   ', ' ')
    
    for ri in rep_dest:
        noescape = noescape.replace(rep_src_frst[rep_dest.index(ri)], ri).replace(rep_src_sec[rep_dest.index(ri)], ri)
    
    return noescape
    
def timeElapsed(time, nz=False):
    minutes, seconds = divmod(time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    rep = l('%s second(s)') % (int(round(seconds)))

    if time >= 60:
        rep = l('%s minute(s) %s') % (int(round(minutes)), rep)
        
    if time >= 3600:
        rep = l('%s hour(s) %s') % (int(round(hours)), rep)
        
    if time >= 86400:
        rep = l('%s day(s) %s') % (int(round(days)), rep)
    
    if nz:
        repl = rep.split(' 0 ', 1)
        return repl[0].strip()
    return rep

def safe_split(parameters: str, spl: str=':') -> list:
    nijirel = parameters.split(spl, 1)
    
    splited = ['', '']
        
    if len(nijirel) == 1:
        splited[0] = nijirel[0].strip()
        splited[1] = ''
    elif len(nijirel) == 2:
        splited[0] = nijirel[0].strip()
        splited[1] = nijirel[1].strip()
    return splited

def sstrp(st: str) -> str:
    if st:
        if isinstance(st, str):
            return st.strip()
        return ''
    return ''

def srepl(st: str, pt: str, rs: str) -> str:
    if st:
        if isinstance(rs, str):
            return st.replace(pt, rs)
        return st
    return ''

#-------------------------------- Fatal console routine -----------------------------------

def ftcompl(text, state):
    if is_var_set('is_console_hide'):
        return

    cmds = get_fatal_var('commands')
    lprompt = get_fatal_var('con_last_prompt')
    fndm = []
    rlst = []
    
    globm = rlcomp.global_matches(text)
    attrm = rlcomp.attr_matches(text)

    rlst.extend(globm)
    rlst.extend(attrm)

    if state == 0:
        cmdlist = list(cmds)

    cmdlist.append('sw')

    owner = get_fatal_var('curr_cons_owner')

    if owner != 'fatal-bot':
        aliaso = get_fatal_var(owner, 'alias')
        cmdlist.extend(list(aliaso.galiaslist))

    n = len(text)

    for word in cmdlist:
        if word[:n] == text:
            fndm.append(word)

    fndm.sort()

    rlbfr = readline.get_line_buffer()

    if len(fndm) > 1:
        sys.stdout.write('\n\n' + ', '.join(fndm) + '.\n\n')
        sys.stdout.write(lprompt + rlbfr)
        
        return text
    elif len(rlst) > 1:
        sys.stdout.write('\n\n' + ', '.join(rlst) + '\n\n')
        sys.stdout.write(lprompt + rlbfr)
        
        return text

    try:
        if fndm:
            return fndm[state] + ' '
        elif rlst:
            cmpl = rlst[state]
            
            if not cmpl.endswith('('):
                cmpl += ' '

            return cmpl
        else:
            return rlcomp.complete(text, state)
    except IndexError:
        return None

def fatal_console():
    os_uname = get_os_uname()
    
    try:
        if not is_param_seti('show_console'):
            return False
        
        owner = get_fatal_var('curr_cons_owner')
        
        opnum = inc_fatal_var('info', 'opnum')
        
        prompt = ''

        if not is_var_set('is_console_hide'):
            prompt = '(%s) %d %% ' % (owner, opnum)

        set_fatal_var('con_last_prompt', prompt)

        conv_line = input(prompt)
                            
        comms = conv_line.strip()
        
        if not comms:
            dec_fatal_var('info', 'opnum')
        
        if is_var_set('is_console_hide'):
            return True

        if comms == 'sw':
            owns = get_fatal_var('console_owners')
            
            if owns:
                nwown = owns.pop(0)
                owns.append(owner)
                
                set_fatal_var('curr_cons_owner', nwown)
                set_fatal_var('console_owners', owns)
            
            comms = ''
        
        splcmd = comms.split(' ', 1)
        
        if splcmd:
            cmd = splcmd[0]
            cmd = cmd.lower()
            
            resource = get_cfg_param('resource')
            
            aliaso = get_fatal_var(owner, 'alias')
            
            if is_var_set('command_handlers', cmd):
                cmdhnd = get_fatal_var('command_handlers', cmd)
                
                init_fatal_event('console_event')
                
                if len(splcmd) > 1:
                    params = ' '.join(splcmd[1:])
                    call_in_sep_thr(owner + '/console', cmdhnd, 'console', [owner + '/' + resource, owner, ''], params)
                else:
                    call_in_sep_thr(owner + '/console', cmdhnd, 'console', [owner + '/' + resource, owner, ''], '')
                
                wait_fatal_event('console_event', 3)

                constr = str(cgv('console_restr'))
                sprint(constr)
            elif cmd in aliaso.galiaslist:
                exp_alias = aliaso.expand(cmd, [owner + '/' + resource, owner, ''])
                
                spl_comm_par = exp_alias.split(' ', 1)
                comm = spl_comm_par[0]
                params = ''
                
                if len(spl_comm_par) >= 2:
                    alias_par = spl_comm_par[1]
                    params = '%s %s' % (alias_par, params)
                    params = params.strip()
                
                if is_var_set('command_handlers', comm.lower()):
                    cmdhnd = get_fatal_var('command_handlers', comm.lower())
                    
                    init_fatal_event('console_event')
                    
                    if params:
                        call_in_sep_thr(owner + '/console', cmdhnd, 'console', [owner + '/' + resource, owner, ''], params)
                    else:
                        call_in_sep_thr(owner + '/console', cmdhnd, 'console', [owner + '/' + resource, owner, ''], '')
                    
                    wait_fatal_event('console_event', 3)
                    
                    constr = str(cgv('console_restr'))
                    sprint(constr)
            else:
                exec(comms, globals())

            if readline:
                readline.write_history_file('.fatalhst')
    except EOFError:
        if is_param_seti('show_console'):
            dec_fatal_var('info', 'opnum')
            
            if not is_var_set('is_console_hide'):
                set_fatal_var('is_console_hide', 1)

                if os_uname == 'linux':
                    sprint('\n\nPress Ctrl+D to show console again.')
                else:
                    sprint('\n\nPress Ctrl+Z and Return to show console again.')
            else:
                set_fatal_var('is_console_hide', 0)

                sprint()
            
            return True
        else:
            sprint()
            return True
    except IOError:
        return False
    except Exception:
        sprint()
        sprint(log_exc_error())
        
#-------------------------------- Plugins routines -----------------------------------------
    
def _chk_md5_and_reld_pls():
    chd_pls = []
    
    plugins = get_fatal_var('plugins')
    
    for plugin in plugins:
        try:
            cpl_md5 = _plmd5hash(plugin)
            
            if get_fatal_var('pls_md5_hash', plugin) != cpl_md5:
                chd_pls.append(plugin)
                set_fatal_var('pls_md5_hash', plugin, cpl_md5)
        except Exception:
            log_exc_error()

    _reload_chd_pls(chd_pls)
    
def _reload_chd_pls(chd_pls):
    lfail = []
    
    for plugin in chd_pls:
        try:
            _reload(plugin)
        except Exception:
            lfail.append(plugin)
            log_exc_error()

    lsucc = [lis for lis in chd_pls if not lis in lfail]
    
    if lsucc:
        reinit_stage1_init_hds()
    
    rltime = time.strftime('%H:%M:%S', time.localtime(time.time()))
    
    if lfail:
        sprint('\n\n[%s] Failed to reload changed plugins (total: %d): %s.' % (rltime, len(lfail), ', '.join(lfail)))

    if lsucc:
        sprint('\n\n[%s] Reload changed plugins (total: %d): %s.' % (rltime, len(lsucc), ', '.join(lsucc)))

def chk_md5_and_reload():
    ocore_md5 = get_fatal_var('core_md5')
    ocfg_md5 = get_fatal_var('cfg_md5')
    ncfg_md5 = core_md5('fatal.conf')
    ncore_md5 = core_md5('fatal.py')
    
    if ocore_md5 != ncore_md5:
        prs = xmpp.Presence(typ='unavailable')
        
        sprint('\n\nCore has been changed.')
        prs.setStatus('Restart due to changes in core...')
        
        jconn = get_client_conn()
        
        if jconn:
            jconn.send(prs)
        
        time.sleep(3)
        sprint('\\Restarting...')
        restart_bot()
    
    if ocfg_md5 != ncfg_md5:
        set_fatal_var('cfg_md5', ncfg_md5)
        relres = rel_fatal_config()
        
        rltime = time.strftime('%H:%M:%S', time.localtime(time.time()))
        
        if relres:
            sprint('\n\n[%s] Reload changed config.' % (rltime))
        else:
            sprint('\n\n[%s] Failed to reload changed config.' % (rltime))

    _chk_md5_and_reld_pls()
    
def rmv_sys_dirs(lst):
    for li in lst:
        if li[0] == '.':
            lst.remove(li)
    return lst
    
def _find_plugins():
    sprint('Loading plugins...')
    plugins = os.listdir('plugins')
    plugins = rmv_sys_dirs(plugins)
    return plugins
    
def _load(plugin):
    __import__(plugin)

def _reload(plugin):
    plfile = get_fatal_var('ldpls', plugin)
    
    locale = get_sys_lang()
    locale = get_param('locale', locale)

    dpath = os.path.dirname(plfile)
    load_lc_msgs(locale, dpath)
    load_hlp_msgs(locale, dpath)
    
    try:
        importlib.reload(sys.modules['%s.%s' % (plugin, plugin)])
    except Exception:
        log_exc_error()

def load_plugins():
    plugins = _find_plugins()
    plugins.sort()
    loadedpl, failedpl, chkddpl = [], [], []
    
    dsblpl = get_lst_cfg_param('disabled_plugins')
    ntrelpl = get_lst_cfg_param('notreld_plugins')

    locale = get_sys_lang()
    locale = get_param('locale', locale)
    
    sprint()
    
    delim = ','
    suff = '(d)'
    ldt = 0
    tldt = 0
    
    for plugin in plugins:
        if plugin == plugins[-1]:
            delim = '.'

        try:
            try:
                if plugin in dsblpl:
                    chkddpl.append(plugin)
                    
                    suff = '(d)'
                    
                    if is_var_set('cle'):
                        sys.stdout.write('%s%s%s%s%s%s%s ' % (cl_cyan, plugin, cl_cyan,  cl_none, suff, delim, cl_none))
                    else:
                        sys.stdout.write('%s%s%s ' % (plugin, suff, delim))
                    
                    continue
            
                ldt = time.time()
            
                _load(plugin)
                
                ldt = round(time.time() - ldt, 2)
                
                tldt += ldt
                
                if ldt >= 0.5:
                    suff = '(%.2f)' % (ldt)
                else:
                    suff = ''
                
                if is_var_set('cle'):
                    sys.stdout.write('%s%s%s%s%s%s%s ' % (cl_bgreen, plugin, cl_bgreen,  cl_none, suff, delim, cl_none))
                else:
                    sys.stdout.write('%s%s%s ' % (plugin, suff, delim))
                    
                plpath = sys.modules[plugin].__path__
                plfile = '%s/%s.py' % (plpath[0], plugin)
                set_fatal_var('ldpls', plugin, plfile)
                loadedpl.append(plugin)
                
                dpath = os.path.dirname(plfile)
                
                if is_param_set('jid'):
                    load_lc_msgs(locale, dpath)
                    load_hlp_msgs(locale, dpath)
                else:
                    load_lc_msgs(locale, dpath, 'fatal-bot')
                    load_hlp_msgs(locale, dpath, 'fatal-bot')
            except Exception:
                suff = '(f)'
                
                if is_var_set('cle'):
                    sys.stdout.write('%s%s%s%s%s%s%s ' % (cl_bred, plugin, cl_bred,  cl_none, suff, delim, cl_none))
                else:
                    sys.stdout.write('%s%s%s ' % (plugin, suff, delim))
                
                log_exc_error()
                failedpl.append(plugin)
                continue

            sys.stdout.flush()
            
            relc = get_int_cfg_param('reload_code')
            
            if relc and plugin not in ntrelpl:
                cpl_md5 = _plmd5hash(plugin)
                set_fatal_var('pls_md5_hash', plugin, cpl_md5)
        except Exception:
            log_exc_error()
            failedpl.append(plugin)
    
    if is_var_set('cle'):
        sprint(cl_none)
    else:
        sprint()
    
    if loadedpl:
        sprint('\n\\Loaded plugins (%.2f) (total: %d).' % (round(tldt, 2), len(loadedpl)))
    
    if chkddpl:
        chkddpl.sort()
        sprint('\n\\Disabled plugins (d) (total: %d):' % (len(chkddpl)))
        displ = ', '.join(chkddpl)
        
        if is_var_set('cle'):
            sprint('%s%s%s%s%s%s ' % (cl_cyan, displ, cl_cyan,  cl_none, delim, cl_none))
        else:
            sprint(displ + '.')
    
    if failedpl:
        failedpl.sort()
        sprint('\n\\Failed to load plugins (f) (total: %d):' % (len(failedpl)))
        invp = ', '.join(failedpl)
        
        if is_var_set('cle'):
            sprint('%s%s%s%s%s%s ' % (cl_bred, invp, cl_bred,  cl_none, delim, cl_none))
        else:
            sprint(invp + '.')
        
        sprint('\nPlugins have inner errors!')
        
    if loadedpl:
        loadedpl.sort()
        
        loadedpl = [li for li in loadedpl if not li in ntrelpl]
        
        add_fatal_var('plugins', loadedpl)
        
        sprint()
    else:
        sprint('\n\\There are no plugins to load!\n')
        
def _base64dec(target):
    decrypted = base64.decodestring(target)
    return decrypted

def _plmd5hash(plugin):
    plf = 'plugins/%s/%s.py' % (plugin, plugin)
    plb = _get_pl_body(plf)
    return _md5hash(plb.encode())

def _get_pl_ctime(plfile):
    if os.path.exists(plfile):
        stat = os.stat(plfile)
        return str(int(stat.st_ctime))
    else:
        return ''

def _get_pl_body(plfile):
    if os.path.exists(plfile):
        fd = open(plfile, 'r', encoding="utf-8")
        plbody = fd.read()
        fd.close()
        return plbody
    else:
        return ''

def xmpp_read_data():
    conn = get_client_conn()
    recv = conn._owner.Connection._recv
    
    data = b''
    
    #while not data:
    try:
        #time.sleep(0.3)
        data = recv(1024)
    except Exception:
        log_exc_error()
        data = b''
    
    req = b''

    while data:
        req += data
        try:
            data = recv(1024)
        except Exception:
            break
        
    return req

def xmpp_nested_rtns(stanza):
    jconn = get_client_conn()
    
    xml=b''
    rcv = ''
    
    set_client_var('stop_xmpp_proc', 1)    
    
    jconn.send(stanza)
    
    #return xmpp_read_data()
    
    unid = 'spf%s' % (rand10())

    while True:
        while rcv == '': 
            rcv = jconn._owner.Connection.receive()
            
            if is_cvar_set(unid): break

        try:
            if rcv == '':
                break
            
            xmpp.simplexml.XML2Node(rcv)
            xml = rcv
            break
        except ExpatError:
            set_client_var(unid, 1)
            
            if rcv != '':
                xml += rcv
            else: break
           
            rcv = ''
    
    rmv_client_var(unid)
    rmv_client_var('stop_xmpp_proc')
    
    return xml

def extr_nested_cmd(expr):
    cn = gcp('comm_nested', '#')
    
    pat = '%s{1,1}[a-z_а-я]{1,}:{2,2}' % (cn)
    sts = []
    
    mit = re.finditer(pat, expr)
    
    for oi in mit:
        sts.append(oi.start())
    
    for s in sts:
        si = s + 1
        
        fe = expr[si:].find(cn) + si
        
        if fe in sts:
            continue
        else:
            return [expr[s:fe+1]]
    return []

def rep_nested_cmds_ex(ttype, source, params):
    cn = gcp('comm_nested', '#')
    
    fcmds = []
    
    def get_fcmds(params):
        frex = '%s{1,1}[a-z_а-я]{1,}%s{1,1}' % (cn, cn)
        
        fcmds = re.findall(frex, params)
        
        if not fcmds:
            fcmds = extr_nested_cmd(params)
            
        return fcmds    
    
    if not (params.count(cn) % 2) and params.count(cn):
        fcmds = get_fcmds(params)
        
        cmdl = get_list_fatal_var('command_handlers')
        
        while fcmds:
            fcmd = fcmds[0]
            
            if fcmd.count('::'):
                spc = fcmd.replace(cn, '')
                spc = safe_split(spc, '::')
                
                com = spc[0]
                par = spc[1]
                
                cnm = get_real_cmd_name(com)
                
                if not cnm:
                    cnm = com
                
                if cnm in cmdl:
                    if check_access(ttype, source, cnm):
                        cmd_hnd = get_fatal_var('command_handlers', cnm)
                        
                        try:
                            res = cmd_hnd(ttype, source, par)
                        except Exception:
                            res = '[-1]'
                        
                        params = params.replace(fcmd, str(res), 1)
                    else:
                        return params
                else:
                    return params
            else:
                spc = fcmd.replace(cn, '')
                com = spc
                
                cnm = get_real_cmd_name(com)
                
                if not cnm:
                    cnm = com
                
                if cnm in cmdl:
                    if check_access(ttype, source, cnm):
                        cmd_hnd = get_fatal_var('command_handlers', cnm)
                        
                        try:
                            res = cmd_hnd(ttype, source, '')
                        except Exception:
                            res = '[-1]'
                        
                        params = params.replace(fcmd, str(res), 1)
                    else:
                        return params
                else:
                    return params
            
            fcmds = get_fcmds(params)

    return params

def rep_nested_cmds(ttype, source, params):
    cn = gcp('comm_nested', '#')
        
    if not (params.count(cn) % 2) and params.count(cn):
        frex = '%s{1,1}[a-z_а-я]{1,}%s{1,1}' % (cn, cn)
        
        fcmds = re.findall(frex, params)
        
        if not fcmds:
            fcmds = extr_nested_cmd(params)
        
        cmdl = get_list_fatal_var('command_handlers')
        
        if fcmds:
            fcmd = fcmds[0]
            
            if fcmd.count('::'):
                spc = fcmd.replace(cn, '')
                spc = safe_split(spc, '::')
                
                com = spc[0]
                par = spc[1]
                
                cnm = get_real_cmd_name(com)
                
                if not cnm:
                    cnm = com
                
                if cnm in cmdl:
                    if check_access(ttype, source, cnm):
                        cmd_hnd = get_fatal_var('command_handlers', cnm)
                        
                        try:
                            res = cmd_hnd(ttype, source, par)
                        except Exception:
                            log_exc_error()
                            res = '[-1]'

                        params = params.replace(fcmd, str(res), 1)
                    else:
                        return params
                else:
                    return params
            else:
                spc = fcmd.replace(cn, '')
                com = spc
                
                cnm = get_real_cmd_name(com)
                
                if not cnm:
                    cnm = com
                
                if cnm in cmdl:
                    if check_access(ttype, source, cnm):
                        cmd_hnd = get_fatal_var('command_handlers', cnm)
                        
                        try:
                            res = cmd_hnd(ttype, source, '')
                        except Exception:
                            res = '[-1]'
                        
                        params = params.replace(fcmd, str(res), 1)
                    else:
                        return params
                else:
                    return params
            
            return rep_nested_cmds(ttype, source, params)
    
    return params

#-------------------------------- Handlers routines ---------------------------------------

def register_message_handler(instance):
    hname = instance.__name__
    set_fatal_var('message_handlers', hname, instance)

def register_outgoing_message_handler(instance):
    hname = instance.__name__
    set_fatal_var('outgoing_message_handlers', hname, instance)
    
def register_join_handler(instance):
    hname = instance.__name__
    set_fatal_var('join_handlers', hname, instance)

def register_leave_handler(instance):
    hname = instance.__name__
    set_fatal_var('leave_handlers', hname, instance)

def register_iq_handler(instance):
    hname = instance.__name__
    set_fatal_var('iq_handlers', hname, instance)

def register_presence_handler(instance):
    hname = instance.__name__
    set_fatal_var('presence_handlers', hname, instance)

def register_stage0_init(instance):
    hname = instance.__name__
    set_fatal_var('stage0_init', hname, instance)
    
def register_stage1_init(instance):
    hname = instance.__name__
    set_fatal_var('stage1_init', hname, instance)

def register_stage2_init(instance):
    hname = instance.__name__
    set_fatal_var('stage2_init', hname, instance)
    
def register_command_handler(instance, command, access=0):    
    set_fatal_var('command_handlers', command, instance)
    set_fatal_var('commands', command, 'access', access)

def reinit_stage1_init_hds():
    cid = get_client_id()
    
    gchs = list(get_dict_fatal_var(cid, 'gchrosters'))
    
    hndns = []

    if is_var_set('stage1_init'):
        hndns = list(get_fatal_var('stage1_init'))

    for groupchat in gchs:
        for hname in hndns:
            stg1_hnd = get_fatal_var('stage1_init', hname)
            
            stin_thr = init_fatal_thr(cid + '/reinit_stage1_init_hds', stg1_hnd, groupchat)
            
            stin_thr.ttype = 'stg'
            
            put_in_thr_pool(st1_prt, stin_thr)

def call_stage0_init_handlers():
    hndns = []

    if is_var_set('stage0_init'):
        hndns = list(get_fatal_var('stage0_init'))

    for hname in hndns:
        stg0_hnd = get_fatal_var('stage0_init', hname)
        
        cid = get_client_id()
        
        stin_thr = init_fatal_thr(cid + '/call_stage0_init_handlers', stg0_hnd)
        
        stin_thr.ttype = 'stg'

        put_in_thr_pool(st0_prt, stin_thr)

def call_stage1_init_handlers(groupchat):
    hndns = []

    if is_var_set('stage1_init'):
        hndns = list(get_fatal_var('stage1_init'))

    for hname in hndns:
        stg1_hnd = get_fatal_var('stage1_init', hname)
        
        cid = get_client_id()
        
        stin_thr = init_fatal_thr(cid + '/call_stage1_init_handlers', stg1_hnd, groupchat)
        
        stin_thr.ttype = 'stg'

        put_in_thr_pool(st1_prt, stin_thr)

def call_stage2_init_handlers():
    hndns = []

    if is_var_set('stage2_init'):
        hndns = list(get_fatal_var('stage2_init'))

    for hname in hndns:
        stg2_hnd = get_fatal_var('stage2_init', hname)
        
        cid = get_client_id()
        
        stin_thr = init_fatal_thr(cid + '/call_stage2_init_handlers', stg2_hnd)
        
        stin_thr.ttype = 'stg'

        put_in_thr_pool(st2_prt, stin_thr)

def call_message_handlers(type, source, body):
    gch_jid = source[1]
    
    gblock = int(get_param('global_lock', '0'))
    cblock = int(get_gch_param(gch_jid, 'conf_lock', '0'))
    jid = get_true_jid(source)
    
    if gblock:
        if not get_fatal_var('admins', jid):
            return
    if cblock:
        if not get_fatal_var('admins', jid):
            return

    hndns = []

    if is_var_set('message_handlers'):
        hndns = list(get_fatal_var('message_handlers'))

    for hname in hndns:
        inmsg_hnd = get_fatal_var('message_handlers', hname)
        
        cid = get_client_id()
        
        thr = init_fatal_thr(cid + '/call_message_handlers', inmsg_hnd, type, source, body)
        
        thr.ttype = 'msg'

        put_in_thr_pool(msg_prt, thr)

def call_outgoing_message_handlers(target, body, obody):
    gch_jid = target

    gblock = int(get_param('global_lock', '0'))
    cblock = int(get_gch_param(gch_jid, 'conf_lock', '0'))
    jid = get_true_jid(target)
    
    if gblock:
        if not is_bot_admin(jid):
            return

    if cblock:
        if not is_bot_admin(jid):
            return
    
    hndns = []

    if is_var_set('outgoing_message_handlers'):
        hndns = list(get_fatal_var('outgoing_message_handlers'))

    for hname in hndns:
        omsg_hnd = get_fatal_var('outgoing_message_handlers', hname)
        
        cid = get_client_id()
        
        thr = init_fatal_thr(cid + '/call_outgoing_message_handlers', omsg_hnd, target, body, obody)
        
        thr.ttype = 'msg'

        put_in_thr_pool(oms_prt, thr)

def call_join_handlers(groupchat, nick, afl, role):
    hndns = []

    if is_var_set('join_handlers'):
        hndns = list(get_fatal_var('join_handlers'))

    for hname in hndns:
        join_hnd = get_fatal_var('join_handlers', hname)
        
        cid = get_client_id()
        
        thr = init_fatal_thr(cid + '/call_join_handlers', join_hnd, groupchat, nick, afl, role)
        
        thr.ttype = 'joi'

        put_in_thr_pool(joi_prt, thr)

def call_leave_handlers(groupchat, nick, reason, code):	
    hndns = []

    if is_var_set('leave_handlers'):
        hndns = list(get_fatal_var('leave_handlers'))

    for hname in hndns:
        leave_hnd = get_fatal_var('leave_handlers', hname)
        
        cid = get_client_id()
        
        thr = init_fatal_thr(cid + '/call_leave_handlers', leave_hnd, groupchat, nick, reason, code)
        
        thr.ttype = 'lev'

        put_in_thr_pool(lev_prt, thr)

def call_iq_handlers(iq):
    hndns = []

    if is_var_set('iq_handlers'):
        hndns = list(get_fatal_var('iq_handlers'))

    for hname in hndns:
        iq_hnd = get_fatal_var('iq_handlers', hname)
        
        cid = get_client_id()
        
        thr = init_fatal_thr(cid + '/call_iq_handlers', iq_hnd, iq)
        
        thr.ttype = 'iq'

        put_in_thr_pool(iq_prt, thr)

def call_presence_handlers(prs):
    hndns = []

    if is_var_set('presence_handlers'):
        hndns = list(get_fatal_var('presence_handlers'))

    for hname in hndns:
        prs_hnd = get_fatal_var('presence_handlers', hname)
        
        cid = get_client_id()
        
        thr = init_fatal_thr(cid + '/call_presence_handlers', prs_hnd, prs)
        
        thr.ttype = 'prs'

        put_in_thr_pool(prs_prt, thr)

def call_command_handlers(command, ttype, source, parameters, callee):
    cid = get_client_id()
    
    gch_jid = source[1]
    alias = get_fatal_var(cid, 'alias')
    real_access = alias.get_access(callee, gch_jid)

    gblock = int(get_param('global_lock', '0'))
    cblock = int(get_gch_param(gch_jid, 'conf_lock', '0'))
    jid = get_true_jid(source)

    guser = str(source[0])

    if gch_jid == jid:
        guser = ''

    if gblock:
        if not is_bot_admin(jid):
            return

    if cblock:
        if not is_bot_admin(jid):
            return

    if is_var_set('command_handlers', command):
        cmd_hnd = get_fatal_var('command_handlers', command)
        
        if check_access(ttype, source, command):
            cmdl = ('acomm', 'ctask', 'remind', 'alias_add', 'galias_add') 

            if not command in cmdl:
                parameters = rep_nested_cmds('null', source, parameters)
            
            if not is_bot_admin(jid):
                log_cmd_run(callee, parameters, guser, jid)
            
            cid = get_client_id()
            
            thr = init_fatal_thr(cid + '/call_command_handlers', cmd_hnd, ttype, source, parameters)
            
            cmd_prt = get_cmd_thr_prt(real_access)
            
            thr.ttype = 'cmd'

            put_in_thr_pool(cmd_prt, thr)
        else:
            reply(ttype, source, l('Too few rights!'))

#------------------------------------------------------------------------------------------

def rmv_cmd_name(aname=''):
    cid = get_client_id()
    
    if not aname:
        sql = 'DELETE FROM cmdnames;'
        args = ()
    else:
        sql = "DELETE FROM cmdnames WHERE aname=?;"
        args = (aname,)
    
    qres = sqlquery('dynamic/%s/cmdnames.db' % (cid), sql, *args)
    
    return qres
    
def cmd_name_exists(real_cmd):
    cid = get_client_id()
    
    sql = "SELECT * FROM cmdnames WHERE iname=?;"
    qres = sqlquery('dynamic/%s/cmdnames.db' % (cid), sql, real_cmd)
    
    if qres:
        return True
    else:
        return False

def get_real_cmd_name(cmdname):
    cid = get_client_id()
    
    sql = "SELECT iname FROM cmdnames WHERE aname=?;"
    qres = sqlquery('dynamic/%s/cmdnames.db' % (cid), sql, cmdname)
    
    if qres:
        iname = qres[0][0]
        return iname
    else:
        return ''
        
def get_cmd_name(real_cmd):
    cid = get_client_id()

    sql = "SELECT aname FROM cmdnames WHERE iname=?;"
    qres = sqlquery('dynamic/%s/cmdnames.db' % (cid), sql, real_cmd)
    
    if qres:
        aname = qres[0][0]
        return aname
    else:
        return ''

def get_cmd_name_list():
    cid = get_client_id()
    
    sql = "SELECT * FROM cmdnames;"
    qres = sqlquery('dynamic/%s/cmdnames.db' % (cid), sql)
    
    if qres:
        return qres
    else:
        return ''

def set_cmd_name(real_cmd, aname):
    cid = get_client_id()
    
    if not cmd_name_exists(real_cmd):
        sql = "INSERT INTO cmdnames (iname, aname) VALUES (?, ?);"
        args = real_cmd.strip(), aname.strip()
    elif get_cmd_name(aname):
        sql = "DELETE FROM cmdnames WHERE iname=?;"
        args = (real_cmd.strip(),)
    else:
        sql = "UPDATE cmdnames SET aname=? WHERE iname=?;"
        args = aname.strip(), real_cmd.strip()
    
    qres = sqlquery('dynamic/%s/cmdnames.db' % (cid), sql, *args)
    
    return qres
        
def cmd_access_exists(cmd):
    cid = get_client_id()

    sql = "SELECT * FROM cmdaccess WHERE cmd=?;"
    qres = sqlquery('dynamic/%s/cmdaccess.db' % (cid), sql, cmd)
    
    if qres:
        return True
    else:
        return False

def get_cmd_access(cmd):
    cid = get_client_id()
    
    sql = "SELECT acc FROM cmdaccess WHERE cmd=?;"
    qres = sqlquery('dynamic/%s/cmdaccess.db' % (cid), sql, cmd)
    
    if qres:
        access = qres[0][0]
        return access
    else:
        return '-1'

def set_cmd_access(cmd, access):
    cid = get_client_id()
    
    if not cmd_access_exists(cmd):
        sql = "INSERT INTO cmdaccess (cmd, acc) VALUES (?, ?);"
        args = cmd.strip(), access.strip()
    else:
        sql = "UPDATE cmdaccess SET acc=? WHERE cmd=?;"
        args = access.strip(), cmd.strip()
    
    qres = sqlquery('dynamic/%s/cmdaccess.db' % (cid), sql, *args)
    
    return qres

#----------------------------------- Dynamic routines ---------------------------------------------------------

def init_dirs():
    if not os.path.exists('dynamic'): 
        os.mkdir('dynamic', 0o755)
    
    if not os.path.exists('syslogs'): 
        os.mkdir('syslogs', 0o755)

def init_dynamic(cid):
    if not os.path.exists('dynamic/%s' % (cid)): 
        os.mkdir('dynamic/%s' % (cid), 0o755)
    
    if not is_db_exists('dynamic/%s/gaccess.db' % (cid)):
        sql = 'CREATE TABLE access (jid VARCHAR(50) NOT NULL, access VARCHAR(4) NOT NULL, UNIQUE(jid));'
        qres = sqlquery('dynamic/%s/gaccess.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX iaccess ON access (jid);'
        sqlquery('dynamic/%s/gaccess.db' % (cid), sql)
        
        if qres != '':
            adms = get_lst_cfg_param('admins')
            
            for jid in adms:
                set_user_access(jid, 100)

    if not is_db_exists('dynamic/%s/gbt_config.db' % (cid)):
        sql = 'CREATE TABLE config (param VARCHAR(50) NOT NULL, value VARCHAR, UNIQUE(param));'
        qres = sqlquery('dynamic/%s/gbt_config.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX iconfig ON config (param);'
        sqlquery('dynamic/%s/gbt_config.db' % (cid), sql)
        
        locale = get_sys_lang()
        set_param('locale', locale)
        
        set_comm_prefix()
    
    if not is_db_exists('dynamic/%s/chatrooms.db' % (cid)):
        sql = 'CREATE TABLE chatrooms (chatroom VARCHAR(50) NOT NULL, nick VARCHAR, pass VARCHAR, UNIQUE(chatroom));'
        qres = sqlquery('dynamic/%s/chatrooms.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX ichatrooms ON chatrooms (chatroom);'
        sqlquery('dynamic/%s/chatrooms.db' % (cid), sql)
        
        if qres != '':
            if is_param_set('default_chatroom'):
                add_chatroom()

    if not is_db_exists('dynamic/%s/alias.db' % (cid)):
        sql = 'CREATE TABLE aliasdb (alias VARCHAR(50) NOT NULL, body VARCHAR, access VARCHAR(3), UNIQUE(alias));'
        sqlquery('dynamic/%s/alias.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX ialiasdb ON aliasdb (alias);'
        sqlquery('dynamic/%s/alias.db' % (cid), sql)

    if not is_db_exists('dynamic/%s/cmdaccess.db' % (cid)):
        sql = 'CREATE TABLE cmdaccess (cmd VARCHAR(50) NOT NULL, acc VARCHAR(3), UNIQUE(cmd));'
        sqlquery('dynamic/%s/cmdaccess.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX icmdaccess ON cmdaccess (cmd);'
        sqlquery('dynamic/%s/cmdaccess.db' % (cid), sql)

    if not is_db_exists('dynamic/%s/cmdnames.db' % (cid)):
        sql = 'CREATE TABLE cmdnames (iname VARCHAR(50) NOT NULL, aname VARCHAR(50) NOT NULL, UNIQUE(iname));'
        sqlquery('dynamic/%s/cmdnames.db' % (cid), sql)
        
        sql = 'CREATE UNIQUE INDEX icmdnames ON cmdnames (iname);'
        sqlquery('dynamic/%s/cmdnames.db' % (cid), sql)

#---------------------------------- Groupchat routines --------------------------------------------------------

def init_gch_roster(gch, reinit=False):
    cid = get_client_id()
    
    if gch:
        if not is_var_set(cid, 'gchrosters', gch) or reinit:
            roster = get_fatal_var(cid, 'roster')
            
            if roster:
                raw_itm = {}
                
                if gch in roster.getItems():
                    raw_itm = roster.getRawItem(gch)
                
                if raw_itm:
                    set_fatal_var(cid, 'gchrosters', gch, raw_itm['resources'])
                    
                    return True
    return False

def rmv_gch_roster(gch):
    cid = get_client_id()
    
    if gch:
        if is_var_set(cid, 'gchrosters', gch):
            rmv_fatal_var(cid, 'gchrosters', gch)
            return True
    return False

def sadmin_jid():
    admlst = get_lst_cfg_param('admins')

    if admlst:
        return admlst[0]
    return 'null'

def is_bot_admin(jid):
    admlst = get_lst_cfg_param('admins')
    
    if isinstance(jid, int):
        gdba = get_tg_usr_acc(jid)
    else:
        gdba = get_user_access(jid)
        
    tgua = get_int_cfg_param('tgbot_admin_id')
    
    if jid in admlst or jid == tgua or gdba == 100:
        return True
    return False

def is_gch_user(gch, nick):
    cid = get_client_id()
    
    if is_var_set(cid, 'gchrosters', gch, nick):
        return True
    return False

def get_user_show(gch, nick):
    cid = get_client_id()
    
    show = get_fatal_var(cid, 'gchrosters', gch, nick, 'show')

    if show:
        return show
    return 'online'
    
def get_user_status(gch, nick):
    cid = get_client_id()
    
    status = get_fatal_var(cid, 'gchrosters', gch, nick, 'status')

    if status:
        return status
    return ''
    
def get_user_jid(gch, nick, full=True):
    cid = get_client_id()
    
    full_jid = get_fatal_var(cid, 'gchrosters', gch, nick, 'rjid')
    
    if full:
        return full_jid
    return get_stripped(full_jid)
    
def get_gch_aff(gch, nick):
    cid = get_client_id()
    
    aff = get_fatal_var(cid, 'gchrosters', gch, nick, 'affiliation')

    if aff:
        return aff
    else:
        return 'none'

def get_gch_role(gch, nick):
    cid = get_client_id()
    
    role = get_fatal_var(cid, 'gchrosters', gch, nick, 'role')

    if role:
        return role
    else:
        return 'none'
        
def is_groupchat(jid):
    cid = get_client_id()
    
    if isinstance(jid, int):
        if jid < 0:
            return True
    
    if is_var_set(cid, 'gchrosters', jid):
        return True
    return False

def get_bot_nick(groupchat):
    if gch_exists(groupchat):
        def_nick = get_cfg_param('default_nick', 'fatal-bot')
        bot_nick = get_chatroom_info(groupchat, 'nick', def_nick)
        
        if bot_nick:
            return bot_nick
        return def_nick
    else:
        return ''
    
def add_chatroom(gch='', nick='', passw=''):
    if not gch:
        gch = get_cfg_param('default_chatroom')

    if not nick:
        nick = get_cfg_param('default_nick')
    
    if not gch: 
        return
    
    if not gch_exists(gch):
        sql = "INSERT INTO chatrooms (chatroom, nick, pass) VALUES (?, ?, ?);"
        args = gch.strip(), nick.strip(), passw.strip()
    else:
        sql = "UPDATE chatrooms SET nick=?, pass=? WHERE chatroom=?;"
        args = nick.strip(), passw.strip(), gch.strip()

    cid = get_client_id()

    qres = sqlquery('dynamic/%s/chatrooms.db' % (cid), sql, *args)

    return qres
    
def add_gch(groupchat='', nick='', passw=''):
    if not groupchat:
        groupchat = get_cfg_param('default_chatroom')

    if not nick:
        nick = get_cfg_param('default_nick')
    
    if gch_exists(groupchat):
        add_chatroom(gch=groupchat, nick=nick, passw=passw)
        return 1
    else:
        if nick and groupchat and passw:
            add_chatroom(gch=groupchat, nick=nick, passw=passw)
        elif nick and groupchat:
            add_chatroom(gch=groupchat, nick=nick)
        elif groupchat:
            remove_chatroom(groupchat)
        elif passw:
            add_chatroom(gch=groupchat, passw=passw)
        else:
            return 0
        return 1

def change_bot_status(gch, status, show=''):
    if gch:
        prs = xmpp.Presence(gch + '/' + get_bot_nick(gch))
    else:
        jid = get_client_id()
        prs = xmpp.Presence(jid)
    
    if status:
        prs.setStatus(status)
        
    if show and (show != 'online'):
        prs.setShow(show)
    
    botver = '[unknown]'
    
    ver = get_fatal_var('ftver', 'botver', 'ver')
    rev = get_fatal_var('ftver', 'rev')
    cpn = get_fatal_var('ftver', 'caps')
    
    if not rev: 
        rev = ''

    if ver:
        botver = ver % (rev)
    
    prs.setTag('c', namespace=xmpp.NS_CAPS, attrs={'node': cpn, 'ver': botver})
    
    jconn = get_client_conn()
    jconn.send(prs)

def set_init_status():
    cprfx = get_comm_prefix()
    
    if not param_exists('', 'status_text'):
        stmsg = l('Type %shelp and follow instructions of the bot to understand how to work with me!') % (cprfx)
        
        set_param('status_text', stmsg)
        set_param('status_show', 'online')
        
        change_bot_status('', stmsg)
    else:
        stmsg = get_param('status_text', l('Type %shelp and follow instructions of the bot to understand how to work with me!') % (cprfx))
        status = get_param('status_show', 'online')
        
        if stmsg.count('%shelp'):
            stmsg = l(stmsg) % (cprfx)
        
        change_bot_status('', stmsg, status)

def join_groupchat(groupchat='', nick='', passw=''):
    cprfx = get_comm_prefix()
    
    if not groupchat:
        groupchat = get_cfg_param('default_chatroom')
    
    if not nick:
        nick = get_chatroom_info(groupchat, 'nick')
    
    if not nick:
        nick = get_cfg_param('default_nick')

        if not nick:
            nick = 'fatal-bot'
    
    add_gch(groupchat, nick, passw)

    prs = xmpp.Presence('%s/%s' % (groupchat, nick))

    if not is_groupchat(groupchat):
        status = l('Loading... Please wait...')
        prs.setStatus(status)
    
    show = get_gch_param(groupchat, 'status_show', 'online')
    stmsg = get_gch_param(groupchat, 'status_text', l('Type %shelp and follow instructions of the bot to understand how to work with me!') % (cprfx))
    
    if stmsg.count('%shelp'):
        stmsg = l(stmsg) % (cprfx)

    if not show:
        show = 'online'
        set_gch_param(groupchat, 'status_show', show)
    
    botver = '[unknown]'
    
    ver = get_fatal_var('ftver', 'botver', 'ver')
    rev = get_fatal_var('ftver', 'rev')
    cpn = get_fatal_var('ftver', 'caps')
    
    if not rev:
        rev = ''
    
    if ver:
        botver = ver % (rev)

    if (show != '') and (show != 'online'):
        prs.setShow(show)
        
    prs.setStatus(stmsg)
    pres = prs.setTag('x', namespace=xmpp.NS_MUC)
    prs.setTag('c', namespace=xmpp.NS_CAPS, attrs={'node': cpn, 'ver': botver})
    pres.addChild('history', {'maxchars': '0', 'maxstanzas': '0'})
    
    if passw:
        pres.setTagData('password', passw)

    jconn = get_client_conn()
    jconn.send(prs)

def leave_groupchat(groupchat, status=''):
    if is_groupchat(groupchat):
        prs = xmpp.Presence(groupchat, 'unavailable')
        
        if status:
            prs.setStatus(status)
        
        jconn = get_client_conn()
        jconn.send(prs)
        
        rmv_gch_roster(groupchat)
        remove_chatroom(groupchat)

def send_tgbot_msg(chatid: Union[int, str], body: str) -> str:
    tbot = get_client_var('tgbot')
    
    if tbot:
        try:
            tbot.send_message(chatid, body)
        except Exception:
            cnt = 5
            snt = 0
            while cnt != 0:
                try:
                    time.sleep(1)
                    snt += 1
                    tbot.send_message(chatid, '<%d> %s' % (snt, body))
                    return body
                except Exception:
                    cnt -= 1
            return ''

def send_tgcli_msg(chatid: Union[int, str], body: str) -> str:
    tgcli = get_client_var('tgram_client')
    
    if tgcli:
        try:
            craiot(tgcli.send_message(chatid, body))
            return body
        except Exception:
            return ''

def msg(target, body, chatid=0):
    if target == 'null':
        return body
    
    if target == 'console':
        if is_param_seti('show_console'):
            constr = '\n' + body + '\n'
        else:
            constr = body
        
        try:
            csv('console_restr', constr)
            
            if is_event_init('console_event'):
                set_fatal_event('console_event')
            else:
                if not is_var_set('is_console_hide'):
                    sys.stdout.write('\n' + constr)
                else:
                    sys.stdout.write(constr)
                    
                sys.stdout.flush()
            
            return
        except Exception:
            log_exc_error()
            return

    if target == 'telegram':
        send_tgbot_msg(chatid, body)

        return

    if target == 'tgclient':
        send_tgcli_msg(chatid, body)
        
        return
    
    if not isinstance(body, str):
        body = body.decode('utf8', 'replace')
        
    obody = body
    
    mess = xmpp.Message(target)
    
    Id = 'msg%s' % (rand10())
    mess.setID(Id)
    
    if is_groupchat(target):
        mess.setType('groupchat')
        
        msg_limit = get_int_cfg_param('msg_chatroom_limit', 5000)
        
        if len(body) > msg_limit:
            body = body[:msg_limit] + ' [...'
            
        if body:
            mess.setBody(body)
        else:
            mess.setTag('body')
    else:
        mess.setType('chat')
        
        if body:
            mess.setBody(body)

    jconn = get_client_conn()

    sres = jconn.send(mess)
    
    if not sres:
        if get_resource(target):
            errm = xmpp.Message(target)
            errm.setType('chat')
            errm.setBody(l("An error has occured while performing this operation. Don't forget to inform administrator."))    
            jconn.send(errm)
            return

    call_outgoing_message_handlers(target, body, obody)
    
    return body

def reply(ltype, source, body):
    groupchat = source[1]
    nick = source[2]
    fjid = source[0]
    
    if not isinstance(body, str):
        body = body.decode('utf8', 'replace')
    
    if ltype == 'public':
        if fjid == groupchat:
            msg(groupchat, body)
        else:
            msg(groupchat, nick + ': ' + body)
        return body
    elif ltype == 'private':
        msg(source[0], body)                     
        return body
    elif ltype == 'console':
        msg('console', body)
        return body
    elif ltype == 'telegram':
        chatid = source[1]
        msg('telegram', body, chatid)
        return body    
    elif ltype == 'null':
        set_client_var(source[0], 'last_cmd_result', body)
        log_null_cmdr(body)
        return body

def get_stripped(jid):
    if not jid:
        return ''
    
    if isinstance(jid, xmpp.JID):
        return jid.getStripped()
    
    sfspl = safe_split(jid, '/')

    return sfspl[0]

def get_resource(jid):
    if not jid: 
        return ''
    
    if isinstance(jid, xmpp.JID):
        return jid.getResource()
    return safe_split(jid, '/')[1]
                                             
def get_usernode(jid):
    if not jid: 
        return ''
    
    if isinstance(jid, xmpp.JID):
        return jid.getNode()
    return safe_split(jid, '@')[0]
    
def get_domain(jid):
    if not jid: 
        return ''
    
    if isinstance(jid, xmpp.JID):
        return jid.getDomain()
        
    sjid = get_stripped(jid)
    
    return safe_split(sjid, '@')[1]

def get_true_jid(jid):
    true_jid = ''
    
    if isinstance(jid, list):
        jid = jid[0]
    
    if isinstance(jid, int):
        return jid

    stripped_jid = get_stripped(jid)
    resource = get_resource(jid)
    
    if not stripped_jid:
        return true_jid

    if not is_groupchat(stripped_jid):
        return stripped_jid
    
    cid = get_client_id()
    
    if is_gch_user(stripped_jid, resource):
        fulljid = get_fatal_var(cid, 'gchrosters', stripped_jid, resource, 'rjid')
        true_jid = get_stripped(fulljid)
        
        if is_groupchat(true_jid):
            return get_fatal_var(cid, 'gchrosters', stripped_jid, resource, 'rjid')
    else:
        true_jid = stripped_jid

    return true_jid

def user_access_exists(jid, gch=''):
    if not jid:
        return False
    
    sql = "SELECT * FROM access WHERE jid=?;"
    
    cid = get_client_id()
    
    if gch and is_groupchat(gch):
        qres = sqlquery('dynamic/%s/%s/access.db' % (cid, gch), sql, jid)
    else:
        qres = sqlquery('dynamic/%s/gaccess.db' % (cid), sql, jid)
    
    if qres:
        return True
    return False

def set_user_access(jid, access=0, gch=''):
    if not jid:
        return ''
   
    if not user_access_exists(jid, gch):
        access = str(access)
        sql = "INSERT INTO access (jid, access) VALUES (?, ?);"
        args = jid.strip(), access.strip()
    else:
        if access:
            access = str(access)
            sql = "UPDATE access SET access=? WHERE jid=?;"
            args = access.strip(), jid.strip()
        else:
            sql = "DELETE FROM access WHERE jid=?;"
            args = (jid.strip(),)
    
    cid = get_client_id()
    
    if gch:
        qres = sqlquery('dynamic/%s/%s/access.db' % (cid, gch), sql, *args)
    else:
        qres = sqlquery('dynamic/%s/gaccess.db' % (cid), sql, *args)
    
    return qres

def change_access_temp(gch, source, level=0):
    cid = get_client_id()
    
    jid = get_true_jid(source)

    if jid == cid:
        return

    try:
        level = int(level)
    except Exception:
        level = 0

    set_fatal_var(cid, 'accbyconf', gch, jid, level)

def user_level(source, gch=''):
    cid = get_client_id()
    jid = get_true_jid(source)
    
    if isinstance(jid, int):
        return get_tg_usr_acc(jid)
    
    if user_access_exists(jid):
        return get_user_access(jid)
    if user_access_exists(jid, gch):
        return get_user_access(jid, gch)
    
    if is_bot_admin(jid):
        return 100
    
    return get_int_fatal_var(cid, 'accbyconf', gch, jid)

def has_access(source, level, gch):
    jid = get_true_jid(source)
        
    if user_level(jid, gch) >= level:
        return 1
    return 0

def usrid_exists(usrid):
    cid = get_client_id()
    
    if type(usrid) != int:
        return False 

    sql = "SELECT * FROM tguserids WHERE id=?;"
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql, usrid)
    
    if qres:
        return True
    return False

def get_tg_usr_acc(usrid):
    cid = get_client_id()
    
    if type(usrid) != int:
        return 0 
    
    if usrid_exists(usrid):
        sql = "SELECT acc FROM tguserids WHERE id=?;"
    else:
        return 0
    
    qres = sqlquery('dynamic/%s/tguserids.db' % (cid), sql, usrid)
    
    if qres:
        return qres[0][0]
    return 0

def check_access(type, source, command):
    usracc = -1
    
    if type == 'telegram':
        usrid = source[1]
        usracc = get_tg_usr_acc(usrid)
    elif type == 'null':
        usrid = source[0]

        if isinstance(usrid, int):
            usracc = get_tg_usr_acc(usrid)
    
    real_access = int(get_cmd_access(command))

    gch = source[1]
    
    if real_access < 0:
        real_access = get_int_fatal_var('commands', command, 'access')

    if has_access(source, real_access, gch) or (usracc >= real_access):
        return True
    return False

def gch_exists(gch):
    cid = get_client_id()
    
    sql = "SELECT chatroom FROM chatrooms WHERE chatroom=?;"
    qres = sqlquery('dynamic/%s/chatrooms.db' % (cid), sql, gch)
    
    if qres:
        return True
    return False

def remove_chatroom(gch):
    sql = ''
    if gch_exists(gch):
        sql = "DELETE FROM chatrooms WHERE chatroom=?;"

    cid = get_client_id()

    qres = sqlquery('dynamic/%s/chatrooms.db' % (cid), sql, gch.strip())

    return qres

def get_chatrooms_list():
    cid = get_client_id()
    
    sql = 'SELECT chatroom FROM chatrooms;'
    qres = sqlquery('dynamic/%s/chatrooms.db' % (cid), sql)
    
    if qres:
        return [gli[0] for gli in qres]
    return []

#------------------------------------------------------------------------------------------

def param_exists(gch, param):
    sql = "SELECT * FROM config WHERE param=?;"
    
    cid = get_client_id()
    
    if gch:
        qres = sqlquery('dynamic/%s/%s/gch_config.db' % (cid, gch), sql, param)
    else:
        qres = sqlquery('dynamic/%s/gbt_config.db' % (cid), sql, param)
    
    if qres:
        return True
    return False

def add_gch_config(gch):
    cid = get_client_id()
    
    if not os.path.exists('dynamic/%s/%s' % (cid, gch)):
        os.mkdir('dynamic/%s/%s' % (cid, gch), 0o755)
        
    if not is_db_exists('dynamic/%s/%s/alias.db' % (cid, gch)):
        sql = 'CREATE TABLE aliasdb (alias VARCHAR(50) NOT NULL, body VARCHAR, access VARCHAR(3), UNIQUE(alias));'
        qres = sqlquery('dynamic/%s/%s/alias.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX ialiasdb ON aliasdb (alias);'
        sqlquery('dynamic/%s/%s/alias.db' % (cid, gch), sql)
        
    if not is_db_exists('dynamic/%s/%s/gch_config.db' % (cid, gch)):
        sql = 'CREATE TABLE config (param VARCHAR(50) NOT NULL, value VARCHAR, UNIQUE(param));'
        qres = sqlquery('dynamic/%s/%s/gch_config.db' % (cid, gch), sql)
            
        sql = 'CREATE UNIQUE INDEX iconfig ON config (param);'
        sqlquery('dynamic/%s/%s/gch_config.db' % (cid, gch), sql)
            
        if qres == '':
            sprint('Unable to create config file for %s!' % (gch))
  
def rmv_gch_param(gch, param):
    cid = get_client_id()
    
    sql = "DELETE FROM config WHERE param=?;"
    
    qres = sqlquery('dynamic/%s/%s/gch_config.db' % (cid, gch), sql, param)
    
    if qres != '':
        return True
    return False
  
def get_gch_param(gch, param, oer=''):
    cid = get_client_id()
    
    sql = "SELECT value FROM config WHERE param=?;"
    qres = sqlquery('dynamic/%s/%s/gch_config.db' % (cid, gch), sql, param)
    
    if qres == '':
        return oer
    else:
        if qres:
            value = qres[0][0]
            return value
        else:
            return oer

def get_gch_params(gch):
    cid = get_client_id()
    
    sql = "SELECT * FROM config;"
    qres = sqlquery('dynamic/%s/%s/gch_config.db' % (cid, gch), sql)
    
    return qres

def set_gch_param(gch, param, value):
    if not param_exists(gch, param):
        sql = "INSERT INTO config (param, value) VALUES (?, ?);"
        args = param.strip(), value.strip()
    else:
        sql = "UPDATE config SET value=? WHERE param=?;"
        args = value.strip(), param.strip()
    
    cid = get_client_id()
    
    qres = sqlquery('dynamic/%s/%s/gch_config.db' % (cid, gch), sql, *args)
    
    if qres != '':
        return True
    return False

def get_param(param, oer=''):
    cid = get_client_id()
    
    sql = "SELECT value FROM config WHERE param=?;"
    qres = sqlquery('dynamic/%s/gbt_config.db' % (cid), sql, param)
    
    if qres == '':
        return oer
    else:
        if qres:
            value = qres[0][0]
            return value
        else:
            return oer

def get_params():
    cid = get_client_id()
    
    sql = 'SELECT * FROM config;'
    qres = sqlquery('dynamic/%s/gbt_config.db' % (cid), sql)
    
    return qres

def set_param(param, value):
    if not param_exists('', param):
        sql = "INSERT INTO config (param, value) VALUES (?, ?);"
        args = param.strip(), value.strip()
    else:
        sql = "UPDATE config SET value=? WHERE param=?;"
        args = value.strip(), param.strip()
    
    cid = get_client_id()
    
    qres = sqlquery('dynamic/%s/gbt_config.db' % (cid), sql, *args)
    
    if qres != '':
        return True
    return False

def get_actual_param(jid, param, oer=''):
    if is_groupchat(jid):
        return get_gch_param(jid, param, oer)
    else:
        return get_param(param, oer)
        
def set_actual_param(jid, param, value):
    if is_groupchat(jid):
        return set_gch_param(jid, param, value)
    else:
        return set_param(param, value)

def get_comm_prefix(jid=''):
    prefix = get_gch_param(jid, 'prefix')
    
    if prefix:
        return prefix
        
    prefix = get_cfg_param('comm_prefix')
        
    prefix = get_param('prefix', prefix)
    
    return prefix

def set_comm_prefix(jid='', prefix=''):
    if not prefix:
        prefix = get_cfg_param('comm_prefix')
    
    return set_actual_param(jid, 'prefix', prefix)

#------------------------------------------------------------------------------------------

def get_chatroom_info(gch, info, idef=''):
    if gch_exists(gch):
        cid = get_client_id()
        
        sql = "SELECT * FROM chatrooms WHERE chatroom=?;"
        qres = sqlquery('dynamic/%s/chatrooms.db' % (cid), sql, gch)
        
        if qres:
            idic = {'chatroom': qres[0][0], 'nick': qres[0][1], 'pass': qres[0][2]}
            return idic[info]
    else:
        return idef

def get_complete_gchs_info(gchs):
    if gchs:
        gchs_struct = {}
        
        for gch in gchs:
            nick = get_chatroom_info(gch, 'nick')
            pswd = get_chatroom_info(gch, 'pass')
            gchs_struct[gch] = {'nick': nick, 'pass': pswd}
        
        return gchs_struct
    else:
        return {}

#------------------------------------------------------------------------------------------

def get_user_access(jid, gch=''):
    sql = "SELECT access FROM access WHERE jid=?;"
    
    cid = get_client_id()
    
    if gch:
        qres = sqlquery('dynamic/%s/%s/access.db' % (cid, gch), sql, jid)
    else:
        qres = sqlquery('dynamic/%s/gaccess.db' % (cid), sql, jid)
    
    if qres:
        access = qres[0][0]
        return int(access)
    else:
        return ''
    
#------------------------------------ XMPP Routines ---------------------------------------

def keep_alive_check():
    bjid = get_client_id()
    ptrs = get_int_cfg_param('ping_tries', 2)
    
    if get_int_fatal_var(bjid, 'keep_alive_checks') >= ptrs:
        dctm = get_ldc_tms()
        sprint('\nKeep alive timed out: %s' % (dctm))
        time.sleep(3)
        sprint('\\Try to reconnect...')
        
        psw = get_client_var('passwd')
        rsc = get_client_var('rsrc')
        prt = get_client_var('port')
        tls = get_client_var('tlssl')

        dec_fatal_var('connected_count') 
        set_client_var('keep_alive_checks', 0)
        
        reconnect(bjid, psw, rsc, prt, tls)
        
        return

    iq = xmpp.Iq()
    iq = xmpp.Iq('get')
    Id = 'ps%s' % (rand10())
    iq.setID(Id)
    iq.addChild('ping', {}, [], 'urn:xmpp:ping')
    
    inc_client_var('keep_alive_checks')

    jconn = get_client_conn()
    
    objl = dir(jconn)
    
    if 'SendAndCallForResponse' in objl:
        jconn.SendAndCallForResponse(iq, keep_alive_check_answ, {'sId': Id})

@handle_xmpp_exc(quiet=True)
def keep_alive_check_answ(coze, res, sId):
    if res:
        Id = res.getID()
        
        if Id != sId:
            return
                
        set_client_var('keep_alive_checks', 0)

#------------------------------------------------------------------------------

@handle_xmpp_exc(quiet=True)
def messageHnd(conn, msg):
    cid = get_client_id()

    msgtype = msg.getType()
    fromjid = msg.getFrom()
    subject = msg.getSubject()
    xprsnt = msg.getTag('x')
    jid = get_true_jid(fromjid)
    
    inc_fatal_var(cid, 'info', 'msg')
    
    gch_jid = get_stripped(fromjid)
    res_nick = get_resource(fromjid)
    
    conf = 0
        
    if is_groupchat(gch_jid):
        conf = 1
        
        if subject:
            set_fatal_var(cid, 'gch_subjs', gch_jid, subject)

    if not conf:
        if user_level(fromjid, gch_jid) == -100:
            return
    
    if not subject and not xprsnt:
        if not is_bot_admin(jid):
            guser = str(fromjid)
            
            if gch_jid == jid:
                guser = ''
            
            if ddos_detect(conf, gch_jid, guser, jid):
                return
            
            if is_jid_deny(jid):
                return

    if msg.timestamp:
        return
    
    body = msg.getBody()
    
    if not body:
        return

    if not subject and not xprsnt:
        if not is_bot_admin(jid):
            init_anti_ddos(conf, gch_jid, jid)

    if not conf or res_nick:
        if user_level(fromjid, gch_jid) >= 10:
            rcpts = msg.getTag('request', {}, 'urn:xmpp:receipts')
            
            if rcpts:
                msgre = xmpp.Message()
                msgre.setTag('received', namespace='urn:xmpp:receipts')
                msgre.setID(msg.getID())
                msgre.setTo(fromjid)
                conn.send(msgre)
    
    msg_prvt_lmt = get_int_cfg_param('msg_private_limit', 10000)
    
    if len(body) > msg_prvt_lmt:
        body = body[:msg_prvt_lmt] + ' [...'
    
    if msgtype == 'groupchat':
        mtype = 'public'
        
        if not xprsnt and not subject:
            if is_var_set(cid, 'gchrosters', gch_jid):
                set_fatal_var(cid, 'gchrosters', gch_jid, res_nick, 'idle', time.time())
    elif msgtype == 'error':
        ecode = msg.getErrorCode()
        
        if ecode == '500':
            time.sleep(0.6)
            conn.send(xmpp.Message(fromjid, body, 'groupchat'))
        elif ecode == '406':
            if not is_cvar_set('disconnected'):
                join_groupchat(gch_jid, '')
                time.sleep(0.6)
                conn.send(xmpp.Message(fromjid, body, 'groupchat'))
        return
    else:
        mtype = 'private'

    call_message_handlers(mtype, [fromjid, gch_jid, res_nick], body)
    
    bot_nick = get_bot_nick(gch_jid)
    
    bnflg = False
    
    if bot_nick == res_nick and res_nick.strip():
        return
    
    command, parameters, cbody, rcmd = '', '', '', ''

    if bot_nick:
        if body.startswith(bot_nick):
            bnflg = True
        
        for x in [bot_nick + x for x in [':', ',', '>']]:
            body = body.replace(x, '')
 
    if not body.strip():
        return
    
    body = body.lstrip()
    
    rcmd = body.split()[0]

    if is_var_set(cid, 'commoff', gch_jid, rcmd):
        return
    
    aliaso = get_fatal_var(cid, 'alias')
    
    cbody = aliaso.expand(body, [fromjid, gch_jid, res_nick])
    command = cbody.split()[0]
    
    if cbody.count(' '):
        parameters = cbody[(cbody.find(' ') + 1):]

    prefix = get_comm_prefix(gch_jid)

    if prefix and command.startswith(prefix):
        command = command.replace(prefix, '', 1)

    if cmd_name_exists(command):
        return

    cname = get_real_cmd_name(command)
    
    if not cname:
        cname = command
   
    if is_var_set('commands', cname):
        if is_var_set(cid, 'commoff', gch_jid, cname):
            return
        
        if command == rcmd and not bnflg:
            if mtype == 'public':
                return
        
        call_command_handlers(cname, mtype, [fromjid, gch_jid, res_nick], str(parameters), rcmd)
        
        inc_fatal_var(cid, 'info', 'cmd')
        set_fatal_var(cid, 'last', 't', time.time())
        set_fatal_var(cid, 'last', 'c', cname)

@handle_xmpp_exc(quiet=True)
def presenceHnd(conn, prs):
    cid = get_client_id()
    
    fromjid = prs.getFrom()
    
    if user_level(fromjid, get_stripped(fromjid)) == -100:
        return
    
    ptype = prs.getType()
    groupchat = get_stripped(fromjid)
    nick = get_resource(fromjid)
    inc_fatal_var(cid, 'info', 'prs')
    rostero = get_fatal_var(cid, 'roster')

    if is_param_seti('auto_subscribe') or get_int_fatal_var(cid, 'manual_subscribe'):
        if ptype == 'subscribe' and rostero:
            rostero.Authorize(fromjid)
            
            if get_int_fatal_var(cid, 'manual_subscribe'):
                sname = get_fatal_var(cid, 'gtemp_subs_name')
                
                if sname:
                    rostero.setItem(fromjid, sname, ['bot-users'])
                    set_fatal_var(cid, 'gtemp_subs_name', '')
                    
                set_fatal_var(cid, 'manual_subscribe', 0)
            else:
                rostero.setItem(fromjid, None, ['bot-users'])
    else:
        if ptype == 'subscribe' and rostero:
            if is_var_set('admins', fromjid):
                rostero.Unauthorize(fromjid)
                rostero.delItem(fromjid)
                set_fatal_var(cid, 'manual_usubscribe', 0)
            else:
                rostero.Authorize(fromjid)
    
    if gch_exists(groupchat):
        init_gch_roster(groupchat)

    if is_groupchat(groupchat):
        if ptype == 'unavailable':
            scode = prs.getStatusCode()
            
            if scode in ['301', '307']:
                reason = prs.getReason()
            else:
                reason = prs.getStatus()
            
            if scode != '303':
                call_leave_handlers(groupchat, nick, reason, scode)
                rmv_fatal_var(cid, 'gch_join_flags', groupchat, nick)
        elif ptype == 'available' or ptype == None:
            if not is_var_set(cid, 'gch_join_flags', groupchat, nick):
                aff = get_gch_aff(groupchat, nick)
                role = get_gch_role(groupchat, nick)
                
                call_join_handlers(groupchat, nick, aff, role)
                set_fatal_var(cid, 'gch_join_flags', groupchat, nick, 1)

    if gch_exists(groupchat):
        if ptype == 'error':
            ecode = prs.getErrorCode()
            
            if ecode:
                if ecode == '409':
                    join_groupchat(groupchat, nick + '.')
                elif ecode == '404':
                    if not is_groupchat(groupchat):
                        remove_chatroom(groupchat)
                elif ecode in ['401', '403', '405', ]:
                    leave_groupchat(groupchat, 'Got %s error code!' % (ecode))
                elif ecode == '503':
                    try:
                        thrc = inc_fatal_var('info', 'thr')
                        st_time = time.strftime('%H.%M.%S', time.localtime(time.time()))
                        thr_name = '%s/join%d.%s.%s' % (cid, thrc, 'presenceHnd', st_time)
                        thr = threading.Timer(60, join_groupchat, (groupchat, nick))
                        thr.setName(thr_name)
                        thr.start()
                    except Exception:
                        log_exc_error()

    if is_groupchat(groupchat):
        call_presence_handlers(prs)

@handle_xmpp_exc(quiet=False)
def iqHnd(conn, iq):
    cid = get_client_id()
    
    fromjid = iq.getFrom()
    
    if user_level(fromjid, get_stripped(fromjid)) == -100: 
        return

    if not iq.getType() == 'error':
        if iq.getTags('query', {}, xmpp.NS_VERSION):
            rev = get_revision()
            
            set_fatal_var('ftver', 'rev', rev)
            
            if not get_fatal_var('ftver', 'botver', 'os'):
                osver = ''
                
                if os.name == 'nt':
                    osname = os.popen('ver')
                    osver = codecs.decode(osname.read().strip().encode(), 'cp866') + '\n'
                    osname.close()
                else:
                    osname = os.popen('uname -sr', 'r')
                    osver = osname.read().strip() + '\n'
                    osname.close()
                    
                pyver = sys.version
                set_fatal_var('ftver', 'botver', 'os', '%s %s' % (osver, pyver))
                
            result = iq.buildReply('result')
            query = result.getTag('query')
            query.setTagData('name', get_fatal_var('ftver', 'botver', 'name'))
            query.setTagData('version', get_fatal_var('ftver', 'botver', 'ver') % (get_fatal_var('ftver', 'rev')))
            query.setTagData('os', get_fatal_var('ftver', 'botver', 'os'))
            conn.send(result)
            raise xmpp.NodeProcessed
        elif iq.getTags('time', {}, 'urn:xmpp:time'):
            tzo = (lambda tup: tup[0] + '%02d:' % (tup[1]) + '%02d' % (tup[2]))((lambda t: tuple(['+' if t < 0 else '-', abs(t) / 3600, abs(t) / 60 % 60]))(time.altzone if time.daylight else time.timezone))
            utc = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            result = iq.buildReply('result')
            reply = result.addChild('time', {}, [], 'urn:xmpp:time')
            reply.setTagData('tzo', tzo)
            reply.setTagData('utc', utc)
            conn.send(result)
            raise xmpp.NodeProcessed
        elif iq.getTags('query', {}, xmpp.NS_LAST):
            stime = get_int_fatal_var('info', 'start')
            uptime = int(time.time() - stime)
            result = iq.buildReply('result')
            query = result.getTag('query')
            query.setAttr('seconds', uptime)
            query.setData('Started: %s.' % (time.ctime(stime)))
            conn.send(result)
            raise xmpp.NodeProcessed
        elif iq.getTags('query', {}, xmpp.NS_TIME):
            timedisp = time.strftime('%a, %d %b %Y %H:%M:%S UTC', time.localtime())
            timetz = time.strftime('%Z', time.localtime())
            
            if os.name == 'nt':
                timetz = codecs.decode(timetz.encode(), 'utf-8') #timetz.decode('cp1251').encode('utf-8')
            
            timeutc = time.strftime('%Y%m%dT%H:%M:%S', time.gmtime())
            result = xmpp.Iq('result')
            result.setTo(fromjid)
            result.setID(iq.getID())
            query = result.addChild('query', {}, [], 'jabber:iq:time')
            query.setTagData('utc', timeutc)
            query.setTagData('tz', timetz)
            query.setTagData('display', timedisp)
            conn.send(result)
            raise xmpp.NodeProcessed
        elif iq.getTags('ping', {}, 'urn:xmpp:ping'):
            result = xmpp.Iq('result')
            result.setTo(iq.getFrom())
            result.setID(iq.getID())
            conn.send(result)
            raise xmpp.NodeProcessed
    
    call_iq_handlers(iq)
    inc_fatal_var(cid, 'info', 'iq')

@handle_xmpp_exc(quiet=True)
def discoHnd(conn, request, typ):
    features = [xmpp.NS_DISCO_INFO, xmpp.NS_DISCO_ITEMS, xmpp.NS_MUC, xmpp.NS_CAPS, xmpp.NS_COMMANDS, xmpp.NS_SI, xmpp.NS_IBB, xmpp.NS_MUC_FILTER, xmpp.NS_VCARD, xmpp.NS_VERSION, xmpp.NS_TIME, xmpp.NS_LAST, xmpp.NS_DATA, xmpp.NS_ROSTER, xmpp.NS_PRIVACY, xmpp.NS_TLS, 'urn:ietf:params:xml:ns:xmpp-ssl', 'urn:xmpp:time', 'urn:xmpp:ping', 'urn:xmpp:receipts', 'fatal:encoding:unicode', 'fatal:chat:logging', 'fatal:muc:amuc', 'fatal:wtf:extended', 'fatal:autosubscribe']

    if typ == 'info':
        ids = []
        
        ver = get_fatal_var('ftver', 'botver', 'ver')
        
        if ver:
            botver = ver.replace('%s', '')
        
        ids.append({'category': 'client', 'type': 'bot', 'name': 'fatal-bot'})
                
        dfdli = [('software', 'fatal-bot [Neutrino]'), ('version', botver)]
        
        svnr = get_revision(True)
        
        if os.name == 'nt':
            osname = os.popen('ver')
            osver = codecs.decode(osname.read().strip().encode(), 'cp866')
            osname.close()
        else:
            osname = os.popen('uname -sr', 'r')
            osver = osname.read().strip()
            osname.close()
        
        if svnr:
            dfdli.append(('git', svnr))
        
        dfdli.append(('os', osver))
        
        disfrm = xmpp.DataForm()
        disfrm.setType('result')
        
        for dfd in dfdli:
            dfld = xmpp.DataField()
            dfld.setVar(dfd[0])
            dfld.setValue(dfd[1])
            disfrm.addChild(node=dfld)
        
        info = {'ids': ids, 'features': features, 'xdata': disfrm}
        
        return info
    elif typ == 'items':
        items = []
        
        if xmpp.NS_COMMANDS in features:
            jid = get_cfg_param('jid')
            resource = get_cfg_param('resource')
            
            jid = '%s/%s' % (jid, resource)
            node = xmpp.NS_COMMANDS
            name = l('Commands')
            
            items.append({'jid': jid, 'node': node, 'name': name})
            
        return items

def reconnect(jid, password, resource, port=5222, tlssl=1):
    try:
        if is_var_set(jid, 'main_xmpp_stanza_pc'):
            mn_xmpp_thr = get_fatal_var(jid, 'main_xmpp_stanza_pc')
            mn_xmpp_thr.kill()
        
        rmv_fatal_var(jid, 'gchrosters')
        
        set_fatal_var(jid, 'reconnect', 1)
        
        init_fatal_event('client_event')
        
        time.sleep(5)

        connect_client(jid, password, resource, port, tlssl)

        if is_var_set(jid, 'if_client_connected'):
            if not is_var_set(jid, 'reconnects'):
                if get_int_cfg_param('reconnect_forever'):
                    set_fatal_var(jid, 'reconnects', 5)
                    set_fatal_var(jid, 'wait_for_try', 3)
    except Exception:
        log_exc_error()

@handle_xmpp_exc()
def dcHnd():
    cid = get_client_id()
    
    if not is_cvar_set('disconnected') and is_param_seti('auto_reconnect'):
        dctm = get_ldc_tms()
        
        sprint('\nDisconnected: %s\n\\Reconnecting...' % (dctm))
        
        dec_fatal_var('connected_count') 
        set_client_var('keep_alive_checks', 0)

        psw = get_client_var('passwd')
        rsc = get_client_var('rsrc')
        port = get_client_var('port')
        tlssl = get_client_var('tlssl')

        call_in_sep_thr(cid + '/start', reconnect, cid, psw, rsc, port, tlssl)
    else:
        sprint('\nClient %s disconnected.' % (cid))
        
        if not is_param_seti('keep_alive'):
            if get_int_fatal_var('clients') == 1:
                sprint(log_error('Exit!'))
                os._exit(1)
    
    set_client_var('client_state', True)

def connect_client(jid, password='', resource='', port=5222, tlssl=1):
    if not jid:
        set_client_var('client_state', False)
        return
    
    username = get_usernode(jid)
    server = get_domain(jid)

    set_client_var('passwd', password)
    set_client_var('rsrc', resource)
    set_client_var('port', port)
    set_client_var('tlssl', tlssl)
    
    dbg_mode = get_int_cfg_param('debug_mode')
    
    if dbg_mode:
        jconn = xmpp.Client(server=server, port=port)
    else:
        jconn = xmpp.Client(server=server, port=port, debug=[])
    
    set_fatal_var('clconns', jid, jconn)
    
    set_client_var('jconn', jconn)
    
    init_dynamic(jid)
    load_locale(jid)
    load_help(jid)
    
    sprint('\nConnecting: %s' % (jid)) 
    
    connect_server = get_cfg_param(jid, server)

    if connect_server != server:
        sprint('\\Specific server: %s' % (connect_server))

    proxy = get_fatal_var('fproxy')
    certificate = get_cfg_param('cert')
    
    if tlssl:
        conn = jconn.connect(server=(connect_server, port), proxy=proxy, cert=certificate, use_srv=False)
    else:
        conn = jconn.connect(server=(connect_server, port), proxy=proxy, secure=tlssl, use_srv=True)
    
    if not conn:
        if get_int_fatal_var(jid, 'reconnects') > 0:
            wait_for_try = get_int_fatal_var(jid, 'wait_for_try')
            
            sprint("\\Couldn't connect!\n\\Wait %s seconds for next try..." % (wait_for_try))
            
            time.sleep(wait_for_try)
            
            call_in_sep_thr(jid + '/start', reconnect, jid, password, resource, port, tlssl)
            
            if not is_param_seti('reconnect_forever'):
                dec_client_var('reconnects')
            
            inc_client_var('wait_for_try', 3)
        else:
            set_client_var('reconnects', 5)
            set_client_var('wait_for_try', 3)

            sprint("\\Couldn't find proper connection with server!")
            
            if not get_int_cfg_param('reconnect_forever'):
                if not is_var_set('connected_count'):
                    if is_param_set('jid'):
                        os._exit(1)
            
            set_client_var('client_state', False)

        return
    else:
        rmv_client_var('reconnect')
        sprint('\\Connected using %s.' % (jconn.isConnected().upper()))

    inc_fatal_var('connected_count')
    set_client_var('reconnects', 5)
    set_client_var('wait_for_try', 3)

    sprint('Try to authenticate...')
    
    if not password:
        password = get_cfg_param('password')
    
    if not resource:
        resource = get_cfg_param('resource')

    auth = jconn.auth(username, password, resource)
    
    if not auth:
        sprint('\\Auth Error. Incorrect login/password?\n\\Error: %s %s' % (jconn.lastErr, jconn.lastErrCode))
        set_client_var('client_state', False)

        return
    else:
        sprint('\\Successfully.')
    
    if not is_cvar_set('info', 'ss'):
        set_client_var('info', 'ss', 1)
    else:
        inc_client_var('info', 'ss')

    if get_int_cfg_param('privacy_lists', 1):
        jconn.RegisterHandler('iq', setPrivacyHandler, 'set', ns=xmpp.NS_PRIVACY)
        
        jlst = get_lst_cfg_param('admins')
        jlst.insert(0, jid)
        set_fatal_privacy(jids=jlst)
        set_active_privacy()
    
#----------- XMPPPY plugins PlugIn -------------------------------------------
    
    ibb = xmpp.filetransfer.IBB()
    ibb.PlugIn(jconn)
    
    browser = xmpp.browser.Browser()
    browser.PlugIn(jconn)
    
    commands = xmpp.commands.Commands(browser)
    commands.PlugIn(jconn)
    
    roster = xmpp.roster.Roster()
    roster.PlugIn(jconn)

#-----------------------------------------------------------------------------

    jconn.RegisterHandler('presence', presenceHnd)
    jconn.RegisterHandler('message', messageHnd)
    jconn.RegisterHandler('iq', iqHnd)
    jconn.RegisterDisconnectHandler(dcHnd)
    jconn.UnregisterDisconnectHandler(jconn.DisconnectHandler)
    jconn.Browser.setDiscoHandler(discoHnd)

    cpn = get_fatal_var('ftver', 'caps')
    ver = get_fatal_var('ftver', 'botver', 'ver')
    rev = get_fatal_var('ftver', 'rev')

    botver = ver % (rev)

    node='%s#%s' % (cpn, botver)

    jconn.Browser.setDiscoHandler(discoHnd, node)

#-----------------------------------------------------------------------------

    set_client_locale()

    call_in_sep_thr(jid + '/connect_client', call_stage0_init_handlers)

    if not is_cvar_set('last', 't'):
        set_client_var('last', 't', time.time())

    set_client_var('roster', roster)
    
    set_init_status()
    
    if not is_cvar_set('reconnect'):
        tname = make_thr_name(jid, 'connect_client', 'task_manager')
        start_scheduler(tname)

    aliaso = get_client_var('alias')
    aliaso.init()

    if is_db_exists('dynamic/%s/chatrooms.db' % (jid)):
        groupchats = get_chatrooms_list()
        
        gchs = get_complete_gchs_info(groupchats)
        
        if groupchats:            
            if get_int_cfg_param('privacy_lists', 1):
                add_jids_to_privacy(groupchats)
            
            sprint('Joining groupchat(s)...')
            
            for groupchat in groupchats:
                if groupchat:
                    add_gch_config(groupchat)
                    aliaso.init(groupchat)
                    
                    call_in_sep_thr(jid + '/connect_client', call_stage1_init_handlers, groupchat)
                    
                    try:            
                        gnick = gchs[groupchat]['nick']
                        passw = gchs[groupchat]['pass']
                        
                        join_groupchat(groupchat, gnick, passw)
                        
                        sprint('\\%s::%s' % (groupchat, gnick))
                    except Exception:
                        sprint('\\Can\'t join: %s.\n' % (groupchat))
                        log_exc_error()
        del gchs
    else:
        sql = 'CREATE TABLE chatrooms (chatroom VARCHAR(50) NOT NULL, nick VARCHAR, pass VARCHAR, UNIQUE (chatroom));'
        qres = sqlquery('dynamic/%s/chatrooms.db' % (jid), sql)
        
        sql = 'CREATE UNIQUE INDEX ichatrooms ON chatrooms (chatroom);'
        sqlquery('dynamic/%s/chatrooms.db' % (jid), sql)
        
        if qres != '':
            add_chatroom()
    
    set_client_var('info', 'ses', time.time())
    set_client_var('info', 'msg', 0)
    set_client_var('info', 'iq', 0)
    set_client_var('info', 'prs', 0)
    set_client_var('info', 'cmd', 0)
    
    call_in_sep_thr(jid + '/connect_client', call_stage2_init_handlers)
    
    keep_alive = get_int_cfg_param('keep_alive')
    
    if keep_alive:
        add_fatal_task('client_keep_alive_check', func=keep_alive_check, ival=keep_alive)

    add_fatal_task('threads_garbage_collector', func=kill_hung_thrs, ival=1800, inthr=False)
              
    mstk_size = get_int_cfg_param('main_proc_stk_size', 1048576)
    
    threading.stack_size(mstk_size)
    mn_xmpp_thr = init_fatal_thr(jid + '/connect_client', main_xmpp_stanza_pc)
    mn_xmpp_thr.ttype = 'sys'
    mn_xmpp_thr.start()
    threading.stack_size(stk_size)
    
    set_client_var('main_xmpp_stanza_pc', mn_xmpp_thr)
    rmv_client_var('reconnect')
    
    set_client_var('client_state', True)
    set_fatal_event('client_event')
    
    if is_param_seti('show_console') and is_var_set('con_last_prompt'):
        prompt = get_fatal_var('con_last_prompt')
        sys.stdout.write('\n' + prompt)
        sys.stdout.flush()

def get_curr_thr_name():
    curr_thr = threading.currentThread()
    thr_name = curr_thr.getName()
    return thr_name

def main_xmpp_stanza_pc():
    cid = get_client_id()
    
    thrn = get_curr_thr_name()

    set_client_var(thrn, 'cnt', 0)

    try:
        jconn = get_client_conn()
        
        while True:
            set_client_var(thrn, 'rtm', time.time())

            if not is_var_set(cid):
                return

            if not is_cvar_set('stop_xmpp_proc'):
                pdata = jconn.Process(1)
            else:
                pdata = '0'
                time.sleep(1)
                
            if is_cvar_set(thrn):
                rtm = get_client_var(thrn, 'rtm')
                lst = time.time() - rtm

                if lst < 1:
                    inc_client_var(thrn, 'cnt')
                else:
                    set_client_var(thrn, 'cnt', 0)

                cnt = get_client_var(thrn, 'cnt')

                if cnt >= 10000:
                    rmv_client_var(thrn)
                    sprint(log_error('\nInfinite loop has been detected, exit that loop!\n'))
                    return

            if pdata and pdata != '0':
                inc_client_var('info', 'btraffic', len(pdata))
                inc_client_var('info', 'pcycles')
            
            if is_cvar_set('raise_exc_flag'):
                rmv_client_var('raise_exc_flag')
                raise Exception
    except Exception:
        mstk_size = get_int_cfg_param('main_proc_stk_size', 1048576)
        stk_size = get_int_cfg_param('def_stk_size', 524288)
        
        threading.stack_size(mstk_size)

        mn_xmpp_thr = init_fatal_thr(cid + '/main_xmpp_stanza_pc', main_xmpp_stanza_pc)
        mn_xmpp_thr.ttype = 'sys'
        mn_xmpp_thr.start()
        threading.stack_size(stk_size)
        log_exc_error()

def findPresenceItem(node):
    for p in [x.getTag('item') for x in node.getTags('x', namespace=xmpp.NS_MUC_USER)]:
        if p != None:
            return p

def is_ruser_prsnt(jid):
    roster = get_client_var('roster')
    
    ritm = roster.getItem(jid)
    
    if ritm:
        if ritm['resources']:
            return True
    return False
    
def dis_service_exists(service):
    jconn = get_client_conn()
    
    res = xmpp.features.discoverInfo(jconn, service)

    if res[0]:
        return True
    return False

def register_adhoc_command(name, title, discohnd=None, cmdhnd=None):
    def discohnd_templ(conn, request, typ):
        discofeatures = [xmpp.NS_COMMANDS, xmpp.NS_DATA]
        discoinfo = {'ids': [{'category': 'automation', 'type': 'command-node', 'name': title}], 'features': discofeatures}
        
        if typ == 'list':
            return (request.getTo(), name, title)
        elif typ == 'items':
            return []
        elif typ == 'info':
            return discoinfo

    def cmdhnd_templ(conn, request):
        action = request.getTagAttr('command', 'action')
        
        if action == 'execute':
            Iq = request.buildReply('result')
            
            command = Iq.addChild('command')
            command.setNamespace(xmpp.NS_COMMANDS)
            command.setAttr('node', name)
            command.setAttr('status', 'completed')
            
            sesId = rand10()
            command.setAttr('sessionid', sesId)
            
            dform = create_result_dform(title, ['This is default template of Ad-Hoc command handler.'])
            
            command.addChild(node=dform)
            
            conn.send(Iq)
            
            raise xmpp.NodeProcessed

    if not discohnd:
        discohnd = discohnd_templ
    
    if not cmdhnd:
        cmdhnd = cmdhnd_templ
    
    jconn = get_client_conn()
    
    try:
        jconn.Commands.addCommand(name, discohnd, cmdhnd)
    except Exception:
        log_exc_error()
    
def unregister_adhoc_command(name):
    jconn = get_client_conn()
    
    try:
        jconn.Commands.delCommand(name)
    except Exception:
        log_exc_error()
    
def create_result_dform(title='', dflst=[]):
    dform = xmpp.DataForm()
    dform.setNamespace(xmpp.NS_DATA)
    dform.setType('result')
    
    if title:
        dform.setTitle(title)
    
    if dflst:
        for dfd in dflst:
            dfld = xmpp.DataField()
            dfld.setType('fixed')
            
            if dfd:
                dfld.setValue(dfd)
            
            dform.addChild(node=dfld)
    return dform

def parse_result_dform(rdform):
    if rdform:
        flds = rdform.getTags('field')
        dfs = {}
        
        for fld in flds:
            var = fld.getAttr('var')
            value = fld.getTagData('value')
            
            if not var: 
                continue
            
            dfs[var] = value
        return dfs

def register_raw_iq_handler(iqhnd):
    jconn = get_client_conn()

    try:
        jconn.RegisterHandler('iq', iqhnd)
    except Exception:
        log_exc_error()

def get_mf_nodes(mfnode):
    if mfnode:
        qns = mfnode.getQueryNS()
        
        if qns == xmpp.NS_MUC_FILTER:
            icnodes = mfnode.getQueryChildren()
            
            if icnodes:
                icnodes = icnodes[0]
                ndtype = icnodes.getName()
                
                if ndtype == 'presence':
                    icnodes = xmpp.Presence(node=icnodes)
                elif ndtype == 'message':
                    icnodes = xmpp.Message(node=icnodes)
                
                return icnodes

def get_mf_prs_nick(mfnode):
    if mfnode:
        tojid = mfnode.getTo()
        jid = xmpp.JID(tojid)
        nick = jid.getResource()
        return nick
    return ''

def get_mf_br_jid(mfnode):
    if mfnode:
        frmjid = mfnode.getFrom()
        jid = xmpp.JID(frmjid)
        brjid = jid.getStripped()
        return brjid
    return ''

def get_mf_jid(mfnode):
    if mfnode:
        frmjid = mfnode.getFrom()
        jid = xmpp.JID(frmjid)
        return jid
    return ''

def get_mf_prs_gch_jid(mfnode):
    if mfnode:
        tojid = mfnode.getTo()
        gch_jid = xmpp.JID(tojid)
        return gch_jid
    return ''

def get_mf_gch(mfnode):
    if mfnode:
        tojid = mfnode.getTo()
        jid = xmpp.JID(tojid)
        gch = jid.getStripped()
        return gch
    return ''

#-----------------------------------------------------------------------------

def setPrivacyHandler(conn, stanza):
    if stanza.T.query['xmlns'] != xmpp.NS_PRIVACY:
        return
        
    Id = stanza.getID()
    tojid = stanza['to']
    frmjid = stanza['from']
    
    iq = xmpp.Iq(typ='result', to=frmjid, frm=tojid)
    iq.setID(Id)
    
    conn.send(iq)
    
    raise xmpp.NodeProcessed

def is_jid_deny(jid, privacy='fatal-anti-flood'):
    privl = get_privacy_list(privacy)
    
    if privl:
        items = [li for li in privl.getChildren() if li['type'] == 'jid']
        
        for item in items:
            if item['value'] == jid:
                if item['action'] == 'deny':
                    return True
    return False

def is_jid_in_privacy(jid, privacy='fatal-anti-flood', tup=False):
    privl = get_privacy_list(privacy)
    
    if privl:
        items = [li for li in privl.getChildren() if li['type'] == 'jid']
        
        for item in items:
            if item['value'] == jid:
                if tup:
                    return [True, privl]
                return True
        
        if tup:
            return [False, privl]
    if tup:
        return [False, None]
    return False

def add_jids_to_privacy(jids, act='allow', privacy='fatal-anti-flood', active=False):
    privl = get_privacy_list(privacy)
    
    if privl:
        items = privl.getChildren()
        litms = len(items)
        
        jids = list(jids)
        jids = sort_list_dist(jids)
        
        for item in items:
            if item['type'] == 'jid' and item['value'] in jids:
                jids.remove(item['value']) 
        
        for jid in jids:
            item = xmpp.Node('item')
            item['type'] = 'jid'
            item['value'] = jid
            item['action'] = act
            item['order'] = '1'
            
            if act == 'allow':
                items.insert(0, item)
            else:
                lidx = len(items) - 1
                items.insert(lidx, item)
        
        if len(items) != litms:
            prlst = xmpp.Node('list')
            oidx = 1
            
            for item in items:
                item['order'] = oidx
                prlst.addChild(node=item)
                oidx += 1
            
            set_privacy_list(prlst, privacy)
            
            if active:
                set_active_privacy(privacy)

def add_jid_to_privacy(jid, act='allow', privacy='fatal-anti-flood', active=False):
    privl = get_privacy_list(privacy)
    
    if privl:
        items = privl.getChildren()
        
        jids = [li['value'] for li in items if li['type'] == 'jid']
        
        if not jid in jids:
            item = xmpp.Node('item')
            item['type'] = 'jid'
            item['value'] = jid
            item['action'] = act
            item['order'] = '1'
            
            if act == 'allow':
                items.insert(0, item)
            else:
                lidx = len(items) - 1
                items.insert(lidx, item)
            
            prlst = xmpp.Node('list')
            oidx = 1
            
            for item in items:
                item['order'] = oidx
                prlst.addChild(node=item)
                oidx += 1
            
            set_privacy_list(prlst, privacy)
            
            if active:
                set_active_privacy(privacy)

def rmv_jid_from_privacy(jid, privacy='fatal-anti-flood', active=False):
    privl = get_privacy_list(privacy)
    
    if privl:
        items = [li for li in privl.getChildren() if li['value'] != jid]
        
        prlst = xmpp.Node('list')
        oidx = 1
        
        for item in items:
            item['order'] = oidx
            prlst.addChild(node=item)
            oidx += 1
        
        set_privacy_list(prlst, privacy)
        
        if active:
            set_active_privacy(privacy)
        
        return prlst
    return []

def set_active_privacy(privacy='fatal-anti-flood'):
    jconn = get_client_conn()
    
    if jconn:
        return features.setActivePrivacyList(jconn, privacy)
    return False

def get_privacy_list(privacy='fatal-anti-flood'):
    jconn = get_client_conn()
    cid = get_client_id()
    
    if jconn:
        privl = get_fatal_var(cid, 'privacy', privacy)
        
        if privl:
            return privl
        
        resp = features.getPrivacyList(jconn, privacy)
        
        if resp:
            set_fatal_var(cid, 'privacy', privacy, resp)
        return resp

def set_privacy_list(prlst, privacy='fatal-anti-flood'):
    cid = get_client_id()
    jconn = get_client_conn()

    if jconn:
        prlst['name'] = privacy
        
        resp = features.setPrivacyList(jconn, prlst)
        
        if resp:
            set_fatal_var(cid, 'privacy', privacy, prlst)

def set_fatal_privacy(privacy='fatal-anti-flood', jids=[], jact='allow'):
    resp = get_privacy_list(privacy)
    
    if not resp:
        oidx = 1
        
        ftlist = xmpp.Node('list')
        item = ftlist.NT.item
        item['type'] = 'subscription'
        item['value'] = 'none'
        item['action'] = 'deny'
        item['order'] = oidx
        
        for jid in jids:
            oidx += 1
            
            item = ftlist.NT.item
            item['type'] = 'jid'
            item['value'] = jid
            item['action'] = jact
            item['order'] = oidx
        
        set_privacy_list(ftlist, privacy)

def rmv_privacy_list(privacy='fatal-anti-flood'):
    jconn = get_client_conn()
    cid = get_client_id()

    if jconn:
        if is_var_set(cid, 'privacy', privacy):
            features.delPrivacyList(jconn, privacy)
            rmv_fatal_var(cid, 'privacy', privacy)
