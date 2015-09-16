#!/bin/bash -x
# Define FE user, Usually fetchitBoy
FEUSER="fetchitBoy"
#Define FE host FQDN
FEHOST="fe2.dnsminer.net"
# Get teh RPZ file for today, ( check your cron and TZ settings if this fails )
TODAYRPZ=$(/bin/date +%Y%m%d)-public-list.rpz
echo $TODAYRPZ

/usr/bin/scp ${TODAYRPZ} ${FEUSER}@${FEHOST}:

echo `date`": RPZ transer complete"