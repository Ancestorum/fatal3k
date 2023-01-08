##   auth.py
##
##   Copyright (C) 2003-2005 Alexey "Snake" Nezhdanov
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

# $Id: auth.py,v 1.41 2008/09/13 21:45:21 normanr Exp $

"""
Provides library with all Non-SASL and SASL authentication mechanisms.
Can be used both for client and transport authentication.
"""

import os
from .protocol import *
from .client import PlugIn
import base64,random,re
from . import dispatcher
import traceback, time

import hmac
import binascii
import logging
import hashlib
from hashlib import pbkdf2_hmac

def b64decode(data, return_type=str):
    if not data:
        raise ValueError('No data to decode')
    if isinstance(data, str):
        data = data.encode()
    result = base64.b64decode(data)
    if return_type == bytes:
        return result
    return result.decode()

def b64encode(data, return_type=str):
    if not data:
        raise ValueError('No data to encode')
    if isinstance(data, str):
        data = data.encode()
    result = base64.b64encode(data)
    if return_type == bytes:
        return result
    return result.decode()

def _hmac(key, message):
    return hmac.new(key=key, msg=message.encode(), digestmod='sha1').digest()

def _xor(x, y):
    return bytes([px ^ py for px, py in zip(x, y)])

def _h(data):
    return hashlib.new('sha1', data).digest()

def _scram_parse(scram_data):
    return dict(s.split('=', 1) for s in scram_data.split(','))

def HH(some): return hashlib.md5(some).hexdigest()
def H(some): return hashlib.md5(some).digest()

def C(some): 
    sms = b''
    for sm in some:
        if type(sm) is bytes:
            sms += sm + b':'
        else:
            sms += sm.encode() + b':'
    return sms[:-1]

def app_file(filename, data):
    try:
        fp = open(filename, 'a', encoding='utf-8')
        fp.write(data)
        fp.close()
    except:
        pass

def log_exc_error(file='error.log'):
    exc_err = traceback.format_exc()
    exc_time = time.strftime('[%H:%M:%S]: ', time.localtime(time.time()))
    app_file(file,'%s%s\n' % (exc_time, exc_err))
    return '%s%s\n' % (exc_time, exc_err)

class NonSASL(PlugIn):
    """ Implements old Non-SASL (JEP-0078) authentication used in jabberd1.4 and transport authentication."""
    def __init__(self,user,password,resource):
        """ Caches username, password and resource for auth. """
        PlugIn.__init__(self)
        self.DBG_LINE='gen_auth'
        self.user=user
        self.password=password
        self.resource=resource

    def plugin(self,owner):
        """ Determine the best auth method (digest/0k/plain) and use it for auth.
            Returns used method name on success. Used internally. """
        if not self.resource: return self.authComponent(owner)
        self.DEBUG('Querying server about possible auth methods','start')
        resp=owner.Dispatcher.SendAndWaitForResponse(Iq('get',NS_AUTH,payload=[Node('username',payload=[self.user])]))
        if not isResultNode(resp):
            self.DEBUG('No result node arrived! Aborting...','error')
            return
        iq=Iq(typ='set',node=resp)
        query=iq.getTag('query')
        query.setTagData('username',self.user)
        query.setTagData('resource',self.resource)

        if query.getTag('digest'):
            self.DEBUG("Performing digest authentication",'ok')
            query.setTagData('digest',hashlib.sha1(owner.Dispatcher.Stream._document_attrs['id']+self.password).hexdigest())
            if query.getTag('password'): query.delChild('password')
            method='digest'
        elif query.getTag('token'):
            token=query.getTagData('token')
            seq=query.getTagData('sequence')
            self.DEBUG("Performing zero-k authentication",'ok')
            hash = hashlib.sha1(hashlib.sha1(self.password).hexdigest()+token).hexdigest()
            for foo in range(int(seq)): hash = hashlib.sha1(hash).hexdigest()
            query.setTagData('hash',hash)
            method='0k'
        else:
            self.DEBUG("Sequre methods unsupported, performing plain text authentication",'warn')
            query.setTagData('password',self.password)
            method='plain'
        resp=owner.Dispatcher.SendAndWaitForResponse(iq)
        if isResultNode(resp):
            self.DEBUG('Sucessfully authenticated with remove host.','ok')
            owner.User=self.user
            owner.Resource=self.resource
            owner._registered_name=owner.User+'@'+owner.Server+'/'+owner.Resource
            return method
        self.DEBUG('Authentication failed!','error')

    def authComponent(self,owner):
        """ Authenticate component. Send handshake stanza and wait for result. Returns "ok" on success. """
        self.handshake=0
        owner.send(Node(NS_COMPONENT_ACCEPT+' handshake',payload=[hashlib.sha1(owner.Dispatcher.Stream._document_attrs['id']+self.password).hexdigest()]))
        owner.RegisterHandler('handshake',self.handshakeHandler,xmlns=NS_COMPONENT_ACCEPT)
        while not self.handshake:
            self.DEBUG("waiting on handshake",'notify')
            owner.Process(1)
        owner._registered_name=self.user
        if self.handshake+1: return 'ok'

    def handshakeHandler(self,disp,stanza):
        """ Handler for registering in dispatcher for accepting transport authentication. """
        if stanza.getName()=='handshake': self.handshake=1
        else: self.handshake=-1

