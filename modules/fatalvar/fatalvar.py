# -*- coding: utf-8 -*-

#  fatal variables module
#  fatalvar.py

#  Copyright © 2009-2013 Ancestors Soft

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

def _md5hash(plbody):
    md5s = hashlib.md5()
    md5s.update(plbody)
    return md5s.hexdigest()

def _eval_md5(path):
    try:
        fp = file(path)
        ccbody = fp.read()
        fp.close()
        return _md5hash(ccbody)
    except Exception:
        return ''

def get_client_id():
    curr_thr = threading.currentThread()
    thr_name = curr_thr.getName()
    sptnm = thr_name.split('/', 1)    
    return sptnm[0]

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
            hlpo.msgsLoad(locf)

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

def start_scheduler(tname, sdel=30):
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

def get_cfg_param(param, oer=''):
    return _fatalConfig.getParam(param, oer)

def get_int_cfg_param(param, oer=0):
    return _fatalConfig.getIntParam(param, oer)

def get_lst_cfg_param(param, oer=[]):
    return _fatalConfig.getListParam(param, oer)

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

def rel_fatal_config():
    return _fatalConfig.Load('fatal.conf')

def enum_cfg_params():
    return _fatalConfig.Params()

def init_fatal_event(ename):
    _fatalVars.addVar(ename, Event())

def wait_fatal_event(ename, timeout=None):
    evnt = _fatalVars.addVar(ename, Event())
    evnt.wait(timeout)

    if timeout: 
        _fatalVars.delVar(ename)

def pass_fatal_event(ename):
    evnt = _fatalVars.getVar(ename)
    evnt.set()
    _fatalVars.delVar(ename)

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
    return vval
    
def set_fatal_var(*args):
    _fatalVars.setVar(*args)

def rmv_fatal_var(*args):
    dvar = _fatalVars.getVar(*args)
    _fatalVars.delVar(*args)
    return dvar

def add_fatal_var(var, value={}):
    return _fatalVars.addVar(var, value)

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

def is_var_set(*args):
    var = _fatalVars.getVar(*args)
    
    if var:
        return True
    return False

def is_config_loaded():
    return _fatalConfig.isLoaded()

