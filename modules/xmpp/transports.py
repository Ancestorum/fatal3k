# -*- coding: utf-8 -*-
##   transports.py
##
##   Copyright (C) 2003-2004 Alexey "Snake" Nezhdanov
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2, or (at your option)
##   any later version.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.

# $Id: transports.py,v 1.35 2009/04/07 08:34:09 snakeru Exp $

"""
This module contains the low-level implementations of xmpppy connect methods or
(in other words) transports for xmpp-stanzas.
Currently here is three transports:
direct TCP connect - TCPsocket class
proxied TCP connect - HTTPPROXYsocket class (CONNECT proxies)
TLS connection - TLS class. Can be used for SSL connections also.

Transports are stackable so you - f.e. TLS use HTPPROXYsocket or TCPsocket as more low-level transport.

Also exception 'error' is defined to allow capture of this module specific exceptions.
"""
import sys
import socket
import select
import base64
import codecs
import ssl

from xml.parsers.expat import ExpatError

from xmpp import dispatcher
from xmpp import simplexml

from .client import PlugIn
from .protocol import *

from .simplexml import ustr
from .simplexml import NodeBuilder

# determine which DNS resolution library is available
HAVE_DNSPYTHON = False
HAVE_PYDNS = False

#try:
#    from ssl import sslwrap_simple
#except ImportError:
#    sslwrap_simple = socket.ssl

try:
    import pydns # http://pydns.sf.net/
    HAVE_PYDNS = True
except ImportError:
    pass

DATA_RECEIVED = 'DATA RECEIVED'
DATA_SENT = 'DATA SENT'

class error:
    """An exception to be raised in case of low-level errors in methods of 'transports' module."""
    def __init__(self,comment):
        """Cache the descriptive string"""
        self._comment=comment

    def __str__(self):
        """Serialise exception into pre-cached descriptive string."""
        return self._comment

BUFLEN = 1024

