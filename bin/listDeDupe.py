#!/usr/bin/env python
#__author__ = 'dleece'
#  The main purpose of this program is to gather what ever domain lists are being regularly collected,
#  de-duplicate them since there is often overlap, and move a copy of the list to the fetch it boy folder.
#
import sys, os, glob, time, datetime, shutil, pwd, grp
#
# Define the list home directory and the fetch it boy pickup location ( to do,  import from param files)
LISTHOME = '/opt/dnsminer-alpha/fib/lists'
FIBHOME = '/opt/dnsminer-alpha/fib'
FIBUID = 'fetchItBoy'
FIBGID = 'fetchItBoy'

#ts = time.time()
# calculate the date that is used for the prefix of the list files
FILEPRE = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
FILEGLOB = FILEPRE +'*' + '.txt'
FILERPZ = FILEPRE + '-public-list.rpz'
RPZPATH = LISTHOME + "/" + FILERPZ
FIBPKG1 = ""
DOMAINLIST = list()

os.chdir(LISTHOME)
print LISTHOME
print FILEGLOB
for LFILE in glob.glob(FILEGLOB):
    # open each file and dump to a list
    try:
        fh = open(LFILE)
    except:
        print "List file not available"
        continue
    for DNAME in fh:
        if not DNAME.strip():
            DNAME = DNAME.strip()
            print DNAME + " precheck"
            if DNAME not in DOMAINLIST:
                print DNAME + " postcheck"
                DOMAINLIST.append(DNAME)

    fh.close()
    print "DOMAINLIST length: " + str(len(DOMAINLIST))
# create the source data for the daily RPZ zone using de-duped list
try:
    rpzfh = open(RPZPATH,'w')
except:
    print "list2file nable to open file " + RPZPATH
for DOM in DOMAINLIST:
    rpzfh.write(DOM + '\n')
rpzfh.close()

# move the file to the fetch it boy pick up location.
try:
    shutil.copy(RPZPATH,FIBHOME)
except:
    print "shu-mv unable to open file " + RPZPATH

# change ownership to fetchitboy.  This seems to need to run as root
UID = pwd.getpwnam(FIBUID).pw_uid
GID = grp.getgrnam(FIBGID).gr_gid
FIBPKG1 = FIBHOME + "/" + FILERPZ
try:
    os.chown(FIBPKG1,UID,GID)
except:
    print "unable to change ownership of this file: " + FIBPKG1

# clean up the old list file because shutil.move was locking up
#try:
#    #os.remove(RPZPATH)
#except:
#    print "unable to remove/clean up file: " + RPZPATH