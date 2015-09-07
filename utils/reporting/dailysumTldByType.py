#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys, os
#import MySQLdb as mdb
import string
import click
from dm_modules import cfgparse_dm, bulkdbselect1w_dm,bulkdbselectJoin1w_dm, dbselectSubqueryExclude_dm
from elasticsearch import Elasticsearch
#from elasticsearch_dsl import Search, Q
from datetime import date, datetime, timedelta
from string import maketrans
from elasticsearch import helpers
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import scan

DNSMinerHome='/opt/dnsminer-alpha'
sitecfg= DNSMinerHome + "/etc/siteSpecific.cfg"

# third party library for bootstrapping command line  http://click.pocoo.org/
@click.command()
@click.option('--vname',prompt='Viewname for report',help='Valid View name within elasticsearch, check Kibana discovery type:DNSQRY')
@click.option('--lookback',default=10,help='Number of days, previous to today to include in report scope')

# The module calling the clik variables needs to be there first it seems.
def runreport(vname,lookback):
    print "running the report for " + vname + ", completing a backwards look for the previous " + str(lookback) + " days. "
    thisidxlist = getindexlist(lookback)
    for name in thisidxlist:
        print name
    # search the view
    searchindexes(thisidxlist,'View',vname,lookback,'DNSQRY')

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

def searchindexes(ilist,wname,wval,lb,dtype):
    daysback = "now-"+str(lb)+"d"
    esclient = Elasticsearch([{'host':'localhost','port':9200}], sniff_on_start=True, sniff_on_connection_fail=True)
    histoList = list()
    dnsHisto = dict()
    dateHisto = dict()
    requests = 1

    # Left big & open for troubleshooting syntax isses
    qry = "{\"fields\": [\"@timestamp\",\"RQuery\",\"RQType\"],\
            \"query\" : {\
            \"bool\": { \"must\": [\
            {\
            \"term\" : { \"" + wname +"\" : \""+ wval + "\" }\
            },{\
            \"range\": {\
                \"@timestamp\": {\
                    \"gt\" : \"" + daysback +"\",\
                 \"lt\" : \"now\"\
                 }\
               }\
             }\
          ]\
      }\
    }\
  }"

    for idx in ilist:
        try:
            response = scan(client=esclient, query=qry, index=idx, doc_type=dtype, scroll="3m", timeout="3m")
            for resp in response:
                docdict=resp['fields']
                dom_tld = fqdnstrip(docdict['RQuery'][0])
                qtype = docdict['RQType'][0]
                tstamp = docdict['@timestamp'][0]
                print str(tstamp)
                # strip out day, add to tuple, once you get the final listloop through each dom_tld
                # and count the occurances, add as 4th field
                # Using tuple so it can be a key but easily split into a list if needed.
                dom_qtype = (dom_tld,qtype)
                # debug
                #print str(dom_qtype[0]) +"," + str(dom_qtype[1])
                # write data to dictionary
                if dom_qtype not in dnsHisto:
                    dnsHisto[dom_qtype] = 1
                else:
                    dnsHisto[dom_qtype] += 1

        except NotFoundError:
            print "Warning, no index found, report may not cover all days scoped"
            sys.exc_clear()

    writereport(dnsHisto,wval)
    return


def fqdnstrip(fqdn):
    fqdn=fqdn.strip()
    fullqry= fqdn.split('.')
    dnsize=len(fullqry)
    if dnsize > 1:
        domonly = fullqry[dnsize -2] + "." + fullqry[dnsize -1]
    elif dnsize == 1:
        domonly = fullqry[0]
    else:
        domonly = "no.tld"

    return domonly


def getreportparams():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    rptbase = thisCfgDict['reportbase']
    rptbase =  DNSMinerHome + "/" + rptbase
    rptsfx = mkserial() # these will be new every 24 hours
    retlist =  [rptbase, rptsfx]
    return retlist

def mkserial():
    todate=date.today()
    # need to deal with leading 0s to avoid zone transfer issues due to bad serial numbers
    day = '%02d' % todate.day
    mth = '%02d' % todate.month
    datestr=str(todate.year) + mth + day
    return datestr

def writereport(resultdict,thisview):
    sortList = list()
    # confirm we have data
    for domKey,domVal in resultdict.items():
        dom, qt = domKey
        tmpLine = str(domVal) + "," + str(dom).strip() +"," + str(qt).strip()
        #print tmpLine
        sortList.append(tmpLine)
    reportList = sorted(sortList)
    fpath = getrptbase(thisview)
    fname = thisview + "-" +mkserial() + ".csv"
    fname = fpath + "/" + fname
    print fname
    file2write=open(fname,'w')
    for sortLine in reportList:
        #print sortLine
        file2write.write(sortLine + '\n')
    file2write.close()
    return

def getrptbase(vname):
    filepath = DNSMinerHome
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    rptbase = thisCfgDict['reportbase']
    filepath = filepath +  rptbase + "/" + vname
    # need a little hook to make directory if not there
    return filepath


if __name__ == '__main__':

    runreport()