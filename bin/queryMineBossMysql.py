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


def userLogin():
    credtest=False
    while not credtest:
        orgContact = raw_input("Enter your org contact email  : ")
        orgContact = inputSanitizer(orgContact,'emailstring')
        orgPasswd = raw_input("Enter org admin's password : ")
        orgPasswd = inputSanitizer(orgPasswd,'password')
        credlist= [orgContact,orgPasswd]
        credauthz = checkauthn(credlist) # return boolean for authenticated and org number ( honey token this?)
        if not credauthz[0]:
            print "credentail failure"
        else:
            credtest = True

    return credauthz

def inputMenu(inputstring):
    menuchoices = ['view','blacklist','whitelist','exit']
    menurequest = []
    if inputstring not in menuchoices:
        print "Sorry, that is not a valid menu choice"
        menurequest = []
    else:
        if inputstring == 'exit':
            menurequest = []
        else:
            operrequest = inputstring
            method = raw_input("creaste new or update existing (new|update)? :")
            menurequest = [operrequest,method]
    return menurequest


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

def checkauthn(checkinput):
    print "checking credentials supplied"
    # by default config parser converts keys to lowercase , https://docs.python.org/2/library/configparser.html
    adminVar= ConfigSectionMap("SectionOne")['databaseuser']
    adminPwd= ConfigSectionMap("SectionOne")['databasepwd']
    ivDBName= ConfigSectionMap("SectionOne")['databasename']
    contactEmail = checkinput[0]
    clearpasswd = checkinput[1]

    authzlist = [False,8287]
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
        sqlStr = "SELECT pwd from org_info WHERE org_contact = '" + contactEmail +"';"
        print sqlStr
        cur.execute(sqlStr)
        storedpwd = cur.fetchone()[0]
        print storedpwd
        # pass the stoed hash to checkPW(st
        testPwd = checkPwd(storedpwd,clearpasswd)
        authzlist[0] = testPwd
        if  authzlist[0]:
            print "cool, you have a good set of creds "
            # from here we'd generated a second query to grab the org_id and over write authzlist[1]
            sqlStr = "SELECT org_id from org_info WHERE org_contact = '" + contactEmail +"';"
            cur.execute(sqlStr)
            storedOrgId = cur.fetchone()[0]
            print storedOrgId
            authzlist[1]= storedOrgId
    dbcon.commit()
    dbcon.close()
    return authzlist

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

def checkPwd(storedpwd,clearpasswd):
    pwdtest = storedpwd==bcrypt.hashpw(clearpasswd,storedpwd)
    return pwdtest

def genBcrpytHash(plainString):
    hashedpwd=bcrypt.hashpw(plainString,bcrypt.gensalt(14))
    return hashedpwd

def userMenu(azlist):
    # accepts a boolean and integer, boolean is proof of authentication and org id is required for all user menu items
    if azlist[0]:
        menuactive=True
        while menuactive:
            print "Customize Mineboss application settings to suit your organization"
            print "menu choices are: view, blacklist, whitelist, exit"
            uinput = raw_input("Enter choice: ")
            uinput = uinput.strip().lower()
            mresult = inputMenu(uinput) # needed to get the status, using lenth of list to avoid global vars
            if not mresult:
                menuactive = False
            else:
                for val in mresult:
                    print val
    else:
        print "invalid credentials"
        exit()
    return

# --- main -----------------------------------

#readConfigIni(dbcfg)  ( convert to function )
dbconnect=ConfigParser.ConfigParser()
dbconnect.read(dbcfg)

# gather org input, outputs a boolean and if true and org_id
loginresult=userLogin()

#
userMenu(loginresult) # allow user to modify and update various fields
# All database changes done via functions
# Parse input array into SQL return a dictionary
#dbinsertdict=createSQLInsertDict(orginfoinputs)


