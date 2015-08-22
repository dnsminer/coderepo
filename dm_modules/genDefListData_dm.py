__author__ = 'dleece'

import menudbinsert_dm, menudbselect_dm, iptoint_dm
from datetime import datetime, date
def genbworgsql(orgid,viewname,shid):
    # debug
    print "executing white list domainsql"
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
    sqlstr = "INSERT into whitelist_host (org_id,wlh_type,wlh_host,wlh_ip,wlh_desc,wlh_date) VALUES ('"\
             + str(orgid) + "','" + deftype + "','" + defwhitehost + "','" + defip + "','" + defdesc +"','" + dstamp +"');"
    print sqlstr
    wldresult=menudbinsert_dm.dbinsert(sqlstr)
    if wldresult == 1:
        print "Default white list host table entry for this organization created successfully"
    else:
        print "You may need to manually check the whitelist_host table"
        # Blacklist domain
    sqlstr = "INSERT into blacklist_domain (org_id,bl_domain,bld_sinkhole,bld_desc,bld_date) VALUES ('" \
             + str(orgid) +"','" + defblackdom + "','" + shid + "','" + defdesc +"','" + dstamp +"');"
    print sqlstr
    wldresult=menudbinsert_dm.dbinsert(sqlstr)
    if wldresult == 1:
        print "Default black list domain table entry for this organization created successfully"
    else:
        print "You may need to manually check the blacklist_domain table"
    # Blacklist host
    sqlstr = "INSERT into whitelist_host (org_id,blh_type,bl_host,blh_ip,blh_sinkhole,blh_desc,blh_date) VALUES ('"\
             + str(orgid) + "','" + deftype + "','" + defblackhost + "','" + defip + "','" + shid + "','" + defdesc +"','" + dstamp +"');"
    print sqlstr
    wldresult=menudbinsert_dm.dbinsert(sqlstr)
    if wldresult == 1:
        print "Default black list host table entry for this organization created successfully"
    else:
        print "You may need to manually check the blacklist_host table"
    return wldresult