class SASL(PlugIn):
    """ Implements SASL authentication. """
    def __init__(self,username,password):
        PlugIn.__init__(self)
        self.username=username
        self.password=password
        self._client_nonce = '%x' % int(binascii.hexlify(os.urandom(24)), 16)
        self._client_first_message_bare = ''
        self._channel_binding = 'n,,'

    def nonce_length(self):
        return len(self._client_nonce)

    def plugin(self,owner):
        if 'version' not in self._owner.Dispatcher.Stream._document_attrs: self.startsasl='not-supported'
        elif self._owner.Dispatcher.Stream.features:
            try: self.FeaturesHandler(self._owner.Dispatcher,self._owner.Dispatcher.Stream.features)
            except NodeProcessed: pass
        else: self.startsasl=None

    def auth(self):
        """ Start authentication. Result can be obtained via "SASL.startsasl" attribute and will be
            either "success" or "failure". Note that successfull auth will take at least
            two Dispatcher.Process() calls. """
        if self.startsasl: pass
        elif self._owner.Dispatcher.Stream.features:
            try: self.FeaturesHandler(self._owner.Dispatcher,self._owner.Dispatcher.Stream.features)
            except NodeProcessed: pass
        else: self._owner.RegisterHandler('features',self.FeaturesHandler,xmlns=NS_STREAMS)

    def plugout(self):
        """ Remove SASL handlers from owner's dispatcher. Used internally. """
        if 'features' in self._owner.__dict__: self._owner.UnregisterHandler('features',self.FeaturesHandler,xmlns=NS_STREAMS)
        if 'challenge' in self._owner.__dict__: self._owner.UnregisterHandler('challenge',self.SASLHandler,xmlns=NS_SASL)
        if 'failure' in self._owner.__dict__: self._owner.UnregisterHandler('failure',self.SASLHandler,xmlns=NS_SASL)
        if 'success' in self._owner.__dict__: self._owner.UnregisterHandler('success',self.SASLHandler,xmlns=NS_SASL)

    def FeaturesHandler(self,conn,feats):
        """ Used to determine if server supports SASL auth. Used internally. """
        if not feats.getTag('mechanisms',namespace=NS_SASL):
            self.startsasl='not-supported'
            self.DEBUG('SASL not supported by server','error')
            return
        mecs=[]
        for mec in feats.getTag('mechanisms',namespace=NS_SASL).getTags('mechanism'):
            mecs.append(mec.getData())
        self._owner.RegisterHandler('challenge',self.SASLHandler,xmlns=NS_SASL)
        self._owner.RegisterHandler('failure',self.SASLHandler,xmlns=NS_SASL)
        self._owner.RegisterHandler('success',self.SASLHandler,xmlns=NS_SASL)
        if "ANONYMOUS" in mecs and self.username == None:
            node=Node('auth',attrs={'xmlns':NS_SASL,'mechanism':'ANONYMOUS'})
        elif "SCRAM-SHA-1" in mecs:
            self._mech = 'SSHA'
            self._client_first_message_bare = 'n=%s,r=%s' % (self.username, self._client_nonce)
            client_first_message = '%s%s' % (self._channel_binding, self._client_first_message_bare)
            
            payload = b64encode(client_first_message)
            
            node=Node('auth',attrs={'xmlns':NS_SASL,'mechanism':'SCRAM-SHA-1'}, payload=[payload])
        elif "DIGEST-MD5" in mecs:
            self._mech = 'DMD5'
            node=Node('auth',attrs={'xmlns':NS_SASL,'mechanism':'DIGEST-MD5'})
        elif "PLAIN" in mecs:
            sasl_data='%s\x00%s\x00%s'%(self.username+'@'+self._owner.Server,self.username,self.password)
            sasl_data = sasl_data.encode()
            sasl_data = base64.encodebytes(sasl_data)
            sasl_data = sasl_data.replace('\r','').replace('\n','')
            node=Node('auth',attrs={'xmlns':NS_SASL,'mechanism':'PLAIN'},payload=[sasl_data])
        else:
            self.startsasl='failure'
            self.DEBUG('I can only use DIGEST-MD5 and PLAIN mecanisms.','error')
            return
        self.startsasl='in-process'
        self._owner.send(node.__str__())
        raise NodeProcessed

    def SASLHandler(self,conn,challenge):
        """ Perform next SASL auth step. Used internally. """
        if challenge.getNamespace()!=NS_SASL: return
        
        if challenge.getName()=='failure':
            self.startsasl='failure'
            try: reason=challenge.getChildren()[0]
            except: reason=challenge
            self.DEBUG('Failed SASL authentification: %s'%reason,'error')
            raise NodeProcessed
        elif challenge.getName()=='success':
            self.startsasl='success'
            self.DEBUG('Successfully authenticated with remote server.','ok')
            handlers=self._owner.Dispatcher.dumpHandlers()
            self._owner.Dispatcher.PlugOut()
            dispatcher.Dispatcher().PlugIn(self._owner)
            self._owner.Dispatcher.restoreHandlers(handlers)
            self._owner.User=self.username
            raise NodeProcessed
    
        if self._mech == 'SSHA':
            server_first_message = challenge.getData()
            server_first_message = b64decode(server_first_message)
            schallenge = _scram_parse(server_first_message)
            client_nonce = schallenge['r'][:self.nonce_length()]
            
            if client_nonce != self._client_nonce:
                raise AuthFail('Invalid client nonce received from server')

            salt = b64decode(schallenge['s'], bytes)
            iteration_count = int(schallenge['i'])

            if iteration_count < 4096:
                raise AuthFail('Salt iteration count to low: %s' % iteration_count)

            salted_password = pbkdf2_hmac('sha1', self.password.encode(), salt, iteration_count)
            
            client_final_message_wo_proof = 'c=%s,r=%s' % (b64encode(self._channel_binding), schallenge['r'])

            client_key = _hmac(salted_password, 'Client Key')
            stored_key = _h(client_key)
            
            auth_message = '%s,%s,%s' % (self._client_first_message_bare, server_first_message, client_final_message_wo_proof)
            client_signature = _hmac(stored_key, auth_message)
            client_proof = _xor(client_key, client_signature)

            client_finale_message = 'c=%s,r=%s,p=%s' % (b64encode(self._channel_binding), schallenge['r'], b64encode(client_proof))

            server_key = _hmac(salted_password, 'Server Key')
            _server_signature = _hmac(server_key, auth_message)

            payload = b64encode(client_finale_message)
            
            node = Node('response', attrs={'xmlns': NS_SASL}, payload=[payload])
            self._owner.send(node.__str__())
        elif self._mech == 'DMD5':        
            incoming_data=challenge.getData()
            chal={}
            data=base64.decodebytes(incoming_data.encode())
            data=data.decode()
            self.DEBUG('Got challenge:'+data,'ok')
            
            for pair in re.findall('(\w+\s*=\s*(?:(?:"[^"]+")|(?:[^,]+)))',data):
                key,value=[x.strip() for x in pair.split('=', 1)]
                if value[:1]=='"' and value[-1:]=='"': value=value[1:-1]
                chal[key]=value
            
            if 'qop' in chal and 'auth' in [x.strip() for x in chal['qop'].split(',')]:
                resp={}
                resp['username']=self.username
                resp['realm']=self._owner.Server
                resp['nonce']=chal['nonce']
                cnonce=''
                for i in range(7):
                    cnonce+=hex(int(random.random()*65536*4096))[2:]
                resp['cnonce']=cnonce
                resp['nc']=('00000001')
                resp['qop']='auth'
                resp['digest-uri']='xmpp/'+self._owner.Server
                mdd = H(C([resp['username'],resp['realm'],self.password]))
                A1=C([mdd,resp['nonce'],resp['cnonce']])
                A2=C(['AUTHENTICATE',resp['digest-uri']])
                response=HH(C([HH(A1),resp['nonce'],resp['nc'],resp['cnonce'],resp['qop'],HH(A2)]))
                resp['response']=response
                resp['charset']='utf-8'
                sasl_data=''
                
                for key in ['charset','username','realm','nonce','nc','cnonce','digest-uri','response','qop']:
                    if key in ['nc','qop','response','charset']: sasl_data+="%s=%s,"%(key,resp[key])
                    else: sasl_data+='%s="%s",'%(key,resp[key])

                sasl_data = sasl_data[:-1]
                sasl_data = base64.encodebytes(sasl_data.encode())
                sasl_data = sasl_data.decode().replace('\r','').replace('\n','')
            
                node=Node('response',attrs={'xmlns':NS_SASL},payload=[sasl_data])
            
                self._owner.send(node.__str__())
            elif 'rspauth' in chal: self._owner.send(Node('response',attrs={'xmlns':NS_SASL}).__str__())
            else: 
                self.startsasl='failure'
                self.DEBUG('Failed SASL authentification: unknown challenge','error')
        
        raise NodeProcessed

