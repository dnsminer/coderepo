__author__ = 'dleece'
# Takes a dictionary of values and writes teh config file out line by line. complex values are passed to functions
# to create rather than deal with hard coding. also allows functions to be fixed when bugs are found

import random,string,base64
DNSMinerHome='/opt/dnsminer-alpha'
tempdir = DNSMinerHome + "/tmp/"

def gentsigcontents(thisorgdict):
    #debug
    #for key,val in thisorgdict.iteritems():
    #    print key,"-->",val
    thislist=[]
    vfileline = "key " + thisorgdict['tsig_name'] + " {"
    thislist.append(vfileline)
    vfileline="\talgorithm hmac-sha256;"
    thislist.append(vfileline)
    vfileline= "\tsecret \"" + gensharedsecret(27) + "\";"
    thislist.append(vfileline)
    vfileline="};"
    # prep for file creation
    vfile = thisorgdict['tsig_name'] + ".tsig"
    thisfile = tempdir + vfile
    # debug
    print thisfile
    writetsigfile(thisfile,thislist)
    return

def gensharedsecret(intlen):
    trand = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(intlen))
    thissharedsec = base64.b64decode(trand)
    return thissharedsec



def writetsigfile(filename,linelist):
    try:
        fh = open(filename,'w')
        for line in linelist:
            line = line + "\n"
            fh.write(line)
    except Exception as e:
        print "Unable to create view file in temp directory or problem with the file content, please debug"
        print type(e)
        print str(e)
        return
    fh.close()
    return