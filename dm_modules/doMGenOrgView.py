__author__ = 'dleece'

# use the org id as a simple auth check,
import sys, time,os, shutil
import menuviewauthz_dm, inputSani_dm, dbselect1row_dm, cfgparse_dm, makeViewFile_dm, makeZoneFile_dm

#
DNSMinerHome='/opt/dnsminer-alpha'
sitecfg = DNSMinerHome + "/etc/siteSpecific.cfg"

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
        thisresult=getdata(tsigsqlstr)
        if thisresult[0] is not None:
            gviewdict['tsig_name'] = thisresult[0]
        else:
            print "no tsig key name found, debug required"
            exit()
    else:
        print "invalid input, I quit"
        exit()
    return

def genshsql(thisvname):
    # This should be presanitized but if we need another check at some point put it here.
    if type(thisvname) == type(str()):
        tmpid=thisvname
        shsqlstr = "SELECT view_sinkholes.sh_fqdn,view_sinkholes.sh_ip FROM view_sinkholes INNER JOIN  bind_views ON view_sinkholes.sinkhole_id = bind_views.def_sh_id "
        shsqlstr = shsqlstr + "WHERE bind_views.view_name = '" + tmpid  + "' ;"
        thisresult=getdata(shsqlstr)
        if thisresult[0] is not None:
            gviewdict['sh_fqdn'] = thisresult[0]
            gviewdict['sh_ip'] = thisresult[1]
        else:
            print "no view name found, debug required"
            exit()
    else:
        print "invalid input, I quit"
        exit()
    return


def getdata(thissqlstr):
    qresult = dbselect1row_dm.dbRecordSelect(thissqlstr)
    return qresult

def makezonename(fqdnstr):
    zoneelems = fqdnstr.split('.')
    if len(zoneelems) == 3:
        internalzone = zoneelems[1] + "." + zoneelems[2]
    return  internalzone

def getnodeinfo():
    thisCfgDict = cfgparse_dm.opencfg(sitecfg,'SectionTwo')
    xferport = thisCfgDict['zonetransferport']
    gviewdict['xfr_port']=xferport
    nodelist = thisCfgDict['recursivenameservers'].split(',')
    # clean up any spaces between the nodes
    rnodestr=''
    for i in range(len(nodelist)):
        rnodestr = rnodestr + nodelist[i].strip() + ","
    gviewdict['rec_nodes'] = rnodestr
    return


def doGenView(thisorgid):
    gviewdict['org_id']=thisorgid
    genviewmenuactive = True
    while genviewmenuactive:
            getviewid = True
            makeview = False
            makezone = False
            print "\nYou are about to generate/regenerate a new Bind View and related zone files."
            filechoice = raw_input("View File or zone file (view|zone)?")
            filechoice = filechoice.strip().lower()
            if filechoice =='view':
                makeview = True
            elif filechoice == 'zone':
                makezone = True
            else:
                print "not a valid choice"

            while getviewid:
                print "You can only generate views assigned to your organization."
                uvinput = raw_input("Enter view name: ")
                uvinput = uvinput.strip().lower()
                viewName = inputSani_dm.inputSanitizer(uvinput,'view')
                authchk=[thisorgid,viewName]
                vresult = authView(authchk) # needed to get the status, using length of list to avoid global vars
                #print vresult[0]
                if  vresult[0]:
                    print "congrats you are authorized for this view "
                    gviewdict['view_id'] = vresult[1]
                    gviewdict['view_name'] = viewName
                    getviewid = False
                    # get tsig key data, this all needs to stay within the authorized section
                    gentsigsql(gviewdict['view_id'])
                    genshsql(gviewdict['view_name'])
                    # create composite content values
                    shzone = makezonename(gviewdict['sh_fqdn'])
                    gviewdict['sh_zone'] = shzone
                    gviewdict['rpz_zone'] = gviewdict['view_name'] + ".rpz"
                    getnodeinfo()
                    gviewdict['acl_name'] = gviewdict['view_name'] + "ACL"
                    # debug
                    #for key,val in gviewdict.iteritems():
                    #    print key,"-->",val
                    # write to file
                    if makeview:
                        makeViewFile_dm.readDict(gviewdict)
                        makeview = False
                    if makezone:
                        makeZoneFile_dm.readDict(gviewdict)
                        makezone = False



            genviewmenuactive=False
