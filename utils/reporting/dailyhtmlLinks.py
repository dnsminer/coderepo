#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys, os, markup, string
#import MySQLdb as mdb
#import string
from dm_modules import cfgparse_dm, bulkdbselect1w_dm,bulkdbselectJoin1w_dm, dbselectSubqueryExclude_dm

DNSMinerHome='/opt/dnsminer-alpha'
sitecfg= DNSMinerHome + "/etc/siteSpecific.cfg"




def getreportparams():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    rptbase = thisCfgDict['reportbase']
    rptbase =  DNSMinerHome  + rptbase
    return rptbase

def genvhtml(flist,vpath):

    title = "Daily reports for View"
    header = "The CSV files below are generated daily, save a local copy and filter using the spreadsheet tool of your choice"
    footer = "Don't forget to revist the Kibana discover application to do additional drill downs into anything from teh reports that piques your curiosity"
    styles = ('/css/style.css')
    blank = "  "
    page = markup.page()
    page.init (title=title,header=header, footer=footer, css=styles)
    page.br()

    for f in flist:
        linkstr = "\"Report: " + f + "\", href='" + f + "' "
        page.a(linkstr)
    page.p(blank)
    # write teh file
    viewhtml = vpath + "/" + "viewnew.html"
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

    genhtmlwrapper()