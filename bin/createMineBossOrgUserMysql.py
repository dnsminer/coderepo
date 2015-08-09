#!/usr/bin/env python
#__author__ = 'dleece'
import sys, time,os, shutil, string, ConfigParser
import MySQLdb as mdb

DNSMinerHome='/opt/dnsminer-alpha'
dbUtilsHome = DNSMinerHome + '/utils/databases/'
dbcfg= DNSMinerHome + "/etc/dbConnections.cfg"


#def readConfigIni(cfgfile):
#    dbconnect=ConfigParser.ConfigParser()
#    dbconnect.read(cfgfile)

def ConfigSectionMap(section):
    dbcfgdict = {}
    cfgoptions = dbconnect.options(section)
    for cfgoption in cfgoptions:
        try:
            dbcfgdict[cfgoption] = dbconnect.get(section, cfgoption)
            if dbcfgdict[cfgoption] == -1:
                print "invalid parameter" + cfgoption
        except:
            print ('exception thrown, on %s' % cfgoption)
            dbcfgdict[cfgoption] = None
    return  dbcfgdict

def getDBConnectionValues():
    dbAdmin = raw_input("Enter application admin user,(the minion account): ")
    dbAdminPWD = raw_input("Enter application admin's  passwd: ")
    dbName = raw_input("What is the name of your application database? :")
    minInputVals = [dbAdmin,dbAdminPWD,dbName]
    return minInputVals

def getOrgInfo():
    inputtest=True
    while inputtest:
        orgName = raw_input("Enter the organization name please : ")
        orgName = inputSanitizer(orgName,'defstring')
        checkit= ['org_name','org_id',orgName]
        inputtest=dbRecordCheck(checkit)
    # reset for next input test
    inputtest=True
    while inputtest:
        orgContact  = raw_input("Enter org admin email address : ")
        orgContact = inputSanitizer(orgContact,'emailstring')
        checkit= ['org_contact','org_id',orgContact]
        inputtest=dbRecordCheck(checkit)
    orgAlert = raw_input("Enter the org monitoring email or sms address: ")
    orgAlert = inputSanitizer(orgAlert,'emailstring')
    orgPasswd = raw_input("Enter org admin's password : ")
    orgPasswd = inputSanitizer(orgPasswd,'password')
    orginputvals = [orgName,orgContact,orgAlert,orgPasswd]
    # Need to run inputs through sanitization
    return orginputvals

def inputSanitizer(inputstring,type):
    # sanitize based on whitelist and what type of input we're expecting
    charwl = string.ascii_letters + string.whitespace + string.digits
    if type == 'emailstring':
        charwl = charwl + '@._-'
    if type ==  'password':
        charwl = string.printable

    outstring = inputstring.strip()
    tmpchar=''
    for tchar in outstring:
        if tchar not in charwl:
            print "replacing invalid character " + tchar
            tchar = '_'
        tmpchar = tmpchar + tchar
    outstring = tmpchar
    return outstring

#def getDBTableDef(inputvals):
#    if inputvals[3] == 'mineboss':
#        resultVar = dbTblCreateMB(inputvals)
#    return resultVar
def dbRecordCheck(checkinput):
    print "checking existing database records"
    adminVar= ConfigSectionMap("SectionOne")['DatabaseUser']
    adminPwd= ConfigSectionMap("SectionOne")['DatabasePwd']
    ivDBName= ConfigSectionMap("SectionOne")['DatabaseName']
    checkcolumn = checkinput[0]
    checktable = checkinput[1]
    checkvalue = checkinput[2]
    var = False
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
        sqlStr = "SELECT count(" + checkcolumn +") from " + checktable + " WHERE " + checkcolumn + " = " + checkvalue
        checkresult = cur.fetchone()
        if checkresult is not None:
            print "Sorry, that record appears to be in use, please provide a different value"
            var= True
    dbcon.commit()
    dbcon.close()
    return var



def dbTblCreateMB(inputvals):
    print "creating database tables for mineboss application"
    adminVar=inputvals[0]
    adminPwd=inputvals[1]
    ivDBName=inputvals[2]
    # Open the SQL script to be used for table creation
    sqlfile = dbUtilsHome + 'mbtables.sql'
    try:
        fh = open(sqlfile)
    except:
        print "SQL tables file not available"
        return


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
        for sqlStr in fh:
            if sqlStr.strip():
                #print sqlStr
                cur.execute (sqlStr)
    dbcon.commit()
    dbcon.close()
    fh.close()
    var = 'Creating mineboss database tables done'
    return var

# --- main -----------------------------------


dbconnect=ConfigParser.ConfigParser()
dbconnect.read(dbcfg)

#readConfigIni(dbcfg)
getOrgInfo()
#newtblvals=getDBConnectionValues()
#print getDBTableDef(newtblvals)