__author__ = 'dleece'
#!/usr/bin/env python
#  The main purpose of this program is to gather what ever domain lists are being regularly collected,
#  de-duplicate them since there is often overlap, and move a copy of the list to the fetch it boy folder.
#
import sys, os, glob, time, datetime, shutil
#
# Define the list home directory and the fetch it boy pickup location ( to do,  import from param files)
LISTHOME = '/home/dleece/dnseval/lists'
FIBHOME = '/home/fib/list1'

#ts = time.time()
# calculate the date that is used for the prefix of the list files
FILEPRE = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
FILEGLOB = FILEPRE +'*' + '.txt'
FILERPZ = FILEPRE + 'public-list.rpz'
RPZPATH = LISTHOME + "/" + FILERPZ
DOMAINLIST = list()

os.chdir(LISTHOME)
for LFILE in glob.glob(FILEGLOB):
    # open each file and dump to a list
    try:
        fh = open(LFILE)
    except:
        print "List file not available"
        continue
    for DNAME in fh:
        DNAME = DNAME.strip()
        if DNAME not in DOMAINLIST:
            DOMAINLIST.append(DNAME)
    fh.close()
# create the source data for the daily RPZ zone using de-duped list
try:
    rpzfh = open(RPZPATH,'w')
except:
    print "Unable to open file " + RPZPATH
for DOM in DOMAINLIST:
    rpzfh.write(DOM + '\n')
rpzfh.close()

# move the file to the fetch it boy pick up location.
try:
    FIBPKG1 = shutil.move(RPZPATH,FIBHOME)
except:
    print "unable to open file " + RPZPATH