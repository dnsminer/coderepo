__author__ = 'dleece'
import cfgparse_dm
import MySQLdb as mdb
import sys

#DNSMinerHome='/opt/dnsminer-alpha'
DNSMinerHome='/opt/dnsminer-alpha'
#dbUtilsHome = DNSMinerHome + '/utils/databases/'
dbcfg= DNSMinerHome + "/etc/dbConnections.cfg"

def dbinsert(insertstr):
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionOne')
    adminVar = thisCfgDict['databaseuser']
    adminPwd= thisCfgDict['databasepwd']
    ivDBName = thisCfgDict['databasename']

    try:
        dbcon = mdb.connect('localhost',adminVar,adminPwd,ivDBName)
        #print "connected in insert function"
    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)

    with dbcon:
        cur=dbcon.cursor()
        sqlStr = "USE " + ivDBName
        cur.execute(sqlStr)
        sqlStr = insertstr
        #print sqlStr
        cur.execute(sqlStr)
        insresult=(cur.rowcount)
    dbcon.commit()
    dbcon.close()
    return insresult