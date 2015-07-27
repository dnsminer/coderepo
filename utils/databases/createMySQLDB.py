#!/usr/bin/env python
#__author__ = 'dleece'
import sys
import MySQLdb as mdb

dbAdmin = raw_input("Enter mysql admin user,(typically root): ")
dbAdminPWD = raw_input("Enter mysql admin's  passwd: ")
dnsMinionPWD = raw_input("Enter the password for dnsMinion -- application DB acct: ")
def dbCreate():

    try:
        dbcon = mdb.connect('localhost',dbAdmin,dbAdminPWD,'mysql')
        #print "connected"

    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)

    with dbcon:
        cur=dbcon.cursor()
        cur.execute("USE mysql")
        cur.execute ("CREATE database dnsminerWA")
        #cur.execute("CREATE TABLE IF NOT EXISTS ccircip(Id INT PRIMARY KEY auto_increment,\
        #IPINT INT UNSIGNED, LASTUPDATE DATE)")
    dbcon.commit()
    dbcon.close()
    var = 'Create Database done'
    return var
def dbUserCreate():
    try:
        dbcon = mdb.connect('localhost',dbAdmin,dbAdminPWD,'mysql')
        #print "connected"

    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)

    with dbcon:
        cur=dbcon.cursor()
        #cur.execute("USE dnsminerWA")
        SQLstring = "CREATE user 'dnsMinion'@'localhost' identified by '" + dnsMinionPWD +"'"
        print SQLstring
        cur.execute (SQLstring)
        #cur.execute("CREATE TABLE IF NOT EXISTS ccircip(Id INT PRIMARY KEY auto_increment,\
        #IPINT INT UNSIGNED, LASTUPDATE DATE)")
    dbcon.commit()
    dbcon.close()
    var = 'Create Database User done'
    return var
def dbUserGrant():
    try:
        dbcon = mdb.connect('localhost',dbAdmin,dbAdminPWD,'mysql')
        #print "connected"

    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)

    with dbcon:
        cur=dbcon.cursor()
        #cur.execute("USE dnsminerWA")
        SQLstring = "GRANT all dnsminerWA.* TO 'dnsMinion'@'localhost'"
        print SQLstring
        cur.execute (SQLstring)
        #cur.execute("CREATE TABLE IF NOT EXISTS ccircip(Id INT PRIMARY KEY auto_increment,\
        #IPINT INT UNSIGNED, LASTUPDATE DATE)")
    dbcon.commit()
    dbcon.close()
    var = 'Create Database User Permissions  done'
    return var
print "Debug"
print dbCreate()
print dbUserCreate()
print dbUserGrant()