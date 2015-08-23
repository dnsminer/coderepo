#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys
import MySQLdb as mdb
from dm_modules import cfgparse_dm, bulkdbselect_dm

DNSMinerHome='/opt/dnsminer-alpha'
dbcfg= DNSMinerHome + "/etc/siteSpecific.cfg"

def getViewIDOrg(oidlist):
    # use the list of distinct org ids, search for all views per org id
    # extract view name and sink hole id, use sh_id to get sh_fqdn
    # pass org_id,view_name,def_sh_fqdn to a function that writes out an RPZ file to a specific directory to
    for item in oidlist:
        if item:
            orgid=item[0]
            selstr = "view_name,def_sh_id"
            slctlist=[selstr,'bind_views','org_id',orgid]
            allorgViews = bulkdbselect_dm.dbRecordSelect(slctlist)
            for rows in allorgViews:
                print "--> Org ID " + str(orgid) + " view name, sinkhole ID"
                for i in range(len(rows)):
                    print rows[i]





def getOrgID():
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionOne')
    adminVar = thisCfgDict['databaseuser']
    adminPwd= thisCfgDict['databasepwd']
    ivDBName = thisCfgDict['databasename']
    #debug
    print "collecing org IDs"
    oidrows = []
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
        sqlStr = "SELECT DISTINCT org_id FROM bind_views;"
        cur.execute(sqlStr)
        rows = cur.fetchall()
        # Make use we got at least one record
        if rows[0] is not None:
            for row in rows:
                oidrows.append(row)
    dbcon.commit()
    dbcon.close()
    return oidrows

def main():
    thisoidlist=getOrgID()
    getViewIDOrg(thisoidlist)

if __name__ == "__main__": main()