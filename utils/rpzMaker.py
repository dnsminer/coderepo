__author__ = 'dleece'
#!/usr/bin/env python
#  The main purpose of this program is to integrate white lie, black list and the de-duped domains from auto sources.
#
# white and black lists will be pulled from database after POC developed using flat files.

import sys, os, glob, time, datetime, shutil, pwd, grp

# calculate the date that is used for the prefix of the list files
FILEPRE = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
FIBHOME = '/home/fib'
CLIENTLIST = list()
BLACKLIST = list()
AUTOLIST = list()
AUTOLISTPATH = FIBHOME + '/' + FILEPRE + '-public-list.rpz'

def getActiveClients(CLIST):
    # return a list of active customers by org ID which is the primary key
    # key is also used to create composite keys when retrieving white list and black list
    PWD=os.getcwd()
    CUSTDB='../var/db/customer.db'
    CUSTDBPATH = os.path.join(os.path.dirname(__file__),CUSTDB)
    try:
        fh = open(CUSTDBPATH,'r')
    except:
        print "List file not available"
    for line in fh:
        line = line.rstrip()
        if not line.startswith('#'):
            LVALUES = line.split(',')
            ORGID =(LVALUES[0])
            if ORGID not in CLIST:
                CLIST.append(ORGID)
    return CLIST


def getBlackList(BLIST):
    # returns a list domain and org id pairs
    BLKDB='../var/db/blacklist.db'
    BLKDBPATH = os.path.join(os.path.dirname(__file__),BLKDB)
    try:
        fhb = open(BLKDBPATH,'r')
    except:
        print "black list file not available"
    for linebl in fhb:
        linebl = linebl.rstrip()
        if not linebl.startswith('#'):
            BLVALUES = linebl.split(',')
            ORGID = (BLVALUES[0])
            BDOM = (BLVALUES[1])
            OCB = ORGID + ',' + BDOM
            if OCB not in BLIST:
                BLIST.append(OCB)
    return BLIST

def getAutoList(ALIST):
    try:
        fha = open(AUTOLISTPATH,'r')
    except:
        print "auto list file not available"
    for linea in fha:
        linea = linea.rstrip()
        ALIST.append(linea)




# extract org ID, I.E, look up clients
getActiveClients(CLIENTLIST)
getBlackList(BLACKLIST)
getAutoList(AUTOLIST)


# debug, make sure we are reading the right files

for ID in CLIENTLIST:
    CBLIST = list()
    for OCBL in BLACKLIST:
        OCBLVALUES = OCBL.split(',')
        if ID == OCBLVALUES[0]:
            if OCBLVALUES[1] not in CBLIST:
                CBLIST.append(OCBLVALUES[1])
    for ADOM in AUTOLIST:
        if ADOM not in CBLIST:
            ADOM = ADOM.rstrip()
            CBLIST.append(ADOM)

# testing
    print ID
    for DOM in CBLIST:
        print DOM





