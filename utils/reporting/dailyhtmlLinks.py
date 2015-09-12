#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys, os, string
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
    # writing the pages out by hand to take advanatge of teh custom style sheet
    httphdr ="<!DOCTYPE html>\n<HTML><HEAD>\n<meta charset=\"utf-8\" />\n<title> Report Index</title>\n\
        <meta name=\"keywords\" content=\"Reports DNS Analysis\" />\n\
        <meta name=\"description\" content=\"DNS Miner automated reports\" />\n\
        <link href=\"/reports/css/style.css\" rel=\"stylesheet\">\n</head>\n"
    httpbdy ="<div class=\"wrapper\">\n<header class=\"header\">\n\
            <h1> Daily reports for View </h1>\n</header><!-- .header-->\n\
            <main class=\"content\">\n\
            <p> The CSV files below are generated daily. Save a local copy and filter as required using the spreadsheet of your choice.</p>\n\
            <table><tr><th>Report Name</th><th>Download link</th></tr>\n"

    # write the table rows
    for f in flist:
        httpbdy = httpbdy + "<tr><td> Report: " + f + "</td><td><a href=\"" + f + "\"> download </a></td></tr>"
    # close the table
    httpbdy = httpbdy + "</table>\n"
    httpbdy = httpbdy + "<p>&nbsp</p><p>Don't forget to revist the Kibana discover application to do additional drill downs\
     into anything from the reports that piques your curiosity</p>"
    httpbdy = httpbdy + "</main><!-- .content -->\n</div><!-- .wrapper -->"
    httpftr = "<footer class=\"footer\">\n\
    <p class=\"foot\"> \"The horses may have already left the barn, take a look though, at least you'll be able to figure out how long they have been gone\" </p>\n\
    <p class=\"footlegal\"> Copyright 2015, DNS Miner. Apache 2.0 license </p>\n\
    <img src=\"/reports/images/python.png\">\n</footer><!-- .footer -->\n</body></html>"

    htmlpage= httphdr + httpbdy + httpftr
    # write teh file
    viewhtml = vpath + "/" + "view.html"
    print viewhtml
    file2write=open(viewhtml,'w')
    file2write.write(htmlpage)
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
                if fname.endswith(".csv"):
                    filepaths.append(fname)
            if len(filepaths) > 1:
                genvhtml(filepaths,vdir)
    return


def genviewdailyhtml():
    reppath = getreportparams()
    getviewlist(reppath)
    return




if __name__ == '__main__':

    genviewdailyhtml()