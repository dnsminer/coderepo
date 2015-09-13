#!/bin/bash -x
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/local/bin:/usr/local/sbin
LISTHOME="/opt/dnsminer-alpha/fib/lists/abuse-ch"
DATESTAMP=`date +%Y%m%d`
/usr/bin/wget -t 3 -O $LISTHOME/$DATESTAMP-feodo.txt --no-check-certificate https://feodotracker.abuse.ch/blocklist/?download=domainblocklist
/usr/bin/wget -t 3 -O $LISTHOME/$DATESTAMP-palevo.txt --no-check-certificate https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist
/usr/bin/wget -t 3 -O $LISTHOME/$DATESTAMP-spyeye.txt --no-check-certificate https://spyeyetracker.abuse.ch/blocklist.php?download=domainblocklist
/usr/bin/wget -t 3 -O $LISTHOME/$DATESTAMP-zeus.txt --no-check-certificate  https://zeustracker.abuse.ch/blocklist.php?download=baddomains

for I in `ls  $LISTHOME/$DATESTAMP-*.txt`; do
echo "processing $I"
grep -v '#' $I >> $LISTHOME/$DATESTAMP-all.tmp
done
/bin/touch /opt/dnsminer-alpha/fib/lists/$DATESTAMP-abuse-ch.txt
/bin/cat $LISTHOME/$DATESTAMP-all.tmp | /usr/bin/sort -u > /opt/dnsminer-alpha/fib/lists/$DATESTAMP-abuse-ch.txt
/bin/rm $LISTHOME/$DATESTAMP-all.tmp