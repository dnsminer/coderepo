__author__ = 'dleece'

import sys
import MySQLdb as mdb
import cfgparse_dm

# This module allows for two conditions to be tested, useful to authorize
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
    selectcolumn0 = selectinput[2]
    selectwhere0 = selectinput[3]
    selectcolumn1 = selectinput[4]
    selectwhere1 = selectinput[5]

    resultlist = []
    var = False
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
        sqlStr = "SELECT " + selectvalue + " from " + selecttable + " WHERE " + selectcolumn0 + " = '" + str(selectwhere0) +"' AND " + selectcolumn1 + " = '" + selectwhere1 + "';"
        #print sqlStr
        cur.execute(sqlStr)
        row = cur.fetchone()
        if row is None:
            print "\nSorry, that view is not associated with your organization"
            var= False
            resultlist.append(var)
            resultlist.append('noauth')
        else:
            vid = row[0]
            var = True
            resultlist.append(var)
            resultlist.append(vid)
    dbcon.commit()
    dbcon.close()
    return resultlist
