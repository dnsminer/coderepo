__author__ = 'dleece'

import menudbinsert_dm, menudbselect_dm
def gentsigsql(orgid,viewname):
    keyname = "mineboss-" + viewname
    sqlstr = "INSERT into tsig_keys (org_id,tsig_name) VALUES ('" + str(orgid) +"','" +keyname +"');"
    #print sqlstr
    tsigresult=menudbinsert_dm.dbinsert(sqlstr)
    #print tsigresult
    if tsigresult == 1:
        print "tsig keys table entry created successfully"
    else:
        print "You may need to manually check the tsig_keys table"
    qresult = gettsigid(keyname)
    #qresult is a list, need to know number of columns if this is going to be a generic module
    return qresult

def gettsigid(thiskeyname):
    thisresultlist=[]
    selectlist=['tsig_id','tsig_keys','tsig_name',thiskeyname]
    thisresultlist = menudbselect_dm.dbRecordSelect(selectlist)
    #print "Length of array/list returned"
    #print len(thisresultlist)
    return thisresultlist


