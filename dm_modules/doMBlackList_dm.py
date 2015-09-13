__author__ = 'dleece'
#from dm_modules
import dbchk_dm, inputSani_dm, iptoint_dm, genRandomString_dm, insertsinkholedata_dm, menudbinsert_dm, genTsigData_dm,menudbselect_dm, insertviewdata_dm, genDefListData_dm, genViewACL_dm, bulkdbselect1w_dm

#from dm_modules import cfgparse_dm, doMView_dm, inputSani_dm, doMGenOrgView, doMBlackList_dm, bulkdbselect1w_dm


def inputView(vname):
    #check for no spaces and make sure it's not already used.
    #viewName = inputSanitizer(vname,'view')
    viewName = inputSani_dm.inputSanitizer(vname,'view')
    print "confirming view name is unique in the system"
    checkviewname=['view_name','bind_views',viewName]  # Column, table, value
    #boolVar= dbRecordCheck(checkviewname)
    boolVar= dbchk_dm.dbRecordCheck(checkviewname)
    checkviewlist = [boolVar,viewName]   # return result of uniqueness test and view name value if it's usable.
    if checkviewlist[0]:
        print "Sorry, that record appears to be in use, please provide a different value"
    return  checkviewlist

def getViewData(oid):
    qrylist = ['view_name,def_sh_id','bind_views','org_id',oid]
    resultrow = bulkdbselect1w_dm.dbRecordSelect(qrylist)
    # To deal with more than one record coming back we need to unpack the tuples and present to user
    vnamelist=[]
    retlist = []
    for rval in resultrow:
        (vwstr, defshid) = rval
        # dump into list iterate by twos and prompt
        vnamelist.append(vwstr,defshid)
    # convert to > 1 for proud
    if len(resultrow) < 5:
        print "There is more than one View assigned to this organization identifer\nselect the View that will be using this blacklist\n"
        i=0
        for i in range(len(vnamelist)):
            print "View : " + vnamelist[i]
            vprompt = True
            while vprompt:
                uvlinput = raw_input("Select (yes/no)?: ")
                uvlinput = inputSani_dm.inputSanitizer(uvlinput,'ynprompt')
                #print uvlinput
                if uvlinput == 'invalid_format':
                    continue
                elif uvlinput == 'no':
                    i = i + 2
                else:
                    retlist.append(vnamelist[i])
                    retlist.append(vnamelist[i + 1])
                    vprompt = False
    return retlist


