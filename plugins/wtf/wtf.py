# -*- coding: utf-8 -*-

#  fatal plugin
#  wtf plugin

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

def wr_op_file(path, data):
    data = data.encode('cp1251')
    write_file(path, data)
    fp = open(path)
    return fp

def si_request(frm, fjid, sid, name, size, entity=''):
    iq = xmpp.Protocol(name='iq', to=fjid, typ='set')
    Id = 'si%s' % (rand10())
    iq.setID(Id)
    si = iq.setTag('si')
    si.setNamespace(xmpp.NS_SI)
    si.setAttr('profile', xmpp.NS_FILE)
    si.setAttr('id', sid)
    file_tag = si.setTag('file')
    file_tag.setNamespace(xmpp.NS_FILE)
    file_tag.setAttr('name', name)
    file_tag.setAttr('size', size)
    desc = file_tag.setTag('desc')
    desc.setData(l('Entity "%s" from wtf base.') % (entity))
    file_tag.setTag('range')
    feature = si.setTag('feature')
    feature.setNamespace(xmpp.NS_FEATURE)
    _feature = xmpp.DataForm(typ='form')
    feature.addChild(node=_feature)
    field = _feature.setField('stream-method')
    field.setAttr('type', 'list-single')
    field.addOption(xmpp.NS_IBB)
    field.addOption('jabber:iq:oob')
    return iq

def check_stream(gch, nick, to, sid):
    try:
        cid = get_client_id()
        
        st_time = time.strftime('%H.%M.%S', time.localtime(time.time()))
        thrc = inc_fatal_var('info', 'thr')
        tmr_name = '%s/check%d.%s.%s' % (cid, thrc, 'check_stream', st_time)
        tmr = threading.Timer(1, check_stream, [gch, nick, to, sid])
        tmr.setName(tmr_name)
        tmr.start()
    except:
        return
    
    jconn = get_client_conn()
    
    if not sid in jconn.IBB._streams:
        tmr.cancel()
    
    if not is_gch_user(gch, nick):
        jconn.send(xmpp.Protocol('iq', to, 'set', payload=[xmpp.Node(xmpp.NS_IBB + ' close', {'sid': sid})]))
        del jconn.IBB._streams[sid]
        tmr.cancel()

def check_reader_id(gch, reader_id):
    cid = get_client_id()
    
    sql = "SELECT * FROM readers WHERE rid=?;"
    qres = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql, reader_id)
    
    if qres:
        return False
    else:
        return True	

def check_entity(gch, entity):
    cid = get_client_id()
    
    sql = "SELECT entity FROM defs WHERE entity=?;"
    qres = sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql, entity)
    
    if qres:
        return True
    else:
        return False

def chk_rdr_ent(gch, entity, reader_id):
    cid = get_client_id()
    
    sql = "SELECT entity FROM %s WHERE entity=?;" % (reader_id)
    qres = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql, entity)
    
    if qres:
        return True
    else:
        return False

def clear_nex(gch, all_wtf, reader_id):
    if all_wtf:
        nex_wtf = [nexwli for nexwli in all_wtf if not check_entity(gch, nexwli[0])]
        
        if nex_wtf:
            for nxi in nex_wtf:
                del_exp_wtf(gch, nxi[0], reader_id)
                all_wtf.remove(nxi)
    return all_wtf
        
def get_ent_count(gch):
    cid = get_client_id()
    
    sql = 'SELECT COUNT(entity) FROM defs;'
    
    qres = sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql)
    
    ent_len = 0
    
    if qres:
        ent_len = qres[0][0]
        
    return ent_len
        
def get_last_wtf(gch, reader_id):
    cid = get_client_id()
    
    sql = 'SELECT * FROM %s ORDER BY last DESC;' % (reader_id)
    qres = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql)
    
    qres = clear_nex(gch, qres, reader_id)
    
    if qres:
        return qres[0]
    else:
        return ''

def clr_rdr_blist(gch, reader_id):
    sql = 'DROP TABLE %s;' % (reader_id)
    
    cid = get_client_id()
    
    qres = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql)
    
    return qres

def del_exp_wtf(gch, entity, reader_id):
    sql = "DELETE FROM %s WHERE entity=?;" % (reader_id)
    
    cid = get_client_id()
    
    qres = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql, entity)
    
    return qres

def get_opened(gch, reader_id):
    cid = get_client_id()
    
    sql = 'SELECT * FROM %s ORDER BY last DESC;' % (reader_id)
    qres = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql)
    
    qres = clear_nex(gch, qres, reader_id)
    
    if qres:
        return qres
    else:
        return ''

