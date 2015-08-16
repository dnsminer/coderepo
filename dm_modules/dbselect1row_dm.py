__author__ = 'dleece'

import sys
import MySQLdb as mdb
import cfgparse_dm

DNSMinerHome='/opt/dnsminer-alpha'
dbcfg= DNSMinerHome + "/etc/dbConnections.cfg"

def dbRecordSelect(selectinput):
    print selectinput
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionOne')
    adminVar = thisCfgDict['databaseuser']
    adminPwd= thisCfgDict['databasepwd']
    ivDBName = thisCfgDict['databasename']
    print " retriving data"

    resultlist = []
    try:
        dbcon = mdb.connect('localhost',adminVar,adminPwd,ivDBName)
        #print "connected"
    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)

    with dbcon:
        cur=dbcon.cursor()
        sqlStr = "USE " + ivDBName
        cur.execute(sqlStr)
        sqlStr = selectinput
        cur.execute(sqlStr)
        row = cur.fetchone()
        if row is not None:
            for i in range(len(row)):
                resultlist.append(row[i])
    dbcon.commit()
    dbcon.close()
    return resultlist
