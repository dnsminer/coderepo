__author__ = 'dleece'


import bulkdbselectJoin1wExclude_dm
#acl firstfireACL { !key mineboss-underground-hosting; key mineboss-firstfire; 104.37.193.75; 45.58.36.25; 104.131.209.101; };

# use viewID to get teh not keys and return list of key names
def genACL(viewdict):
    thisvid=viewdict['view_id']
    thisacl = viewdict['acl_name']
    aclstr = "acl " + thisacl + "( "
    exkeylist=getexcludekeys(thisvid)
    if exkeylist[0]:
        for val in exkeylist:
            print val[0]
            aclstr = aclstr + "!key " + val[0] + ";"

    print aclstr

    return

def getexcludekeys(vid):
#select tsig_name from tsig_keys inner join bind_views on tsig_keys.tsig_id=bind_views.tsig_id where bind_views.view_id !=3 ;
    # use view ID in sql join with where to get data for rpz needed by each view
    selstr = "tsig_keys.tsig_name"
    stbl = "tsig_keys"
    jtbl = "bind_views"
    jv1 = "tsig_keys.tsig_id"
    jv2 = "bind_views.tsig_id"
    wval = "bind_views.view_id"
    slctlist=[selstr,stbl,jtbl,jv1,jv2,wval,vid]
    excludekeys = bulkdbselectJoin1wExclude_dm.dbRecordSelect(slctlist)
    return excludekeys


