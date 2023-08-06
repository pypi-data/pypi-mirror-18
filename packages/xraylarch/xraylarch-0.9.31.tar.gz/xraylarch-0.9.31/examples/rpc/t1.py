#!/usr/bin/env python

import xmlrpclib
import time
import json
from larch.utils.jsonutils import decode4js
s = xmlrpclib.ServerProxy('http://127.0.0.1:4966')

print 'Avaialable Methods from XML-RPC server: ', s.system.listMethods()
print s.system.methodHelp('dir')

#s.larch('m = 222.3')

# s.larch('g = group(x=linspace(0, 10, 11))')
# s.larch('g.z = cos(g.x)')

# show and print will be done in server process of course!!!
s.larch('show(g)')
# s.larch('show(_main)')

# s.larch('print g.z[3:10]')

# print '== Messages:'
# print s.get_messages()
# print '=='

# print("hello ")


gx  = decode4js(s.get_data('g.z'))
print 'm = ', s.get_data('m')
print 'x = ', s.get_data('x')

print 'gx = ',  gx, type(gx), gx.dtype

# could tell server to exit!
# s.exit()