class TCPsocket(PlugIn):
    """ This class defines direct TCP connection method. """
    def __init__(self, server=None, use_srv=True):
        """ Cache connection point 'server'. 'server' is the tuple of (host, port)
            absolutely the same as standard tcp socket uses. However library will lookup for 
            ('_xmpp-client._tcp.' + host) SRV record in DNS and connect to the found (if it is)
            server instead
        """
        PlugIn.__init__(self)
        self.DBG_LINE='socket'
        self._exported_methods=[self.send,self.disconnect]
        self._server, self.use_srv = server, use_srv

    def _is_sock_alive(self, sock):
        try:
            conn.send('\n')
        except:
            return False
        return True

    def _check_ogoing_data(self, data):
        if isinstance(data, simplexml.Node):
            data = ustr(data)
        else:
            if data.startswith('CONNECT'):
                return data
        
        if len(data) > 65536:
            return ''
            
        stream_parser = NodeBuilder()
        
        try:
            stream_parser.Parse(data)
        except ExpatError:
            return ''
        
        parsed = stream_parser.getDom()
        
        if parsed:
            return parsed
        
        return ''

    def srv_lookup(self, server):
        " SRV resolver. Takes server=(host, port) as argument. Returns new (host, port) pair "
        if HAVE_DNSPYTHON or HAVE_PYDNS:
            host, port = server
            possible_queries = ['_xmpp-client._tcp.' + host]

            for query in possible_queries:
                try:
                    if HAVE_DNSPYTHON:
                        answers = [x for x in dns.resolver.query(query, 'SRV')]
                        if answers:
                            host = str(answers[0].target)
                            port = int(answers[0].port)
                            break
                    elif HAVE_PYDNS:
                        # ensure we haven't cached an old configuration
                        pydns.DiscoverNameServers()
                        response = pydns.Request().req(query, qtype='SRV')
                        answers = response.answers
                        if len(answers) > 0:
                            # ignore the priority and weight for now
                            _, _, port, host = answers[0]['data']
                            del _
                            port = int(port)
                            break
                except:
                    self.DEBUG('An error occurred while looking up %s' % query, 'warn')
            server = (host, port)
        else:
            self.DEBUG("Could not load one of the supported DNS libraries (dnspython or pydns). SRV records will not be queried and you may need to set custom hostname/port for some servers to be accessible.\n",'warn')
        # end of SRV resolver
        return server

    def plugin(self, owner):
        """ Fire up connection. Return non-empty string on success.
            Also registers self.disconnected method in the owner's dispatcher.
            Called internally. """
        if not self._server:
            self._server = (self._owner.Server, 5222)
            
        if self.use_srv:
            server = self.srv_lookup(self._server)
        else:
            server = self._server
        
        if not self.connect(server):
            return
        
        self._owner.Connection = self
        self._owner.RegisterDisconnectHandler(self.disconnected)
        return 'ok'

    def getHost(self):
        """ Return the 'host' value that is connection is [will be] made to."""
        return self._server[0]
    def getPort(self):
        """ Return the 'port' value that is connection is [will be] made to."""
        return self._server[1]

    def connect(self,server=None):
        """ Try to connect to the given host/port. Does not lookup for SRV record.
            Returns non-empty string on success. """
        try:
            if not server: server=self._server
            self._sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.connect((server[0], int(server[1])))
            self._send=self._sock.sendall
            self._recv=self._sock.recv
            self.DEBUG("Successfully connected to remote host %s"%repr(server),'start')
            return 'ok'
        except socket.error as sockerr:        
            if isinstance(sockerr, tuple):
                errno, strerror = sockerr
                
                self.DEBUG("Failed to connect to remote host %s: %s (%s)"%(repr(server), strerror, errno),'error')
            else:
                self.DEBUG("Failed to connect to remote host %s: %s"%(repr(server), str(sockerr)),'error')
        except: pass

    def plugout(self):
        """ Disconnect from the remote server and unregister self.disconnected method from
            the owner's dispatcher. """
        self._sock.close()
        if 'Connection' in self._owner.__dict__:
            del self._owner.Connection
            self._owner.UnregisterDisconnectHandler(self.disconnected)

    def receive(self):
        """ Reads all pending incoming data.
            In case of disconnection calls owner's disconnected() method and then raises IOError exception."""
        
        received = ''
        
        try:
            received = self._recv(BUFLEN)
        except socket.sslerror as e:
            self._seen_data=0
            print(1313)
            if e[0]==socket.SSL_ERROR_WANT_READ: return ''
            if e[0]==socket.SSL_ERROR_WANT_WRITE: return ''
            self.DEBUG('Socket error while receiving data','error')
            sys.exc_clear()
            self._owner.disconnected()
            #raise IOError("Disconnected from server")
        except:
            received = ''

        while self.pending_data(0):
            try:
                add = self._recv(BUFLEN)
            except IOError:
                return ''
            except Exception:
                add = ''
            
            received += add
            
            if not add:
                break

        if len(received): # length of 0 means disconnect
            self._seen_data=1
            self.DEBUG(received,'got')
            if hasattr(self._owner, 'Dispatcher'):
                self._owner.Dispatcher.Event('', DATA_RECEIVED, received)
        else:
            self.DEBUG('Socket error while receiving data','error')
            self._owner.disconnected()
            #raise IOError("Disconnected from server")
            return ''
        return received

    def send(self, raw_data):
        """ Writes raw outgoing data. Blocks until done.
            If supplied data is unicode string, encodes it to utf-8 before send."""
        
        if type(raw_data)==type(''): 
            raw_data = raw_data.encode()
        elif type(raw_data)!=type(''): 
            raw_data = ustr(raw_data).encode()
        
        #checked_data = self._check_ogoing_data(raw_data)

        #if type(raw_data) == type(''):
        #    raw_data = str(checked_data).encode()
        #elif type(raw_data) != type(''):
        #    raw_data = ustr(checked_data).encode()

        pcres = False

        if raw_data:
            pcres = True

        try:
            self._send(raw_data)
        
            # Avoid printing messages that are empty keepalive packets.
            if raw_data.strip():
                self.DEBUG(raw_data, 'sent')
                
                if hasattr(self._owner, 'Dispatcher'): # HTTPPROXYsocket will send data before we have a Dispatcher
                    self._owner.Dispatcher.Event('', DATA_SENT, raw_data)

            return pcres
        except:
            self.DEBUG("Socket error while sending data",'error')
            self._owner.disconnected()
            return False

    def pending_data(self, timeout=0):
        """ Returns true if there is a data ready to be read. """
        return select.select([self._sock],[],[],timeout)[0]

    def disconnect(self):
        """ Closes the socket. """
        self.DEBUG("Closing socket",'stop')
        self._sock.close()

    def disconnected(self):
        """ Called when a Network Error or disconnection occurs.
            Designed to be overidden. """
        self.DEBUG("Socket operation failed",'error')

