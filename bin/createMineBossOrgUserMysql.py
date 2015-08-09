#!/usr/bin/env python
#__author__ = 'dleece'
import sys
import string
import ConfigParser
import bcrypt
from itertools import izip

# noinspection PyUnresolvedReferences
import MySQLdb as mdb

DNSMinerHome='/opt/dnsminer-alpha'
dbUtilsHome = DNSMinerHome + '/utils/databases/'
dbcfg= DNSMinerHome + "/etc/dbConnections.cfg"


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

# Could use this as a check to handle the lack of a database config file
def getDBConnectionValues():
    dbAdmin = raw_input("Enter application admin user,(the minion account): ")
    dbAdminPWD = raw_input("Enter application admin's  passwd: ")
    dbName = raw_input("What is the name of your application database? :")
    dbType = raw_input("What type of database is this (mysql|postgres)? :")
    minInputVals = [dbType,dbName,dbAdmin,dbAdminPWD]
    return minInputVals

def getOrgInfo():
    inputtest=True
    while inputtest:
        orgName = raw_input("Enter the organization name please : ")
        orgName = inputSanitizer(orgName,'defstring')
        checkit= ['org_name','org_info',orgName]
        inputtest=dbRecordCheck(checkit)
    # reset for next input test
    inputtest=True
    while inputtest:
        orgContact  = raw_input("Enter org admin email address : ")
        orgContact = inputSanitizer(orgContact,'emailstring')
        checkit= ['org_contact','org_info',orgContact]
        inputtest=dbRecordCheck(checkit)
    orgAlert = raw_input("Enter the org monitoring email or sms address: ")
    orgAlert = inputSanitizer(orgAlert,'emailstring')
    orgPasswd = raw_input("Enter org admin's password : ")
    orgPasswd = inputSanitizer(orgPasswd,'password')
    orgPasswd = genBcrpytHash(orgPasswd)
    orginputvals = ['org_name',orgName,'org_contact',orgContact,'alert_contact',orgAlert,'pwd',orgPasswd]
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

def dbRecordCheck(checkinput):
    print "checking existing database records"
    # by default config parser converts keys to lowercase , https://docs.python.org/2/library/configparser.html
    adminVar= ConfigSectionMap("SectionOne")['databaseuser']
    adminPwd= ConfigSectionMap("SectionOne")['databasepwd']
    ivDBName= ConfigSectionMap("SectionOne")['databasename']
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
        sqlStr = "SELECT count(1) from " + checktable + " WHERE " + checkcolumn + " = '" + checkvalue +"';"
        cur.execute(sqlStr)
        if cur.fetchone()[0]:
            print "Sorry, that record appears to be in use, please provide a different value"
            var= True
    dbcon.commit()
    dbcon.close()
    return var

def createSQLInsertDict(inputvals):
    # broke this out from the main org input collection to reduce clutter and allow debugging
    iraw=iter(inputvals)
    insertdict = dict(izip(iraw,iraw))
    #for key, value in insertdict.iteritems():
    #    print "Column: " + key
    #    print "Value: " + value
    return insertdict


def dbTblInsert(insertdict,dbtable):
    # by default config parser converts keys to lowercase , https://docs.python.org/2/library/configparser.html
    adminVar= ConfigSectionMap("SectionOne")['databaseuser']
    adminPwd= ConfigSectionMap("SectionOne")['databasepwd']
    ivDBName= ConfigSectionMap("SectionOne")['databasename']
    var = 'Record inserted successfully'

    columnlist = []
    valuelist = []
    for key, value in insertdict.iteritems():
        #print "Column: " + key
        columnlist.append(key)
        #print "Value: " + value
        valuelist.append(value)
    valstring ="','".join(valuelist)  # need the ticks for sql insert to work in mysql
    colstring =",".join(columnlist)
    sqlStrI = "INSERT INTO " + dbtable + "(" + colstring +") VALUES ('" + valstring +"');"
    #print sqlStrI
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
        #for sqlStr in fh:
        #    if sqlStr.strip():
        #        #print sqlStr
        cur.execute (sqlStrI)
    dbcon.commit()
    dbcon.close()
    return var

def genBcrpytHash(plainString):
    hashedpwd=bcrypt.hashpw(plainString,bcrypt.gensalt(14))
    return hashedpwd
# --- main -----------------------------------

#readConfigIni(dbcfg)  ( convert to function )
dbconnect=ConfigParser.ConfigParser()
dbconnect.read(dbcfg)

# gather org input, outputs an array of table columns and values to be feed into a dictionary
orginfoinputs=getOrgInfo()
# Parse input array into SQL return a dictionary
dbinsertdict=createSQLInsertDict(orginfoinputs)

# feed dictionary into sql insert
dbTblInsert(dbinsertdict,'org_info')
