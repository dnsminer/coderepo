__author__ = 'dleece'

import sys, os, glob, time, datetime, shutil, pwd, grp, cfgparse_dm

DNSMinerHome='/opt/dnsminer-alpha'
sitecfg = DNSMinerHome + "/etc/siteSpecific.cfg"


def getpathinfo():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    keydir = thisCfgDict['keybase']
    clientdir = thisCfgDict['rpzbase']
    acldir = thisCfgDict['aclbase']
    tmpdir = thisCfgDict['dmtemp']
    pathlist = [keydir,clientdir,acldir,tmpdir]

    return  pathlist


def getAppOwnerInfo():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionFour')
    dnsmgid = thisCfgDict['dmgid']
    mbuid = thisCfgDict['aouid']
    uinfo=[mbuid,dnsmgid]
    return uinfo


def mkclientdir(oid):
    dirlist=getpathinfo()
    dirname = dirlist[1] + "/" + str(oid)
    ulist= getAppOwnerInfo()
    uid = ulist[0]
    gid = ulist[1]
    if not os.path.exists(dirname):
        try:
            os.mkdir(dirname,0775)
            os.chown(dirname,uid,gid)
        except Exception as e:
            print "Unable to create directory, please debug"
            print type(e)
            print str(e)
    return


def copyfile(fname,ftype,oid):
    print "copying file"
    dirlist=getpathinfo()
    movefile = dirlist[3] + "/" + fname
    clntdir = dirlist[1] + "/" + str(oid)
    ulist= getAppOwnerInfo()
    uid = ulist[0]
    gid = ulist[1]

    if ftype == 'key':
        try:
            shutil.copy(movefile,dirlist[0])

        except:
            print "shu-mv unable to copy file " + fname
    elif ftype == 'acl':
        try:
            shutil.copy(movefile,dirlist[2])
        except:
            print "shu-mv unable to copy file " + fname
    elif ftype == 'zone':
        try:
            shutil.copy(movefile,clntdir)
            # Allow group perm to overwrite if needed
            newfile = clntdir + "/" + fname
            os.chown(newfile,uid,gid)
            os.chmod(newfile,0775)
        except:
            print "shu-mv unable to copy file " + fname
    else:
        print "no valid file type provided for " + fname

    return

