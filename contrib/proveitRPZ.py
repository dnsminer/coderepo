#!/usr/bin/env python
import dns.query
import dns.name
import dns.message
from dns.exception import DNSException
import random
import time
from random import randint
from time import sleep
import sys


def opendomfile(filename):
    try:
        fh = open(filename,'r')
        linelist=fh.readlines()
    except Exception as e:
        print "Unable to create view file in temp directory or problem with the file content, please debug"
        print type(e)
        print str(e)
        return
    fh.close()
    return linelist

def genrandhost():
    wfile = "dgafaker.txt"
    WORDS = open(wfile).read().splitlines()
    word = random.choice(WORDS)
    word = word + random.choice(WORDS)
    return word

def openlogfile(fname):
    try:
        fh = open(fname,'a')
    except Exception as e:
        print "Unable to create view file in temp directory or problem with the file content, please debug"
        print type(e)
        print str(e)
    return fh

def getldns(divint):
    dnslist=['192.168.59.29','192.168.59.28']
    thisns=dnslist[divint%2]
    return thisns


def genRPZtraffic(dlist):
    thisfh = openlogfile("proveit.log")
    RDTYPE=['A','MX','NS','A','A','AAAA','TXT','MX','A','A','A','AAAA','A','A']
    while True:
        thisint = (randint(0,499))
        ldns=getldns(thisint)
        thishost = genrandhost()
        thisdom = dlist[thisint]
        fqdn = thishost + "." + thisdom
        domobj = dns.name.from_text(fqdn.strip())
        thisfh.write(fqdn + "\n")
        #randrd = 'dns.rdatatype.' + random.choice(RDTYPE)
        req = dns.message.make_query(domobj, dns.rdatatype.A, dns.rdataclass.IN)
        try:
            resp = dns.query.udp(req,ldns)
            if len(resp.answer) == 0:
                print " do it again "
                sleep(2)
                resp = dns.query.udp(req,ldns)
            print resp.answer
        except DNSException as ex:
            print ex
        sleep(randint(45,549))
        thisfh.close()
        return



def  main():
    localns = '192.168.59.29'
    domlist=opendomfile('test.txt')
    genRPZtraffic(domlist)


if __name__ == "__main__": main()


