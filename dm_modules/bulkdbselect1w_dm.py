__author__ = 'dleece'

import sys
import MySQLdb as mdb
import cfgparse_dm, inputSani_dm

DNSMinerHome='/opt/dnsminer-alpha'
dbcfg= DNSMinerHome + "/etc/dbConnections.cfg"

def dbRecordSelect(selectinput):
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionOne')
    adminVar = thisCfgDict['databaseuser']
    adminPwd= thisCfgDict['databasepwd']
    ivDBName = thisCfgDict['databasename']
    print " retriving data"
    selectvalue = str(selectinput[0])
    selecttable = str(selectinput[1])
    selectcolumn = str(selectinput[2])
    selectwhere = str(selectinput[3])

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
        sqlStr = sqlStr = "SELECT " + selectvalue + " from " + selecttable + " WHERE " + selectcolumn + " = '" + selectwhere +"';"
        print  sqlStr
        cur.execute(sqlStr)
        rows = cur.fetchall()
        print len(rows)
        # Make use we got at least one record
        if len(rows) > 0:
            for row in rows:
                resultlist.append(row)
        else:
            print " empty records, please debug"
    dbcon.commit()
    dbcon.close()
    return resultlist
