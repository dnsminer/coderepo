#__author__ = 'dleece'
import  string
import re

def inputSanitizer(inputstring,type):
    # sanitize based on whitelist and what type of input we're expecting
    charwl = string.ascii_letters + string.whitespace + string.digits
    if type == 'emailstring':
        charwl = charwl + '@._-'
        chkdstring = checkwhitelist(inputstring,charwl)
    if type ==  'password':
        charwl = string.printable
        chkdstring = checkwhitelist(inputstring,charwl)
    if type == 'view':
        charwl = string.ascii_letters + string.digits + '-_'
        chkdstring = checkwhitelist(inputstring,charwl)
    if type == 'ip':
        v4pat = re.compile(('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'))
        chkv4pat = v4pat.match(inputstring)
        if not chkv4pat:
            print "Invalid IP address, please redo"
            chkdstring = 'invalid_format'
    if type == 'cidr':
        v4pat = re.compile(('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}'))
        chkv4pat = v4pat.match(inputstring)
        if not chkv4pat:
            print "Invalid CIDR address, please redo"
            chkdstring = 'invalid_format'

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
