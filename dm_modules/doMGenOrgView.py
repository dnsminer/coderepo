__author__ = 'dleece'

# use the org id as a simple auth check,

import menuviewauthz_dm, inputSani_dm, dbselect1row_dm

#
gviewdict=dict()


def authView(authzlist):
    #check for no spaces and make sure it's not already used.
    print "confirming authorization for view name"
    checkviewauth=['view_id','bind_views','org_id',authzlist[0],'view_name',authzlist[1]]  # Column, table, value
    #boolVar= dbRecordCheck(checkviewname)
    authzresults= menuviewauthz_dm.dbRecordSelect(checkviewauth)
    return  authzresults

def gentsigsql(thisvid):
    # debug
    #print type(thisvid)
    if type(thisvid) == type(long()):
        tmpid=str(thisvid)
        tsigsqlstr = "SELECT tsig_keys.tsig_name FROM tsig_keys INNER JOIN  bind_views ON tsig_keys.tsig_id = bind_views.tsig_id "
        tsigsqlstr = tsigsqlstr + "WHERE bind_views.view_id = '" + tmpid  + "' ;"
        print tsigsqlstr
        thisresult=gettsigdata(tsigsqlstr)
        for val in thisresult:
            print val
    else:
        print "invalid input, I quit"
        exit()
    return

def gettsigdata(thissqlstr):
    qresult = dbselect1row_dm.dbRecordSelect(thissqlstr)
    return qresult

def doGenView(thisorgid):
    gviewdict['org_id']=thisorgid
    genviewmenuactive = True
    while genviewmenuactive:
            getviewid = True
            print "\nYou are about to generate/regenerate a new Bind View and related zone files."
            while getviewid:
                print "You can only generate views assigned to your organization."
                uvinput = raw_input("Enter view name: ")
                uvinput = uvinput.strip().lower()
                viewName = inputSani_dm.inputSanitizer(uvinput,'view')
                authchk=[thisorgid,viewName]
                vresult = authView(authchk) # needed to get the status, using length of list to avoid global vars
                if  vresult[0]:
                    print "congrats you are authorized for this view "
                    gviewdict['view_id'] = vresult[1]
                    getviewid = False

                # get tsig key data
                print gviewdict['view_id']
                gentsigsql(gviewdict['view_id'])



                # debug
                for key,val in gviewdict.iteritems():
                    print key,"-->",val

            genviewmenuactive=False
