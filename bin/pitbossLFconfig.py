#!/usr/bin/env python
#__author__ = 'dleece'
import sys

FEFQDN=""
FEPORT=""
SSLCert=""
MIConf="no"
def minInput():
    FEFQDN = raw_input("Enter the FQDN for the Find Evil server, EG fe2.dnsminer.net: ")
    FEPort = raw_input("Enter the logstash receiver TCP/IP port, EG  2112: ")
    print "Enter the path to the SSL public cert copied from FE server"
    SSLCert = raw_input( "EG, /var/lib/logstash-forwarder/keys/fePub.crt : ")

def confMinInput():
    print "confirm settings"
    print "FQDN of Find Evil server: " + FEFQDN
    print "TCP/IP port for Logstash on FE server: " + FEPORT
    print "The full path to the FE public SSL cert: " + SSLCert


while True:
    if MIConf=='yes':
        break
    minInput()
    confMinInput()
    RI=raw_input("Are these settings correct?  yes/no:")
    MIConf=str.lower(RI.strip())