def show_opened(gch, opli):
    nopli = []
    
    if opli:
        nopli = [l('%s) %s, page: %s of %s (chrs/pg: %s)') % (opli.index(oli) + 1, oli[0], oli[1], oli[3], oli[2]) for oli in opli if oli[1] != oli[3]]
        return nopli
    else:
        return ''
        
def get_rdr_wtf(gch, reader_id, entity):
    cid = get_client_id()
    
    sql = "SELECT * FROM %s WHERE entity=?;" % (reader_id)
    qres = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql, entity)
    
    if qres:
        return qres[0]
    else:
        return ''

def get_reader_id(gch, jid):
    cid = get_client_id()
    
    sql = "SELECT rid FROM readers WHERE jid=?;"
    reader_id = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql, jid)
    
    if reader_id:
        return reader_id[0][0]
    else:
        return ''

def save_pos(gch, jid, entity, last, part, spart, qop, reader_id=''):
    cid = get_client_id()
    
    if not reader_id:
        reader_id = 'reader%s' % (rand10())
        chk_rid = check_reader_id(gch, reader_id)
        
        while not chk_rid:
            reader_id = 'reader%s' % (rand10())
            chk_rid = check_reader_id(gch, reader_id)
        
        sql = "INSERT INTO readers (jid, rid) VALUES (?, ?);"
        
        res = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql, jid, reader_id)
        
        sql = '''CREATE TABLE %s(entity VARCHAR NOT NULL, 
                                 part VARCHAR NOT NULL, 
                                 spart VARCHAR NOT NULL, 
                                 qop VARCHAR NOT NULL, 
                                 last VARCHAR NOT NULL, 
                                 UNIQUE (entity));''' % (reader_id)
        
        res = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX i%s ON %s (entity);' % (reader_id, reader_id)
        sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql)
    
    sql = "SELECT * FROM %s WHERE entity=?" % (reader_id)
    res = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql, entity)
    
    if not res:
        sql = "INSERT INTO %s (entity, part, spart, qop, last) VALUES (?, ?, ?, ?, ?);" % (reader_id)
        args = entity, part, spart, qop, last
    else:
        sql = "UPDATE %s SET part=?, spart=?, qop=?, last=? WHERE entity=?;" % (reader_id)
        args = part, spart, qop, last, entity
    
    res = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql, *args)
    
    if res == '':
        sql = '''CREATE TABLE %s(entity VARCHAR NOT NULL, 
                                 part VARCHAR NOT NULL, 
                                 spart VARCHAR NOT NULL, 
                                 qop VARCHAR NOT NULL, 
                                 last VARCHAR NOT NULL, 
                                 UNIQUE (entity));''' % (reader_id)
        
        res = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX i%s ON %s (entity);' % (reader_id, reader_id)
        sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql)
        
        sql = "INSERT INTO %s (entity, part, spart, qop, last) VALUES (?, ?, ?, ?, ?);" % (reader_id)
        
        res = sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql, entity, part, spart, qop, last)

    return res
        
def get_part_list(entli, part, quantity):
    if not entli:
        return entli
    
    qtt = len(entli)
    
    if qtt <= quantity:
        qofparts = 1
        quantity = qtt
    else:
        qofparts = qtt // quantity
        isadparts = qtt % quantity
         
        if isadparts:
            qofparts += 1
            
    if part > qofparts:
        part = qofparts
    
    startind = part * quantity - quantity
    endind = part * quantity
    
    prtli = entli[startind:endind]
    
    return (prtli, part, quantity, qofparts, startind)		
        
def get_ent_list(gch):
    cid = get_client_id()
    
    sql = 'SELECT entity FROM defs ORDER BY entity;'
    qres = sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql)
    
    if qres:
        qres = [li[0] for li in qres]
        return qres
    else:
        return ''
        
def get_book_list(gch):
    cid = get_client_id()
    
    sql = "SELECT entity FROM defs WHERE author='книга' OR author='book' ORDER BY entity;"
    qres = sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql)
    
    if qres:
        qres = [li[0] for li in qres]
        return qres
    else:
        return ''
        