DBG_CONNECT_PROXY='CONNECTproxy'
class HTTPPROXYsocket(TCPsocket):
    """ HTTP (CONNECT) proxy connection class. Uses TCPsocket as the base class
        redefines only connect method. Allows to use HTTP proxies like squid with
        (optionally) simple authentication (using login and password). """
    def __init__(self,proxy,server,use_srv=True):
        """ Caches proxy and target addresses.
            'proxy' argument is a dictionary with mandatory keys 'host' and 'port' (proxy address)
            and optional keys 'user' and 'password' to use for authentication.
            'server' argument is a tuple of host and port - just like TCPsocket uses. """
        TCPsocket.__init__(self,server,use_srv)
        self.DBG_LINE=DBG_CONNECT_PROXY
        self._proxy=proxy

    def plugin(self, owner):
        """ Starts connection. Used interally. Returns non-empty string on success."""
        owner.debug_flags.append(DBG_CONNECT_PROXY)
        return TCPsocket.plugin(self,owner)

    def connect(self,dupe=None):
        """ Starts connection. Connects to proxy, supplies login and password to it
            (if were specified while creating instance). Instructs proxy to make
            connection to the target server. Returns non-empty sting on success. """
        if not TCPsocket.connect(self,(self._proxy['host'],self._proxy['port'])): return
        self.DEBUG("Proxy server contacted, performing authentification",'start')
        connector = ['CONNECT %s:%s HTTP/1.0' % (self._server),
            'Proxy-Connection: Keep-Alive',
            'Pragma: no-cache',
            'Host: %s:%s' % (self._server),
            'User-Agent: HTTPPROXYsocket/v0.1']
        if 'user' in self._proxy and 'password' in self._proxy:
            credentials = '%s:%s' % (self._proxy['user'],self._proxy['password'])
            credentials = base64.encodestring(credentials).strip()
            connector.append('Proxy-Authorization: Basic ' + credentials)
        connector.append('\r\n')
        
        self.send('\r\n'.join(connector))
        
        try:
            reply = self.receive().replace('\r','')
        except:
            self.DEBUG('Proxy suddenly disconnected', 'error')
            self._owner.disconnected()
            return
        
        try:
            proto, code, desc = reply.split('\n')[0].split(' ', 2)
        except:
            raise error('Invalid proxy reply')

        if code!='200':
            self.DEBUG('Invalid proxy reply: %s %s %s'%(proto,code,desc),'error')
            self._owner.disconnected()
            return
        
        while reply.find('\n\n') == -1:
            try:
                reply += self.receive().replace('\r', '')
            except IOError:
                self.DEBUG('Proxy suddenly disconnected', 'error')
                self._owner.disconnected()
                return
            
        self.DEBUG("Authentification successfull. Jabber server contacted.",'ok')
        
        return 'ok'

    def DEBUG(self,text,severity):
        """Overwrites DEBUG tag to allow debug output be presented as "CONNECTproxy"."""
        return self._owner.DEBUG(DBG_CONNECT_PROXY,text,severity)

