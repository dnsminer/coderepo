__author__ = 'dleece'

#Open a file of key value pairs and dump them into a dictionary
file2open = raw_input("Enter name of csv file containing key/value pairs: ")
try:
    file2read=open(file2open)
except:
    print "No such file ",file2open
    exit()
tmpList= list()
histoList = list()
dnsHisto = dict()
requests = 1
clientQuery = 'no.domain.tld'
lastRequest = '1-Jan-1970 00:00:00.001'
for line in file2read: #ough for historical analysis
    if 'queries: info: client ' in line :
        line = line.rstrip()
        tmpList = line.split()
        clientQuery = tmpList[9]

        lastRequest = tmpList[0] + "," + tmpList[1]
    # ignore all local queries
    if 'queries: info: client 127.0.0.1' in line : continue
    #confirm it's a valid query line and extract data elements of host/domain requested and build a last seen var
    #  Assumes log timetamps are sequentuial, usually true, close en
    # write data to dictionary
    if clientQuery in dnsHisto:
        histoList = dnsHisto[clientQuery]
        requests = int(histoList[0]) + 1
        histoList[0] = requests
        histoList[1] = lastRequest
    else:
        histoList = [int(1),lastRequest]
        dnsHisto[clientQuery] = histoList

sortList = list()
# confirm we have data
for domKey,domVal in dnsHisto.items():
    tmpLine = domVal[0], domKey, domVal[1]
    sortList.append(tmpLine)
reportList = sorted(sortList)

file2write=open('dailyQuerySummary.csv','w')

for sortLine in reportList:
    file2write.write(str(sortLine[0]) +',' + sortLine[1] + ',' + sortLine[2]+'\n')
file2write.close()
#print sorted(dnsHisto.values(),reverse=True)


