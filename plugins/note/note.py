# -*- coding: utf-8 -*-

#  fatal plugin
#  note plugin

#  Copyright © 2009-2013 Ancestors Soft

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

def get_note_jid(gch, nick):
    cid = get_client_id()
    
    nick = nick.replace('"', '&quot;')
    sql = "SELECT jid FROM users WHERE nick='%s';" % (nick)
    qres = sqlquery('dynamic/%s/%s/users.db' % (cid, gch), sql)
    
    if qres:
        jid = qres[0][0]
        return jid
        
def show_notes(gch, notes, pref='', miff='', start=0, end=10):
    rng = []
    
    if notes:
        if start == 0 and end == 10:
            if len(notes) >= 10:
                rng = list(range(10))
            else:
                rng = list(range(len(notes)))
        else:
            rng = list(range(end - start))
        
    nosli = ['%s) %s%s%s%s:\n%s' % (li + start + 1, pref, time.strftime('%d.%m.%Y', time.localtime(float(notes[li + start][0]))), miff, time.strftime('%H:%M:%S', time.localtime(float(notes[li + start][0]))), notes[li + start][1].replace('&quot;', '"')) for li in rng]
            
    return nosli
    
def del_note(gch, notes_id, note):
    del_sql = "DELETE FROM %s WHERE note='%s';" % (notes_id, note)
    
    cid = get_client_id()
    
    res = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), del_sql)
    
    return res
    
def delall_notes(gch, notes_id):
    drop_sql = 'DROP TABLE %s;' % (notes_id)
    
    cid = get_client_id()
    
    res = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), drop_sql)
    
    return res

def get_notes(gch, notes_id):
    cid = get_client_id()
    
    sql = 'SELECT * FROM %s ORDER BY ndate DESC;' % (notes_id)
    notes = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
    return notes

def check_notes_id(gch, notes_id):
    cid = get_client_id()
    
    sql = "SELECT * FROM notes WHERE id='%s';" % (notes_id)
    qres = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
    
    if qres:
        return False
    else:
        return True	
    
def get_notes_id(gch, jid):
    cid = get_client_id()
    
    sql = "SELECT id FROM notes WHERE jid='%s';" % (jid)
    notes_id = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
    
    if notes_id:
        return notes_id[0][0]

def note_add(gch, jid, note, notes_id=''):
    cid = get_client_id()
    
    if not notes_id:
        notes_id = 'notes%s' % (random.randrange(10000000, 99999999))
        chk_ntsid = check_notes_id(gch, notes_id)
        
        while not chk_ntsid:
            notes_id = 'notes%s' % (random.randrange(10000000, 99999999))
            chk_ntsid = check_notes_id(gch, notes_id)
        
        sql = "INSERT INTO notes (jid,id) VALUES ('%s','%s');" % (jid, notes_id)
        
        res = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
    
        sql = 'CREATE TABLE %s (ndate varchar not null, note varchar not null, unique(note));' % (notes_id)
        
        res = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX i%s ON %s (note);' % (notes_id, notes_id)
        sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
    
    note = note.replace(r'"', r'&quot;')
    date = time.time()
    
    sql = "INSERT INTO %s (ndate,note) VALUES ('%s','%s');" % (notes_id, date, note)
    
    res = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
    
    if res == '':
        sql = 'CREATE TABLE %s (ndate varchar not null, note varchar not null, unique(note));' % (notes_id)
        
        res = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX i%s ON %s (note);' % (notes_id, notes_id)
        sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
        
        sql = "INSERT INTO %s (ndate,note) VALUES ('%s','%s');" % (notes_id, date, note)
        
        res = sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)

    return res

def get_note_state(gch):
    cid = get_client_id()
    
    if not is_db_exists('dynamic/%s/%s/notes.db' % (cid, gch)):
        sql = 'CREATE TABLE notes (jid varchar not null, id varchar not null, unique(jid,id));'
        sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)
        
        sql = 'CREATE UNIQUE INDEX inotes ON notes (jid,id);'
        sqlquery('dynamic/%s/%s/notes.db' % (cid, gch), sql)