class TLS(PlugIn):
    """ TLS connection used to encrypts already estabilished tcp connection."""
    def PlugIn(self,owner,now=0):
        """ If the 'now' argument is true then starts using encryption immidiatedly.
            If 'now' in false then starts encryption as soon as TLS feature is
            declared by the server (if it were already declared - it is ok).
        """
        if 'TLS' in owner.__dict__: return  # Already enabled.
        PlugIn.PlugIn(self,owner)
        DBG_LINE='TLS'
        if now: return self._startSSL()
        if self._owner.Dispatcher.Stream.features:
            try: self.FeaturesHandler(self._owner.Dispatcher,self._owner.Dispatcher.Stream.features)
            except NodeProcessed: pass
        else: self._owner.RegisterHandlerOnce('features',self.FeaturesHandler,xmlns=NS_STREAMS)
        self.starttls=None

    def plugout(self,now=0):
        """ Unregisters TLS handler's from owner's dispatcher. Take note that encription
            can not be stopped once started. You can only break the connection and start over."""
        self._owner.UnregisterHandler('features',self.FeaturesHandler,xmlns=NS_STREAMS)
        self._owner.UnregisterHandler('proceed',self.StartTLSHandler,xmlns=NS_TLS)
        self._owner.UnregisterHandler('failure',self.StartTLSHandler,xmlns=NS_TLS)

    def FeaturesHandler(self, conn, feats):
        """ Used to analyse server <features/> tag for TLS support.
            If TLS is supported starts the encryption negotiation. Used internally"""
        if not feats.getTag('starttls',namespace=NS_TLS):
            self.DEBUG("TLS unsupported by remote server.",'warn')
            return
        self.DEBUG("TLS supported by remote server. Requesting TLS start.",'ok')
        self._owner.RegisterHandlerOnce('proceed',self.StartTLSHandler,xmlns=NS_TLS)
        self._owner.RegisterHandlerOnce('failure',self.StartTLSHandler,xmlns=NS_TLS)
        self._owner.Connection.send('<starttls xmlns="%s"/>'%NS_TLS)
        raise NodeProcessed

    def pending_data(self,timeout=0):
        """ Returns true if there possible is a data ready to be read. """
        return self._tcpsock._seen_data or select.select([self._tcpsock._sock],[],[],timeout)[0] # 

    def _startTLS(self):
        """ Immidiatedly switch socket to TLS mode. Used internally."""
        """ Here we should switch pending_data to hint mode."""
        
        #context = ssl.create_default_context()

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        
        context.load_verify_locations(self._owner._cert)
        
        tcpsock=self._owner.Connection
        #tcpsock._sslObj = ssl.wrap_socket(tcpsock._sock, None, None)
        
        tcpsock._sslObj = context.wrap_socket(tcpsock._sock, server_hostname=self._owner.Server)
        
        tcpsock._recv = tcpsock._sslObj.recv
        tcpsock._send = tcpsock._sslObj.sendall
        tcpsock._sslObj.setblocking(0)
                
        tcpsock._seen_data=1
        self._tcpsock=tcpsock
        tcpsock.pending_data=self.pending_data
          
        self.starttls='success'

    def StartTLSHandler(self, conn, starttls):
        """ Handle server reply if TLS is allowed to process. Behaves accordingly.
            Used internally."""
        if starttls.getNamespace()!=NS_TLS: return
        self.starttls=starttls.getName()
        if self.starttls=='failure':
            self.DEBUG("Got starttls response: "+self.starttls,'error')
            return
        self.DEBUG("Got starttls proceed response. Switching to TLS/SSL...",'ok')

        self._owner.Dispatcher.PlugOut()
        
        self._startTLS()
        
        dispatcher.Dispatcher().PlugIn(self._owner)
