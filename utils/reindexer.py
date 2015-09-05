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

client = Elasticsearch([{'host':'localhost','port':9200}], sniff_on_start=True, sniff_on_connection_fail=True)
#query={"query": {"match_all" : {}}}
#scanResp = client.search(index="logstash-2015.08.11", doc_type=["DNSQRY","PDNS"], body=query, search_type="scan", scroll="10m", size=10000)
#for key,val in scanResp.iteritems():
#    print key, '-->', scanResp[key]
#scrollId=scanResp['_scroll_id']
#response = client.scroll(scroll_id=scrollId, scroll="10m")

response = client.cat.indices( index='logstash-*', h=['index','docs.count'])

print "this is the response"

responselist = response.splitlines()
for line in responselist:
    print line