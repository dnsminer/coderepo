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
@click.option('--dname',prompt='domain name of interst',help='The partial domain name you are looking for, often a third party IOC')
@click.option('--lookback',default=10,help='Number of days, previous to today to include in report scope')

# The module calling the clik variables needs to be there first it seems.
def runreport(dname,lookback):
    print "running the report for " + dname + ", completing a backwards look for the previous " + str(lookback) + " days. "
    thisidxlist = getindexlist(lookback)
    for idxname in thisidxlist:
        print idxname
    # search the view
    searchindexes(thisidxlist,'AA',"T",lookback,'PDNS')

def searchindexes(ilist,wname,wval,lb,dtype):
    print "running search indexes"
    daysback = "now-"+str(lb)+"d"
    esclient = Elasticsearch([{'host':'localhost','port':9200}], sniff_on_start=True, sniff_on_connection_fail=True)
    histoList = list()
    dnsHisto = dict()
    dateHisto = dict()
    requests = 1

    # Left big & open for troubleshooting syntax isses
    # use term for non-analyzed fields and match for analyzed
    qry = "{\"fields\": [\"@timestamp\",\"soans\",\"query\",\"answers\",\"rcodename\",\"qtypename\"],\
            \"query\" : {\
            \"bool\": { \"must\": [\
            {\
            \"match\" : { \"" + wname +"\" : \""+ wval + "\" }\
            },{\
            \"range\": {\
                \"@timestamp\": {\
                    \"gt\" : \"" + daysback +"\",\
                 \"lt\" : \"now\"\
                 }\
               }\
             }\
          ]\
      },{\
     \"must_not\": {\"regexp\": { \"query\": \".*shawcable.net\"}}}\
    }\
  }"

    print qry
    for idx in ilist:
        try:
            response = scan(client=esclient, query=qry, index=idx, doc_type=dtype, scroll="3m", timeout="3m")
            for resp in response:
                docdict=resp['fields']
                tstamp = docdict['@timestamp'][0]
                authns = docdict['soans'][0]
                resqry = fqdnstrip(docdict['query'][0])
                ans = docdict['answers'][0]
                qtype = docdict['qtypename'][0]
                rcode = docdict['rcodename'][0]
                #tsint = getepoch(str(tstamp))
                print "TS: " + str(tstamp) + " SOANS: " + str(authns) + " QRY: " + resqry + " ANS: " + ans \
                + " QT: " + qtype + " Resp: " + rcode
                # strip out day, add to tuple, once you get the final listloop through each dom_tld
                # and count the occurances, add as 4th field
                # Using tuple so it can be a key but easily split into a list if needed.
                #dom_qtype = (dom_tld,qtype)
                #dom_qtype_ts = (dom_tld,qtype,tsint)

                # write data to dictionary
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
            print "Warning, no index found, report may not cover all days scoped"
            sys.exc_clear()

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

    runreport()
