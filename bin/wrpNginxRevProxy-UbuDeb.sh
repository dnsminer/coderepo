#!/bin/bash
#
#  DNS Miner installation wrapper
#
#  in the spirit of semi-automation this should simplify the installation
#  of an nginx reverse proxy to protect the kibana instance with SSL and
#  http basic authentication.
#  This wrapper is Debian/Ubuntu specific if you have a different OS and there
#  is no wrapper script then simply run each script manually.

# Edit the DNSMINERHOME path to the local git repo location
#
export DNSMINERHOME="/opt/dnsminer-alpha"
#
#  Nothing more to be edited
#
export DNSMINERBIN=${DNSMINERHOME}/bin
export DNSMINERCONTRIB=${DNSMINERHOME}/contrib
#
echo " During the installation process you will be prompted for site specific information"
sleep 8
#
##  Install Nginx from packages:
#
apt-get -f  install nginx nginx-common nginx-full
sleep 8
#
## Create SSL self signed certs
#
bash $DNSMINERBIN/dmSSLSelfSigned.sh
sleep 8
#
## Create custom nginx config
#
python $DNSMINERBIN/dmNginxRevProxy.py
sleep 8
#
## Create at least one user for http authentication
#
echo " please run $DNSMINERBIN/dmNginxAuth.py to create at least one user account"
python $DNSMINERBIN/dmNginxAuth.py
sleep 8
echo "testing nginx installation"
/etc/init.d/nginx configtest
echo " if you didn't get any warnings or errors start nginx and log into your Elastic Search Kibana console."