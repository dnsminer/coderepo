__author__ = 'dleece'


DNSMinerHome='/opt/dnsminer-alpha'
tempdir = DNSMinerHome + "/tmp/"

def readDict(thisorgdict):
    for key,val in thisorgdict.iteritems():
        print key,"-->",val
        vfile = thisorgdict['view_name'] + ".view"

    thisfile = tempdir + vfile
    print thisfile
    try:
        fh = open(thisfile,'w')
        #thisfh= getfilehandle(vfile)
        for key,val in thisorgdict.iteritems():
            line = " ( or { or // " + key + " more stuff \n" + val + "} } \n"
            fh.write(line)
    except:
        print "Unable to create view file in temp directory, please debug"
        return


    fh.close()
    return
