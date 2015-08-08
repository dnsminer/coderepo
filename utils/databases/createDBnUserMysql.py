#!/usr/bin/env python
#__author__ = 'dleece'
import sys, time
import MySQLdb as mdb

def getCreateValues():
    dbAdmin = raw_input("Enter mysql admin user,(typically root): ")
    dbAdminPWD = raw_input("Enter mysql admin's  passwd: ")
    dbName = raw_input("What do you want to call your mineboss application database? :")
    print "\n You need to create an new account specifically for this application to access it's database,  "
    print " don't reuse the mysql root account, create a minion\n"
    dbMinionUser = raw_input("What is the application account name? : ")
    dnsMinionPWD = raw_input("Enter the password for  the database minion acct: ")
    minInputVals = [dbAdmin,dbAdminPWD,dbName,dbMinionUser,dnsMinionPWD]
    return minInputVals

def dbCreate(inputvals):
    print "creating database for mineboss application"
    adminVar=inputvals[0]
    adminPwd=inputvals[1]
    ivDBName=inputvals[2]
    try:
        dbcon = mdb.connect('localhost',adminVar,adminPwd,'mysql')
        #print "connected"
    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)

    with dbcon:
        cur=dbcon.cursor()
        cur.execute("USE mysql")
        createDBStr = "CREATE database IF NOT EXISTS " + ivDBName
        cur.execute (createDBStr)
    dbcon.commit()
    dbcon.close()
    var = 'Creating mineboss database done'
    return var
def dbUserCreate(inputvals):
    adminVar=inputvals[0]
    adminPwd=inputvals[1]
    ivDBName=inputvals[2]
    ivMinionUser=inputvals[3]
    ivMinionPwd=inputvals[4]
    try:
        dbcon = mdb.connect('localhost',adminVar,adminPwd,'mysql')
        #print "connected"
    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)
    with dbcon:
        cur=dbcon.cursor()
        SQLstring = "CREATE user '" + ivMinionUser + "'@'localhost' identified by '" + ivMinionPwd +"'"
        #print SQLstring
        cur.execute (SQLstring)
    dbcon.commit()
    dbcon.close()
    var = 'Creating database user for mineboss application done'
    return var
def dbUserGrant(inputvals):
    adminVar=inputvals[0]
    adminPwd=inputvals[1]
    ivDBName=inputvals[2]
    ivMinionUser=inputvals[3]
    ivMinionPwd=inputvals[4]
    try:
        dbcon = mdb.connect('localhost',adminVar,adminPwd,'mysql')
        #print "connected"
    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)
    with dbcon:
        cur=dbcon.cursor()
        SQLstring = "GRANT ALL ON  " + ivDBName +".* TO '" + ivMinionUser +"'@'localhost'"
        #print SQLstring
        cur.execute (SQLstring)
        #cur.execute("CREATE TABLE IF NOT EXISTS ccircip(Id INT PRIMARY KEY auto_increment,\
        #IPINT INT UNSIGNED, LASTUPDATE DATE)")
    dbcon.commit()
    dbcon.close()
    var = 'The dnsMinion application user account permissions done'
    return var

newdbvals=getCreateValues()
print dbCreate(newdbvals)
time.sleep(2)
print dbUserCreate(newdbvals)
time.sleep(2)
print dbUserGrant(newdbvals)