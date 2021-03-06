#!/usr/bin/env python
__author__ = 'dleece'
import sys, os
from dm_modules import cfgparse_dm, bulkdbselect1w_dm,bulkdbselectJoin1w_dm, dbselectSubqueryExclude_dm
from datetime import date, datetime, timedelta
# call the reporting job in the same directory
import  dailysumTldByType
import subprocess
# general elastic search collection
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import scan


# Update if installed in non-default location
DNSMinerHome='/opt/dnsminer-alpha'
sitecfg= DNSMinerHome + "/etc/siteSpecific.cfg"

#  Nothing below here likely needs to be edited unless debugging

def aggbuckets(idxnamewq,wname,wval,lb,dtype):
    # Get all the Views that have had some activity in the previous 10 days, count DNSQRY docs, bucket by View
    daysback = "now-"+str(lb)+"d"
    esclient = Elasticsearch([{'host':'localhost','port':9200}], sniff_on_start=True, sniff_on_connection_fail=True)
    # Left big & open for troubleshooting syntax isses
    qry = "{ \"query\": {\
            \"filtered\" : {\
                \"filter\": {\
                        \"range\": { \"@timestamp\" : { \"gt\" : \"" + daysback + "\", \"lt\" : \"now\"}}\
                        }\
                }\
        },\
        \"aggs\": {\
                \"aggname\": {\
                        \"" + wname + "\" : {\
                                \"field\": \"" + wval + "\"\
                                }\
                        }\
                }\
}"
    # debug
    #print qry
    avlist=[]
    try:
        response = esclient.search(index=idxnamewq, body=qry, doc_type=dtype)
        for tag in response['aggregations']['aggname']['buckets']:
            # debug
            #print(tag['key'],tag['doc_count'])
            viewname = tag['key']
            avlist.append(viewname)
    except NotFoundError:
        print "Warning, no index found, report may not cover all days scoped"
        sys.exc_clear()
    # debug print out list
    #for i in range(len(viewlist)):
    #    print viewlist[i]

    return avlist


def repdirmgmt(avl):
    # parse active view list, confirm dir exists and is writable
    evlist = []  # store if dir exists test results
    # get report path
    rbase = getreportparams()
    for thisview in avl:
        viewrptdir = rbase + "/" + thisview
        #print viewrptdir
        if os.path.isdir(viewrptdir):
            if os.access(viewrptdir,os.W_OK):
                evlist.append(thisview)
            else:
                logme = "fix file permissions for this directory: " + viewrptdir
                writeerrorlog(logme)
        else:
            try:
                os.mkdir(viewrptdir,0755)
                evlist.append(thisview)
                if os.access(viewrptdir,os.W_OK):
                    evlist.append(thisview)
                else:
                    logme = "fix file permissions for this directory: " + viewrptdir
                    writeerrorlog(logme)
            except OSError as e:
                print "Sorry, looks like the report directory for this view was not created : " + thisview +"\n"
                writeerrorlog(e)
                sys.exc_clear()
    return evlist


def writeerrorlog(estring):
    evtdate = mkserial()
    logline = evtdate + ":" + estring
    logname = DNSMinerHome + "/" + "errors.log"
    file2write=open(logname,'a')
    file2write.write(logline + '\n')
    file2write.close()
    return


def mkserial():
    todate=date.today()
    day = '%02d' % todate.day
    mth = '%02d' % todate.month
    datestr=str(todate.year) + mth + day
    return datestr

def getreportparams():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    rptbase = thisCfgDict['reportbase']
    rptbase =  DNSMinerHome  + rptbase
    return rptbase


def dodsum1(uvl):
    # usable View list is parsed to pass arguments to dailyTLD summary program
    repscript = DNSMinerHome + "/utils/reporting/dailysumTldByType.py"
    for uview in uvl:
        #params = '--vname ' + uview
        # not a fan but need to rework method input, click seems to be messing it up
        #subprocess.call([repscript, params])
        dailysumTldByType.runreport(uview,10)
    return


if __name__ == '__main__':

    activeviewlist=aggbuckets('dmlogstash2-*','terms','View','10','DNSQRY')
    vlist = repdirmgmt(activeviewlist)
    dodsum1(vlist)


