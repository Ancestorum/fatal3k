# -*- encoding: utf-8 -*-
# $Id: __init__.py,v 1.8.2.7.2.2 2011/03/23 01:42:07 customdesigned Exp $
#
# This file is part of the pydns project.
# Homepage: http://pydns.sourceforge.net
#
# Changes for Python3 port © 2011 Scott Kitterman <scott@kitterman.com>
#
# This code is covered by the standard Python License. See LICENSE for details.

# __init__.py for DNS class.

__version__ = '3.0.1'

from . import Type
from . import Opcode
from . import Status
from . import Class
from .Base import DnsRequest
from .Base import DNSError
from .Lib import DnsResult
from .Base import *
from .Lib import *
Error=DNSError
from .lazy import *
Request = DnsRequest
Result = DnsResult

Base._DiscoverNameServers()

#
# $Log: __init__.py,v $
# Revision 1.8.2.7.2.2  2011/03/23 01:42:07  customdesigned
# Changes from 2.3 branch
#
# Revision 1.8.2.7.2.1  2011/02/18 19:35:22  customdesigned
# Python3 updates from Scott Kitterman
#
# Revision 1.8.2.7  2009/06/09 18:05:29  customdesigned
# Release 2.3.4
#
# Revision 1.8.2.6  2008/08/01 04:01:25  customdesigned
# Release 2.3.3
#
# Revision 1.8.2.5  2008/07/28 02:11:07  customdesigned
# Bump version.
#
# Revision 1.8.2.4  2008/07/28 00:17:10  customdesigned
# Randomize source ports.
#
# Revision 1.8.2.3  2008/07/24 20:10:55  customdesigned
# Randomize tid in requests, and check in response.
#
# Revision 1.8.2.2  2007/05/22 21:06:52  customdesigned
# utf-8 in __init__.py
#
# Revision 1.8.2.1  2007/05/22 20:39:20  customdesigned
# Release 2.3.1
#
# Revision 1.8  2002/05/06 06:17:49  anthonybaxter
# found that the old README file called itself release 2.2. So make
# this one 2.3...
#
# Revision 1.7  2002/05/06 06:16:15  anthonybaxter
# make some sort of reasonable version string. releasewards ho!
#
# Revision 1.6  2002/03/19 13:05:02  anthonybaxter
# converted to class based exceptions (there goes the python1.4 compatibility :)
#
# removed a quite gross use of 'eval()'.
#
# Revision 1.5  2002/03/19 12:41:33  anthonybaxter
# tabnannied and reindented everything. 4 space indent, no tabs.
# yay.
#
# Revision 1.4  2001/11/26 17:57:51  stroeder
# Added __version__
#
# Revision 1.3  2001/08/09 09:08:55  anthonybaxter
# added identifying header to top of each file
#
# Revision 1.2  2001/07/19 06:57:07  anthony
# cvs keywords added
#
#
