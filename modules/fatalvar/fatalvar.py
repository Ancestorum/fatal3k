# -*- coding: utf-8 -*-

#  fatal variables module
#  fatalvar.py

#  Copyright © 2009-2024 Ancestors Soft

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful, 
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import sys
import os
import random
import time
import types
import hashlib
import queue
import heapq
import threading
from math import gcd
from math import trunc
from functools import reduce

from threading import Event

import xmpp
import alias

# Console colors

cl_green = chr(27) + "[32m"
cl_red = chr(27) + "[31m"
cl_bgreen = chr(27) + "[32;1m"
cl_yellow = chr(27) + "[33;1m"
cl_bred = chr(27) + "[31;1m"
cl_bblue = chr(27) + "[34;1m"
cl_bcyan = chr(27) + "[36;1m"
cl_magenta = chr(27) + "[35m"
cl_brown = chr(27) + "[33m"
cl_lgray = chr(27) + "[37m"
cl_purple = chr(27) + "[35;1m"
cl_cyan = chr(27) + "[36m"

cl_blink = chr(27) + "[5m"
cl_none = chr(27) + '[0m'

cl_error = cl_bred + cl_blink
cl_warn = cl_magenta + cl_blink

def _app_file(filename, data):
    try:
        if os.path.exists(filename):
            if os.path.getsize(filename) >= 3145728:
                fp = open(filename, 'w', encoding='utf-8')
            else:
                fp = open(filename, 'a', encoding='utf-8')
        else:
            fp = open(filename, 'a', encoding='utf-8')

        fp.write(data)
        fp.close()
    except Exception:
        pass

def log_thread(thro, file='syslogs/threads.log'):
    stm = time.time()
    
    sstm = str(stm)
    sptl = sstm.split('.', 1)
    stim = sptl[1]
    stim = stim[:3]

    stz_time = time.strftime('[%d.%m.%Y/%H:%M:%S.', time.localtime(stm))
    stz_time = '%s%s]: '% (stz_time, stim) 
    _app_file(file, '\n%s%s\n' % (stz_time, thro))
    return '%s%s\n' % (stz_time, thro)

def _md5hash(plbody):
    md5s = hashlib.md5()
    md5s.update(plbody.encode())
    return md5s.hexdigest()

def _eval_md5(path):
    try:
        fp = open(path, 'r')
        ccbody = fp.read()
        fp.close()
        return _md5hash(ccbody)
    except Exception:
        return ''

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

def change_locale(locale):
    cid = get_client_id()
    
    loco = get_fatal_var(cid, 'locale')
    
    if loco:   
        loco.setLocale(locale)
    
def load_lc_msgs(locale, dpath='', cid=''):
    locf = '%s/langs/%s.msg' % (dpath, locale)
    
    if not dpath:
        locf = 'langs/%s.msg' % (locale)
    
    cids = get_lst_cfg_param('jid')

    if cid:
        cids = [cid]
    
    for cid in cids:
        loco = get_fatal_var(cid, 'locale')
        
        if loco:
            loco.msgsLoad(locf)    

def reld_acc_lc_msgs(locale, cid):
    plsl = os.listdir('plugins')
    plsl = [dli for dli in plsl if not dli.startswith('.')]
    
    for pli in plsl:
        dpath = 'plugins/%s' % (pli)
        locf = '%s/langs/%s.msg' % (dpath, locale)
        
        loco = get_fatal_var(cid, 'locale')
        
        if loco:
            loco.msgsLoad(locf)    

def get_lc_str(orig):
    cid = get_client_id()
    
    loco = get_fatal_var(cid, 'locale')
    
    if loco:   
        return loco.getString(orig)
        
    return ''

def set_lc_str(orig, alt):
    cid = get_client_id()
    
    loco = get_fatal_var(cid, 'locale')

    if loco:   
        loco.setString(orig, alt)

def set_help_locale(locale, cid=''):
    if not cid:
        cid = get_client_id()
    
    hlpo = get_fatal_var(cid, 'help')
    
    if hlpo:   
        hlpo.setLocale(locale)

def load_hlp_msgs(locale, dpath, cid=''):
    locf = '%s/help/help.%s' % (dpath, locale)
    
    cids = get_lst_cfg_param('jid')

    if cid:
        cids = [cid]
    
    for cid in cids:
        hlpo = get_fatal_var(cid, 'help')

        if hlpo:
            hlpo.msgsLoad(locf, dpath)

def reld_acc_hlp_msgs(locale, cid):
    plsl = os.listdir('plugins')
    plsl = [dli for dli in plsl if not dli.startswith('.')]
    
    for pli in plsl:
        dpath = 'plugins/%s' % (pli)
        locf = '%s/help/help.%s' % (dpath, locale)
        
        hlpo = get_fatal_var(cid, 'help')
        
        if hlpo:
            hlpo.msgsLoad(locf)    

def get_help_sect(hnam, sect):
    cid = get_client_id()

    hlpo = get_fatal_var(cid, 'help')

    if hlpo:
        return hlpo.getHelpSect(hnam, sect)

    return ''

def set_help_sect(hnam, sect, sval):
    cid = get_client_id()
    
    hlpo = get_fatal_var(cid, 'help')
    
    if hlpo:   
        hlpo.setHelpSect(hnam, sect, sval)

def add_help_sect(hnam, sect, sval):
    cid = get_client_id()
    
    hlpo = get_fatal_var(cid, 'help')
    
    if hlpo:   
        hlpo.addHelpSect(hnam, sect, sval)

def start_scheduler(tname, sdel=8):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.Start(tname, sdel)

def add_fatal_task(tskn, func, args=(), ival=60, once=False, inthr=True):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.addTask(func, args, tskn, ival, once, inthr)

