#!/usr/bin/env python
#__author__ = 'dleece'
import sys, os, time, shutil, subprocess, shlex

# while we could build this by hand in python, it's easier to add the apache2-utils
# These are the default paths expected, seldom require editing but can be safely adjusted
htppwbin='/usr/bin/htpasswd'
uauthfile='/etc/nginx/local/user_auth'
nginxlocal= '/etc/nginx/local'

# functions
def minInput():
    UNAME = raw_input("Enter user name to be created: ")
    UNAME = UNAME.strip()
    UPWD = raw_input("Enter password: ")
    UPWD = UPWD.strip()
    minInputVals = [UNAME,UPWD]
    return minInputVals

def isFileValid(pathStr):
    TBool = os.path.isfile(pathStr)
    return TBool

def isPathValid(pathStr):
    TBool = os.path.isdir(pathStr)
    return TBool

def doHTPASSWD(udata):
    if isFileValid(uauthfile):
        cmdStr = htppwbin + " -b " + uauthfile + " " + udata[0] + " " + udata[1]
        #cmdArgStr = "[\"" + htppwbin + "\", \"-b\", \"" + uauthfile + "\", \"" +  udata[0] + "\", \"" + udata[1] + "\"]"
    else:
        cmdStr = htppwbin + " -b -c " + uauthfile + " " + udata[0] + " " + udata[1]
        #cmdArgStr = "[\"" + htppwbin + "\", \"-b\", \"-c\", \"" + uauthfile + "\", \"" +  udata[0] + "\", \"" + udata[1] + "\"]"
    #print cmdStr
    cmdArgs = shlex.split(cmdStr)
    #htpaswdresult=subprocess.Popen(cmdArgStr,stdout=subprocess.PIPE)
    p=subprocess.Popen(cmdArgs,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #htpasswdResult = p.communicate()
    return p #htpasswdResult

### main

# We need to stop if htpasswd isn't installed or nginx/local is missing
if not isFileValid(htppwbin):
    print "Oops, we need the htpasswd binary and can't find it"
    print "install the apache2-utils package from your OS or correct the path in this script"
    exit()

if not isPathValid(nginxlocal):
    print "Oops, looks like the nginx config is not quite as expected"
    print "If you haven't done so, install nginx and then run dmNginxRevProxy.py"
    exit()

# start teh loop to add users
ADDUSERS='yes'
while True:
    thisList = []
    if ADDUSERS=='yes':
        print "Adding users to the local htpasswd file"
        thisList=minInput()
        #print thisList[0]
        #print thisList[1]
        procResult=doHTPASSWD(thisList)
        showResult = procResult.stdout.read()
        print showResult
        RI=raw_input("Add another user? (yes|no)?:")
        ADDUSERS=str.lower(RI.strip())
    else:
        break