class Bind(PlugIn):
    """ Bind some JID to the current connection to allow router know of our location."""
    def __init__(self):
        PlugIn.__init__(self)
        self.DBG_LINE='bind'
        self.bound=None

    def plugin(self,owner):
        """ Start resource binding, if allowed at this time. Used internally. """
        if self._owner.Dispatcher.Stream.features:
            try: self.FeaturesHandler(self._owner.Dispatcher,self._owner.Dispatcher.Stream.features)
            except NodeProcessed: pass
        else: self._owner.RegisterHandler('features',self.FeaturesHandler,xmlns=NS_STREAMS)

    def plugout(self):
        """ Remove Bind handler from owner's dispatcher. Used internally. """
        self._owner.UnregisterHandler('features',self.FeaturesHandler,xmlns=NS_STREAMS)

    def FeaturesHandler(self,conn,feats):
        """ Determine if server supports resource binding and set some internal attributes accordingly. """
        if not feats.getTag('bind',namespace=NS_BIND):
            self.bound='failure'
            self.DEBUG('Server does not requested binding.','error')
            return
        if feats.getTag('session',namespace=NS_SESSION): self.session=1
        else: self.session=-1
        self.bound=[]

    def Bind(self,resource=None):
        """ Perform binding. Use provided resource name or random (if not provided). """
        while self.bound is None and self._owner.Process(1): pass
        if resource: resource=[Node('resource',payload=[resource])]
        else: resource=[]
        resp=self._owner.SendAndWaitForResponse(Protocol('iq',typ='set',payload=[Node('bind',attrs={'xmlns':NS_BIND},payload=resource)]))
        if isResultNode(resp):
            self.bound.append(resp.getTag('bind').getTagData('jid'))
            self.DEBUG('Successfully bound %s.'%self.bound[-1],'ok')
            jid=JID(resp.getTag('bind').getTagData('jid'))
            self._owner.User=jid.getNode()
            self._owner.Resource=jid.getResource()
            resp=self._owner.SendAndWaitForResponse(Protocol('iq',typ='set',payload=[Node('session',attrs={'xmlns':NS_SESSION})]))
            if isResultNode(resp):
                self.DEBUG('Successfully opened session.','ok')
                self.session=1
                return 'ok'
            else:
                self.DEBUG('Session open failed.','error')
                self.session=0
        elif resp: self.DEBUG('Binding failed: %s.'%resp.getTag('error'),'error')
        else:
            self.DEBUG('Binding failed: timeout expired.','error')
            return ''