def rmv_fatal_task(tskn):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.rmvTask(tskn)

def enum_fatal_tasks():
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.Enumerate()

def is_thr_exists(thr_name):
    thrl = threading.enumerate()
    
    thrl = [li for li in thrl if li.name.count(thr_name)]
    
    if thrl:
        return True
    return False

def is_task_exists(tskn):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.isTaskExists(tskn)

def list_fatal_tasks():
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.lstTasks()
 
def recalc_task_miv():
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.recalcTaskGCD()
 
def get_task_miv():
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.getTaskMiv()
        
def get_task_count(tskn):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.getTaskCount(tskn)

def get_task_last(tskn):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.getTaskLast(tskn)
    
def set_task_last(tskn, last, resume=True):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.setTaskLast(tskn, last, resume)

def set_task_remns(tskn, remns):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.setTaskRemns(tskn, remns)

def get_task_remns(tskn):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.getTaskRemns(tskn)

def set_task_count(tskn, count=0):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.setTaskCount(tskn, count)
        
def get_task_ival(tskn):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.getTaskIval(tskn)
 
def get_task_next(tskn):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.getTaskNext(tskn)
        
def get_task_nnxt(tskn):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.getTaskNNXT(tskn)
 
def set_task_next(tskn, tnxt):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.setTaskNext(tskn, tnxt)
        
def get_task_strd(tskn):
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        return tsko.getTaskStrd(tskn)

def rmv_all_tasks():
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.Clear()

def stop_scheduler():
    cid = get_client_id()
    
    tsko = get_fatal_var(cid, 'scheduler')
    
    if tsko:
        tsko.Stop()

def gcp(param, oer=''):
    return get_cfg_param(param, oer)

def get_cfg_param(param, oer=''):
    return _fatalConfig.getParam(param, oer)

def gip(param, oer=0):
    return get_int_cfg_param(param, oer)
    
def get_int_cfg_param(param, oer=0):
    return _fatalConfig.getIntParam(param, oer)

def glp(param, oer=[]):
    return get_lst_cfg_param(param, oer)

def get_lst_cfg_param(param, oer=[]):
    return _fatalConfig.getListParam(param, oer)

def gfp(param, oer=0.0):
    return get_flt_cfg_param(param, oer)

def get_flt_cfg_param(param, oer=0.0):
    return _fatalConfig.getFloatParam(param, oer)

def set_cfg_param(param, value):
    setres = _fatalConfig.setParam(param, value)
    
    if setres:
        cfg_md5 = _eval_md5('fatal.conf')
        set_fatal_var('cfg_md5', cfg_md5)
        
    return setres

def is_param_set(param):
    param = _fatalConfig.getParam(param, None)

    if param:
        return True
    return False

def is_param_seti(param):
    param = _fatalConfig.getIntParam(param, 0)

    if param:
        return True
    return False

def rel_fatal_config():
    return _fatalConfig.Load('fatal.conf')

def enum_cfg_params():
    return _fatalConfig.Params()

def is_event_set(ename):
    cid = get_client_id()    
    
    evnt = _fatalVars.getVar(cid, ename, 'evnt')
    
    if evnt.is_set():
        return True
    return False

def is_event_init(ename):
    cid = get_client_id()    
    
    evnt = _fatalVars.getVar(cid, ename)
    
    if evnt:
        return True
    return False

def iawt_fatal_event(ename, timeout=None, cid=None):
    init_fatal_event(ename, cid)
    wait_fatal_event(ename, timeout, cid)

def ife(ename, cid=None):
    init_fatal_event(ename, cid)

def init_fatal_event(ename, cid=None):
    if not cid:
        cid = get_client_id()    

    _fatalVars.setVar(cid, ename, 'evnt', Event())

def wfe(ename, timeout=None, cid=None):
    wait_fatal_event(ename, timeout, cid)

def wait_fatal_event(ename, timeout=None, cid=None):
    if not cid:
        cid = get_client_id()
    
    evnt = _fatalVars.getVar(cid, ename, 'evnt')
    
    if is_event_init(ename):
        _fatalVars.setVar(cid, ename, 'start', trunc(time.time()))
    
    if evnt:
        evnt.wait(timeout)

    if timeout: 
        _fatalVars.delVar(cid, ename)

def sfe(ename, cid=None):
    set_fatal_event(ename, cid)

def set_fatal_event(ename, cid=None):
    if not cid:
        cid = get_client_id()
    
    evnt = get_fatal_var(cid, ename, 'evnt')

    evnt.set()
    
    rmv_fatal_var(cid, ename)

def cgv(*args):
    cid = get_client_id()
    return get_fatal_var(cid, *args)

def get_client_var(*args):
    cid = get_client_id()
    return get_fatal_var(cid, *args)

def find_fatal_var(patt):
    return _fatalVars.findVar(patt)

def get_fatal_var(*args):
    return _fatalVars.getVar(*args)

def get_int_fatal_var(*args):
    vval = _fatalVars.getVar(*args)
    
    if not vval:
        return 0
    return vval

def get_dict_fatal_var(*args):
    vval = _fatalVars.getVar(*args)
    
    if not vval:
        return {}
    return vval

def get_list_fatal_var(*args):
    vval = _fatalVars.getVar(*args)
    
    if not vval:
        return ['']
    return list(vval)

def csv(*args):
    cid = get_client_id()
    set_fatal_var(cid, *args)
 
def set_client_var(*args):
    cid = get_client_id()
    set_fatal_var(cid, *args)
 
def set_fatal_var(*args):
    _fatalVars.setVar(*args)

def rcv(*args):
    cid = get_client_id()
    return rmv_fatal_var(cid, *args)

