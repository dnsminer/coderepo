__author__ = 'dleece'

import menudbinsert_dm, menudbselect_dm
from datetime import datetime, date
def genbworgsql(orgid,viewname,shid):
    # values for SQL statements
    defwhitedom =  viewname + "-white.local"
    defwhitehost = "ignore." + defwhitedom
    defblackdom = viewname + "-black.local"
    defblacktest = "confirm." + defblackdom
    defdesc = "Default entry created on setup, not expected to be used"
    dstamp = date.isoformat(datetime.now())
    #
    sqlstr = "INSERT into whitelist_domain (org_id,wl_domain,wld_desc,wld_date) VALUES ('" + str(orgid) +"','" + defwhitedom +"','" + defdesc +"','" + dstamp +"');"
    print sqlstr
    wldresult=menudbinsert_dm.dbinsert(sqlstr)
    #print tsigresult
    if wldresult == 1:
        print "Default White list domain table entry for this organization created successfully"
    else:
        print "You may need to manually check the whitelist_domain table"
    #qresult = gettsigid(keyname)
    #qresult is a list, need to know number of columns if this is going to be a generic module
    return

#def gettsigid(thiskeyname):
#    thisresultlist=[]
#    selectlist=['tsig_id','tsig_keys','tsig_name',thiskeyname]
#    thisresultlist = menudbselect_dm.dbRecordSelect(selectlist)
#    #print "Length of array/list returned"
3    #print len(thisresultlist)
#    return thisresultlist
