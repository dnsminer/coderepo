#!/usr/bin/env python
#__author__ = 'dleece'
import sys

#FEFQDN=""
#FEPORT=""
#SSLCertPath=""
MIConf="no"
def minInput():
    FEFQDN = raw_input("Enter the FQDN for the Find Evil server, EG fe2.dnsminer.net: ")
    FEPort = raw_input("Enter the logstash receiver TCP/IP port, EG  2112: ")
    print "Enter the path to the SSL public cert copied from FE server"
    SSLCertPath = raw_input( "EG, /var/lib/logstash-forwarder/keys/fePub.crt : ")
    minInputVals = [FEFQDN,FEPort,SSLCertPath]
    return minInputVals

def confMinInput(miList):
    print "confirm settings"
    print "FQDN of Find Evil server: " + miList[0]
    print "TCP/IP port for Logstash on FE server: " + miList[1]
    print "The full path to the FE public SSL cert: " + miList[2]


while True:
    if MIConf=='yes':
        break
    thisList=minInput()
    confMinInput(thisList)
    RI=raw_input("Are these settings correct?  yes/no:")
    MIConf=str.lower(RI.strip())
