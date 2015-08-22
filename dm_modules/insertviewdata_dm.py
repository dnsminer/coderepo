__author__ = 'dleece'

import menudbinsert_dm, menudbselect_dm
def genviewgsql(viewsqllist):

    valstr ="','".join(map(str,viewsqllist))
    sqlstr = "INSERT into bind_views (org_id,view_name,def_sh_id,view_src_acl_ips,view_desc,tsig_id) VALUES ('" + valstr +"');"
    #print sqlstr
    viewresult=menudbinsert_dm.dbinsert(sqlstr)
    #print tsigresult
    if viewresult == 1:
        print "bind view data table entry created successfully"
    else:
        print "You may need to manually check the bind_views table"

    qresult = getviewid(viewsqllist[1])
    #qresult is a list, need to know number of columns if this is going to be a generic module
    return qresult

def getviewid(thiskeyname):
    thisresultlist=[]
    selectlist=['view_id','bind_views','view_name',thiskeyname]
    thisresultlist = menudbselect_dm.dbRecordSelect(selectlist)
    #print "Length of array/list returned"
    #print len(thisresultlist)
    return thisresultlist