def get_revision(sim=False):
    try:
        if os.path.exists('.git\logs\HEAD'):
            fp = open('.git\logs\HEAD', 'r')
        else:
            return ''
                
        data = fp.read()
        
        revc = 0
        
        if data.count('commit:'):
            revc = data.count('\tcommit:')
        else:
            return ''        
        
        fp.close()
       
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
        self._checks = 0
        self._fails = 0
        self._ivals = []
        self._nivls = []
        self._ntsks = {}
        self._rtsks = []
        self._ivst = 0
        self._miv = 10
        self._nmiv = 0
        self._liv = 0
        self._strd = 0
   
    def _calc_miv(self, *args):
        lst = list(args)

        if not lst:
            return 1
        elif len(lst) < 2:
            return lst[0]

        if lst[-2] != 0:
            a = lst[-1]
            b = lst[-2]

            if a > b:
                mai = -1
                su = a - b
            elif b > a:
                mai = -2
                su = b - a
            else:
                mai = -1
                su = a - b

            lst[mai] = su
            
            lst.sort()
        else:
            return lst[-1]

        return self._calc_miv(*lst)

    def _worker(self):
        while True:
            tskl = tuple(self._tasks)

            for tsk in tskl:
                func = self._tasks[tsk]['func']
                args = self._tasks[tsk]['args']
                ival = self._tasks[tsk]['ival']
                count = self._tasks[tsk]['count']
                once = self._tasks[tsk]['once']
                strd = self._tasks[tsk]['strd']
                pmiv = self._tasks[tsk]['pmiv']
                inth = self._tasks[tsk]['inthr']

                shft = self._miv
                nmiv = self._nmiv

                if not strd:
                    shft = 0
                elif pmiv != shft:
                    if pmiv > shft:
                        shft = pmiv

                if shft != nmiv and nmiv:
                    if count + nmiv == ival - shft:
                        self._miv = nmiv

                try:
                    if count >= ival - shft:
                        self._tasks[tsk]['count'] = 0

                        if once:
                            self.rmvTask(tsk)
                        
                        if inth and self._thrd:
                            cid = get_client_id()
                            thrc = inc_fatal_var('info', 'thr')
                            st_time = time.strftime('%H.%M.%S', time.localtime(time.time()))
                            thr_name = '%s.%s%d.%s' % ('%s/task_manager' % (cid), func.__name__, thrc, st_time)

                            fthr = fThread(None, func, thr_name, args)
                            fthr.start()
                        else:
                            func(*args)
                        
                        self._tasks[tsk]['pmiv'] = self._miv
                        self._tasks[tsk]['last'] = time.time()
                        self._tasks[tsk]['strd'] += 1
                        self._strd += 1
                    else:
                        self._tasks[tsk]['count'] += self._miv
                except Exception:
                    self._fails += 1

            self._checks += 1
            
            self._liv = self._miv
            
            self._ivst = time.time()

            time.sleep(self._miv)

            if self._rtsks:
                rtsks = tuple(self._rtsks)

                for tskl in rtsks:
                    ival = self._tasks[tskl]['ival']
                    self._ivals.remove(ival)
                    del self._tasks[tskl]

                self._rtsks = []

                self._nmiv = self._calc_miv(*self._ivals)

                if self._nmiv < self._miv:
                    self._miv = self._nmiv

            self._ivals.extend(self._nivls)

            for tskn in self._ntsks:
                self._tasks[tskn] = dict(self._ntsks[tskn])

                once = self._tasks[tskn]['once']
                ival = self._tasks[tskn]['ival']
                last = self._tasks[tskn]['last']

                if once:
                    self._ivals.remove(ival)

                    ival -= int(round(time.time() - last)) + 1

                    self._tasks[tskn]['ival'] = ival

                    self._ivals.append(ival)

                self._tasks[tskn]['last'] = time.time()
             
            if self._nivls:
                self._nmiv = self._calc_miv(*self._ivals)
                
                if self._nmiv < self._miv:
                    self._miv = self._nmiv

            self._nivls = []
            self._ntsks = {}

    def addTask(self, func, args=(), tskn=None, ival=60, once=False, inthr=True):
        if type(func) in (types.FunctionType, types.BuiltinFunctionType):
            if not tskn:
                func_name = func.__name__
                
                self._tid += 1

                tskn = '%s%d' % (func_name, self._tid)

            self._nivls.append(ival)
            self._ntsks[tskn] = {'func': func, 'ival': ival, 'args': args, 'count': 0, 'once': once, 'last': time.time(), 'strd': 0, 'pmiv': 0, 'inthr': inthr}

    def rmvTask(self, tskn):
        if tskn in self._tasks:
            self._rtsks.append(tskn)
        elif tskn in self._ntsks:
            ival = self._ntsks[tskn]['ival']

            self._nivls.remove(ival)

            del self._ntsks[tskn]
            
    def Clear(self):
        self._tasks = {}

    def Enumerate(self):
        return tuple(self._tasks)

    def Start(self, tname='cycle_timer', sdel=30):
        if not self._wrktmr:
            self._tname = tname
            
            tskl = tuple(self._tasks)

            for tsk in tskl:
                self._tasks[tsk]['count'] = 0
                self._tasks[tsk]['last'] = time.time()
            
            if self._ivals:
                self._miv = self._calc_miv(*self._ivals)
            else:
                self._miv = sdel
            
            self._wrktmr = fThread(None, self._worker, tname)
            self._wrktmr.ttype = 'sys'
            self._wrktmr.start()

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

    def _str_to_list(self, strng, spltr=','):
        if strng:
            lst = strng.split(spltr)
            lst = [li.strip() for li in lst]
            return lst
        else:
            return []

    def _write_file(self, filename, data):
        try:
            fp = open(filename, 'w')
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
            return self._str_to_list(value)
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
    
    def setLocale(self, locale):
        mfiles = self._files
        self._files = []
        self._data = {}
        
        for fli in mfiles:
            dof = os.path.dirname(fli)
            hlf = '%s/help.%s' % (dof, locale)

            if os.path.exists(hlf):
                self.msgsLoad(hlf)
                continue
            
            self.msgsLoad('%s/help.ru' % (dof))
    
    def msgsLoad(self, filename):
        self._files.append(filename)
        msgs = self._read_file(filename)
        
        for cli in msgs:
            if '#' in cli or not cli.strip():
                continue
            
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
                
                if not hnam in self._data:
                    self._data[hnam] = {}
                
                dhvl = hval
                
                if hsec in ('ccat', 'exam'):
                    if not hsec in self._data[hnam]:
                        self._data[hnam][hsec] = []
                    
                    if not dhvl in self._data[hnam][hsec]:
                        if hsec == 'exam':
                            dhvl = [dhvl.strip()]
                        else:
                            dhvl = self._str_to_list(dhvl)
                        
                        if len(dhvl) > 1:
                            dhvl = [hvi.strip() for hvi in dhvl if not hvi in self._data[hnam][hsec]] 
                        
                        if dhvl:
                            self._data[hnam][hsec].extend(dhvl)
                    
                    continue
                
                self._data[hnam][hsec] = dhvl.strip()
    
    def setHelpSect(self, hnam, sect, sval):
        if hnam in self._data:
            if not sect in self._data[hnam]:
                self._data[hnam][sect] = sval

    def addHelpSect(self, hnam, sect, sval):
        if not hnam in self._data:
            self._data[hnam] = {'desc': '', 'ccat': '', 'exam': '', 'synt': ''}
        
        if sect in self._data[hnam]:
            self._data[hnam][sect] = sval

    def getHelpSect(self, hnam, sect):
        if hnam in self._data:
            if sect in self._data[hnam]:
                return self._data[hnam][sect]
        return ''

    def getHelpCats(self):
        hdat = self._data.copy()
        cats = []
        
        for hnm in hdat:
            clst = hdat[hnm]['ccat']

            for ci in clst:
                if not ci in cats:
                    cats.append(ci)
        
        cats.sort()

        return cats

    def getHelpInfo(self, hnam, sect=''):
        if hnam in self._data:
            if sect:
                if sect in self._data[hnam]:
                    return self._data[hnam][sect]
            else:
                return self._data[hnam]
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

_fatalVars.addVar('hgrepos', 'https://github.com/Ancestorum/fatal3k')

_revision = get_revision()
_fatalVars.addVar('ftver', {'rev': _revision, 'caps': 'http://fatal-dev.ru/bot/caps', 'botver': {'name': 'fatal-bot [Neutrino]', 'ver': 'v3.0a%s', 'os': ''}})

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