def rmv_client_var(*args):
    cid = get_client_id()
    return rmv_fatal_var(cid, *args)
    
def rmv_fatal_var(*args):
    dvar = _fatalVars.getVar(*args)
    _fatalVars.delVar(*args)
    return dvar

def add_fatal_var(var, value={}):
    return _fatalVars.addVar(var, value)

def inc_client_var(*args):
    cid = get_client_id()
    return inc_fatal_var(cid, *args)

def inc_fatal_var(*args):
    incto = 1
    
    if args:
        incto = args[-1]
        
        if type(incto) is int:
            args = list(args)
            args.pop()
        else:
            incto = 1

    vval = _fatalVars.getVar(*args)
    
    if type(vval) is int:
        args = list(args)
        vval += incto
        args.append(vval)
        _fatalVars.setVar(*args)
    
        return vval
    return 0

def dec_client_var(*args):
    cid = get_client_id()
    return dec_fatal_var(cid, *args)

def dec_fatal_var(*args):
    decto = 1
    
    if args:
        decto = args[-1]
        
        if type(decto) is int:
            args = list(args)
            args.pop()
        else:
            decto = 1

    vval = _fatalVars.getVar(*args)
    
    if type(vval) is int:
        args = list(args)
        vval -= decto
        args.append(vval)
        _fatalVars.setVar(*args)
        
        return vval
    return 0

def enum_fatal_vars():
    return _fatalVars.Vars()

def iscvs(*args):
    cid = get_client_id()
    return is_var_set(cid, *args)

def is_cvar_set(*args):
    cid = get_client_id()
    return is_var_set(cid, *args)

def is_var_set(*args):
    var = _fatalVars.getVar(*args)
    
    if var:
        return True
    return False

def is_config_loaded():
    return _fatalConfig.isLoaded()

def get_revision(sim=False):
    try:
        revc = ''

        if os.name == 'posix':
            pipe = os.popen('sh -c "git rev-list --count main" 2>&1')
            revc = pipe.read()
            pipe.close()
        elif os.name == 'nt':
            pipe = os.popen('git rev-list --count main')
            revc = pipe.read()
            pipe.close()
       
        revc = revc.strip()

        if not revc.isdigit():
            return ''

        if sim:
            return 'r%s' % (revc)
        else:
            return ' (r%s)' % (revc)
    except Exception:
       return ''

class fThread(threading.Thread):
    
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        self.ttype = 'otr'
        
    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        self.strtd = time.time()
        threading.Thread.start(self)
        
        if is_param_seti('log_thrs'):
            log_thread(self.name)
        
    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
        
    def globaltrace(self, frame, why, arg):
        if why == 'call': 
            return self.localtrace
        else: 
            return None
        
    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line': 
                raise SystemExit()    
        return self.localtrace
        
    def kill(self): 
        self.killed = True

