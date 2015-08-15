#__author__ = 'dleece'
import  string
import re
import socket

def inputSanitizer(inputstring,type):
    # sanitize based on whitelist and what type of input we're expecting
    chkdstring = 'invalid_format'
    charwl = string.ascii_letters + string.whitespace + string.digits
    if type == 'emailstring':
        charwl = charwl + '@._-'
        chkdstring = checkwhitelist(inputstring,charwl)
    if type ==  'password':
        charwl = string.printable
        chkdstring = checkwhitelist(inputstring,charwl)
    if type == 'desc1':
        if len(inputstring) > 80:
            print "Description too long, please abbreviate"
        else:
            charwl = string.ascii_letters + string.whitespace + string.digits + '-_.,'
            chkdstring = checkwhitelist(inputstring,charwl)
    if type == 'view':
        charwl = string.ascii_letters + string.digits + '-_'
        chkdstring = checkwhitelist(inputstring,charwl)
    if type == 'ip':
        print "testing IP" + inputstring
        testres = checkIPsock(inputstring)
        if testres:
            chkdstring = inputstring
        else:
            print "Invalid IP address, please redo"
    if type == 'cidr':
        print "testing cidr"
        ipipmask = inputstring.split('/')
        testres = checkIPsock(ipipmask[0])
        testmask = int(ipipmask[1])
        if  testres and testmask < 33 and testmask > 0 :
            chkdstring = inputstring
        else:
            print "Invalid IP address or subnet mask, please redo"

        # do some ip regex check

    return chkdstring

def checkwhitelist(istring,wl):
    outstring = istring.strip()
    tmpchar=''
    for tchar in outstring:
        if tchar not in wl:
            print "replacing invalid character " + tchar + " with an underscore _ "
            tchar = '_'
        tmpchar = tmpchar + tchar
    outstring = tmpchar
    return outstring

def checkIPsock(addr):
    try:
        socket.inet_aton(addr)
        return True
    except:
        return False