__author__ = 'dleece'
# Takes a dictionary of values and writes teh config file out line by line. complex values are passed to functions
# to create rather than deal with hard coding. also allows functions to be fixed when bugs are found

DNSMinerHome='/opt/dnsminer-alpha'
tempdir = DNSMinerHome + "/tmp/"

def readDict(thisorgdict):
    #debug
    #for key,val in thisorgdict.iteritems():
    #    print key,"-->",val
    thislist=[]
    vfileline = "view \"" + thisorgdict['view_name'] + "\" in {"
    thislist.append(vfileline)
    vfileline = "\tmatch-clients { " + thisorgdict['acl_name'] + "; };"
    thislist.append(vfileline)
    vfileline="\trecursion yes;"
    thislist.append(vfileline)
    vfileline=mkallowquery(thisorgdict['rec_nodes'])
    thislist.append(vfileline)
    vfileline="\tadditional-from-auth yes;\n\tadditional-from-cache yes;"
    thislist.append(vfileline)
    vfileline="\t// required for views to work, also needs to be commented out of named.conf"
    thislist.append(vfileline)
    vfileline="\tinclude \"/etc/bind/named.conf.default-zones\";"
    thislist.append(vfileline)
    vfileline="\t//authoritative zone needed for RPZ cname"
    thislist.append(vfileline)
    vfileline="\tzone \"" + thisorgdict['sh_zone'] + "\" {"
    thislist.append(vfileline)
    vfileline = "\ttype master;"
    thislist.append(vfileline)
    vfileline=mklzonepath(thisorgdict['org_id'],thisorgdict['sh_zone'])
    thislist.append(vfileline)
    # new these next two more than once so changing the variable name
    notifyline = mkanotify(thisorgdict['rec_nodes'],thisorgdict['xfr_port'],thisorgdict['tsig_name'])
    thislist.append(notifyline)
    xferline = mktransfer(thisorgdict['rec_nodes'],thisorgdict['tsig_name'])
    thislist.append(xferline)
    # close the zone
    vfileline="\t};"
    thislist.append(vfileline)
    vfileline="\t// Enable RPZ"
    thislist.append(vfileline)
    vfileline="\tresponse-policy { zone \"" + thisorgdict['rpz_zone'] + "\"; };"
    vfileline="\t//Add RPZ definition"
    thislist.append(vfileline)
    vfileline="\tzone \"" + thisorgdict['rpz_zone'] + "\" {"
    thislist.append(vfileline)
    vfileline = "\ttype master;"
    thislist.append(vfileline)
    vfileline=mklzonepath(thisorgdict['org_id'],thisorgdict['rpz_zone'])
    thislist.append(vfileline)
    thislist.append(notifyline)
    thislist.append(xferline)
    # close the zone
    vfileline="\t};"
    thislist.append(vfileline)
    # close the view
    vfileline="}; // End " + thisorgdict['view_name'] + " primary view"
    thislist.append(vfileline)
    # prep for file creation
    vfile = thisorgdict['view_name'] + ".primaryview"
    thisfile = tempdir + vfile
    # debug
    #print thisfile
    writeviewfile(thisfile,thislist)
    return

def mkallowquery(rnodestr):
    rnlist=rnodestr.split(',')
    aqrystr = '\tallow-query {'
    for i in range(len(rnlist)):
        if rnlist[i]:
            aqrystr = aqrystr + rnlist[i].strip() + "; "
    aqrystr = aqrystr + "};"
    return aqrystr

def mklzonepath(oid,shz):
    fpath = "\tfile \"/etc/bind/clients/"
    fpath = fpath + str(oid) + "/" + shz + "\";"
    return fpath

def mkanotify(rnodestr,xport,tsig):
    antfystr="\talso-notify { "
    rnlist=rnodestr.split(',')
    for i in range(len(rnlist)):
        if rnlist[i]:
            antfystr = antfystr + rnlist[i].strip() + " port " + xport + " key " + tsig +"; "
    antfystr = antfystr + " };"
    return antfystr

def mktransfer(rnodestr,tsig):
    axferstr="\tallow-transfer { " + tsig + "; "
    rnlist=rnodestr.split(',')
    for i in range(len(rnlist)):
        if rnlist[i]:
            axferstr = axferstr + rnlist[i].strip() + "; "
    axferstr = axferstr + " };"
    return axferstr

def writeviewfile(filename,linelist):
    try:
        fh = open(filename,'w')
        for line in linelist:
            line = line + "\n"
            fh.write(line)
    except Exception as e:
        print "Unable to create view file in temp directory or problem with the file content, please debug"
        print type(e)
        print str(e)
        return
    fh.close()
    return