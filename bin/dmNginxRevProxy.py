#!/usr/bin/env python
#__author__ = 'dleece'
import sys, os, time, shutil
# functions

nginxbin = '/usr/sbin/nginx'
nginxdir = '/etc/nginx'
DNSMHome = '/opt/dnsminer-alpha'

def minInput():
    FEFQDN = raw_input("Enter the FQDN for the Find Evil server, EG fe2.dnsminer.net: ")
    FEPort = raw_input("Enter the HTTPS port , Usually 443: ")
    KPORT = raw_input( "Enter the port Kibana is using, ( unless you changed it it's 5601: ")
    minInputVals = [FEFQDN,FEPort,KPORT]
    return minInputVals

def isFileValid(pathStr):
    TBool = os.path.isfile(pathStr)
    return TBool

def isPathValid(pathStr):
    TBool = os.path.isdir(pathStr)
    return TBool

def genConfig(valList):
    # current file location when installing package from elastic search
    CFG = nginxdir + "/sites-available/revproxynginx"
    CFGOrig = nginxdir + "/sites-enabled/default"
    CFGLn = nginxdir + "/sites-enabled/revproxynginx"
    if isFileValid(CFGOrig):
        try:
            os.unlink(CFGOrig)
            print "Symlink to "+ CFGOrig + " has been removed"
        except:
            print " unable to remove symfile"
            cStatus = "Check file permissions"
    # Rather than mess with the package version which could change over time just write from scratch
    CFGfh = open(CFG,'a')
    # build the config
    wline = "server {\n"
    wline = wline + "  server_name " + valList[0] + ";\n"
    wline = wline + "    listen " + valList[1] + " default ssl;\n"
    wline = wline + "    ssl_certificate  /etc/nginx/local/dnsminer.crt;\n"
    wline = wline + "    ssl_certificate_key /etc/nginx/local/dnsminerpriv.key;\n"
    wline = wline + "    access_log /var/log/nginx/nginx.access.log combined;\n"
    wline = wline + "    error_log /var/log/nginx/nginx_error.log notice;\n\n"
    wline = wline + "location / {\n"
    wline = wline + "  include proxy.conf;\n"
    wline = wline + "  auth_basic  \" Restricted to authorized users only\"\n"
    wline = wline + "  auth_basic_user_file /etc/nginx/local/user_auth;\n"
    wline = wline + "  proxy_pass http://127.0.0.1:" + valList[2] + ";\n"
    wline = wline + " }\n}\n"
    CFGfh.write(wline)
    CFGfh.close()

    if isFileValid(CFG):
        try:
            os.symlink(CFG,CFGLn)
            print "symlink to " + CFG + " has been created"
        except:
            print "Unable to create symlink, check file permissions"

def copyProxyConf:
    PConf = DNSMHome + "/contrib/proxy.conf"
    NGINXLocal = nginxdir +"/local/"
    if isFileValid('PConf'):
        shutil.copy(PConf,NGINXLocal)


if isFileValid(nginxbin) and isPathValid(nginxdir):
    print "looks good, Nginx is installed "
else:
    print "Nginx does not appear to be installed"
    quit()

conflist = minInput()
for items in conflist:
    print items

genConfig(conflist)
copyProxyConf()
