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

# extract org ID, I.E, look up clients
getActiveClients(CLIENTLIST)

# debug, make sure we are reading the right files
for ID in CLIENTLIST:
    print ID
