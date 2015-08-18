__author__ = 'dleece'
# Takes a dictionary of values and writes teh config file out line by line. complex values are passed to functions
# to create rather than deal with hard coding. also allows functions to be fixed when bugs are found

DNSMinerHome='/opt/dnsminer-alpha'
tempdir = DNSMinerHome + "/tmp/"

import datetime

def readDict(thisorgdict):
    #debug
    #for key,val in thisorgdict.iteritems():
    #    print key,"-->",val
    thislist=[]
    vfileline = "; This zone is needed to leverage CNAME capability in RPZ, TLD and host are random for opsec\n;"
    thislist.append(vfileline)
    vfileline = "$ORIGIN " +  thisorgdict['sh_zone'] + ".\n"
    thislist.append(vfileline)
    vfileline="$TTL\t1800\t; thirty  minutes to allow for more query data to be recorded"
    thislist.append(vfileline)
    vfileline="@\tIN\tSOA\tmineboss.dnsminer.net. info.dnsminer.net. ("
    thislist.append(vfileline)
    vfileline="\t\t\t" + mkserial(1) + "\t; serial"
    thislist.append(vfileline)
    vfileline="\t\t\t28800\t; refresh 8 hours"
    thislist.append(vfileline)
    vfileline="\t\t\t7200\t; retry 2 hours"
    thislist.append(vfileline)
    vfileline="\t\t\t864000\t; expire 10 days"
    thislist.append(vfileline)
    vfileline="\t\t\t86400 )\t; min ttl 1 day"
    thislist.append(vfileline)
    vfileline="; resource records"
    thislist.append(vfileline)
    vfileline="\t\t\tIN\tNS\tmineboss.dnsminer.net."
    thislist.append(vfileline)
    vfileline="\t\t\tIN\tA\t10.42.42.42"
    thislist.append(vfileline)
    vfileline = getlzonehost(thisorgdict['sh_fqdn']) +"\t\tIN\tA\t" + thisorgdict['sh_ip']
    thislist.append(vfileline)
    # close the zone file
    vfileline="; End " + thisorgdict['sh_zone'] + " zone file"
    thislist.append(vfileline)
    # prep for file creation
    vfile = thisorgdict['sh_zone']
    thisfile = tempdir + vfile
    # debug
    print thisfile
    writezonefile(thisfile,thislist)
    return

def mkserial(sint):
    todate=datetime.date.today()
    serialstr=str(todate.year) + str(todate.month) + str(todate.day)
    # add 10 to avoid dealing with leading 0 being lost
    zoneversion = 10 + sint
    serialstr = serialstr + str(zoneversion)
    return serialstr

def getlzonehost(fqdn):
    fqdnlist=fqdn.split('.')
    return fqdnlist[0]

def writezonefile(filename,linelist):
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