def get_part(gdef, part, spart=2000):
    if not gdef:
        return gdef
    
    gdef = gdef.encode('utf-8')
    
    qtt = len(gdef)
    
    if qtt <= spart:
        qofparts = 1
        spart = qtt
    else:
        qofparts = qtt // spart
        isadparts = qtt % spart
         
        if isadparts:
            qofparts += 1
            
    if part > qofparts:
        part = qofparts
    
    startind = part * spart - spart
    endind = part * spart
    
    if part == 1 and qofparts != part:
        endind = gdef.find(b' ', int(endind))
    elif part == 1 and qofparts == part:
        endind = qtt
    elif part == qofparts:
        startind = gdef.find(b' ', int(startind))
        endind = qtt
    else:
        startind = gdef.find(b' ', int(startind))
        endind = gdef.find(b' ', int(endind))
    
    opart = gdef[startind:endind]
    opart = opart.decode('utf-8')
    
    if len(opart) < spart:
        spart = len(opart)	
    
    return (opart.strip(), part, spart, qofparts, startind)

def add_def(gch, entity, gdef, author=''):
#-----------------------Local Functions----------------------------------------
    
    def filter_ent(entity):
        for chr in ["'", '"', '!', '?', '~', '`', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', '[', ']', '{', '}', '|', '\\', '/', ';', ':', '\'', '<', '>', '.']:
            entity = entity.replace(chr, '')
        
        return entity.lower()
        
#-----------------------End Of Local Functions---------------------------------

    ajid = get_user_jid(gch, author)

    if len(gdef) <= 255:
        dpath = gdef.encode('utf-8')
        if os.path.exists(dpath):
            if is_bot_admin(ajid):
                tmp_gdef = read_file(dpath.strip())
            
                if tmp_gdef.strip():
                    gdef = tmp_gdef.decode('utf-8')
                
                    if len(gdef) >= 50000:
                        author = 'book'
            else:
                return ('b', entity)
    
    entity = filter_ent(entity)
    
    action = ''
    
    if not check_entity(gch, entity):
        sql = "INSERT INTO defs (entity, def, author) VALUES (?, ?, ?);"
        action = 'a'
        args = entity.strip(), gdef.strip(), author
    else:
        sql = "UPDATE defs SET def=?, author=? WHERE entity=?;"
        action = 'u'
        args = gdef.strip(), author, entity.strip()
    
    cid = get_client_id()
    
    qres = sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql, *args)
    
    if qres != '':
        return (action, entity)
    else:	
        return qres
        
def del_def(gch, entity):
    cid = get_client_id()
    
    del_sql = "DELETE FROM defs WHERE entity=?;"

    qres = sqlquery('dynamic/%s/%s/def.db' % (cid, gch), del_sql, entity)

    return qres		
        
def get_def(gch, entity):
    cid = get_client_id()
    
    sql = "SELECT def, entity FROM defs WHERE entity LIKE ? ORDER BY entity LIMIT 1;"
    qres = sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql, '{}%'.format(entity))
    
    if qres:
        gdef = qres[0][0]
        entity = qres[0][1]
        
        return (gdef, entity)
    else:
        return ''
        
def get_rnd_def(gch):
    cid = get_client_id()
    
    sql = 'SELECT * FROM defs ORDER BY RANDOM() LIMIT 1;'
    qres = sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql)
    
    if qres:
        gdef = qres[0][0]
        entity = qres[0][1]
        author = qres[0][2]
        
        return (gdef, entity, author)
    else:
        return ''
        
def find_ent_def(gch, key):
    cid = get_client_id()
    
    sql = "SELECT entity FROM defs WHERE entity LIKE ? ORDER BY entity;"
    ent_res = sqlquery('dynamic/%s/%s/def.db', sql, '%{}%'.format(key))
    
    sql = "SELECT entity FROM defs WHERE def LIKE ? ORDER BY entity;"
    def_res = sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql, '%{}%'.format(key))
    
    ent_list = []
    def_list = []
    
    if ent_res:
        ent_list = [eli[0] for eli in ent_res if eli[0]]
        
    if def_res:
        def_list = [dli[0] for dli in def_res if dli[0]]	
    
    return (ent_list, def_list)

def get_wtf_state(gch):
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/def.db' % (cid, gch)):
        sql = 'CREATE TABLE defs(entity VARCHAR, def TEXT, author VARCHAR, UNIQUE (entity));'
        sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX idefs ON defs (entity);'
        sqlquery('dynamic/%s/%s/def.db' % (cid, gch), sql)
        
    if not is_db_exists('dynamic/%s/%s/readers.db' % (cid, gch)):
        sql = 'CREATE TABLE readers(jid VARCHAR, rid VARCHAR, UNIQUE (rid))'
        sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX ireaders ON readers (jid,rid);'
        sqlquery('dynamic/%s/%s/readers.db' % (cid, gch), sql)

