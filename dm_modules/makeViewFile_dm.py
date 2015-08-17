__author__ = 'dleece'


DNSMinerHome='/opt/dnsminer-alpha'
tempdir = DNSMinerHome + "/tmp/"

def readDict(thisorgdict):
    for key,val in thisorgdict.iteritems():
        print key,"-->",val
        vfile = thisorgdict['view_name'] + ".view"

    thisfh= getfilehandle(vfile)
    for key,val in thisorgdict.iteritems():
        line = " ( or { or // " + key + " more stuff \n" + val + "} } \n"
        thisfh.write(line)
    thisfh.close()
    return

def getfilehandle(fname):
    thisfile = tempdir + fname
    try:
        fh = open(thisfile,'w')
    except:
        print "Unable to create view file in temp directory, please debug"
        return fh