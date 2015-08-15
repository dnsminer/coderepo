__author__ = 'dleece'

import socket
import struct

def intTodotQuad(ipint):
    dotquad = socket.inet_ntoa(struct.pack('>L',ipint))
    return  dotquad