#!/usr/bin/env python
#__author__ = 'dleece'
import sys, os, time, shutil
# functions

def minInput():
    FEFQDN = raw_input("Enter the FQDN for the Find Evil server, EG fe2.dnsminer.net: ")
    FEPort = raw_input("Enter the HTTPS port , Usually 443: ")
    KPORT = raw_input( "Enter the port Kibana is using, ( unless you changed it it's 5601: ")
    minInputVals = [FEFQDN,FEPort,KPORT]
    return minInputVals


def isPathValid(pathStr):
    TBool = os.path.isfile(pathStr)
    return TBool


print "testing"
if isPathValid('/usr/sbin/nginx') and isPathValid('/etc/nginx'):
    print "looks good, Nginx is installed "
else:
    print "Nginx does not appear to be installed"
    quit()