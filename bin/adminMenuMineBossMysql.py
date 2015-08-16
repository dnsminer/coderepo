#!/usr/bin/env python
#__author__ = 'dleece'
# Set the path to include the dns miner modules directory
import sys
DNSMinerHome='/opt/dnsminer-alpha'
dm_modules = DNSMinerHome + "/dm_modules"
#print dm_modules


from itertools import izip
import bcrypt
from dm_modules import cfgparse_dm, doMView_dm, inputSani_dm, doMGenOrgView

# noinspection PyUnresolvedReferences
import MySQLdb as mdb

#DNSMinerHome='/opt/dnsminer-alpha'
dbUtilsHome = DNSMinerHome + '/utils/databases/'
dbcfg= DNSMinerHome + "/etc/dbConnections.cfg"
nodecfg = DNSMinerHome + "/etc/nodes.cfg"

def userLogin():
    credtest=False
    while not credtest:
        orgContact = raw_input("Enter your org contact email  : ")
        #orgContact = inputSanitizer(orgContact,'emailstring')
        orgContact = inputSani_dm.inputSanitizer(orgContact,'emailstring')
        orgPasswd = raw_input("Enter org admin's password : ")
        orgPasswd = inputSani_dm.inputSanitizer(orgPasswd,'password')
        #orgPasswd = inputSanitizer(orgPasswd,'password')
        credlist= [orgContact,orgPasswd]
        credauthz = checkauthn(credlist) # return boolean for authenticated and org number ( honey token this?)
        if not credauthz[0]:
            print "credentail failure"
        else:
            credtest = True
    return credauthz

def inputMenu(inputstring):
    menuchoices = ['view','genorgview','blacklist','whitelist','exit']
    menurequest = []
    if inputstring not in menuchoices:
        print "Sorry, that is not a valid menu choice"
        menurequest = ['invalid']
    else:
        if inputstring == 'exit':
            menurequest = []
        else:
            operrequest = inputstring
            method = raw_input("create new or update existing (new|update)? :")
            menurequest = [operrequest,method]
    return menurequest


def checkauthn(checkinput):
    print "checking credentials supplied"
    # by default config parser converts keys to lowercase , https://docs.python.org/2/library/configparser.html
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionOne')
    adminVar = thisCfgDict['databaseuser']
    adminPwd= thisCfgDict['databasepwd']
    ivDBName = thisCfgDict['databasename']
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
        #print sqlStr
        cur.execute(sqlStr)
        storedpwd = cur.fetchone()[0]
        #print storedpwd
        # pass the stored hash to checkPW(st
        testPwd = checkPwd(storedpwd,clearpasswd)
        authzlist[0] = testPwd
        if  authzlist[0]:
            print "cool, you have a valid set of creds "
            # from here we'd generated a second query to grab the org_id and over write authzlist[1]
            sqlStr = "SELECT org_id from org_info WHERE org_contact = '" + contactEmail +"';"
            cur.execute(sqlStr)
            storedOrgId = cur.fetchone()[0]
            #print storedOrgId
            authzlist[1]= storedOrgId
    dbcon.commit()
    dbcon.close()
    return authzlist

#def createSQLInsertDict(inputvals):
#    # broke this out from the main org input collection to reduce clutter and allow debugging
#    iraw=iter(inputvals)
#    insertdict = dict(izip(iraw,iraw))
#    #for key, value in insertdict.iteritems():
#    #    print "Column: " + key
#    #    print "Value: " + value
#    return insertdict


#def dbTblInsert(insertdict,dbtable):
#    # by default config parser converts keys to lowercase , https://docs.python.org/2/library/configparser.html
#    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionOne')
#    adminVar = thisCfgDict['databaseuser']
#    adminPwd= thisCfgDict['databasepwd']
#    ivDBName = thisCfgDict['databasename']
#    var = 'Record inserted successfully'
#
#    columnlist = []
#    valuelist = []
#    for key, value in insertdict.iteritems():
#        #print "Column: " + key
#        columnlist.append(key)
#        #print "Value: " + value
#        valuelist.append(value)
#    valstring ="','".join(valuelist)  # need the ticks for sql insert to work in mysql
#    colstring =",".join(columnlist)
#    sqlStrI = "INSERT INTO " + dbtable + "(" + colstring +") VALUES ('" + valstring +"');"
#    #print sqlStrI
#    try:
#        dbcon = mdb.connect('localhost',adminVar,adminPwd,ivDBName)
#        #print "connected"
#    except mdb.Error, e:
#        print e.args[0]
#        sys.exit(1)
#
#    with dbcon:
#        cur=dbcon.cursor()
#        sqlStr = "USE " + ivDBName
#        cur.execute(sqlStr)
#        cur.execute (sqlStrI)
#    dbcon.commit()
#    dbcon.close()
#    return var

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
            print "\nCustomize Mineboss application settings to suit your organization"
            print "menu choices are: view, genorgview, blacklist, whitelist, exit\n"
            uinput = raw_input("Enter choice: ")
            uinput = uinput.strip().lower()
            mresult = inputMenu(uinput) # needed to get the status, using length of list to avoid global vars
            if not mresult:
                menuactive = False
                print "\nThankyou, goodbye\n"
            elif mresult[0] == 'invalid':  # catch the bad input and keep menu open for retry
                menuactive = True
            else:
                #print azlist[1]
                doMenuSelect(mresult,azlist[1])
    else:
        print "invalid credentials and something funny is going on here, quitting now"
        exit()
    return

def doMenuSelect(menulist,orgid):
    # sort of a long way around sanitizing the input and then calling the SQL function required
    if menulist[0] == 'view':
        #if menulist[1] == 'update':
        doMWList = [menulist[0],menulist[1],orgid]
        doMView_dm.doView(doMWList)
    elif menulist[0] == 'genorgview':
        # debug
        #print "\nGenerating a view file for org " + str(orgid)
        doMGenOrgView.doGenView(orgid)
    elif menulist[0] == 'blacklist':
        if menulist[1] == 'update':
            print "\nsend blacklist,update to blacklist function for org " + str(orgid)
        else:
            print "\nsend blacklist,new to blacklist function for org " + str(orgid)
    else:
        if menulist[1] == 'update':
            print "\nsend whitelist,update to whitelist function for org " + str(orgid)
        else:
            print "\nsend whitelist,new to whitelist function for org " + str(orgid)
    return


    # store all answers in a dictinary and then use dictionry to create SQL
    # prompt for view name,   check for no spaces and make sure it's not already used.
    # prompt for ip address inside org to be populated into the zone file
    # prompt for ip address view traffic will be coming from.  Make this a list which could be turned into an ACL.
    # generate tsig key ( seperate function)
    # generate random domain name
    # build zone file using random domain name and local IP address
    # if update:
    # prompt for view name,   check for no spaces and make sure it's not already used.
    # prompt for ip address inside org to be populated into the zone file
    # prompt for ip address view traffic will be coming from.  Make this a list which could be turned into an ACL.
    #return




# --- main -----------------------------------
# gather org input, outputs a boolean and if true and org_id
loginresult=userLogin()

userMenu(loginresult) # allow user to modify and update various fields
# All database changes done via functions called from doMenuSelect