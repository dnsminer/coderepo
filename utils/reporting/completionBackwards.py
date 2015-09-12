#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys, os
#import MySQLdb as mdb
import string
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


def runreport(lookback):
    # Need to pass index wildcard, number of days to look backwards and the type of document, I.e PDNS or DNSQRY
    searchindexes('dmlogstash2-*',lookback,'PDNS')
    return


def getfibrpz():
    # parsse the config file to figure out the location of the RPZ files,  look for the newest and return a lsit with file path and file name
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    fibpath = thisCfgDict['fibhome']
    newest = 19992359
    thisrpz = ''
    rpzlist = os.listdir(fibpath)
    retlist = [fibpath]

    for fname in rpzlist:
        fname = fname.strip()
        if fname.endswith(".rpz"):
            fnamesplit = fname.split('-')
            try:
                fnamedate = int(fnamesplit[0])
                if fnamedate > newest:
                    newest = fnamedate
                    thisrpz = fname
            except:
                print "rpz file not in expected format"
                sys.exc_clear()
            filepaths = []
            # expecting yyyymmdd-*.rpz
            if len(thisrpz) > 11 :
                retlist.append(thisrpz)
            else:
                print "Sorry, unable to find a usable RPZ file, please debug"
    return retlist


def mkserial():
    todate=date.today()
    # need to deal with leading 0s to avoid zone transfer issues due to bad serial numbers
    day = '%02d' % todate.day
    mth = '%02d' % todate.month
    datestr=str(todate.year) + mth + day
    return datestr


def writeerrorlog(estring):
    evtdate = mkserial()
    logline = evtdate + ":" + estring
    logname = DNSMinerHome + "/" + "errors.log"
    file2write=open(logname,'a')
    file2write.write(logline + '\n')
    file2write.close()
    return


def readrpzfile():
    rpzlist = getfibrpz()
    if len(rpzlist)== 2:
        rpzfname = rpzlist[0] + "/" + rpzlist[1]
        try:
            file2read=open(rpzfname,'r')
        except OSError as e:
                print "Sorry, looks like there is a problem opening that file  : " + rpzfname +"\n"
                writeerrorlog(e)
                sys.exc_clear()
                return
    return file2read


def getreportparams():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    rptbase = thisCfgDict['dmhome']
    rptbase = rptbase + "/var/reports"
    return rptbase


def searchindexes(idxname,lb,dtype):
    #print "running search indexes"
    daysback = "now/d-"+str(lb)+"d"
    esclient = Elasticsearch([{'host':'localhost','port':9200}], sniff_on_start=True, sniff_on_connection_fail=True)
    # get the domain names from teh RPZ file
    thisrpzfh = readrpzfile()
    # Temp file just to test timing
    cbfname = getreportparams()
    cbfname = cbfname + "/" + mkserial() + "-cb.txt"
    try:
        file2write=open(cbfname,'w')
    except OSError as e:
        print "Sorry, looks like there is a problem opening that file  : " + cbfname +"\n"
        writeerrorlog(e)
        sys.exc_clear()
        return

    # Need to create unique queries to be passed to the bulk index search
    for tiname in thisrpzfh:
        tiname = tiname.strip()

        qry = "{\"fields\": [\"@timestamp\",\"soans\",\"query\",\"answers\",\"rcodename\",\"qtypename\"],\
        \"query\": {\
            \"filtered\" : {\
                \"query\": {\
                    \"bool\": { \"should\": [\
                                    { \"wildcard\": { \"query\": \"*" + tiname + "*\" }},\
                                    { \"wildcard\": { \"answers\": \"*" + tiname + "*\" }}\
                                ],\
                                \"minimum_should_match\": 1\
                        }\
                },\
                \"filter\": {\
                        \"range\": { \"@timestamp\" : { \"gt\" : \"" + daysback + "\", \"lt\" : \"now/d\"}}\
                        }\
                }\
        }\
}'"
        print qry
        #for idx in ilist:
        try:
            response = scan(client=esclient, query=qry, index=idxname, doc_type=dtype, scroll="6m", timeout="6m")
            for resp in response:
                docdict=resp['fields']
                tstamp = docdict['@timestamp'][0]
                authns = docdict['soans'][0]
                dedupeqry = fqdnstrip(docdict['query'][0])
                resqry = docdict['query'][0]
                ans = docdict['answers'][0]
                qtype = docdict['qtypename'][0]
                rcode = docdict['rcodename'][0]
                #tsint = getepoch(str(tstamp))
                fileline = "TS: " + str(tstamp) + " SOANS: " + str(authns) + "DDQRY: " + dedupeqry + " QRY: " + resqry + " ANS: " + ans \
                + " QT: " + qtype + " Resp: " + rcode
                # Temp file just to test timing
                file2write.write(fileline +"\n")
        except NotFoundError:
            #print "Warning, no index found, report may not cover all days scoped"
            sys.exc_clear()

    file2write.close()
    #writereport(dnsHisto,wval,dateHisto)
    return


if __name__ == '__main__':

    runreport(30)