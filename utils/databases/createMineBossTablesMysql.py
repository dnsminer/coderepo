#!/usr/bin/env python
#__author__ = 'dleece'
import sys, time,os, shutil
import MySQLdb as mdb

DNSMinerHome='/opt/dnsminer-alpha'
dbUtilsHome = DNSMinerHome + '/utils/databases/'

def getTableCreateValues():
    dbAdmin = raw_input("Enter mysql admin user,(typically root): ")
    dbAdminPWD = raw_input("Enter mysql admin's  passwd: ")
    dbName = raw_input("What is the name of your application database? :")
    dbType = raw_input("Which application tables are you creating (mineboss|something not yet buit) ? :")
    dbType = dbType.strip().lower()
    minInputVals = [dbAdmin,dbAdminPWD,dbName,dbType]
    return minInputVals

def getDBTableDef(inputvals):
    if inputvals[3] == 'mineboss':
        resultVar = dbTblCreateMB(inputvals)
    return resultVar

def dbTblCreateMB(inputvals):
    print "creating database tables for mineboss application"
    adminVar=inputvals[0]
    adminPwd=inputvals[1]
    ivDBName=inputvals[2]
    # Open the SQL script to be used for table creation
    sqlfile = dbUtilsHome + 'mbtables.sql'
    try:
        fh = open(sqlfile)
    except:
        print "SQL tables file not available"
        return

    for CMD DNAME in fh:
        if not DNAME.strip():
            DNAME = DNAME.strip()
            if DNAME not in DOMAINLIST:
                DOMAINLIST.append(DNAME)
    fh.close()

    try:
        dbcon = mdb.connect('localhost',adminVar,adminPwd,'mysql')
        #print "connected"
    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)

    with dbcon:
        cur=dbcon.cursor()
        sqlStr = "USE " + ivDBName
        cur.execute(sqlStr)
        for sqlStr in fh:
            if sqlStr.strip():
                print sqlStr
               #cur.execute (sqlStr)
    dbcon.commit()
    dbcon.close()
    var = 'Creating mineboss database tables done'
    return var

newtblvals=getTableCreateValues()
print getDBTableDef(newtblvals)