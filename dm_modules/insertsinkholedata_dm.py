__author__ = 'dleece'

#hard coding the dictionary values because it contains other values besides the sinkhole info
def parsemenudict(vdict):
    thislist=[]
    thisval=vdict['org_id']
    thislist.append(thisval)
    thisval=vdict['sh_fqdn']
    thislist.append(thisval)
    thisval=vdict['sh_ip']
    thislist.append(thisval)
    thisval=vdict['sh_desc']
    thisInsertStr = genSHsqlString(thislist)
    return thisInsertStr

def genSHsqlString(valuelist):
    valstr ="','".join(map(str,valuelist))
    sqlstr = "INSERT into view_sinkholes (org_id,sh_fqdn,sh_ip,sh_desc) VALUES ('" + valstr + "');"
    return  sqlstr


