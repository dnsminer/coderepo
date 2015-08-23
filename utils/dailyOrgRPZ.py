#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys
import MySQLdb as mdb
from dm_modules import cfgparse_dm, bulkdbselect1w_dm,bulkdbselectJoin1w_dm

DNSMinerHome='/opt/dnsminer-alpha'
dbcfg= DNSMinerHome + "/etc/siteSpecific.cfg"

def getViewIDOrg(oidlist):
    # use the list of distinct org ids, search for all views per org id
    # extract view name and sink hole id, use sh_id to get sh_fqdn
    # pass org_id,view_name,def_sh_fqdn to a function that writes out an RPZ file to a specific directory to
    for item in oidlist:
        if item:
            orgid=item[0]
            viewmdata = getViewRPZdata(orgid)
            #
            for rows in viewmdata:
                print "--> Org ID " + str(orgid) + " view name, view ID, sh fqdn"
                for i in range(len(rows)):
                    print rows[i]
    return

def getViewRPZdata(oid):
    # use Org ID in sql join with where to get data for rpz needed by each view
    selstr = "bind_views.org_id,bind_views.view_name,bind_views.view_id,view_sinkholes.sh_fqdn"
    stbl = "bind_views"
    jtbl = "view_sinkholes"
    jv1 = "bind_views.def_sh_id"
    jv2 = "view_sinkholes.sinkhole_id"
    wval = "bind_views.org_id"
    slctlist=[selstr,stbl,jtbl,jv1,jv2,wval,orgid]
    allorgViews = bulkdbselectJoin1w_dm.dbRecordSelect(slctlist)

    return allorgViews


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