def handler_wtf(type, source, parameters):
    groupchat = source[1]
    jid = get_true_jid(source)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        parameters = parameters.strip()
        parsepar = parameters.split(' ')
        parsepar.append(' ')
        
        part = parsepar[0]
        spart = parsepar[1]
        
        if not spart.isalpha() and spart[-1] == 'k':
            spart = int(spart[:-1]) * 1000
            spart = str(spart)
        elif not part.isalpha() and part[-1] == 'k':
            part = int(part[:-1]) * 1000
            part = str(part)
            
        if part.isdigit() and not spart.isdigit():
            part = int(part)
            spart = 2000			
            entity = parsepar[1:]
            entity = ' '.join(entity)
            entity = entity.strip()
        elif not part.isdigit() and not spart.isdigit():
            part = 1
            spart = 2000
            entity = ' '.join(parsepar)
            entity = entity.strip()
        else:
            if part.isdigit():
                part = int(part)
            else:
                part = 1
            
            if spart.isdigit():
                spart = int(spart)
            else:
                spart = 2000
                
            entity = parsepar[2:]
            entity = ' '.join(entity)
            entity = entity.strip()
        
        tdef = get_def(groupchat, entity)
        gdef = ''
        
        if tdef:
            gdef = tdef[0]
            entity = tdef[1]
        
        if gdef:
            prt = get_part(gdef, part, spart)
            
            reader_id = get_reader_id(groupchat, jid)
            
            if prt[3] > 1:
                save_pos(groupchat, jid, entity, trunc(time.time()), prt[1], spart, prt[3], reader_id)
            
            pref = ''
            suff = ''
            
            if prt[1] > 1:
                pref = '...] '
            if prt[1] != prt[3]:
                suff = ' [...'
            
            if pref or suff:
                rep = l('Article (title: %s; page: %s of %s): %s%s%s') % (entity, prt[1], prt[3], pref, prt[0], suff)
            else:
                rep = l('Article (title: %s): %s') % (entity, prt[0])

            return reply(type, source, rep)
        else:
            return reply(type, source, l('Article with title "%s" not found!') % (entity))
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_wtfp(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        if type == 'public':
            rep = handler_wtf('private', source, parameters)
            reply(type, source, l('Sent!'))
            return rep
        else:
            return handler_wtf(type, source, parameters)
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_prev(type, source, parameters):
    groupchat = source[1]
    jid = get_true_jid(source)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    decpart = 1
    reader_id = get_reader_id(groupchat, jid)
    last_wtf = get_last_wtf(groupchat, reader_id)
    
#-----------------------Local Functions--------------
    
    def out_part(groupchat, jid, entity, part, spart, reader_id, force=False, rnow=False):
        tdef = get_def(groupchat, entity)
        gdef = tdef[0]
        prt = get_part(gdef, part, spart)
        
        if prt[1] != 1 or force:
            save_pos(groupchat, jid, entity, trunc(time.time()), prt[1], spart, prt[3], reader_id)
        
        pref = ''
        suff = ''
        
        if prt[1] > 1:
            pref = '...] '
        if prt[1] != prt[3]:
            suff = ' [...'
        
        if not rnow:
            if pref or suff:
                rep = l('Article (title: %s; page: %s of %s): %s%s%s') % (entity, prt[1], prt[3], pref, prt[0], suff)
            else:
                rep = l('Article (title: %s): %s') % (entity, prt[0])
        else:
            if pref or suff:
                rep = '- %s/%s -\n%s%s%s\n- %s/%s -' % (prt[1], prt[3], pref, prt[0], suff, prt[1], prt[3])
            else:
                rep = l('Article (title: %s): %s') % (entity, prt[0])
        
        return rep
            
#-----------------------End Of Local Functions--------------
    
    if not last_wtf:
        return reply(type, source, l('Article is not specified!'))

    if parameters:
        spltdp = parameters.split(' ', 1)
        
        entity = ''
        
        if len(spltdp) >= 1:
            entstp = spltdp[0]
            
            if entstp.isdigit():
                decpart = int(entstp)
                
                if decpart <= 0:
                    decpart = 1
            else:
                entity = parameters
                
            if entity:
                if chk_rdr_ent(groupchat, entity, reader_id):
                    gwtf = get_rdr_wtf(groupchat, reader_id, entity)
                    
                    part = int(gwtf[1])
                    spart = int(gwtf[2])
                    rpos = int(gwtf[3])
                    
                    rep = out_part(groupchat, jid, entity, part, spart, reader_id, force=True)
                    return reply(type, source, rep)
                elif check_entity(groupchat, entity):
                    part = 1
                    spart = 2000
                    rpos = 0
                    
                    rep = out_part(groupchat, jid, entity, part, spart, reader_id)
                    return reply(type, source, rep)
                else:
                    return reply(type, source, l('Article with title "%s" not found!') % (entity))
            else:
                entity = last_wtf[0]
                
                part = int(last_wtf[1])
                prev_part = part - decpart
                
                if prev_part <= 0:
                    prev_part = 1

                spart = int(last_wtf[2])
                rpos = int(last_wtf[3])
                
                rep = out_part(groupchat, jid, entity, prev_part, spart, reader_id, rnow=True)
                return reply(type, source, rep)
        else:	
            return reply(type, source, l('Invalid syntax!'))
    else:
        entity = last_wtf[0]
        
        currtm = trunc(time.time())
        last = int(last_wtf[4])
        tmlong = currtm - last
        
        part = int(last_wtf[1])
        
        rnow = False
        
        if tmlong <= 900:
            rnow = True
            prev_part = part - decpart
        else:
            prev_part = part
        
        if prev_part <= 0:
            prev_part = 1
        
        spart = int(last_wtf[2])
        rpos = int(last_wtf[3])
        
        rep = out_part(groupchat, jid, entity, prev_part, spart, reader_id, rnow=rnow)
        return reply(type, source, rep)

def handler_next(type, source, parameters):
    groupchat = source[1]
    jid = get_true_jid(source)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    incpart = 1
    reader_id = get_reader_id(groupchat, jid)
    last_wtf = get_last_wtf(groupchat, reader_id)
    
#-----------------------Local Functions--------------
    
    def out_part(groupchat, jid, entity, part, spart, reader_id, force=False, rnow=False):
        tdef = get_def(groupchat, entity)
        gdef = tdef[0]
        prt = get_part(gdef, part, spart)
        
        if prt[3] != prt[1] or force:
            save_pos(groupchat, jid, entity, trunc(time.time()), prt[1], spart, prt[3], reader_id)
        else:
            del_exp_wtf(groupchat, entity, reader_id)
        
        pref = ''
        suff = ''
        
        if prt[1] > 1:
            pref = '...] '
        if prt[1] != prt[3]:
            suff = ' [...'
        
        if not rnow:
            if pref or suff:
                rep = l('Article (title: %s; page: %s of %s): %s%s%s') % (entity, prt[1], prt[3], pref, prt[0], suff)
            else:
                rep = l('Article (title: %s): %') % (entity, prt[0])
        else:
            if pref or suff:
                rep = '- %s/%s -\n%s%s%s\n- %s/%s -' % (prt[1], prt[3], pref, prt[0], suff, prt[1], prt[3])
            else:
                rep = l('Article (title: %s): %') % (entity, prt[0])
        
        return rep
            
#-----------------------End Of Local Functions--------------
    
    if not last_wtf:
        return reply(type, source, l('Article is not specified!'))

    if parameters:
        spltdp = parameters.split(' ', 1)
        
        entity = ''
        
        if len(spltdp) >= 1:
            entstp = spltdp[0]
            
            if entstp.isdigit():
                incpart = int(entstp)
                
                if incpart <= 0:
                    incpart = 1
            else:
                entity = parameters
                
            if entity:
                if chk_rdr_ent(groupchat, entity, reader_id) and check_entity(groupchat, entity):
                    gwtf = get_rdr_wtf(groupchat, reader_id, entity)
                    
                    part = int(gwtf[1])
                    spart = int(gwtf[2])
                    rpos = int(gwtf[3])
                    
                    rep = out_part(groupchat, jid, entity, part, spart, reader_id, force=True)
                    return reply(type, source, rep)
                elif check_entity(groupchat, entity):
                    part = 1
                    spart = 2000
                    rpos = 0
                    
                    rep = out_part(groupchat, jid, entity, part, spart, reader_id)
                    return reply(type, source, rep)
                else:
                    return reply(type, source, l('Article with title "%s" not found!') % (entity))
            else:
                entity = last_wtf[0]
                
                part = int(last_wtf[1])
                next_part = part + incpart
                
                spart = int(last_wtf[2])
                rpos = int(last_wtf[3])
                
                rep = out_part(groupchat, jid, entity, next_part, spart, reader_id, rnow=True)
                return reply(type, source, rep)
        else:	
            return reply(type, source, l('Invalid syntax!'))
    else:
        entity = last_wtf[0]
        
        currtm = trunc(time.time())
        last = int(last_wtf[4])
        tmlong = currtm - last
        
        part = int(last_wtf[1])
        
        rnow = False
        
        if tmlong <= 900:
            rnow = True
            next_part = part + incpart
        else:
            next_part = part
        
        spart = int(last_wtf[2])
        rpos = int(last_wtf[3])
        
        rep = out_part(groupchat, jid, entity, next_part, spart, reader_id, rnow=rnow)
        return reply(type, source, rep)

def handler_list(type, source, parameters):
    groupchat = source[1]
    jid = get_true_jid(source)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

#-----------------------Local Functions--------------

    def out_list(entli, part, quantity):
        if entli:
            prt = get_part_list(entli, part, quantity)
            elist = prt[0]
        
            pref = ''
            suff = '.'
            
            if prt[1] > 1:
                pref = '...] '
            if prt[1] != prt[3]:
                suff = ', [...'
            
            if pref or suff:
                rep = l('List of articles (displayed: %s of %s; page: %s of %s):\n\n%s%s%s') % (len(elist), len(entli), prt[1], prt[3], pref, ', '.join(elist), suff)
            else:
                rep = l('List of articles (total: %s):\n\n%s.') % (len(entli), ', '.join(elist))
        else:
            rep = l('There are no any articles!')
        
        return rep
            
#-----------------------End Of Local Functions--------------
    
    if parameters:
        parsepar = parameters.split(' ', 2)
        
        part = parsepar[0]
        quantity = ''
        
        if len(parsepar) == 2:
            quantity = parsepar[1]
        
        if len(parsepar) == 2 and part.isdigit() and quantity.isdigit():
            part = int(part)
            quantity = int(quantity)			
        elif len(parsepar) == 1 and part.isdigit():
            part = int(part)
            quantity = 50
        else:
            return reply(type, source, l('Invalid syntax!'))

        entli = get_ent_list(groupchat)
        
        rep = out_list(entli, part, quantity)
        return reply(type, source, rep)   
    else:
        entli = get_ent_list(groupchat)
        rep = out_list(entli, 1, 50)
        return reply(type, source, rep)

def handler_books(type, source, parameters):
    groupchat = source[1]
    jid = get_true_jid(source)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

#-----------------------Local Functions--------------

    def out_list(entli, part, quantity):
        if entli:
            prt = get_part_list(entli, part, quantity)
            elist = prt[0]
        
            pref = ''
            suff = '.'
            
            if prt[1] > 1:
                pref = '...] '
            if prt[1] != prt[3]:
                suff = ', [...'
            
            if pref or suff:
                rep = l('List of books (displayed: %s of %s; page: %s of %s):\n\n%s%s%s') % (len(elist), len(entli), prt[1], prt[3], pref, ', '.join(elist), suff)
            else:
                rep = l('List of books (total: %s):\n\n%s.') % (len(entli), ', '.join(elist))
        else:
            rep = l('There are no any books!')
        
        return rep
            
#-----------------------End Of Local Functions--------------
    
    if parameters:
        parsepar = parameters.split(' ', 2)
        
        part = parsepar[0]
        quantity = ''
        
        if len(parsepar) == 2:
            quantity = parsepar[1]
        
        if len(parsepar) == 2 and part.isdigit() and quantity.isdigit():
            part = int(part)
            quantity = int(quantity)			
        elif len(parsepar) == 1 and part.isdigit():
            part = int(part)
            quantity = 50
        else:
            return reply(type, source, l('Invalid syntax!'))

        entli = get_book_list(groupchat)
        
        rep = out_list(entli, part, quantity)
        return reply(type, source, rep)	
    else:
        entli = get_book_list(groupchat)
        rep = out_list(entli, 1, 50)
        return reply(type, source, rep)

def handler_stat(type, source, parameters):
    groupchat = source[1]
    jid = get_true_jid(source)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    reader_id = get_reader_id(groupchat, jid)
    opli = get_opened(groupchat, reader_id)

    if not parameters:
        if opli:
            nopli = show_opened(groupchat, opli)
            
            if nopli:
                rep = l('Opened books (total: %s):\n\n%s') % (len(nopli), '\n'.join(nopli))
            else:
                rep = l('There are no opened books!')
            
            return reply(type, source, rep)
        else:
            return reply(type, source, l('There are no opened books!'))
    else:
        bnum = parameters[1:]
        
        if not opli:
            return reply(type, source, l('There are no opened books!'))

        if bnum.isdigit() and parameters[0] == '-' and len(parameters) >= 2:
            if int(bnum) <= len(opli):
                dbki = int(bnum) - 1
                entity = opli[dbki][0]
                res = del_exp_wtf(groupchat, entity, reader_id)
                
                if res != '':
                    return reply(type, source, l('Book with title "%s" has been closed!') % (entity))
                else:
                    return reply(type, source, l('Unable to close this book!'))
            else:
                return reply(type, source, l('Invalid number of opened book!'))
        elif len(parameters) == 1 and parameters[0] == '-':
            res = clr_rdr_blist(groupchat, reader_id)
            
            if res != '':
                return reply(type, source, l('All opened books have been closed!'))
            else:
                return reply(type, source, l('Unable to close these books!'))
        else:
            return reply(type, source, l('Invalid syntax!'))
        
def handler_dfn(type, source, parameters):
    groupchat = source[1]
    nick = source[2]

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        parsepar = parameters.split('=', 1)
        
        if len(parsepar) == 2:
            entity = parsepar[0].strip()
            gdef = parsepar[1].strip()
            author = nick
            
            if not entity.strip():
                return reply(type, source, l('Article must have title!'))
            elif not gdef.strip():
                return reply(type, source, l('Article can not be empty!'))

            ent_len = len(entity.split())
            
            if ent_len <= 5:
                res = add_def(groupchat, entity, gdef, author)
                
                if res:
                    if res[0] == 'a':
                        rep = l('New article with title "%s" has been added!') % (res[1])
                    elif res[0] == 'u':
                        rep = l('Article with title "%s" has been updated!') % (res[1])
                    elif res[0] == 'b':
                        rep = l('Access denied! Only bot admins can add books!')
                else:
                    rep = l('Insert error!')
                    
                return reply(type, source, rep)
            else:
                return reply(type, source, l('Title of article must not be longer than five words!'))
        else:
            return reply(type, source, l('Invalid syntax!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
        
def handler_del(type, source, parameters):
    groupchat = source[1]

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        entity = parameters.strip()
        
        if check_entity(groupchat, entity):
            res = del_def(groupchat, entity)
        else:
            return reply(type, source, l('Article with title "%s" not found!') % (entity))

        if res != '':
            rep = l('Article with title "%s" has been removed!') % (entity)
        else:
            rep = l('Delete error!')
            
        return reply(type, source, rep)			
    else:
        return reply(type, source, l('Invalid syntax!'))
        
def handler_rnd(type, source, parameters):
    groupchat = source[1]
    jid = get_true_jid(source)
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if not parameters:
        res = get_rnd_def(groupchat)
        
        if res != '':
            entity = res[0]
            gdef = res[1]
            prt = get_part(gdef, 1, 2000)
            
            reader_id = get_reader_id(groupchat, jid)
            
            if prt[3] > 1:
                save_pos(groupchat, jid, entity, trunc(time.time()), prt[1], 2000, prt[3], reader_id)
            
            pref = ''
            suff = ''
            
            if prt[1] > 1:
                pref = '...] '
            if prt[1] != prt[3]:
                suff = ' [...'
            
            if pref or suff:
                rep = l('Random article (title: %s; page: %s of %s): %s%s%s') % (entity, prt[1], prt[3], pref, prt[0], suff)
            else:
                rep = l('Random article (title: %s): %s') % (entity, prt[0])
                
            return reply(type, source, rep)
        else:
            return reply(type, source, l('Unknown error!'))
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_find(type, source, parameters):
    groupchat = source[1]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        key = parameters.strip()
        ent_def_res = find_ent_def(groupchat, key)
        
        rep = ''
        
        ent_list = ent_def_res[0]
        def_list = ent_def_res[1]
        
        if ent_list:
            rep += l('Found in titles (total: %s): %s.') % (len(ent_list), ', '.join(ent_list))
            
        if def_list:
            rep += l('\n\nFound in articles (total: %s): %s') % (len(def_list), ', '.join(def_list))
            
        if rep:
            return reply(type, source, rep.strip())
        else:
            return reply(type, source, l('Nothing found!'))
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_search(type, source, parameters):
    groupchat = source[1]
    jid = get_true_jid(source)

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

#-----------------------Local Functions--------------
    
    def out_part(groupchat, jid, entity, pgdef, part, qofparts, reader_id):
        if qofparts != part:
            save_pos(groupchat, jid, entity, trunc(time.time()), part, 2000, qofparts, reader_id)
        
        pref = ''
        suff = ''
        
        if prt[1] > 1:
            pref = '...] '
        if prt[1] != prt[3]:
            suff = ' [...'
        
        if pref or suff:
            rep = l('Article (title: %s; page: %s of %s): %s%s%s') % (entity, part, qofparts, pref, pgdef, suff)
        else:
            rep = l('Article (title: %s): %s') % (entity, pgdef)
        
        return rep
            
#-----------------------End Of Local Functions--------------

    reader_id = get_reader_id(groupchat, jid)

    if parameters:
        parsepar = parameters.split(':', 1)
        
        if len(parsepar) == 2:
            entity = parsepar[0].strip()
            qstr = parsepar[1].strip()
                
            if qstr:
                if entity:
                    if check_entity(groupchat, entity):
                        tdef = get_def(groupchat, entity)
                        gdef = tdef[0]
                        prt = get_part(gdef, 1)
                        
                        qofparts = prt[3]
                        pgdef = prt[0]
                        pglist = []
                        
                        if pgdef.find(qstr) != -1:
                            pglist.append(1)
                        
                        pind = 2
                        prt = get_part(gdef, pind)
                        pgdef = prt[0]
                        
                        while pind != qofparts + 1:
                            if pgdef.find(qstr) != -1:
                                pglist.append(pind)
                            
                            pind += 1
                            prt = get_part(gdef, pind)
                            pgdef = prt[0]
                    
                        if pglist:
                            prt = get_part(gdef, pglist[0])
                            strpgli = [str(sli) for sli in pglist[1:]]
                            pgdef = prt[0]
                            
                            rep = out_part(groupchat, jid, entity, pgdef, prt[1], qofparts, reader_id)
                            
                            if strpgli:
                                rep += l('\n\nMatches also found on pages (total: %s): %s.') % (len(strpgli), ', '.join(strpgli))

                            return reply(type, source, rep.replace(qstr, ' -> %s <- ' % (qstr.upper())))
                        else:
                            return reply(type, source, l('Nothing found!'))
                    else:
                        return reply(type, source, l('Article with title "%s" not found!') % (entity))
                else:
                    return reply(type, source, l('Article is not specified!'))
            else:
                return reply(type, source, l('Search string is empty!'))
        else:
            return reply(type, source, l('Invalid syntax!'))
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_count(type, source, parameters):
    groupchat = source[1]

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    ent_count = get_ent_count(groupchat)
    
    if ent_count != 0:
        rep = l('Count of articles: %s.') % (ent_count)
    else:
        rep = l('There are no any articles!')
        
    return reply(type, source, rep)

def handler_get_wtf(type, source, parameters):
    groupchat = source[1]
    nick = source[2]

    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    if parameters:
        entity = parameters.strip()
        gdef = get_def(groupchat, entity)
        
        if gdef:
            data = gdef[0]
            entity = gdef[1]
        else:
            return reply(type, source, l('Article with title "%s" not found!') % (entity))
        
        to = get_user_jid(groupchat, nick)
        
        if not to:
            return reply(type, source, l('Internal error, unable to perform operation!'))
        
        sid = 'file%s' % (rand10())
        name = '%s.txt' % (sid)
        
        cid = get_client_id()
        
        fp = wr_op_file('dynamic/%s/%s' % (cid, name), data)
        
        bjid = get_client_id()
        resource = get_cfg_param('resource')
        
        frm = '%s/%s' % (bjid, resource)
        
        sireq = si_request(frm, to, sid, name, len(data), entity)
        
        jconn = get_client_conn()
        jconn.SendAndCallForResponse(sireq, handler_load_answ, args={'type': type, 'source': source, 'sid': sid, 'to': to, 'fp': fp})
    else:
        return reply(type, source, l('Invalid syntax!'))

@handle_xmpp_exc(quiet=True)
def handler_load_answ(coze, resp, type, source, sid, to, fp):
    rtype = resp.getType()
    groupchat = source[1]
    nick = source[2]
    
    if rtype == 'result':
        jconn = get_client_conn()
        jconn.IBB.OpenStream(sid, to, fp, 1024)
        check_stream(groupchat, nick, to, sid)
        
        name = fp.name
        os.remove(name)
    else:
        name = fp.name
        fp.close()
        os.remove(name)
        return reply(type, source, l('File transfer has failed!'))

register_command_handler(handler_wtf, 'wtf', 11)
register_command_handler(handler_wtfp, 'wtfp', 11)
register_command_handler(handler_next, 'next', 11)
register_command_handler(handler_prev, 'prev', 11)
register_command_handler(handler_list, 'list', 11)
register_command_handler(handler_books, 'books', 11)
register_command_handler(handler_stat, 'stat', 11)
register_command_handler(handler_dfn, 'dfn', 11)
register_command_handler(handler_del, 'del', 20)
register_command_handler(handler_rnd, 'rnd', 11)
register_command_handler(handler_find, 'find', 11)
register_command_handler(handler_search, 'search', 11)
register_command_handler(handler_count, 'count', 11)
register_command_handler(handler_get_wtf, 'get_wtf', 11)

register_stage1_init(get_wtf_state)
