#!/usr/bin/env python
#__author__ = 'dleece'
# Currently a standalone script to be used in nightly cron. If a user updates their blck of white list they
# will pull the list contents from the daily TI database table rather than each user opening the file each time

import sys, time,os, shutil, datetime
import MySQLdb as mdb
from dm_modules import cfgparse_dm

DNSMinerHome='/opt/dnsminer-alpha'
sitecfg = DNSMinerHome + "/etc/siteSpecific.cfg"

def getTIListsrc():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionThree')
    thisfibhome = thisCfgDict['fibhome']
    listbase = thisfibhome + "/lists/"
    return  listbase


def loadtable(sortedlist):
    print "checking credentials supplied"
    # by default config parser converts keys to lowercase , https://docs.python.org/2/library/configparser.html
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionOne')
    adminVar = thisCfgDict['databaseuser']
    adminPwd= thisCfgDict['databasepwd']
    ivDBName = thisCfgDict['databasename']

    try:
        dbcon = mdb.connect('localhost',adminVar,adminPwd,ivDBName)
        print "connected " + time.ctime()
    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)

    with dbcon:
        cur=dbcon.cursor()
        sqlStr = "USE " + ivDBName
        cur.execute(sqlStr)
        sqlStr = "DROP TABLE IF EXISTS tlist_domains;"
        cur.execute(sqlStr)
        sqlStr = "CREATE TABLE tlist_domains (domain VARCHAR(300), PRIMARY KEY(domain)) ENGINE=INNODB;"
        cur.execute(sqlStr)
        for line in sortedlist:
            #print line
            sqlStr = "INSERT INTO tlist_domains (domain) VALUES ('" + line + "');"
            cur.execute(sqlStr)
    dbcon.commit()
    dbcon.close()
    print "completed " + time.ctime()
    return

def genlistname(filebase):
    todate=datetime.date.today()
    #datestr=str(todate.year) + str(todate.month) + str(todate.day)
    month2d = '%02d' % todate.month
    day2d = '%02d' %todate.day
    datestr = str(todate.year) + month2d + day2d
    listname = datestr + "-public-list.rpz"
    listpath = filebase  + listname
    return listpath


def filetolist(filepath):
    #debug, dump file into list to save IO while inserting SQL
    print filepath
    thislist=[]
    try:
        print "reading file " + time.ctime()
        thislist =[line.strip() for line in open(filepath,'r')]
    except Exception as e:
        print "Unable to open public list file "
        print type(e)
        print str(e)
        return
    return thislist

# Main function
#def doload():
# get today's threat intel (ti) file name
titoday = genlistname(getTIListsrc())
tilist = filetolist(titoday)
loadtable(tilist)
#    return

