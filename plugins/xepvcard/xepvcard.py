# -*- coding: utf-8 -*-

#  fatal plugin
#  xepvcard plugin

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Some portions of code © 2010 Quality <admin@qabber.ru>
#  Copyright © 2009-2012 Ancestors Soft

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
from muc import kick, ban, visitor, del_banned

def handler_vcardget(type, source, parameters):
    gch_jid = source[1]
    nick = source[2]

    if parameters.strip():
        if is_groupchat(gch_jid):
            if is_gch_user(gch_jid, parameters):
                nick = parameters
                jid = '%s/%s' % (gch_jid, nick)
            else:
                jid = parameters
                nick = jid
        else:
            jid = parameters
            nick = jid
    else:
        if is_groupchat(gch_jid):
            jid = '%s/%s' % (gch_jid, nick)
        else:
            jid = gch_jid
        
        nick = ''
    
    vcard_iq = xmpp.Iq('get')
    Id = 'vcard%s' % (time.time())
    vcard_iq.setID(Id)
    vcard_iq.addChild('vCard', {}, [], 'vcard-temp')
    vcard_iq.setTo(jid)
    jconn = get_client_conn()
    jconn.SendAndCallForResponse(vcard_iq, handler_vcardget_answ, {'type': type, 'source': source, 'nick': nick, 'sId': Id})

