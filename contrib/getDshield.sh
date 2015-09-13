#!/bin/bash -x
LISTHOME="/opt/dnsminer-alpha/fib/lists/dshield"
LISTWIP="/opt/dnsminer-alpha/fib/lists"
DATESTAMP=`date +%Y%m%d`
/usr/bin/wget -O $LISTHOME/$DATESTAMP-dslow.txt http://www.dshield.org/feeds/suspiciousdomains_Low.txt
/usr/bin/wget -O $LISTHOME/$DATESTAMP-dsmed.txt http://www.dshield.org/feeds/suspiciousdomains_Medium.txt
/usr/bin/wget -O $LISTHOME/$DATESTAMP-dshigh.txt http://www.dshield.org/feeds/suspiciousdomains_High.txt

for I in `ls  $LISTHOME/$DATESTAMP-*.txt`; do
echo "processing $I"
grep -v '#' $I | egrep '.*\..*'  >> $LISTHOME/$DATESTAMP-all.tmp
done
/bin/cat $LISTHOME/$DATESTAMP-all.tmp | sort -u > $LISTWIP/$DATESTAMP-dshield-all.txt
/bin/rm  $LISTHOME/$DATESTAMP-all.tmp
