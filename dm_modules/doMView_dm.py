__author__ = 'dleece'
#from dm_modules
import dbchk_dm, inputSani_dm, iptoint_dm, genRandomString_dm, insertsinkholedata_dm

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


def doView(mwlist):
    #print "do menu view"
    #for val in mwlist:
    #    print val
    # create a dictionary to collect all the results to generate SQL inserts or update
    viewDict = dict()
    # insert org id into dictionary
    viewDict['org_id'] = mwlist[2]
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
                print "\nIdeally you want to direct traffic to a server you control, AKA, sinkhole"
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
                print uvlinput
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

            print "\n please standby, generating a view specific domain for RPZ usage."
            dompart = genRandomString_dm(8)
            hostpart = genRandomString_dm(6)
            shfqdn = hostpart + '.' + dompart + '.local'
            print "\n created this virtually unguessable FQDN just for this view: " + shfqdn
            viewDict['sh_fqdn'] = shfqdn
            # generate the list to be fed to db-insert_sinkholedata
            sinkholesql = insertsinkholedata_dm(viewDict)
            print viewDict
            print sinkholesql

            viewmenuactive=False


        return