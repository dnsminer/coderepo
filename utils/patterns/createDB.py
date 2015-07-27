#!/usr/bin/env python
#__author__ = 'dleece'
import sys
import MySQLdb as mdb

dbAdmin = raw_input("Enter mysql admin user,(typically root): ")
dbAdminPWD = raw_input("Enter mysql admin's  passwd: ")

def dbCreate():

    try:
        dbcon = mdb.connect('localhost',dbAdmin,dbAdminPWD,'dnsminerWA')
        print "connected"

    except mdb.Error, e:
        print e.args[0]
        sys.exit(1)

    with dbcon:
        cur=dbcon.cursor()
        cur.execute("USE dnsminerWA")
        cur.execute("CREATE TABLE IF NOT EXISTS ccircip(Id INT PRIMARY KEY auto_increment,\
        IPINT INT UNSIGNED, LASTUPDATE DATE)")
    dbcon.commit()
    dbcon.close()
    var = 'done'
    return var

print "Debug"
print dbCreate()
