#!/usr/bin/env python
#__author__ = 'dleece'
import sys
import string
import ConfigParser
import socket
import struct
from itertools import izip
import random

import bcrypt
from dm_modules import cfgparse_dm, dbchk_dm, inputSani_dm, iptoint_dm





# noinspection PyUnresolvedReferences
import MySQLdb as mdb

DNSMinerHome='/opt/dnsminer-alpha'
dbUtilsHome = DNSMinerHome + '/utils/databases/'
dbcfg= DNSMinerHome + "/etc/dbConnections.cfg"
nodecfg = DNSMinerHome + "/etc/nodes.cfg"

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
    menuchoices = ['view','blacklist','whitelist','exit']
    menurequest = []
    if inputstring not in menuchoices:
        print "Sorry, that is not a valid menu choice"
        menurequest = ['invalid']
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
    if type == 'view':
        charwl = string.ascii_letters + string.digits + '-_'

    outstring = inputstring.strip()
    tmpchar=''
    for tchar in outstring:
        if tchar not in charwl:
            print "replacing invalid character " + tchar + " with an underscore _ "
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



def checkauthn(checkinput):
    print "checking credentials supplied"
    # by default config parser converts keys to lowercase , https://docs.python.org/2/library/configparser.html
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionOne')
    #print thisCfgDict
    #adminVar= ConfigSectionMap("SectionOne")['databaseuser']
    adminVar = thisCfgDict['databaseuser']
    #adminPwd= ConfigSectionMap("SectionOne")['databasepwd']
    adminPwd= thisCfgDict['databasepwd']
    #ivDBName= ConfigSectionMap("SectionOne")['databasename']
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
    #print thisCfgDict
    #adminVar= ConfigSectionMap("SectionOne")['databaseuser']
    #adminPwd= ConfigSectionMap("SectionOne")['databasepwd']
    #ivDBName= ConfigSectionMap("SectionOne")['databasename']
    thisCfgDict = cfgparse_dm.opencfg(dbcfg,'SectionOne')
    adminVar = thisCfgDict['databaseuser']
    adminPwd= thisCfgDict['databasepwd']
    ivDBName = thisCfgDict['databasename']
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
            print "\nCustomize Mineboss application settings to suit your organization"
            print "menu choices are: view, blacklist, whitelist, exit\n"
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
        doMWView(doMWList)
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

def inputView(vname):
    #check for no spaces and make sure it's not already used.
    #viewName = inputSanitizer(vname,'view')
    viewName = inputSani_dm.inputSanitizer(vname,'view')
    print "confirming view name is unique in the system"
    checkviewname=['view_name','bind_views',viewName]  # Column, table, value
    #boolVar= dbRecordCheck(checkviewname)
    boolVar= dbchk_dm.dbRecordCheck(checkviewname)
    checkviewlist = [boolVar,viewName]   # return result of uniqueness test and view name value if it's usable.
    return  checkviewlist

def dotQuadtoInt(dquad):
    dquad = inputSani_dm.inputSanitizer(dquad,'ip')
    if dquad =='invalid_format':
        ipInt = 10
    else:
        ipInt = struct.unpack('>L',socket.inet_aton(dquad))[0]
    #print dquad
    #print ipInt
    return  ipInt

def intTodotQuad(ipint):
    dotquad = socket.inet_ntoa(struct.pack('>L',ipint))
    return  dotquad
def doMWView(mwlist):
    print "do menu view"
    for val in mwlist:
        print val
    # create a dictionary to collect all the results to generate SQL insert or update
    viewDict = dict()
    if mwlist[1] != 'update':
        # start the menu to gather view details
        viewmenuactive=True
        while viewmenuactive:
            getviewname = True
            while getviewname:
                print "\nYou are about to create a new Bind View and related zone files."
                print "\nThe view must be a unique name within the system,"
                print "it must also be a single word with no spaces, letters, dashes, underscores and digits ok"
                uvinput = raw_input("Enter view name: ")
                uvinput = uvinput.strip().lower()
                vresult = inputView(uvinput) # needed to get the status, using length of list to avoid global vars
                if not vresult[0]:
                    viewDict['view_name'] = vresult[1]
                    getviewname = False
            getmonip = True
            while getmonip:
                uvlinput = raw_input("What is the internal IP for the monitoring application? ( dotted quad): ")
                #uvlinput = dotQuadtoInt(uvlinput)
                uvlinput = iptoint_dm.dotQuadtoInt(uvlinput)
                if uvlinput > 10:
                    viewDict['sh_ip'] = uvlinput
                    getmonip = False
                else:
                    print "hmm, looks like that wasn't a dotted quad, EG 172.16.28.7, please enter again"

            getviewip = True
            viewClientIPList=[]
            print "\nDefine the the source IP(s)/ subnets for the recursive clients using this view( dotted quad or cidr): "
            while getviewip:
                addrtype= raw_input("Is this a single IP or subnet (ip|cidr)? ")
                addrtype = addrtype.strip().lower()
                if addrtype == 'ip':
                    uvsinput = raw_input("What is the source IP for the recursive clients?( dotted quad): ")
                    uvsinput = inputSani_dm.inputSanitizer(uvsinput,'ip')
                    if uvsinput == 'invalid_format':
                        print "hmm, looks like that wasn't a dotted quad, EG 172.16.28.7, please enter again"
                        continue
                else:
                    uvsinput = raw_input("What is the source subnet for the recursive clients?( cidr notation): ")
                    uvsinput = inputSani_dm.inputSanitizer(uvsinput,'cidr')
                    if uvsinput == 'invalid_format':
                        print "hmm, looks like that wasn't cidr notation, EG 172.16.28.0/26, please enter again"
                        continue
                viewClientIPList.append(uvsinput)
                nextIP = raw_input("Do you need to add another IP address (yes|no)?")
                nextIP = nextIP.strip().lower()
                if nextIP == 'no':
                    getviewip = False
                # build IPs and cidr into a CSV string to be used with views
                rcsvclients  = ",".join(map(str,viewClientIPList))
            viewDict['view_src_ip'] = rcsvclients  # build into an ACL data structure later on
            viewmenuactive = False
        print viewDict





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
    return


def genRPZCname():
    # Each view needs an authoritiative zone to resolve the cname. Although the view could be reused per view
    # generating random makes it very difficult for anyone to guess the name and potentially probe for zone contents.
    dom = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    dom = dom + '.local'
    return  dom

# --- main -----------------------------------

#readConfigIni(dbcfg)  ( convert to function )
dbconnect=ConfigParser.ConfigParser()
dbconnect.read(dbcfg)

# gather org input, outputs a boolean and if true and org_id
loginresult=userLogin()

userMenu(loginresult) # allow user to modify and update various fields
# All database changes done via functions called from doMenuSelect