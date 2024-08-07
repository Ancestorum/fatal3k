#!/usr/bin/python3

#  fatal core
#  fatal.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Parts of code Copyright © Boris Kotov <admin@avoozl.ru>
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
import getopt

fatalexe = os.path.realpath(sys.argv[0])
fataldir = os.path.dirname(fatalexe)

os.chdir(fataldir)

sys.path.insert(1, 'modules')
sys.path.insert(1, 'plugins')

import time
import threading
import signal

from fatalapi import *

import pickle

#---------------------------------------------------------------------------

if not is_config_loaded():
    sprint()
    sprint(log_error('Error: Configuration file not found!'))
    os._exit(1)

#------------------------ IO redirection section ----------------------------

if not os.path.exists('syslogs'):
    os.mkdir('syslogs', 0o755)

if os.path.exists('syslogs/error.log'):
    if os.path.getsize('syslogs/error.log') >= 1048576:
        error_log = open('syslogs/error.log', 'w')
    else:
        error_log = open('syslogs/error.log', 'a')
else:
    error_log = open('syslogs/error.log', 'a')

sys.stderr = error_log

#----------------------------------------------------------------------------

def main():
    def signal_handler(signal, frame):    
        raise KeyboardInterrupt

    try:
        cthr = threading.current_thread()
        
        sttm = time.time()
        
        st_time = time.strftime('%H.%M.%S', time.localtime(sttm))
        
        cthr.name = 'all/main.main_thread.%s' % (st_time)
        
        set_fatal_var('info', 'start', sttm)
        
        sprint('\n...---===STARTING FATAL-BOT===---...\n')
        
        sttm = get_ldc_tms(sttm)

        sprint('\\Starting time: %s\n' % (sttm))
        
        if is_param_seti('reload_code'):
            cr_md5 = core_md5('fatal.py')
            cfg_md5 = core_md5('fatal.conf')
            add_fatal_var('core_md5', cr_md5)
            add_fatal_var('cfg_md5', cfg_md5)
        
        init_dirs()        
        
        cljds = get_lst_cfg_param('jid')
        cpsws = get_lst_cfg_param('password')
        crscs = get_lst_cfg_param('resource')
        ports = get_lst_cfg_param('port')
        tlss = get_lst_cfg_param('use_tls_ssl')
        
        if not cljds:
            init_clients_vars(['fatal-bot'])
            load_locale('fatal-bot')
        else:
            init_clients_vars(cljds)
        
        modl = get_lst_cfg_param('modules_path')
        
        for mdp in modl:
            sys.path.insert(1, mdp)
        
        load_plugins()
        
        set_fatal_var('curr_cons_owner', 'fatal-bot')
        set_fatal_var('console_owners', cljds[1:])
        
        if cljds:
            set_fatal_var('curr_cons_owner', cljds[0])
        
        if len(cljds) > 1:
            set_fatal_var('multiple_login', True)
            sprint('Connecting accounts...')
        elif cljds:
            sprint('Connecting account...')
        else:
            sprint('Could not find any accounts!')
        
        set_fatal_var('clients', len(cljds))
        
        start_thr_disp()

        set_fatal_var('connected_count', 0)

        equalize_lists(cljds, crscs, 'r' + rand10())
        equalize_lists(cljds, ports, 5222)
        equalize_lists(cljds, tlss, 1)

        ports = [int(li) for li in ports]
        tlss = [int(li) for li in tlss]

        while cljds:
            cli = cljds.pop(0)
            pswi = cpsws.pop(0)
            rsci = crscs.pop(0)
            prti = ports.pop(0)
            tlsi = tlss.pop(0)
            
            init_fatal_event('client_event', cli)

            call_in_sep_thr(cli + '/main', connect_client, cli, pswi, rsci, prti, tlsi)
        
            wait_fatal_event('client_event', cid=cli)
        
            if not iscvs('client_state'): 
                if is_param_seti('reconnect_forever'):
                    if cli:
                        cljds.append(cli)
                        cpsws.append(pswi)
            elif iscvs('client_state'):
                set_fatal_var(cli, 'if_client_connected', 1)
        
        os_uname = get_os_uname()

        if not os_uname == 'freebsd' and is_param_seti('show_console'):
            if os_uname == 'linux':
                sprint('\nPress Ctrl+D to hide console.\n')
            else:
                sprint('\nPress Ctrl+Z and Return to hide console.\n')
        
        sprint("All ready, let's work! ;)\n")
        
        if readline:
            readline.set_completer(ftcompl)
        
        if is_param_seti('reload_code'):
            relc = get_int_cfg_param('reload_code')
            add_fatal_task('chk_md5_and_reload', func=chk_md5_and_reload, ival=relc)
        
        while True:
            try:                
                if not is_param_seti('show_console'):
                    iawt_fatal_event('suspend_term')
                
                if is_cycle_overload('console_cycle'):
                    break
                
                if os_uname == 'freebsd':
                    iawt_fatal_event('suspend_error')
                
                ires = fatal_console()    
                    
                if ires == False:
                    iawt_fatal_event('suspend_error')
                else:
                    continue
            except KeyboardInterrupt:
                if not sys.stdin.isatty():
                    log_error('Error: Unresolved Ctrl+C operation!')
                    
                    continue
                else:
                    sprint('\n\nThis operation stops fatal-bot, are you sure?\n')
                    
                    answ = ''

                    try:
                        answ = input('(Y/n): ')
                        answ = answ.lower()
                    except KeyboardInterrupt:
                        sprint()
                        interrupt()

                    if answ.startswith('n'):
                        sprint()

                        dec_fatal_var('info', 'opnum')

                        continue
                    
                    interrupt()
    except Exception:
        print((log_exc_error()))

