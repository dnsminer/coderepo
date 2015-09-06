#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys, os
import MySQLdb as mdb
import string
import click
from dm_modules import cfgparse_dm, bulkdbselect1w_dm,bulkdbselectJoin1w_dm, dbselectSubqueryExclude_dm
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from datetime import date, datetime, timedelta
from string import maketrans

DNSMinerHome='/opt/dnsminer-alpha'
sitecfg= DNSMinerHome + "/etc/siteSpecific.cfg"

# third party library for bootstrapping command line  http://click.pocoo.org/
@click.command()
@click.option('--vname',prompt='Viewname for report',help='Valid View name within elasticsearch, check Kibana discovery type:DNSQRY')
@click.option('--lookback',default=10,help='Number of days, previous to today to include in report scope')

def mkserial():
    todate=date.today()
    # need to deal with leading 0s to avoid zone transfer issues due to bad serial numbers
    day = '%02d' % todate.day
    mth = '%02d' % todate.month
    datestr=str(todate.year) + mth + day
    return datestr

# The module calling the clik variables needs to be there first it seems.
def runreport(vname,lookback):
    print "running the report for " + vname + ", completing a backwards look for the previous " + str(lookback) + " days. "
    thisidxlist = getindexlist(lookback)
    for name in thisidxlist:
        print name

    return


def getindexlist(lbdays):
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    idxpre = thisCfgDict['lsindexprefix']
    idxlist = []
    while lbdays > 0:
        d = date.today() - timedelta(days=lbdays)
        chrtrans = maketrans("-",".")
        idxsfx = str(d).translate(chrtrans)
        idxname = idxpre + "-" + idxsfx
        idxlist.append(idxname)
        lbdays = lbdays - 1
    return idxlist




def getreportparams():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    rptbase = thisCfgDict['reportbase']
    rptbase =  DNSMinerHome + "/" + rptbase
    rptsfx = mkserial() # these will be new every 24 hours
    retlist =  [rptbase, rptsfx]
    return retlist








if __name__ == '__main__':

    runreport()