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
    #debug
    print " sanitizing input data"
    selectvalue1 = str(selectinput[0])
    selectvalue1 = inputSani_dm.inputSanitizer(selectvalue1,'sqlval')
    selecttable = str(selectinput[1])
    selecttable = inputSani_dm.inputSanitizer(selecttable,'sqlval')
    firsttable = str(selectinput[2])
    firsttable = inputSani_dm.inputSanitizer(firsttable,'sqlval')
    subval = str(selectinput[3])
    subval = inputSani_dm.inputSanitizer(subval,'sqlval')
    subtable = str(selectinput[4])
    subtable = inputSani_dm.inputSanitizer(subtable,'sqlval')
    wherecol = str(selectinput[5])
    wherecol = inputSani_dm.inputSanitizer(wherecol,'sqlval')
    whereval = str(selectinput[6])
    whereval = inputSani_dm.inputSanitizer(whereval,'sqlval')
    # debug
    #for val in selectinput:
    #    print val

    #debug
    print "retrieving data"
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
        sqlStr = "SELECT " + selectvalue1 + " from " + selecttable + " where " + firsttable + " NOT in ( SELECT "\
                 + subval + " FROM " + subtable + " WHERE " + wherecol + " = '" + whereval +"');"
        #print sqlStr
        cur.execute(sqlStr)
        rows = cur.fetchall()
        # Make use we got at least one record
        if rows[0] is not None:
            for row in rows:
                resultlist.append(row[0])
    dbcon.commit()
    dbcon.close()
    return resultlist