if __name__ == "__main__":
    pols, args = [], []
    
    try:
        pols, args = getopt.gnu_getopt(sys.argv[1:], 'hvdkp:', ['help', 'version', 'daemon', 'ki`ll', 'port='])
    except Exception as exc:
        sprint('\nError: %s!\n' % (str(exc).capitalize()))
        sys.exit(1)
    
    dmnrun = False
    
    pid = read_pid_file()

    for opt, oval in pols:
        if opt in ('-h', '--help'):
            fatal_help()
            sys.exit(0)
        elif opt in ('-v', '--version'):
            fatal_version()
            sys.exit(0)
        elif opt in ('-p', '--port'):
            if oval.isdigit():
                set_cfg_param('port', oval)
        elif opt in ('-d', '--daemon'):
            dmnrun = True
        elif opt in ('-k', '--kill'):
            try:
                os.kill(int(pid), 9)
                sprint("\nInfo: fatal-bot with pid %s has been killed!\n" % (pid))
                sys.exit(0)
            except OSError:
                sprint()
                sprint(log_error("Error: Couldn't kill fatal-bot because it's not started!"))
                sys.exit(1)
            except Exception:
                sprint()
                sprint(log_error("Error: Unknown error has occured while killing fatal-bot!"))
                sys.exit(1)

    if pid:
        if is_pid_alive(pid):
            sprint()
            sprint(log_error('Error: It may be the second instance of fatal-bot in memory. Exit!'))
            os._exit(1)
    
    set_fatal_var('main_proc', main)
    
    if dmnrun:
        pidfile = '%s/fatal.pid' % (fataldir)
        stderr = '%s/syslogs/error.log' % (fataldir)
        stdout = '%s/syslogs/output.log' % (fataldir)
        sprint('\nInfo: fatal-bot continues to run in daemon mode!\n')
        
        if os.path.exists('syslogs/output.log'):
            if os.path.getsize('syslogs/output.log') >= 1048576:
                output_log = open('syslogs/output.log', 'w')
            else:
                output_log = open('syslogs/output.log', 'a')
        else:
            output_log = open('syslogs/output.log', 'a')
        
        os_uname = get_os_uname()
        
        if is_param_seti('show_console'):
            set_cfg_param('show_console', 0)
        
        if os_uname.count('win'):
            start_win_dmn(stdout=output_log, stderr=error_log)
        else:
            start_nix_dmn(pidfile, main, stdout, stderr)
    else:
        copyright()
        create_pid_file()
        atexit.register(rmv_pid_file)
        main()

