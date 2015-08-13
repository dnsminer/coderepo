#__author__ = 'dleece'
import  string

def inputSanitizer(inputstring,type):
    # sanitize based on whitelist and what type of input we're expecting
    charwl = string.ascii_letters + string.whitespace + string.digits
    if type == 'emailstring':
        charwl = charwl + '@._-'
    if type ==  'password':
        charwl = string.printable
    if type == 'view':
        charwl = string.ascii_letters + string.digits + '-_'

    outstring = inputstring.strip()
    tmpchar=''
    for tchar in outstring:
        if tchar not in charwl:
            print "replacing invalid character " + tchar + " with an underscore _ "
            tchar = '_'
        tmpchar = tmpchar + tchar
    outstring = tmpchar
    return outstring
