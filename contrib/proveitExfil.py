#!/usr/bin/env python
import dns.query
import dns.name
import dns.message
from dns.exception import DNSException
import sys, os, time, shutil, random
from random import randint
from time import sleep
from datetime import datetime
from datetime import date
from dm_modules import cfgparse_dm


DNSMinerHome='/opt/dnsminer-alpha'
#dbUtilsHome = DNSMinerHome + '/utils/databases/'
dbcfg= DNSMinerHome + "/etc/siteSpecific.cfg"
# DNS server path to be tested; provide at least one DNS server that the tester can reach, two or three recomended
dnstesters=['192.168.59.29','192.168.59.28']

# Define the random window
randlow = 25
randhigh = 624

def openrecordfile(filename):
    try:
        fh = open(filename,'r')
        linelist=fh.readlines()
    except Exception as e:
        print "Unable to read the record file, please debug, probably permissions"
        print type(e)
        print str(e)
        return
    fh.close()
    return linelist

def genrandhost(wfile):
    try:
        WORDS = open(wfile,'r').read().splitlines()
    except Exception as e:
        print "Unable to read the words list or problem with the file content, please debug"
    word = random.choice(WORDS)
    word = word + random.choice(WORDS)
    return word

def openlogfile(fname):
    try:
        fh = open(fname,'a')
    except Exception as e:
        print "Unable to create program logfile file in temp directory or problem with the file content, please debug"
        print type(e)
        print str(e)
    return fh

def getldns():
    # Generate some randomness by picking mulitple DNS servers
    thislist=dnstesters
    thisint = (randint(0,len(thislist) -1))
    thisns=thislist[thislist]
    return thisns


def genXfilTraffic(dlist,wlist):
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionThree')
    usertemp = thisCfgDict['dmtemp']
    plog = usertemp + "/proveitRPZ.log"
    thisfh = openlogfile(plog)
    RDTYPE=['A','MX','NS','A','A','AAAA','TXT','MX','A','A','A','AAAA','A','A']
    while True:

        ldns=getldns(thisint)
        thishost = genrandhost(wlist)

        fqdn = thishost + "." + thisdom
        domobj = dns.name.from_text(fqdn.strip())
        thisfh.write(logts() + ": Test_generated: " + fqdn + "\n")
        # Just going with A records for now,
        #randrd = 'dns.rdatatype.' + random.choice(RDTYPE)
        req = dns.message.make_query(domobj, dns.rdatatype.A, dns.rdataclass.IN)
        try:
            resp = dns.query.udp(req,ldns)
            if len(resp.answer) == 0:
                print " do it again "
                sleep(2)
                resp = dns.query.udp(req,ldns)
            if len(resp.answer) == 0:
                thisfh.write(logts() + ": Test_result: no response " + fqdn + "\n")
            else:
                respstr = str(resp.answer)
                thisfh.write(logts() + ": Test_result: " + respstr + "\n")
            print resp.answer
        except DNSException as ex:
            thisfh.write(logts() + ": Test_exception: " + ex + "\n")
            print ex
        sleep(randint(randlow,randhigh))
    thisfh.close()
    return

def logts():
    tsnow=time.time()
    tsstr = datetime.fromtimestamp(tsnow).strftime('%Y-%m-%d %H:%M:%S')
    return tsstr

def minInput():
    print "Enter the exfiltration domain name, domain and TLD only \n"
    xdom = raw_input("Eg testplace.info : ")
    print "Works best with one record per line, less that 200 chars per record"
    xdata = raw_input("Enter the file path for the test data,: ")
    minInputVals = [xdom,xdata]
    return minInputVals

def confMinInput(miList):
    print "\n\nconfirming paths to the record file"
    print "Test exfil records : " + miList[1]
    print "domain name used for testing : " + miList[0]
    testFilePath = isPathValid(miList[1])
    if not testFilePath:
        print "\n......... attention............"
        print "\ncan't find it eh, might want to double check, path to word list "
    return miList

def isPathValid(pathStr):
    TBool = os.path.isfile(pathStr)
    return TBool


def  main():
    MIConf='no'
    while MIConf=='no':
        thisList=minInput()
        confList=confMinInput(thisList)
        RI=raw_input("Are these settings correct (yes|no)?:")
        MIConf=str.lower(RI.strip())
    domlist=openrecordfile(confList[1])
    genXfilTraffic(confList[0],domlist)


if __name__ == "__main__": main()