@handle_xmpp_exc('Unknown error!')
def handler_vcardget_answ(coze, res, type, source, nick, sId):
    rep = ''
    
    if res:
        Id = res.getID()
        
        if not Id == sId:
            return reply(type, source, l('Unknown error!'))
        
        ptype = res.getType()
            
        if ptype == 'error':
            ecode = res.getErrorCode()
            
            if ecode == '404':
                return reply(type, source, l('User not found!'))
            else:
                return reply(type, source, l('Not supported by user client!'))
        elif ptype == 'result':
            name, nickname, prefix, given, middle, family, suffix, bday, street, pobox, extadr, extadd, locality, region, pcode, ctry, home, number, tz, jid, title, role, orgname, orgunit, url, email, desc, binval, typep = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
            
            if res.getChildren():
                props = res.getChildren()[0]
                props = props.getChildren()
            else:
                return reply(type, source, l('Empty vCard!'))
            
            for p in props:
                if p.getName() == 'NICKNAME': 
                    nickname = p.getData()
                    
                if p.getName() == 'FN': 
                    name = p.getData()
                
                if p.getName() == 'N':
                    for pc in p.getChildren():
                        if pc.getName() == 'PREFIX': 
                            prefix = pc.getData()
                        if pc.getName() == 'GIVEN': 
                            given = pc.getData()
                        if pc.getName() == 'MIDDLE': 
                            middle = pc.getData()
                        if pc.getName() == 'FAMILY': 
                            family = pc.getData()
                        if pc.getName() == 'SUFFIX': 
                            suffix = pc.getData()
                        
                if p.getName() == 'BDAY': 
                    bday = p.getData()
                
                if p.getName() == 'ADR':
                    for pc in p.getChildren():
                        if pc.getName() == 'STREET': 
                            street = pc.getData()
                        if pc.getName() == 'POBOX': 
                            pobox = pc.getData()
                        if pc.getName() == 'EXTADR': 
                            extadr = pc.getData()
                        if pc.getName() == 'EXTADD': 
                            extadd = pc.getData()
                        if pc.getName() == 'LOCALITY': 
                            locality = pc.getData()
                        if pc.getName() == 'REGION': 
                            region = pc.getData()
                        if pc.getName() == 'PCODE': 
                            pcode = pc.getData()
                        if pc.getName() == 'CTRY': 
                            ctry = pc.getData()
                        
                if p.getName() == 'TEL':
                    for pc in p.getChildren():
                        if pc.getName() == 'HOME': 
                            home = pc.getData()
                        if pc.getName() == 'NUMBER': 
                            number = pc.getData()
                        
                if p.getName() == 'TZ': 
                    tz = p.getData()
                if p.getName() == 'JABBERID': 
                    jid = p.getData()
                if p.getName() == 'TITLE': 
                    title = p.getData()
                if p.getName() == 'ROLE': 
                    role = p.getData()
                
                if p.getName() == 'ORG':
                    for pc in p.getChildren():
                        if pc.getName() == 'ORGNAME': 
                            orgname = pc.getData()
                        if pc.getName() == 'ORGUNIT': 
                            orgunit = pc.getData()
                
                if p.getName() == 'URL': 
                    url = p.getData()
                
                if p.getName() == 'EMAIL': 
                    for pc in p.getChildren():
                        if pc.getName() == 'USERID': 
                            email = pc.getData()
                
                if p.getName() == 'DESC': 
                    desc = p.getData()
                
                if p.getName() == 'PHOTO':
                    for pc in p.getChildren():
                        if pc.getName() == 'BINVAL': 
                            avlen = len(base64.decodestring(pc.getData()))
                            avlkb = round(float(avlen) / 1024, 1)
                            binval = '%s кБ.' % (avlkb)
                        
                        if pc.getName() == 'TYPE': 
                            typep = pc.getData().strip('/')
                        
            if not nick:
                rep = l('Information from vCard:\n')
            else:
                rep = l('Information about "%s" from vCard:\n') % (nick)
                    
            if nickname: 
                rep += l('\nNick: %s.') % (nickname)
                
            if name: 
                rep += l('\nFull name: %s.') % (name)
                
            if prefix: 
                rep += l('\nPrefix: %s.') % (prefix)
                
            if given: 
                rep += l('\nName: %s.') % (given)
                
            if middle: 
                rep += l('\nLast name: %s.') % (middle)
                
            if family: 
                rep += l('\nFamily name: %s.') % (family)
                
            if suffix: 
                rep += l('\nSuffix: %s.') % (suffix)
                
            if bday: 
                rep += l('\nBirthday: %s.') % (bday)
                
            if extadr: 
                rep += l('\nStreet: %s.') % (street)
                
            if extadr: 
                rep += l('\nPostal box: %s.') % (pobox)
                
            if extadr: 
                rep += l('\nAdditional address : %s.') % (extadd)
                
            if extadr: 
                rep += l('\nExtended address: %s.') % (extadr)
                
            if locality: 
                rep += l('\nCity: %s.') % (locality)
                
            if region: 
                rep += l('\nRegion: %s.') % (region)
                
            if pcode: 
                rep += l('\nPostal code: %s.') % (pcode)
                
            if ctry: 
                rep += l('\nCountry: %s.') % (ctry)
                
            if home: 
                rep += l('\nPhone number (home): %s.') % (home)
                
            if number: 
                rep += l('\nPhone number (mobile): %s.') % (number)
                
            if tz: 
                rep += l('\nTime zone: %s.') % (tz)
                
            if jid: 
                rep += l('\nJID: %s') % (jid)
                
            if url: 
                rep += l('\nURL: %s') % (url)
                
            if title: 
                rep += l('\nPost: %s.') % (title)
                
            if role: 
                rep += l('\nProfession: %s.') % (role)
                
            if orgname: 
                rep += l('\nOrganization name: %s.') % (orgname)
                
            if orgunit: 
                rep += l('\nOrganization unit: %s.') % (orgunit)
                
            if email: 
                rep += l('\nE-mail: %s') % (email)
                
            if desc: 
                rep += l('\nAbout: %s.') % (desc)
                
            if binval: 
                rep += l('\nPhoto size: %s') % (binval)
                
            if typep: 
                rep += l('\nPhoto type: %s.') % (typep)
            
            if rep == '': 
                rep = l('Empty vCard!')
        else:
            rep = l('Not supported by user client!')
    else:
        rep = l('Unknown error!')
    
    return reply(type, source, rep)

