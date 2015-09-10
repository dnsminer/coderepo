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



def getviewlist(dirpath):
    #Get all the directories that are not empty
    viewlist = os.listdir(dirpath)
    for fdir in viewlist:
        vdir = dirpath + "/" + fdir
        print vdir
        for dpath, dname, fname in os.walk(vdir):
            flist = os.path.join(dpath,fname)
            print len(flist)


    return



def genhtmlwrapper():
    reppath = getreportparams()
    vlist = getviewlist(reppath)


    return




if __name__ == '__main__':

    genhtmlwrapper()