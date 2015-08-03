#!/bin/bash
#
# DNS Miner
# generates a self signed cert and places files in correct directory for Nginx reverse proxy
#
# 2015/08/02 assumes NGINX is installed or will be installed in /etc/nginx/
#            place files like SSL certs and user_auth into a local directory

# Confirm openssl is availiable
OPENSSLBIN=`which openssl`
if [ -z "$OPENSSLBIN" ]; then
    echo " Sorry, openssl does not appear to be installed"
    echo " If it is, update PATH variable to include the path to the openssl binary"
    exit 1
fi

#
echo "Preparing an SSL self signed certificate for the NGinx reverse proxy"
echo " "
sleep 2
#
TDIR=`date +%Y%M%d%H`
if [ ! -d /var/tmp/$TDIR ]; then
    mkdir /var/tmp/$TDIR
fi
#
cd /var/tmp/$TDIR
#
# This will pop open a shell to allow the SSL files to be created
$OPENSSLBIN req -x509 -sha256 -nodes -days 730 -newkey rsa:2048 -keyout dnsminerpriv.key -out dnsminer.crt

if [ ! -d /etc/nginx/local ] ; then
    mkdir -p /etc/nginx/local
fi

mv dnsminerpriv.key /etc/nginx/local
mv dnsminer.crt /etc/nginx/local

# Clean up the creation directory
rm -rf /var/tmp/$TDIR