def handler_novcard_join(groupchat, nick, aff, role):
    nvcres = get_gch_param(groupchat, 'novc_res', 'ignore')
    jid = groupchat + '/' + nick
        
    type = 'public'
    source = [groupchat + '/' + nick, groupchat, nick]
        
    if aff == 'none' and nvcres != 'ignore':
        vcard_iq = xmpp.Iq('get')
        Id = 'vcard%s' % (time.time())
        vcard_iq.setID(Id)
        vcard_iq.addChild('vCard', {}, [], 'vcard-temp')
        vcard_iq.setTo(jid)
        
        jconn = get_client_conn()
        jconn.SendAndCallForResponse(vcard_iq, handler_novcardget_answ, {'type': type, 'source': source, 'nick': nick, 'sId': Id})

@handle_xmpp_exc(quiet=True)
def handler_novcardget_answ(coze, res, type, source, nick, sId):
    groupchat = source[1]
    rep = 0
    nvcres = ''
    nvcmess = ''
    
    if res:
        Id = res.getID()
        
        if not Id == sId:
            return reply(type, source, l('Unknown error!'))
        
        ptype = res.getType()    
        
        if ptype == 'error':
            nvcres = get_gch_param(groupchat, 'novc_res', 'ignore').strip()
            nvcmess = get_gch_param(groupchat, 'novc_mess', l('Fill your vCard and then rejoin groupchat!'))
        elif ptype == 'result':
            props = None
            
            if res.getChildren():
                props = res.getChildren()[0].getChildren()
            else:
                nvcres = get_gch_param(groupchat, 'novc_res', 'ignore').strip()
                nvcmess = get_gch_param(groupchat, 'novc_mess', l('Fill your vCard and then rejoin groupchat!'))
            
            if not props:
                nvcres = get_gch_param(groupchat, 'novc_res', 'ignore').strip()
                nvcmess = get_gch_param(groupchat, 'novc_mess', l('Fill your vCard and then rejoin groupchat!'))

    if nvcres:
        if nvcres == 'kick':
            kick(groupchat, nick, nvcmess)
        elif nvcres == 'ban':
            ban(groupchat, nick, nvcmess)
            del_banned(groupchat, nick)
        elif nvcres == 'visitor':
            visitor(groupchat, nick, nvcmess)
            msg(groupchat + '/' + nick, nvcmess)
        elif nvcres == 'warn':
            msg(groupchat + '/' + nick, nvcmess)

def handler_novcard_res(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if not parameters.strip() in ['ignore', 'warn', 'kick', 'ban', 'visitor']:
            return reply(type, source, l('Invalid syntax!'))

        set_gch_param(groupchat, 'novc_res', parameters.strip())
        return reply(type, source, l('Reaction on empty vCard has been set to %s.') % (parameters.strip()))
    else:
        nvcres = get_gch_param(groupchat, 'novc_res', 'ignore').strip()
        return reply(type, source, l('Reaction on empty vCard is set to %s.') % (nvcres))
        
def handler_novcard_mess(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        set_gch_param(groupchat, 'novc_mess', parameters.strip())
        return reply(type, source, l('Message if vCard is empty has been set!'))
    else:
        nvcmess = get_gch_param(groupchat, 'novc_mess', l('Fill your vCard and then rejoin groupchat!'))
        return reply(type, source, l('Message if vCard is empty is set to: %s') % (nvcmess))

def get_novcard_state(gch):
    if not param_exists(gch, 'novc_res'):
        set_gch_param(gch, 'novc_res', 'ignore')
    if not param_exists(gch, 'novc_mess'):
        set_gch_param(gch, 'novc_mess', l('Fill your vCard and then rejoin groupchat!'))

register_command_handler(handler_novcard_mess, 'novc_mess', 20)
register_command_handler(handler_novcard_res, 'novc_res', 20)
register_command_handler(handler_vcardget, 'vcard', 10)

register_stage1_init(get_novcard_state)
register_join_handler(handler_novcard_join)
