#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys, os, markup, string
#import MySQLdb as mdb
#import string
from dm_modules import cfgparse_dm, bulkdbselect1w_dm,bulkdbselectJoin1w_dm, dbselectSubqueryExclude_dm

DNSMinerHome='/opt/dnsminer-alpha'
sitecfg= DNSMinerHome + "/etc/siteSpecific.cfg"




def getreportparams():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    rptbase = thisCfgDict['reportbase']
    rptbase =  DNSMinerHome  + rptbase
    return rptbase

def genvhtml(flist):
    for f in flist:
        print f

    return



def getviewlist(dirpath):
    #Get all the directories that are not empty

    viewlist = os.listdir(dirpath)
    for fdir in viewlist:
        filepaths = []
        vdir = dirpath + "/" + fdir
        print vdir
        for dpath, dname, fnames in os.walk(vdir):
            for fname in fnames:
                filepaths.append(fname)
            if len(filepaths) > 1:
                genvhtml(filepaths)


    return



def genhtmlwrapper():
    reppath = getreportparams()
    vlist = getviewlist(reppath)


    return




if __name__ == '__main__':

    genhtmlwrapper()