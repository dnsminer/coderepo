__author__ = 'dleece'

import menudbinsert_dm, menudbselect_dm, iptoint_dm, dbchk_dm
from datetime import datetime, date
def genbworgsql(orgid,viewname,shid):
    # debug
    #print "executing white list domainsql"
    # Make sure there is no existing lists before going to the trouble of creating the SQL, additional views
    # will use the same white and black lists. This could change in a later release
    bwresult = inputOrgId(orgid) # needed to get the status, using length of list to avoid global vars
    if bwresult[0]:
        print "\nWarning\nThat org id appears to have white and black lists already,"
        print "if this is an additional view for the same organiation this message can be ignored"
        return
    # values for SQL statements
    defwhitedom =  viewname + "-white.local"
    defwhitehost = "ignore." + defwhitedom
    defblackdom = viewname + "-black.local"
    defblackhost = "confirm." + defblackdom
    defdesc = "Default entry created on setup, not expected to be used"
    dstamp = date.isoformat(datetime.now())
    defip = str(iptoint_dm.dotQuadtoInt('198.51.100.187'))
    deftype = 'A'
    #
    # Whitelist domain
    sqlstr = "INSERT into whitelist_domain (org_id,wl_domain,wld_desc,wld_date) VALUES ('" + str(orgid) +"','" + defwhitedom +"','" + defdesc +"','" + dstamp +"');"
    print sqlstr
    wldresult=menudbinsert_dm.dbinsert(sqlstr)
    if wldresult == 1:
        print "Default white list domain table entry for this organization created successfully"
    else:
        print "You may need to manually check the whitelist_domain table"
    # Whitelist host
    sqlstr = "INSERT into whitelist_host (org_id,wlh_type,wl_host,wlh_ip,wlh_desc,wlh_date) VALUES ('"\
             + str(orgid) + "','" + deftype + "','" + defwhitehost + "','" + defip + "','" + defdesc +"','" + dstamp +"');"
    print sqlstr
    wldresult=menudbinsert_dm.dbinsert(sqlstr)
    if wldresult == 1:
        print "Default white list host table entry for this organization created successfully"
    else:
        print "You may need to manually check the whitelist_host table"
        # Blacklist domain
    sqlstr = "INSERT into blacklist_domain (org_id,bl_domain,bld_sinkhole,bld_desc,bld_date) VALUES ('" \
             + str(orgid) +"','" + defblackdom + "','" + str(shid) + "','" + defdesc +"','" + dstamp +"');"
    print sqlstr
    wldresult=menudbinsert_dm.dbinsert(sqlstr)
    if wldresult == 1:
        print "Default black list domain table entry for this organization created successfully"
    else:
        print "You may need to manually check the blacklist_domain table"
    # Blacklist host
    sqlstr = "INSERT into blacklist_host (org_id,blh_type,bl_host,blh_ip,blh_sinkhole,blh_desc,blh_date) VALUES ('"\
             + str(orgid) + "','" + deftype + "','" + defblackhost + "','" + defip + "','" + str(shid) + "','" + defdesc +"','" + dstamp +"');"
    print sqlstr
    wldresult=menudbinsert_dm.dbinsert(sqlstr)
    if wldresult == 1:
        print "Default black list host table entry for this organization created successfully"
    else:
        print "You may need to manually check the blacklist_host table"
    return wldresult


def inputOrgId(orgid):
    #make sure there is not already a list set for this org and bail if the org ID is not a valid long/int
    if type(orgid) == type(long()):
        oid=str(orgid)
    else:
        print "there may be a problem with the org id provided, please debug"
        exit()
    print "confirming there is no existing black or white list for this organization"
    checkorgbw=['org_id','whitelist_domain',oid]  # Column, table, value
    boolVar= dbchk_dm.dbRecordCheck(checkorgbw)
    checkviewlist = [boolVar,orgid]   # return result of uniqueness test and view name value if it's usable.
    return  checkviewlist