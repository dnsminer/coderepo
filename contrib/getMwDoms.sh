#!/bin/bash -x

LISTHOME="/opt/dnsminer-alpha/fib/lists/mwdoms"
LISTWIP="/opt/dnsminer-alpha/fib/lists"
DATESTAMP=`date +%Y%m%d`
/usr/bin/wget -O $LISTHOME/$DATESTAMP-mwdoms.txt http://mirror1.malwaredomains.com/files/spywaredomains.zones

for I in `ls  $LISTHOME/$DATESTAMP-*.txt`; do
echo "processing $I"
grep zone $I | awk '{print $2}' | sed -e 's/"//g' >> $LISTHOME/$DATESTAMP-all.tmp
done
/bin/cat $LISTHOME/$DATESTAMP-all.tmp | sort -u > $LISTWIP/$DATESTAMP-mwDoms-all.txt
/bin/rm  $LISTHOME/$DATESTAMP-all.tmp