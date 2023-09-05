#!/usr/bin/python

#  fatal core
#  fatal.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Parts of code Copyright © Boris Kotov <admin@avoozl.ru>
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

if not sys.stdin.isatty():
    if os.path.exists('syslogs/output.log'):
        if os.path.getsize('syslogs/output.log') >= 1048576:
            output_log = open('syslogs/output.log', 'w')
        else:
            output_log = open('syslogs/output.log', 'a')
    else:
        output_log = open('syslogs/output.log', 'a')

    sys.stdout = output_log

#----------------------------------------------------------------------------
    
def main():
    try:
        cthr = threading.current_thread()
        
        sttm = time.time()
        
        st_time = time.strftime('%H.%M.%S', time.localtime(sttm))
        
        cthr.name = 'all/main.main_thread.%s' % (st_time)
        
        set_fatal_var('info', 'start', sttm)
        
        sprint('\n...---===STARTING FATAL-BOT===---...\n')
        
        sttm = time.strftime('%d.%m.%Y, %H:%M:%S', time.localtime(sttm))

        sprint('\Starting time: %s\n' % (sttm))
        
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
        
        load_plugins()
        
        chk_md5_and_reload()
        
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
            
            call_in_sep_thr(cli + '/main', connect_client, cli, pswi, rsci, prti, tlsi)
        
            sres = read_client_state()
        
            if sres == 'brk':
                if get_int_cfg_param('reconnect_forever'):
                    if cli:
                        cljds.append(cli)
                        cpsws.append(pswi)
            elif sres == 'suc':
                set_fatal_var(cli, 'if_client_connected', 1)

        if not get_os_uname() == 'freebsd' and get_int_cfg_param('show_console'):
            sprint('\nPress Ctrl+D to hide console.\n')
        
        close_state_pipes()
        
        sprint("All ready, let's work! ;)\n")
        
        os_uname = get_os_uname()
        
        if readline:
            readline.set_completer(ftcompl)
        
        while True:
            try:                
                if not get_int_cfg_param('show_console'):
                    if os_uname == 'linux':
                        signal.pause()

                    break
                
                if is_cycle_overload('console_cycle'):
                    break
                
                if os_uname == 'freebsd':
                    break
                
                ires = fatal_console()
                    
                if ires == False and os_uname == 'linux':
                    signal.pause()
                    
                    break
            except KeyboardInterrupt:
                if not sys.stdin.isatty():
                    log_error('Error: Unresolved Ctrl+C operation!')
                    
                    continue
                else:
                    cpipeo = rmv_fatal_var('console_cpipeo')

                    if cpipeo:
                        sys.stdout.write('\r')
                        os.close(cpipeo)
                        
                        dec_fatal_var('info', 'opnum')

                        continue

                    sprint('\n\nThis operation stops fatal-bot, are you sure?\n')

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
        pols, args = getopt.gnu_getopt(sys.argv[1:], 'hvdkp:', ['help', 'version', 'daemon', 'kill', 'port='])
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
    
    create_fatal_mmap()
    
    set_fatal_var('main_proc', main)
    
    if dmnrun:
        pidfile = '%s/fatal.pid' % (fataldir)
        stderr = '%s/syslogs/error.log' % (fataldir)
        stdout = '%s/syslogs/output.log' % (fataldir)
        sprint('\nInfo: fatal-bot continues to run in daemon mode!\n')
        start_daemon(pidfile, main, stdout, stderr)
    else:
        copyright()
        create_pid_file()
        atexit.register(rmv_pid_file)
        main()