def handler_notes(type, source, parameters, recover=False, jid='', rcts=''):
    groupchat = source[1]
    nick = source[2]
    
    if not is_groupchat(groupchat):
        return reply(type, source, l('This command can be used only in groupchat!'))

    jid = get_note_jid(groupchat, nick)
    
    notes_id = get_notes_id(groupchat, jid)
    notes = get_notes(groupchat, notes_id)
    tonos = len(notes)

#-----------------------Local Functions--------------

    def add_note(type, source, groupchat, jid, parameters, notes_id):
        res = note_add(groupchat, jid, parameters, notes_id)
        
        if res != '':
            return reply(type, source, l('Note has been added!'))
        else:
            return reply(type, source, l('Insert error! May be this note already exists!'))
            
    def out_notes(type, source, groupchat, notes, tonos, stn, enn):
        notl = show_notes(groupchat, notes, l('Added') + ' ', ' ' + l('at') + ' ', stn - 1, enn)		

        head = ''
        foot = ''	
                
        if stn >= 2 and stn != enn:
            head = l('[<---start---]\n\n')
        
        if enn < tonos and stn != enn:
            foot = l('\n\n[---end--->]')
        elif enn == tonos and tonos == 10:
            foot = ''
        
        if notl:
            if type == 'public':
                if stn == enn:
                    rep = l('Note (total: %s):\n\n%s%s%s') % (tonos, head, '\n\n'.join(notl), foot)
                else:
                    rep = l('Notes (total: %s):\n\n%s%s%s') % (tonos, head, '\n\n'.join(notl), foot)
                
                reply(type, source, l('Look in private!'))
                
                return reply('private', source, rep)
            else:
                if stn == enn:
                    rep = l('Note (total: %s):\n\n%s%s%s') % (tonos, head, '\n\n'.join(notl), foot)
                else:
                    rep = l('Notes (total: %s):\n\n%s%s%s') % (tonos, head, '\n\n'.join(notl), foot)
                    
                return reply(type, source, rep)
        else:
            return reply(type, source, l('There are no notes!'))

#--------------------End Of Local Functions----------

    if parameters:
        spltdp = parameters.split(' ', 1)
        nnote = spltdp[0]
        
        if len(spltdp) == 1:
            if '-' in nnote:
                nnote = nnote.split('-', 1)
                nnote = rmv_empty_items(nnote)
                
                if len(nnote) == 2:
                    if nnote[0].isdigit():
                        stn = int(nnote[0])
                        
                        if not stn:
                            return add_note(type, source, groupchat, jid, parameters, notes_id)
                    else:
                        return add_note(type, source, groupchat, jid, parameters, notes_id)
                    
                    if nnote[1].isdigit():
                        enn = int(nnote[1])
                        
                        if enn > tonos:
                            return add_note(type, source, groupchat, jid, parameters, notes_id)
                    else:
                        return add_note(type, source, groupchat, jid, parameters, notes_id)
                    
                    if stn > enn:
                        return add_note(type, source, groupchat, jid, parameters, notes_id)
                    
                    return out_notes(type, source, groupchat, notes, tonos, stn, enn)	
                elif len(nnote) == 1:
                    if nnote[0].isdigit():
                        nno = int(nnote[0])
                        
                        if nno > tonos or nno == 0:
                            return add_note(type, source, groupchat, jid, parameters, notes_id)

                        note = notes[nno - 1][1].strip()
                        res = del_note(groupchat, notes_id, note)
                        
                        if res != '':
                            return reply(type, source, l('Note number %s has been deleted!') % (nno))
                        else:
                            return reply(type, source, l('Delete error!'))
                    else:
                        return add_note(type, source, groupchat, jid, parameters, notes_id)	
                elif not nnote:
                    delall_notes(groupchat, notes_id)
                    return reply(type, source, l('All notes has been removed!'))
            else:
                if nnote.isdigit():
                    if int(nnote) != 0 and int(nnote) <= tonos:
                        nnote = int(nnote)
                        
                        return out_notes(type, source, groupchat, notes, tonos, nnote, nnote)	
                    else:
                        return add_note(type, source, groupchat, jid, parameters, notes_id)
                else:
                    return add_note(type, source, groupchat, jid, parameters, notes_id)
        else:
            return add_note(type, source, groupchat, jid, parameters, notes_id)
    else:
        return out_notes(type, source, groupchat, notes, tonos, 1, 10)

register_stage1_init(get_note_state)

register_command_handler(handler_notes, 'note', 11)
