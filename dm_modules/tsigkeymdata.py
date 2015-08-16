__author__ = 'dleece'

import menudbinsert_dm, menudbselect_dm
def gentsigsql(orgid,viewname):
    keyname = "mineboss-" + viewname
    sqlstr = "INSERT into tsig_keys (org_id,tsig_name) VALUES ('" + str(orgid) +"','" +viewname +"';"
    tsigresult=menudbinsert_dm.dbinsert(sqlstr)
    print tsigresult
    qresult = gettsigid(keyname)
    #qresult = str(qresult)
    return qresult

def gettsigid(thiskeyname):
    thisresultlist=[]
    selectlist=['tsig_id','tsig_keys','tsig_name',thiskeyname]
    thisresultlist = menudbselect_dm.dbRecordSelect(selectlist)
    for row in thisresultlist:
        print row
    return


