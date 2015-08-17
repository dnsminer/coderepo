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
            line = " ( or { or // " + key + "\n more stuff \n" + str(val) + "} } \n"
            fh.write(line)
    except Exception as e:
        print "Unable to create view file in temp directory, please debug"
        print type(e)
        print str(e)
        return


    fh.close()
    return
