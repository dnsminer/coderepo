#!/usr/bin/env python
#__author__ = 'dleece'
import sys, os

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
    print "confirm settings"
    print "FQDN of Find Evil server: " + miList[0]
    print "TCP/IP port for Logstash on FE server: " + miList[1]
    print "The full path to the FE public SSL cert: " + miList[2]
    testFilePath = isPathValid(miList[2])
    if not testFilePath:
        print "......... attention............"
        print "hmm, might want to double check, path to SSL cert may not be correct"
    return miList

def isPathValid(pathStr):
    TBool = os.path.isfile(pathStr);
    return TBool

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