def doBlackList(mwlist):
    #print "do menu view"
    viewdata = getViewData(mwlist[2])
    for data in viewdata:
        print data
    blkDict = dict()
    blkDict['view_name'] = viewdata[0]
    blkDict['def_sh_id'] = viewdata[1]
    #for val in mwlist:
    #    print val
    # create a dictionary to collect all the results to generate SQL inserts or update

    # insert org id into dictionary
    viewDict['org_id'] = mwlist[2]
    if mwlist[1] != 'update':
        # start the menu to gather view details
        viewmenuactive=True
        while viewmenuactive:
            getviewname = True
            print "\nYou are about to provide the data needed for a new Bind View and related zone files."
            print "\nThe view must be a unique name within the system,"
            print "it must also be a single word with no spaces, letters, dashes, underscores and digits ok"
            while getviewname:
                uvinput = raw_input("Enter view name: ")
                uvinput = uvinput.strip().lower()
                vresult = inputView(uvinput) # needed to get the status, using length of list to avoid global vars
                if not vresult[0]:
                    viewDict['view_name'] = vresult[1]
                    getviewname = False

            getmonip = True
            while getmonip:
                print "\nIdeally you want to direct suspicious traffic to a server you control, AKA, sinkhole"
                uvlinput = raw_input("What is the internal IP for the monitoring application? ( dotted quad): ")
                uvlinput = iptoint_dm.dotQuadtoInt(uvlinput)
                if uvlinput > 10:
                    viewDict['sh_ip'] = uvlinput
                    getmonip = False
                else:
                    print "hmm, looks like that wasn't a dotted quad, EG 172.16.28.7, please enter again"

            print"\nProvide a short description of this sink hole, EG, .net app running in Calgary office"
            getmondesc = True
            while getmondesc:
                uvlinput = raw_input("Description: ")
                uvlinput = inputSani_dm.inputSanitizer(uvlinput,'desc1')
                #print uvlinput
                if uvlinput == 'invalid_format':
                    continue
                else:
                    viewDict['sh_desc'] = uvlinput
                    getmondesc = False

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
                nextIP = raw_input("\nDo you need to add another IP address (yes|no)?")
                nextIP = nextIP.strip().lower()
                if nextIP == 'no':
                    getviewip = False
                    # build IPs and cidr into a CSV string to be used with views
                    rcsvclients  = ",".join(map(str,viewClientIPList))
                    viewDict['view_src_acl_ips'] = rcsvclients  # build into an ACL data structure later on

            getviewdesc = True
            print"\nProvide a short description of what's behind these IP addresses,  EG, Eastern office or Engineering dept"
            while getviewdesc:
                uvlinput = raw_input("Description: ")
                uvlinput = inputSani_dm.inputSanitizer(uvlinput,'desc1')
                #print uvlinput
                if uvlinput == 'invalid_format':
                    continue
                else:
                    viewDict['view_desc'] = uvlinput
                    getviewdesc = False

            print "\n please standby, generating a view specific domain for RPZ usage."
            dompart = genRandomString_dm.genString(7)
            hostpart = genRandomString_dm.genString(6)
            shfqdn = hostpart + '.' + dompart + '.local'
            print "\n created this virtually unguessable FQDN just for this view: " + shfqdn
            viewDict['sh_fqdn'] = shfqdn
            # generate the list to be fed to db-insert_sinkholedata
            sinkholesql = insertsinkholedata_dm.parsemenudict(viewDict)
            #print sinkholesql
            shresult=menudbinsert_dm.dbinsert(sinkholesql)
            #print shresult
            if shresult == 1:
                print "sinkhole table entry created successfully"
                # grab teh sinkhole id to dump into the view table
                shselect = ['sinkhole_id','view_sinkholes','sh_fqdn',shfqdn]
                thisresultlist = menudbselect_dm.dbRecordSelect(shselect)
                if len(thisresultlist) == 1:
                    viewDict['def_sh_id'] = thisresultlist[0]
                else:
                    print "failed to retrieve sinkhole ID, you should probably exit and debug this"
            else:
                print "You may need to manually check the view_sinkholes table"

            #generate tsig_key meta data, ( this is static even if the keys are updated
            oid = viewDict['org_id']
            vname = viewDict['view_name']
            tsigid = genTsigData_dm.gentsigsql(oid,vname)
            newtsigid = tsigid[0]
            viewDict['tsig_id'] = newtsigid
            # debug dictionary contents
            #for key,val in viewDict.iteritems():
            #    print key, '-->', viewDict[key]
            # generate the list from dictinary values and push data
            viewsqlinsert=[viewDict['org_id'],viewDict['view_name'],viewDict['def_sh_id'],viewDict['view_src_acl_ips'],viewDict['view_desc'],viewDict['tsig_id']]
            # debug                 (org_id,view_name,def_sh_id,view_src_acl_ips,view_desc,tsig_id)
            #for val in viewsqlinsert:
            #    print val
            thisviewid = insertviewdata_dm.genviewgsql(viewsqlinsert)
            newviewid = thisviewid[0]
            if len(thisviewid) == 1:
                print "\nProgress report: \nCreation of view " + viewDict['view_name'] + " confirmed successful, please generate an view file for this organiztion now, menu/genorgview\n"

            # generate black and white list entries since there is a now a view for the org
            print "\nStand by, just making a few internal database updates"
            shid = viewDict['def_sh_id']
            wlcreate = genDefListData_dm.genbworgsql(oid,vname,shid)
            if wlcreate == 1:
                print "All black list and white list default records were successfully initialized"

            # exit do view menu
            viewmenuactive=False

    return