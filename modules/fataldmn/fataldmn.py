# -*- coding: utf-8 -*-

#  Daemon module
#  daemon.py

#  Initial copyright © Unknown
#  Modification copyright © 2012 Ancestors Soft

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
import atexit
import time
from signal import SIGTERM

class fDaemon:
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, wfunc=None, wfargs=[], stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.worker = wfunc
        self.wfargs = wfargs
    
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent
                sys.exit(0) 
        except OSError as e: 
            sys.stderr.write('Error: Fork #1 failed: %d (%s)!\n' % (e.errno, e.strerror))
            sys.exit(1)
    
        # decouple from parent environment
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit from second parent
                sys.exit(0) 
        except OSError as e: 
            sys.stderr.write('Error: Fork #2 failed: %d (%s)!\n' % (e.errno, e.strerror))
            sys.exit(1) 
        
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        atexit.register(self.rmv_pid_file)
        pid = str(os.getpid())
        self.create_pid_file(pid)
    
    def create_pid_file(self, pid):
        try:
            pif = open(self.pidfile, 'w+')
            pif.write("%s\n" % (pid))
            pif.close()
        except Exception as exc:
            pass
    
    def read_pid_file(self):
        try:
            pif = open(self.pidfile,'r')
            pid = pif.read()
            pid = int(pid.strip())
            pif.close()
            return pid
        except IOError:
            return None
    
    def rmv_pid_file(self):
        try:
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
        except Exception:
            pass
    
    def start(self):
        """
        Start the daemon
        """
        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        pid = self.read_pid_file()
        
        # Try killing the daemon process
        try:
            os.kill(pid, SIGTERM)
        except OSError as err:
            err = str(err)
            
            if err.find("No such process") > 0:
                self.rmv_pid_file()
            else:
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
        try:
            if self.worker:
                self.worker(*self.wfargs)
        except Exception as exc:
            pass
