__author__ = 'dleece'

import sys
import MySQLdb as mdb
import cfgparse_dm

DNSMinerHome='/opt/dnsminer-alpha'
dbcfg= DNSMinerHome + "/etc/dbConnections.cfg"

def dbRecordSelect(selectinput):
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionOne')
    adminVar = thisCfgDict['databaseuser']
    adminPwd= thisCfgDict['databasepwd']
    ivDBName = thisCfgDict['databasename']
    print " retriving data"
    selectvalue = selectinput[0]
    selecttable = selectinput[1]
    selectcolumn = selectinput[2]
    selectwhere = selectinput[3]

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
        sqlStr = "SELECT " + selectvalue + " from " + selecttable + " WHERE " + selectcolumn + " = '" + selectwhere +"';"
        cur.execute(sqlStr)
        rows = cur.fetchall()
        # Make use we got at least one record
        if rows[0] is not None:
            for row in rows:
                resultlist.append(row)
    dbcon.commit()
    dbcon.close()
    return resultlist
