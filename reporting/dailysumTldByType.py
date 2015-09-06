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

@click.command()
@click.option('--vname',prompt='Viewname for report',help='Valid View name within elasticsearch, check Kibana discovery type:DNSQRY')
@click.option('--lookback',default=10,help='Number of days, previous to today to include in report scope')

def runreport(vname,lookback):
    print "running teh report for " + vname
    print "this will run " +str(lookback) + " times"
    return


if __name__ == '__main__':
    runreport()