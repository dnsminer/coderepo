#!/usr/bin/env python
__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys
import MySQLdb as mdb
from dm_modules import cfgparse_dm, bulkdbselect1w_dm,bulkdbselectJoin1w_dm, dbselectSubqueryExclude_dm

DNSMinerHome='/opt/dnsminer-alpha'
dbcfg= DNSMinerHome + "/etc/siteSpecific.cfg"
rpzbase = getrpzbase()


def genRPZFiles(oidlist):
    # use the list of distinct org ids, search for all views per org id
    # extract view name and sink hole id, use sh_id to get sh_fqdn
    # pass org_id,view_name,def_sh_fqdn to a function that writes out an RPZ file to a specific directory to
    for item in oidlist:
        if item:
            orgid=item[0]
            # get org wide, dom list,
            # remove white list entries from public list

            # add black list entries, store as a temp list pubwhiteblackdomlist
            makeorgpwblist(orgid)
            # Get view metadata
            viewmdata = getViewRPZdata(orgid)
            # Debug
            #for rows in viewmdata:
            #    print "--> Org ID " + str(orgid) + " view name, view ID, sh fqdn"
            #    for i in range(len(rows)):
            #        print rows[i]

            # Generate view specific header

            # Open file handle, use rpzbase/orgid/view.rpz as path,
            # write header
            # iterate through pubwhiteblackdomlist and add view specific sh_fqdn as cname per line
            # rpz should have dom cname fqdn.  and *.dom cname fqdn.  ( end dots important)

            #close file handle,
            # do next view
            # if no more views go to next org id




    return


def makeorgpwblist(oid):
    pubwhtblk = []
    # Remove any white list domains from public list and write to temp list
    selstr = "tlist_domains.domain"
    stbl = "tlist_domains"
    sval = "tlist_domains.domain"
    sval2 = "wl_domain"
    stbl2 = "whitelist_domain"
    wval = "whitelist_domain.org_id"
    slctlist=[selstr,stbl,sval,sval2,stbl2,wval,oid]
    pubwhtblk = dbselectSubqueryExclude_dm.dbRecordSelect(selstr)
    # debug
    print "public minus white list :" + str(len(pubwhtblk))
    # select black list doms and append to list
    selstr = "bl_domain"
    stbl = "blacklist_domains"
    slctlist = [selstr,stbl,oid]
    tmpblk = bulkdbselect1w_dm.dbRecordSelect(slctlist)
    if tmpblk[0]:
        for val in tmpblk:
            pubwhtblk.append(val[0])
    print "public minus white list  plust black:" + str(len(pubwhtblk))


    return pubwhtblk


def getViewRPZdata(oid):
    # use Org ID in sql join with where to get data for rpz needed by each view
    selstr = "bind_views.org_id,bind_views.view_name,bind_views.view_id,view_sinkholes.sh_fqdn"
    stbl = "bind_views"
    jtbl = "view_sinkholes"
    jv1 = "bind_views.def_sh_id"
    jv2 = "view_sinkholes.sinkhole_id"
    wval = "bind_views.org_id"
    slctlist=[selstr,stbl,jtbl,jv1,jv2,wval,oid]
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


def getrpzbase():
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionThree')
    dirbase = thisCfgDict['rpzbase']
    return dirbase

def main():
    thisoidlist=getOrgID()

    genRPZFiles(thisoidlist)

if __name__ == "__main__": main()