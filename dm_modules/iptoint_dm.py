#__author__ = 'dleece'
# slight kludge to deal with invalid IP addresses, print out a message and retunr an integer that makes no sense,
# then test for greater than 10 before using.  Fastest way to handle prior to in database insert.

import socket
import struct

def dotQuadtoInt(dquad):
    dquad = inputSani_dm.inputSanitizer(dquad,'ip')
    if dquad =='invalid_format':
        ipInt = 10
    else:
        ipInt = struct.unpack('>L',socket.inet_aton(dquad))[0]
    return  ipInt