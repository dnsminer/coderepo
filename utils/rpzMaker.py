__author__ = 'dleece'
#!/usr/bin/env python

import sys, os, glob, time, datetime
#
# Define the list home directory, ( to do,  import from param files)
LISTHOME = '/home/dleece/dnseval/lists'

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
# create the RPZ zone using de-duped list
try:
    rpzfh = open(RPZPATH,'w')
except:
    print "Unable to open file " + RPZPATH
for DOM in DOMAINLIST:
    rpzfh.write(DOM + '\n')
rpzfh.close()


#FILE2READ = str(sys.argv[1])
#FILE2WRITE = str(sys.argv[2])
#ENDSTRING = str(sys.argv[3])

#fr = open(FILE2READ,'r')
#fw = open(FILE2WRITE,'w')

#for line in fr:
#    testline = line.strip()
#    #print testline
#    if testline.endswith(ENDSTRING):
#        #print testline,
#        fw.write(line)
#
#fw.close()
#fr.close()