#!/usr/bin/env python
#__author__ = 'dleece'
import sys, os, time, shutil

# Vars used through out the program
FEFQDN=""
FEPort=""
SSLCertPath=""
MIConf="no"

# functions
def minInput():
    FEFQDN = raw_input("Enter the FQDN for the Find Evil server, EG fe2.dnsminer.net: ")
    FEPort = raw_input("Enter the logstash receiver TCP/IP port, EG  2112: ")
    print "Enter the path to the SSL public cert copied from FE server"
    SSLCertPath = raw_input( "EG, /var/lib/logstash-forwarder/fePub.crt : ")
    minInputVals = [FEFQDN,FEPort,SSLCertPath]
    return minInputVals

def confMinInput(miList):
    print "\n\nconfirm settings"
    print "FQDN of Find Evil server: " + miList[0]
    print "TCP/IP port for Logstash on FE server: " + miList[1]
    print "The full path to the FE public SSL cert: " + miList[2]
    testFilePath = isPathValid(miList[2])
    if not testFilePath:
        print "\n......... attention............"
        print "\nhmm, might want to double check, path to SSL cert may not be correct"
    return miList

def confDQPath():
    # This tests for default location of the pitboss query log, alerts if missing and
    # gives admin options to correct.  Teh logstash forwarder config file can also be
    # manually edited if that is preferential or the config program is buggy.
    #
    # This is the correct path the logfile if the logging inclusion statement was added
    # to the named.conf file
    DQPath='/var/log/named/dnsQueries.log'
    DQLogs = isPathValid(DQPath)
    while DQLogs is False:
        print "\n......... attention............"
        print "\nhmm, the DNS query logs are usually here: "
        print "/var/log/named/dnsQueries.log"
        inqDNSRun = raw_input("Is DNS running and writing logs (yes|no)?:")
        if inqDNSRun.strip(str.lower()) == 'yes':
            print " might want to double check the path and file permissions"
            DQPath = raw_input( "Enter the path to the DNS query logs please : ")
            DQPath = DQPath.strip()
            DQLogs = isPathValid(DQPath)
        if inqDNSRun.strip(str.lower()) == 'no':
            DQPath = raw_input( "No problem, just enter the path to the DNS query logs please : ")
            DQPath = DQPath.strip()
            # Fake out the test for file path,
            DQLogs = True
    if DQLogs:
        confList.append(DQPath)

def confPDNSPath():
    # This tests for default location of the pitboss query log, alerts if missing and
    # gives admin options to correct.  Teh logstash forwarder config file can also be
    # manually edited if that is preferential or the config program is buggy.
    #
    #This is the correct path if Bro was installed from source using default config settings
    PDNSPath = '/usr/local/bro/logs/current/dns.log'
    PDNSLogs = isPathValid(PDNSPath)
    while PDNSLogs is False:
        print "\n......... attention............"
        print "\nhmm, the Passive DNS response logs are usually here: "
        print "/usr/local/bro/logs/current/dns.log"
        inqPDNSRun = raw_input("Is Bro running and writing logs (yes|no)?:")
        if inqPDNSRun.strip(str.lower()) == 'yes':
            print " might want to double check the path and file permissions"
            PDNSPath = raw_input( "Enter the path to the current Bro DNS log please : ")
            PDNSPath = PDNSPath.strip()
            PDNSLogs = isPathValid(PDNSPath)
        if inqPDNSRun.strip(str.lower()) == 'no':
            PDNSPath = raw_input( "No problem, just enter the path to the current Bro DNS log please : ")
            PDNSPath = PDNSPath.strip()
            # Fake out the test for file path,
            PDNSLogs = True
    if PDNSLogs:
        confList.append(PDNSPath)


def isPathValid(pathStr):
    TBool = os.path.isfile(pathStr)
    return TBool

def genConfig(valList):
    # current file location when installing package from elastic search
    CFG = '/etc/logstash-forwarder.conf'
    CFGOrig = '/etc/logstash-forwarder.conf-pkgOrig'
    if isPathValid(CFG):
        try:
            shutil.move(CFG,CFGOrig)
            print "Package config backed up to " + CFGOrig
        except:
            print " unable to move file"
            cStatus = "Check file permissions"
    # Rather than mess with the package version which could change over time just write from scratch
    CFGfh = open(CFG,'a')
    #
    wline = "{\n"
    wline = wline + "  \"network\": {\n"
    wline = wline + "    \"servers\": [ \"" + valList[0] + ":" + valList[1] +"\" ],\n"
    wline = wline + "    \"ssl ca\": \"" + valList[2] + "\",\n"
    wline = wline + "    \"timeout\": 15\n  },\n\n"
    CFGfh.write(wline)
    # break it in two for debugging
    wline = "  \"files\": [\n{\n"
    wline = wline + "  \"paths\": [\n"
    wline = wline + "    \"" + valList[3] +"\"\n    ],\n"
    wline = wline + "  \"fields\": { \"type\": \"DNSQRYPBOSS\" }\n},\n"
    CFGfh.write(wline)
    wline = "{\n"
    wline = wline + "  \"paths\": [\n"
    wline = wline + "    \"/usr/local/bro/spool/bro/dns.log\"\n"
    wline = wline + "  ],\n"
    wline = wline + "  \"fields\": { \"type\": \"PDNS\" }\n}\n"
    wline = wline + "  ]\n}"
    CFGfh.write(wline)
    CFGfh.close()
    if isPathValid(CFG):
        cStatus = 'the new Logstash forwarder config file is good to go, \n make sure you have log files before starting the forwarder\n'
    else:
        cStatus = ' Sorry, something seems to have gone wrong in the config creation, maybe manually editing is needed\n'
    return cStatus

### main
while True:
    thisList = []
    if MIConf=='yes':
        FEFQDN=confList[0]
        FEPort=confList[1]
        SSLCertPath=confList[2]
        break
    thisList=minInput()
    confList=confMinInput(thisList)
    RI=raw_input("Are these settings correct (yes|no)?:")
    MIConf=str.lower(RI.strip())

# confirm the paths to the log files being monitored
confDQPath()
confPDNSPath()
# assuming all went well above should have enough to write a config file that works
if len(confList)==5:
    print "Good job eh,\nlooks like all the config data is in place"
    for items in confList:
        print items
    print " Generating a replacement /etc/logstash-forwarder.conf file"
    status=genConfig(confList)
    print status

else :
    print "We seem to be missing some config data, please rerun or edit the logstash-forwarder.conf file manually"
    time.sleep(5)
    exit()