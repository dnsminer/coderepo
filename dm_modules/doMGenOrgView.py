__author__ = 'dleece'

# use the org id as a simple auth check,

import menuviewauthz_dm, inputSani_dm, dbchk_dm

def authView(authzlist):
    #check for no spaces and make sure it's not already used.
    print "confirming authorization for view name"
    checkviewauth=['view_id','bind_views','org_id',authzlist[0],'view_name',authzlist[1]]  # Column, table, value
    #boolVar= dbRecordCheck(checkviewname)
    authzresults= menuviewauthz_dm.dbRecordSelect(checkviewauth)
    return  authzresults



def doGenView(thisorgid):
    gviewdict=dict()
    gviewdict['org_id']=thisorgid
    genviewmenuactive = True
    while genviewmenuactive:
            getviewname = True
            print "\nYou are about to generate/regenerate a new Bind View and related zone files."
            while getviewname:
                print "\nYou can only generate views assigned to your organization."
                uvinput = raw_input("Enter view name: ")
                uvinput = uvinput.strip().lower()
                viewName = inputSani_dm.inputSanitizer(uvinput,'view')
                authchk=[thisorgid,viewName]
                vresult = authView(authchk) # needed to get the status, using length of list to avoid global vars
                if  vresult[0]:
                    print "congrats you are authorized for this view "
                    gviewdict['view_id'] = vresult[1]
                    getviewname = False
                # debug
                for key,val in gviewdict:
                    print key,"-->",val

            genviewmenuactive=False