class ComponentBind(PlugIn):
    """ ComponentBind some JID to the current connection to allow router know of our location."""
    def __init__(self, sasl):
        PlugIn.__init__(self)
        self.DBG_LINE='bind'
        self.bound=None
        self.needsUnregister=None
        self.sasl = sasl

    def plugin(self,owner):
        """ Start resource binding, if allowed at this time. Used internally. """
        if not self.sasl:
            self.bound=[]
            return
        if self._owner.Dispatcher.Stream.features:
            try: self.FeaturesHandler(self._owner.Dispatcher,self._owner.Dispatcher.Stream.features)
            except NodeProcessed: pass
        else:
            self._owner.RegisterHandler('features',self.FeaturesHandler,xmlns=NS_STREAMS)
            self.needsUnregister=1

    def plugout(self):
        """ Remove ComponentBind handler from owner's dispatcher. Used internally. """
        if self.needsUnregister:
            self._owner.UnregisterHandler('features',self.FeaturesHandler,xmlns=NS_STREAMS)

    def FeaturesHandler(self,conn,feats):
        """ Determine if server supports resource binding and set some internal attributes accordingly. """
        if not feats.getTag('bind',namespace=NS_BIND):
            self.bound='failure'
            self.DEBUG('Server does not requested binding.','error')
            return
        if feats.getTag('session',namespace=NS_SESSION): self.session=1
        else: self.session=-1
        self.bound=[]

    def Bind(self,domain=None):
        """ Perform binding. Use provided domain name (if not provided). """
        while self.bound is None and self._owner.Process(1): pass
        if self.sasl:
            xmlns = NS_COMPONENT_1
        else:
            xmlns = None
        self.bindresponse = None
        ttl = dispatcher.DefaultTimeout
        self._owner.RegisterHandler('bind',self.BindHandler,xmlns=xmlns)
        self._owner.send(Protocol('bind',attrs={'name':domain},xmlns=NS_COMPONENT_1))
        while self.bindresponse is None and self._owner.Process(1) and ttl > 0: ttl-=1
        self._owner.UnregisterHandler('bind',self.BindHandler,xmlns=xmlns)
        resp=self.bindresponse
        if resp and resp.getAttr('error'):
            self.DEBUG('Binding failed: %s.'%resp.getAttr('error'),'error')
        elif resp:
            self.DEBUG('Successfully bound.','ok')
            return 'ok'
        else:
            self.DEBUG('Binding failed: timeout expired.','error')
            return ''

    def BindHandler(self,conn,bind):
        self.bindresponse = bind
        pass

class AuthFail(Exception):
    pass
