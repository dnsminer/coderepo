#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys, os
import MySQLdb as mdb
import sys
import json
import string
from dm_modules import cfgparse_dm, bulkdbselect1w_dm,bulkdbselectJoin1w_dm, dbselectSubqueryExclude_dm
from datetime import date, datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch import helpers
from elasticsearch.helpers import reindex

## site specific settings
DNSMinerHome='/opt/dnsminer-alpha'
dbcfg= DNSMinerHome + "/etc/siteSpecific.cfg"

def unicodelinesplitter(uline):
    aline = str(uline)
    aline = aline.strip()
    rowlist = aline.split()
    return rowlist

#query={"query": {"match_all" : {}}}
#scanResp = client.search(index="logstash-2015.08.11", doc_type=["DNSQRY","PDNS"], body=query, search_type="scan", scroll="10m", size=10000)
#for key,val in scanResp.iteritems():
#    print key, '-->', scanResp[key]
#scrollId=scanResp['_scroll_id']
#response = client.scroll(scroll_id=scrollId, scroll="10m")


def getsourceindexs(srcprefix):
# get list of non-empty source indexs to be passed to reindexer function
# assuming we are using prefix-date stamp since this tends to be the autocreate default
    indexlist = []
    srxidx = srcprefix + "*"
    client = Elasticsearch([{'host':'localhost','port':9200}], sniff_on_start=True, sniff_on_connection_fail=True)
    indexcat = client.cat.indices( index=srxidx, h=['index','docs.count'])

# The result comes out as a unicode string, needed to do a little slicing and dicing to create a list to return
    icatlist = indexcat.splitlines()
    for line in icatlist:
        resultlist = unicodelinesplitter(line)
        if resultlist[1] > 0:
            indexlist.append(resultlist[0])
    return indexlist

def doreindex(srcidxlist,dstidx):
    print "reindexing to " + dstidx
    for row in srcidxlist:
        print row[0]

def reindexmenu():
    doindexing=True
    while doindexing:
        print "\nYou are about to reindex a potentially large amount of data, this could take a while"
        print "\nWhat is the prefix of the source indexes? EG, logstash-2015.08.31 would be logstash"
        while doindexing:
            uidxinput = raw_input("Enter source index prefix: ")
            uidxinput = uidxinput.strip().lower()
            ilist = getsourceindexs(uidxinput)
            if len(ilist) > 0:
                print "great, looks like we have " + str(len(ilist)) + "indices to reindex"
            else:
                print "sorry, that doesn't look like a valid index prefix"
                print "try running a command like this curl -GET http://localhost:9200/_cat/indices?v from the FE server command prompt to display the index names"
                continue

            uidxinput = raw_input("Enter destination index name: ")
            uidxinput = uidxinput.strip().lower()

            # This is where we could write a create index with mapping function but for now we're just going to assume
            # the index is ready waiting and properly configured.
            doreindex(ilist,uidxinput)
            doindexing = False


reindexmenu()