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
    thisidxlist = getindexlist(lookback)
    #for idxname in thisidxlist:
    #    print idxname
    # search the view
    searchindexes(thisidxlist,lookback,'PDNS')

def readrpzfile():
    rpzfname = "/var/tmp/test500.rpz"
    file2read=open(rpzfname,'r')

    return file2read




def searchindexes(ilist,lb,dtype):
    #print "running search indexes"
    daysback = "now/d-"+str(lb)+"d"
    esclient = Elasticsearch([{'host':'localhost','port':9200}], sniff_on_start=True, sniff_on_connection_fail=True)
    histoList = list()
    dnsHisto = dict()
    dateHisto = dict()
    requests = 1

    # get the domain names from teh RPZ file
    thisrpzfh = readrpzfile()
    for tiname in thisrpzfh:
        tiname = tiname.strip()
        print tiname
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
    # Temp file just to test timing
    fname = "/var/tmp/rpztest.txt"
    file2write=open(fname,'w')
    for idx in ilist:
        try:
            response = scan(client=esclient, query=qry, index=idx, doc_type=dtype, scroll="6m", timeout="6m")
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

                #if dom_qtype not in dnsHisto:
                #    dnsHisto[dom_qtype] = 1
                #    # write tuple and time stamp to datehistory dictionary
                #    dateHisto[dom_qtype_ts] = tsint
                #else:
                #    dnsHisto[dom_qtype] += 1
                    # test if dom_type time stamp exits, if not add value,
                    # select occurances and lowest value at print time.
                #    if dom_qtype_ts not in dateHisto:
                #        dateHisto[dom_qtype_ts] = tsint

        except NotFoundError:
            #print "Warning, no index found, report may not cover all days scoped"
            sys.exc_clear()
    file2write.close()
    #writereport(dnsHisto,wval,dateHisto)
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

if __name__ == '__main__':

    runreport(15)
