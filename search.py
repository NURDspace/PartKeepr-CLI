import sys
from pprint import pprint
from prettytable import PrettyTable
from partkeepr import partkeepr

x = PrettyTable(["ID","Part", "Stock", "Location","Description"])
x.align = "l"
x.max_width['Description']=30

prtkpr = partkeepr('192.168.1.203','test','nurdspace',1)
searchdata = prtkpr.search(" ".join(sys.argv[1:]))

#debugging
#pprint(searchdata)

for item in searchdata['response']['data']:
    x.add_row([item['id'],item['name'],item['stockLevel'],item['storageLocationName'],item['description']])
x.add_row(['','    Total',searchdata['response']['totalCount'],'',''])
print x
