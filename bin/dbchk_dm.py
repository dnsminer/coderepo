##__author__ = 'dleece'
## Module to be used for checking data values in database tables before updating or creating.
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
