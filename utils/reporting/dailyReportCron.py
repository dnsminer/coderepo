#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys, os, markup, string
#import MySQLdb as mdb
#import string
from dm_modules import cfgparse_dm, bulkdbselect1w_dm,bulkdbselectJoin1w_dm, dbselectSubqueryExclude_dm

DNSMinerHome='/opt/dnsminer-alpha'
sitecfg= DNSMinerHome + "/etc/siteSpecific.cfg"

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import scan




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
    print qry
    viewlist=[]
    try:
        response = esclient.search(index=idxnamewq, body=qry, doc_type=dtype)
        for tag in response['aggregations']['aggname']['buckets']:
            print(tag['key'],tag['doc_count'])
            viewname = tag['key']
            print viewname
            viewlist.append(viewname)
    except NotFoundError:
        print "Warning, no index found, report may not cover all days scoped"
        sys.exc_clear()
    # debug print out list
    for i in range(len(viewlist)):
        print viewlist[i]

    return







def getreportparams():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    rptbase = thisCfgDict['reportbase']
    rptbase =  DNSMinerHome  + rptbase
    return rptbase

def genvhtml(flist,vpath):

    title = "Daily reports for View"
    header = "The CSV files below are generated daily, save a local copy and filter using the spreadsheet tool of your choice"
    footer = "Don't forget to revist the Kibana discover application to do additional drill downs into anything from teh reports that piques your curiosity"
    blank = "  "
    page = markup.page()
    page.init (title=title,header=header, footer=footer)
    page.br()

    for f in flist:
        linkstr = "\"Report: " + f + "\", href='" + f + "' "
        page.a(linkstr)
    page.p(blank)
    # write teh file
    viewhtml = vpath + "/" + "view.html"
    print viewhtml
    htmlstr = str(page)
    file2write=open(viewhtml,'w')
    file2write.write(htmlstr)
    file2write.close()
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
                genvhtml(filepaths,vdir)


    return



def genhtmlwrapper():
    reppath = getreportparams()
    vlist = getviewlist(reppath)


    return




if __name__ == '__main__':

    aggbuckets('dmlogstash2-*','terms','View','10','DNSQRY')