class _fCycleTasks(object):

    def __init__(self, thrd=True):
        self._tasks = {}
        self._thrd = thrd
        self._tid = 0
        self._wrktmr = None
        self._tname = 'cycle_timer'
        self._fails = 0
        self._ivals = []
        self._nivls = []
        self._ntsks = {}
        self._rtsks = []
        self._miv = 1  
        self._nmiv = 1 
        self._strd = 0
        self._resume = False
        self._sdel = 1
        self._just_started = False

    def _shift_times(self):
        cid = get_client_id()
        
        if self._miv > 1:
            try:
                tskl = tuple(self._tasks)
                
                curt = trunc(time.time())
                
                strt = get_fatal_var(cid, 'task_manager_event', 'start')
                
                tmel = curt-strt
                
                for tsk in tskl:
                    last = self._tasks[tsk]['last']
                    
                    self._tasks[tsk]['count'] += tmel
                    self._tasks[tsk]['remns'] -= tmel
            except Exception:
                pass

    def _calc_gcd(self, numl):
        if numl:
            x = reduce(gcd, numl)
            return x
        return 1
        
    def _recalc_gcd(self):
        tskl = tuple(self._tasks)

        gcdl = []

        for tsk in tskl:
            gcdl.append(self._tasks[tsk]['remns'])
        
        gcdl = [li for li in gcdl if li != 0]
        
        if len(gcdl) <= 1:
            gcdl.append(1)
        
        self._miv = self._calc_gcd(gcdl)

    def _correct_remns(self):
        tskl = tuple(self._tasks)
        curt = trunc(time.time())
        chng = False
        
        for tsk in tskl:
            rmns = self._tasks[tsk]['remns']
            nela = self._tasks[tsk]['next']
            
            rmnt = trunc(curt + rmns - nela)
            
            if rmnt > 0:
                if tsk.count('cycle'):
                    self._tasks[tsk]['nnxt'] = rmnt
                    self._tasks[tsk]['remns'] -= rmnt
                    self._tasks[tsk]['count'] += rmnt
                    chng = True
        
        if chng:
            self._recalc_gcd()

    def _worker(self):
        while True:
            if self._sdel:
                time.sleep(self._sdel)
                self._sdel = 0
        
            tskl = tuple(self._tasks)
            
            if self._just_started:
                self._miv = self._calc_gcd(self._ivals)
                self._just_started = False
            
            for tsk in tskl:
                func = self._tasks[tsk]['func']
                args = self._tasks[tsk]['args']
                ival = self._tasks[tsk]['ival']
                count = self._tasks[tsk]['count']
                once = self._tasks[tsk]['once']
                strd = self._tasks[tsk]['strd']
                inth = self._tasks[tsk]['inthr']
                rmns = self._tasks[tsk]['remns']
                tla = self._tasks[tsk]['last']
                nnx = self._tasks[tsk]['nnxt']

                nela = trunc(self._tasks[tsk]['next'])
                
                curt = trunc(time.time())
                
                try:
                    if nela <= curt:
                        self._tasks[tsk]['count'] = 0
                        self._tasks[tsk]['remns'] = ival

                        if once:
                            self.rmvTask(tsk)
                        
                        if is_param_seti('log_tsks'):
                            tla = time.strftime('%H:%M:%S', time.localtime(tla))
                            tnx = time.strftime('%H:%M:%S', time.localtime(nela))
                            nnx = time.strftime('%H:%M:%S', time.localtime(nela + nnx))        
                        
                        if inth and self._thrd:
                            cid = get_client_id()
                            thrc = inc_fatal_var('info', 'thr')
                            st_time = time.strftime('%H.%M.%S', time.localtime(trunc(time.time())))
                            thr_name = '%s.%s%d.%s' % ('%s/task_manager' % (cid), func.__name__, thrc, st_time)

                            fthr = fThread(None, func, thr_name, args)
                            fthr.ttype = 'sys'
                            fthr.start()
                        else:
                            func(*args)
                        
                        if is_param_seti('log_tsks'):
                            log_thread('%s (%s, %s, %s, %s, %s, %s)' % (tsk, ival, count, rmns, tla, tnx, nnx), 'syslogs/tasks.log')
                        
                        self._tasks[tsk]['last'] = curt
                        self._tasks[tsk]['next'] = curt + ival
                        self._tasks[tsk]['strd'] += 1
                        self._strd += 1
                        
                        self._recalc_gcd()
                except Exception:
                    print('task_mgr_error')
                    self._fails += 1
            
            iawt_fatal_event('task_manager_event', self._miv)

            for tsk in tskl:
                self._tasks[tsk]['count'] += self._miv
                self._tasks[tsk]['remns'] -= self._miv

            self._correct_remns()

            if self._rtsks:
                rtsks = tuple(self._rtsks)

                for tskl in rtsks:
                    if tskl in self._tasks:
                        ival = self._tasks[tskl]['ival']
                        self._ivals.remove(ival)
                        del self._tasks[tskl]

                self._rtsks = []

                self._recalc_gcd()
                
            self._ivals.extend(self._nivls)

            for tskn in self._ntsks:
                self._tasks[tskn] = dict(self._ntsks[tskn])

                if not self._resume:
                    self._tasks[tskn]['last'] = trunc(time.time())
                    self._resume = False
             
            if self._nivls:
                self._recalc_gcd()
                                
            init_fatal_event('task_manager_event')
            
            self._nivls = []
            self._ntsks = {}

    def addTask(self, func, args=(), tskn=None, ival=60, once=False, inthr=True):
        if type(func) in (types.FunctionType, types.BuiltinFunctionType):
            if not tskn:
                func_name = func.__name__
                
                self._tid += 1

                tskn = '%s%d' % (func_name, self._tid)
            
            crtm = trunc(time.time())
            
            self._nivls.append(ival)
            self._ntsks[tskn] = {'func': func, 'ival': ival, 'args': args, 'count': 0, 'remns': ival, 'once': once, 'last': crtm, 'next': crtm+ival, 'strd': 0, 'inthr': inthr, 'nnxt': 0}
         
            self._shift_times()
         
            self._recalc_gcd()
         
            if is_event_init('task_manager_event'):
                set_fatal_event('task_manager_event')

    def getTaskLast(self, tskn):
        if tskn in self._ntsks:
            return self._ntsks[tskn]['last'] + self._ntsks[tskn]['ival']
        elif tskn in self._tasks:
            return self._tasks[tskn]['last'] + self._tasks[tskn]['ival']
        return 0

    def setTaskLast(self, tskn, last, resume=False):
        self._resume = resume
        
        if tskn in self._ntsks:
            self._ntsks[tskn]['last'] = last
        if tskn in self._tasks:
            self._tasks[tskn]['last'] = last

    def getTaskCount(self, tskn):
        if tskn in self._ntsks:
            return self._ntsks[tskn]['count']
        if tskn in self._tasks:
            return self._tasks[tskn]['count']
            
    def getTaskNNXT(self, tskn):
        if tskn in self._ntsks:
            return self._ntsks[tskn]['nnxt']
        if tskn in self._tasks:
            return self._tasks[tskn]['nnxt']
            
    def setTaskCount(self, tskn, count=0):
        if tskn in self._ntsks:
            self._ntsks[tskn]['count'] = count
        if tskn in self._tasks:
            self._tasks[tskn]['count'] = count
            
    def setTaskNext(self, tskn, tnxt):
        if tskn in self._ntsks:
            self._ntsks[tskn]['next'] = tnxt
        if tskn in self._tasks:
            self._tasks[tskn]['next'] = tnxt

    def setTaskRemns(self, tskn, trmn):
        if tskn in self._ntsks:
            self._ntsks[tskn]['remns'] = trmn
        if tskn in self._tasks:
            self._tasks[tskn]['remns'] = trmn
            
    def getTaskRemns(self, tskn):
        if tskn in self._ntsks:
            return self._ntsks[tskn]['remns']
        if tskn in self._tasks:
            return self._tasks[tskn]['remns']

    def getTaskNext(self, tskn):
        if tskn in self._ntsks:
            return self._ntsks[tskn]['next']
        if tskn in self._tasks:
            return self._tasks[tskn]['next']

    def getTaskIval(self, tskn):
        if tskn in self._ntsks:
            return self._ntsks[tskn]['ival']
        elif tskn in self._tasks:
            return self._tasks[tskn]['ival']
        return 0
        
    def getTaskStrd(self, tskn):
        if tskn in self._tasks:
            return self._tasks[tskn]['strd']
        return 0
        
    def getTaskMiv(self):
        return self._miv
        
    def recalcTaskGCD(self):
        self._recalc_gcd()

    def rmvTask(self, tskn):
        if tskn in self._tasks:
            self._rtsks.append(tskn)
        elif tskn in self._ntsks:
            ival = self._ntsks[tskn]['ival']

            self._nivls.remove(ival)

            del self._ntsks[tskn]
        
        self._shift_times()
        self._recalc_gcd()
        
        if is_event_init('task_manager_event'):
            set_fatal_event('task_manager_event')
    
    def isTaskExists(self, tskn):
        if (tskn in self._ntsks) or (tskn in self._tasks):
            return True
        return False
    
    def lstTasks(self):
        return tuple(self._ntsks)
            
    def Clear(self):
        self._tasks = {}

    def Enumerate(self):
        return tuple(self._tasks)

    def Start(self, tname='cycle_timer', sdel=1):
        if not self._wrktmr:
            self._tname = tname
            
            self._sdel = sdel
            
            tskl = tuple(self._tasks)

            for tsk in tskl:
                self._tasks[tsk]['count'] = 0
                self._tasks[tsk]['last'] = trunc(time.time())
            
            if self._ivals:
                self._miv = self._calc_gcd(self._ivals)
            else:
                self._miv = sdel
            
            self._wrktmr = fThread(None, self._worker, tname)
            self._wrktmr.ttype = 'sys'
            self._wrktmr.start()
            self._just_started = True

    def Stop(self):
        if self._wrktmr:
            self._wrktmr.kill()
            self._wrktmr = None

