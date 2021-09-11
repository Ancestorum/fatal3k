"""
 $Id: Opcode.py,v 1.6.4.2 2011/03/23 01:42:07 customdesigned Exp $

 This file is part of the pydns project.
 Homepage: http://pydns.sourceforge.net

 This code is covered by the standard Python License. See LICENSE for details.

 Opcode values in message header. RFC 1035, 1996, 2136.
"""



QUERY = 0
IQUERY = 1
STATUS = 2
NOTIFY = 4
UPDATE = 5

# Construct reverse mapping dictionary

_names = dir()
opcodemap = {}
for _name in _names:
    if _name[0] != '_': opcodemap[eval(_name)] = _name

def opcodestr(opcode):
    if opcode in opcodemap: return opcodemap[opcode]
    else: return repr(opcode)

#
# $Log: Opcode.py,v $
# Revision 1.6.4.2  2011/03/23 01:42:07  customdesigned
# Changes from 2.3 branch
#
# Revision 1.6.4.1  2011/02/18 19:35:22  customdesigned
# Python3 updates from Scott Kitterman
#
# Revision 1.6  2002/04/23 10:51:43  anthonybaxter
# Added UPDATE, NOTIFY.
#
# Revision 1.5  2002/03/19 12:41:33  anthonybaxter
# tabnannied and reindented everything. 4 space indent, no tabs.
# yay.
#
# Revision 1.4  2002/03/19 12:26:13  anthonybaxter
# death to leading tabs.
#
# Revision 1.3  2001/08/09 09:08:55  anthonybaxter
# added identifying header to top of each file
#
# Revision 1.2  2001/07/19 06:57:07  anthony
# cvs keywords added
#
#