class fpQueue(queue.Queue):

    def _init(self, maxsize):
        self.queue = []

    def _qsize(self, len=len):
        return len(self.queue)

    def _put(self, item, heappush=heapq.heappush):
        heappush(self.queue, item)

    def _get(self, heappop=heapq.heappop):
        item = heappop(self.queue)
        
        if type(item) is tuple:
            return item[2]
        else:
            return item

class fTimerQueue(fpQueue):
    
    def _put(self, item, heappush=heapq.heappush):
        heappush(self.queue, item)

    def _get(self, heappop=heapq.heappop):
        item = heappop(self.queue)
        return item

class _fConfig(object):
    
    def _read_file(self, filename):
        try:
            fp = open(filename, encoding="utf-8")
            data = fp.readlines()
            fp.close()
            return data
        except Exception:
            return ''
    
    def __init__(self):
        self._filename = ''
        self._status = False

    def _is_digit(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return  False
            
    def _str_to_list(self, strng, spltr=','):
        if strng:
            lst = strng.split(spltr)
            lst = [li.strip() for li in lst]
            return lst
        else:
            return []

    def _write_file(self, filename, data):
        try:
            fp = open(filename, 'w', encoding='utf-8')
            fp.write(data)
            fp.close()
        except Exception:
            pass

    def _write_cfg_param(self, param, value):
        try:
            cfg_line = [li for li in self._config if param in li and li.startswith(param)]
                           
            prmidx = self._config.index(cfg_line[0])
            self._config[prmidx] = '%s = %s' % (param, value.strip())
            
            config = '\n'.join(self._config)
            self._write_file(self._filename, config)
            return value.strip()
        except Exception:
            return ''

    def _get_cfg_param(self, param):
        config = [li.strip() for li in self._config if not '#' in li and li.strip()]
        
        try:
            cfg_line = [li for li in config if li.startswith(param)]
            
            values = []
            
            for cli in cfg_line:
                splp = cli.split('=', 1)
                
                cparam = splp[0].strip(' ')
                
                if param == cparam:
                    value = splp[1].strip(' ')
                    values.append(value)
                
            return ', '.join(values)
        except Exception:
            return ''
    
    def _get_param(self, param, typ=str):
        if typ == str:
            return self._get_cfg_param(param)
        elif typ == int:
            try:
                return typ(self._get_cfg_param(param))
            except Exception:
                return 0
        elif typ == float:
            try:
                return typ(self._get_cfg_param(param))
            except Exception:
                return 0.0

    def Load(self, filename):
        self._filename = filename
        self._config = self._read_file(self._filename)
        self._config = [li.replace('\n', '') for li in self._config]
        
        if self._config:
            self._status = True
            return self._status
        return False

    def getParam(self, param, oer=''):
        value = self._get_param(param)
        
        if value:
            return value
        return oer

    def getIntParam(self, param, oer=0):
        value = self._get_param(param, int)
        
        if value:
            return value
        return oer
        
    def getFloatParam(self, param, oer=0.0):
        value = self._get_param(param, float)
        
        if value:
            return value
        return oer

    def getListParam(self, param, oer=[]):
        value = self._get_param(param)
        
        if value:
            lop = self._str_to_list(value)
            rsl = []
            
            for lpi in lop:
                if self._is_digit(lpi):
                    rsl.append(int(lpi))
                else:
                    rsl.append(lpi)
            return rsl
        return list(oer)

    def setParam(self, param, value):
        value = '%s' % (value)
        return self._write_cfg_param(param, value)
    
    def Params(self):
        config = [li.split('=', 1) for li in self._config if not '#' in li and li.strip()]
        config = [li[0].strip() for li in config]
        return config
    
    def isLoaded(self):
        return self._status

class fLocale(object):

    def _read_file(self, filename):
        try:
            fp = open(filename, encoding="utf-8")
            data = fp.readlines()
            fp.close()
            return data
        except Exception:
            return ''

    def __init__(self, delimeter='='):
        self.dlm = delimeter
        self._files = []
        self._data = {}

    def setLocale(self, locale):
        mfiles = self._files
        self._files = []
        self._data = {}
        
        for fli in mfiles:
            dof = os.path.dirname(fli)

            if os.path.exists(dof):
                self.msgsLoad('%s/%s.msg' % (dof, locale))
    
    def msgsLoad(self, filename):
        self._files.append(filename)
        msgs = self._read_file(filename)
        
        for cli in msgs:
            if '#' in cli or not cli.strip():
                continue
            
            if not cli.endswith('\n'):
                cli = cli + '\n'
            
            cli = cli.replace('\\n', '\n')
            splp = cli.split(self.dlm, 1)
            orig = splp[0].strip(' ')
            alt = splp[1].strip(' ')
            self._data[orig] = alt

    def getString(self, orig):
        alt = ''
        
        if orig in self._data:
            alt = self._data[orig]
            
        if alt.endswith('\n'):
            alt = alt[:-1]
            
        return alt

    def setString(self, orig, alt):
        alt = ''
        
        if not orig in self._data:
            self._data[orig] = alt.strip()
    
class _fHelp(fLocale):
    
    def _str_to_list(self, strng, spltr=','):
        if strng:
            lst = strng.split(spltr)
            lst = [li.strip() for li in lst]
            return lst
        else:
            return []
    
    def _get_slave_dict(self, hnam, ddict):
        kks = list(self._data)
        ndt = {}
        
        for ki in kks:
            if hnam in list(self._data[ki]):
                ndt = self._data[ki] 
                break
        
        return ndt
         
    def setLocale(self, locale):
        mfiles = self._files
        self._files = []
        self._data = {}
        
        for fli in mfiles:
            dof = os.path.dirname(fli)
            
            spll = fli.split('/')
            dpt = spll[-3]
            
            if dpt.count('\\'):
                spll = dpt.split('\\')
                dpt = spll[-1]
            
            hlf = '%s/help.%s' % (dof, locale)

            if os.path.exists(hlf):
                self.msgsLoad(hlf, dpt)
                continue
            
            self.msgsLoad('%s/help.ru' % (dof), dpt)
    
    def msgsLoad(self, filename, dpath=''):
        if not filename in self._files:
            self._files.append(filename)
        
        msgs = self._read_file(filename)
       
        dpt = ''
       
        if dpath:
            if dpath.count('\\'):
                spll = dpath.split('\\')
                dpt = spll[-1]
            else:
                spll = dpath.split('/')
                dpt = spll[-1]
         
        self._data[dpt] = {}
        
        for cli in msgs:
            if not cli.endswith('\n'):
                cli = cli + '\n'
            
            cli = cli.replace('\\n', '\n')
            splp = cli.split('=', 1)
            
            if len(splp) != 2:
                continue
            
            hpar = splp[0].strip(' ')
            hval = splp[1].strip(' ')
            
            sphp = hpar.split('.', 1)
            
            if len(sphp) == 2:
                hnam = sphp[0]
                hsec = sphp[1]
                
                if len(hnam) > 17:
                    continue
                
                if not hnam in self._data[dpt]:
                    self._data[dpt][hnam] = {}
                
                dhvl = hval
                
                if hsec in ('ccat', 'exam'):
                    if not hsec in self._data[dpt][hnam]:
                        self._data[dpt][hnam][hsec] = []
                    
                    if not dhvl in self._data[dpt][hnam][hsec]:
                        if hsec == 'exam':
                            dhvl = [dhvl.strip()]
                        else:
                            dhvl = self._str_to_list(dhvl)
                        
                        dhvl = [hvi.strip() for hvi in dhvl if not hvi in self._data[dpt][hnam][hsec]] 
                        
                        self._data[dpt][hnam][hsec].extend(dhvl)

                    continue
                
                self._data[dpt][hnam][hsec] = dhvl.strip()
    
    def setHelpSect(self, hnam, sect, sval):
        ndt = self._get_slave_dict(hnam, self._data)

        if hnam in ndt:
            if not sect in ndt[hnam]:
                ndt[hnam][sect] = sval

    def addHelpSect(self, hnam, sect, sval):
        ndt = self._get_slave_dict(hnam, self._data)
        
        if not hnam in ndt:
            ndt[hnam] = {'desc': '', 'ccat': '', 'exam': '', 'synt': ''}
        
        if sect in ndt[hnam]:
            ndt[hnam][sect] = sval

    def getHelpSect(self, hnam, sect):
        ndt = self._get_slave_dict(hnam, self._data)        
        
        if hnam in ndt:
            if sect in ndt[hnam]:
                return ndt[hnam][sect]
        return ''

    def getHelpCats(self):
        hdat = {}
        
        for ki in list(self._data):
            for ti in list(self._data[ki]):
                hdat[ti] = self._data[ki][ti]
        
        #hdat = self._data.copy()
        cats = []
        
        for hnm in hdat:
            clst = hdat[hnm]['ccat']

            for ci in clst:
                if not ci in cats:
                    cats.append(ci)
        
        cats.sort()

        return cats

    def getHelpInfo(self, hnam, sect=''):
        ndt = self._get_slave_dict(hnam, self._data)
        
        if hnam in ndt:
            if sect:
                if sect in ndt[hnam]:
                    return ndt[hnam][sect]
            else:
                return ndt[hnam]
        return {}
    
class _fVars(object):
    
    def __init__(self):
        self._vars = {}
    
    def _sfr_dic_val(self, dic, *args):
        for dar in args:
            if type(dic) is dict:
                if dar in dic:
                    dic = dic[dar]
                else:
                    return None
            elif type(dic) in [list, tuple]:
                value = args[-1]
                
                if value in dic:
                    return dic
                else:
                    return None
            else:
                return None
        return dic

    def _sfs_dic_val(self, dic, *args):
        args = list(args)
        value = None
        
        if args and len(args) >= 2:
            value = args.pop()
        else:
            return None
        
        for dar in args:
            if type(dic) == dict:
                if dar in dic:
                    ind = list(args).index(dar)
                    
                    if ind == len(args) - 1:
                        dic[dar] = value
                        
                        return dic[dar]
                    
                    dic = dic[dar]
                else:
                    ind = list(args).index(dar)
                    
                    if ind != len(args) - 1:
                        dic[dar] = {}
                        dic = dic[dar]
                        continue
                    
                    dic[dar] = value
                    return dic[dar]
            else:
                return None

    def _sfd_dic_val(self, dic, *args):
        for dar in args:
            if type(dic) == dict:
                if dar in dic:
                    ind = list(args).index(dar)
                    
                    if ind == len(args) - 1:
                        del dic[dar]
                        
                        return
                    
                    dic = dic[dar]
                else:
                    return None
            else:
                return None

    def findVar(self, patt):
        keyl = self._vars.keys()
        
        for key in keyl:
            if key.startswith(patt):
                return self.getVar(key)

    def getVar(self, *args):
        return self._sfr_dic_val(self._vars, *args)
    
    def addVar(self, var, value={}):
        self._vars[var] = value
        return self._vars[var]

    def setVar(self, *args):
        self._sfs_dic_val(self._vars, *args)

    def delVar(self, *args):
        self._sfd_dic_val(self._vars, *args)
    
    def Vars(self):
        return list(self._vars)

class fDataForm(xmpp.DataForm):
    
    def __init__(self, title='', instr=''):
        xmpp.DataForm.__init__(self)
        
        self._simple_scheme = []
        self.setNamespace(xmpp.NS_DATA)
        self.setType('form')
    
        if title:
            self.setTitle(title)
        
        if instr:
            self.setInstructions(instr)

    def _read_file(self, filename):
        try:
            fp = open(filename, encoding="utf-8")
            data = fp.read()
            fp.close()
            return data
        except Exception:
            return ''

    def _def_list_single_field(self, var='', label='', value='', opts=[]):
        if not var:
            var = 'var%s' % (random.randrange(1000, 9999))
            
        return ({var: (label, value), 'options': opts}, )
        
    def _def_list_multi_field(self, var='', label='', value='', opts=[]):
        if not var:
            var = 'var%s' % (random.randrange(1000, 9999))
            
        return ({var: [label, value], 'options': opts}, )
    
    def _def_text_private_field(self, var='', label='', value=''):
        if not var:
            var = 'var%s' % (random.randrange(1000, 9999))
            
        return [{var: [label, value]}, ]
    
    def _def_text_multi_field(self, var='', label='', value=''):
        if not var:
            var = 'var%s' % (random.randrange(1000, 9999))
            
        return [{var: (label, value)}, ]
    
    def _def_text_single_field(self, var='', label='', value=''):
        if not var:
            var = 'var%s' % (random.randrange(1000, 9999))
            
        return {var: [label, value]}
    
    def _def_boolean_field(self, var='', label='', value=''):
        if not var:
            var = 'var%s' % (random.randrange(1000, 9999))
            
        return {var: (label, value)}

    def _process_requested_params_dform(self, dfsch):
        for dsli in dfsch:
            if type(dsli) is str:
                dfld = xmpp.DataField()
                dfld.setType('fixed')
                
                if dsli:
                    dfld.setValue(dsli)
                    
                self.addChild(node=dfld)
            elif type(dsli) is tuple:
                for tli in dsli:
                    for fv in list(tli):
                        if fv != 'options':
                            di = tli[fv]
                            
                            if type(di) is tuple:
                                dfld = xmpp.DataField()
                                dfld.setType('list-single')
                                dfld.setVar(fv)
                                
                                if di:
                                    dfld.setLabel(di[0])
                                    dfld.setValue(di[1])
                                    
                                    opts = tli['options']
                                    dfld.setOptions(opts)
                                    
                                self.addChild(node=dfld)
                            if type(di) is list:
                                dfld = xmpp.DataField()
                                dfld.setType('list-multi')
                                dfld.setVar(fv)
                                
                                if di:
                                    dfld.setLabel(di[0])
                                    dfld.setValue(di[1])
                                    
                                    opts = tli['options']
                                    dfld.setOptions(opts)
                                    
                                self.addChild(node=dfld)
            elif type(dsli) is list:
                for tli in dsli:
                    for fv in list(tli):
                        di = tli[fv]
                        
                        if type(di) is tuple:
                            dfld = xmpp.DataField()
                            dfld.setType('text-multi')
                            dfld.setVar(fv)
                            
                            if di[0]:
                                dfld.setLabel(di[0])
                            
                            vlst = di[1].split('\n')
                            
                            if vlst: 
                                dfld.setValues(vlst)
                                
                            self.addChild(node=dfld)
                        elif type(di) is list:
                            dfld = xmpp.DataField()
                            dfld.setType('text-private')
                            dfld.setVar(fv)
                            
                            if di[0]: 
                                dfld.setLabel(di[0])
                                
                            if di[1]: 
                                dfld.setValue(di[1])
                                
                            self.addChild(node=dfld)
            elif type(dsli) is dict:
                for fv in list(dsli):
                    di = dsli[fv]
                    if type(di) is tuple:
                        dfld = xmpp.DataField()
                        dfld.setType('boolean')
                        dfld.setVar(fv)
                        
                        if di[0]: 
                            dfld.setLabel(di[0])
                        
                        if di[1]: 
                            dfld.setValue(di[1])
                        
                        self.addChild(node=dfld)
                    if type(di) is list:
                        dfld = xmpp.DataField()
                        dfld.setType('text-single')
                        dfld.setVar(fv)
                        
                        if di[0]: 
                            dfld.setLabel(di[0])
                            
                        if di[1]: 
                            dfld.setValue(di[1])
                        
                        self.addChild(node=dfld)
    
    def addLSField(self, var='', label='', value='', opts=[]):
        fld = self._def_list_single_field(var, label, value, opts)
        self._simple_scheme.append(fld)
        
    def addLMField(self, var='', label='', value='', opts=[]):
        fld = self._def_list_multi_field(var, label, value)
        self._simple_scheme.append(fld)
        
    def addTPField(self, var='', label='', value=''):
        fld = self._def_text_private_field(var, label, value)
        self._simple_scheme.append(fld)

    def addTMField(self, var='', label='', value=''):
        fld = self._def_text_multi_field(var, label, value)
        self._simple_scheme.append(fld)

    def addTSField(self, var='', label='', value=''):
        fld = self._def_text_single_field(var, label, value)
        self._simple_scheme.append(fld)

    def addBField(self, var='', label='', value=''):
        fld = self._def_boolean_field(var, label, value)
        self._simple_scheme.append(fld)
    
    def addFField(self, value=''):
        self._simple_scheme.append(value)

    def LoadScheme(self, filename):
        sch = self._read_file(filename)
        sch_lines = sch.splitlines()
        
        if not sch: 
            return False
        
        try:
            for sln in sch_lines:
                psch = eval(sln)
                self._simple_scheme.append(psch)
            return True
        except Exception:
            return False
        
    def ClearScheme(self):
        self._simple_scheme = []
    
    def getScheme(self):
        return self._simple_scheme

    def ProcessForm(self):
        self._process_requested_params_dform(self._simple_scheme)
        self._simple_scheme = []

#---------------- MAIN VARIABLES DEFINITION SECTION--------------------- #
 
_fatalVars = _fVars()
_fatalConfig = _fConfig()
_fatalHelp = _fHelp()

_fatalVars.addVar('config_filename', 'fatal.conf')

_fatalConfig.Load('fatal.conf')

_fatalVars.addVar('commands', {})

#------------------------ lists handlers -----------------------------------

_fatalVars.addVar('command_handlers', {})
_fatalVars.addVar('message_handlers', {})
_fatalVars.addVar('outgoing_message_handlers', {})
_fatalVars.addVar('join_handlers', {})
_fatalVars.addVar('leave_handlers', {})
_fatalVars.addVar('iq_handlers', {})
_fatalVars.addVar('presence_handlers', {})
_fatalVars.addVar('stage0_init', {})
_fatalVars.addVar('stage1_init', {})
_fatalVars.addVar('stage2_init', {})

#----------------------------------------------------------------------------

_fatalVars.addVar('pls_md5_hash', {})
_fatalVars.addVar('reload_code', {})

#-----------------------------------------------------------------------------

_fatalVars.addVar('roles', {'none': 0, 'visitor': 0, 'participant': 10, 'moderator': 15})

_fatalVars.addVar('affiliations', {'none': 0, 'member': 1, 'admin': 5, 'owner': 15})

_fatalVars.addVar('last', {'c': '', 't': 0})

_fatalVars.addVar('info', {'start': 0, 'ses': 0, 'msg': 0, 'prs': 0, 'iq': 0, 'cmd': 0, 'thr': 0, 'pcycles': 1, 'btraffic': 0, 'pld_thr_id': 0})

_fatalVars.addVar('repos', 'https://github.com/Ancestorum/fatal3k')

_revision = get_revision()
_fatalVars.addVar('ftver', {'rev': _revision, 'caps': 'http://fatal-dev.ru/bot/caps', 'botver': {'name': 'fatal-bot [Neutrino]', 'ver': 'v3.1%s', 'os': ''}})

#-------------------------------- Misc vars --------------------------------

_fatalVars.setVar('info', 'opnum', 0)

_fatalVars.addVar('thread_pool', fpQueue())

if 'TERM' in os.environ:
    _fatalVars.addVar('cle', True)

#-------------------------- Config parameters ----------------------------------

_phost = _fatalConfig.getParam('proxy_host')
_pport = _fatalConfig.getIntParam('proxy_port')
_puser = _fatalConfig.getParam('proxy_user')
_ppassword = _fatalConfig.getParam('proxy_password')

if _phost and _pport:
    _fatalVars.setVar('fproxy', 'host', _phost)
    _fatalVars.setVar('fproxy', 'port', _pport)
    _fatalVars.setVar('fproxy', 'user', _puser)
    _fatalVars.setVar('fproxy', 'password', _ppassword)

def init_clients_vars(cids):
    for cid in cids:
        set_fatal_var(cid, 'locale', fLocale())
        set_fatal_var(cid, 'help', _fHelp())
        set_fatal_var(cid, 'scheduler', _fCycleTasks())

        set_fatal_var(cid, 'gchrosters', {})
        set_fatal_var(cid, 'alias', alias.Alias())
        set_fatal_var(cid, 'accbyconf', {})
        set_fatal_var(cid, 'commoff', {})
        
        set_fatal_var(cid, 'checks_count', 0)
        set_fatal_var(cid, 'keep_alive_checks', 0)

        set_fatal_var(cid, 'reconnects', 5)
        set_fatal_var(cid, 'wait_for_try', 3)
        
        set_fatal_var(cid, 'disconnected', False)
        
        set_fatal_var(cid, 'manual_subscribe', 0)
        set_fatal_var(cid, 'manual_usubscribe', 0)
        
        set_fatal_var(cid, 'last_cmd_result', '')
        set_fatal_var(cid, 'info', 'pcycles', 0)
        set_fatal_var(cid, 'info', 'btraffic', 0)
        set_fatal_var(cid, 'info', 'ses', 0)

