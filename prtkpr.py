#!/usr/bin/env python
"""PartKeepr CLI

Usage:
  prtkpr.py search <query>
  prtkpr.py part <id>
  prtkpr.py stockadd <id> <amount> <price>
  prtkpr.py stockrm <id> <amount>
  prtkpr.py -h | --help
  prtkpr.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

__version__ = "0.0.1-dev"

from docopt import docopt
from partkeepr import partkeepr
from prettytable import PrettyTable
import ConfigParser
import sys

config = ConfigParser.RawConfigParser()
config.read('partkeepr.conf')


def search(query):
    x = PrettyTable(["ID","Part", "Stock", "Location","Description"])
    x.align = "l"
    x.max_width['Description']=30
    searchdata = prtkpr.search(query)
    for item in searchdata['response']['data']:
        x.add_row([item['id'],item['name'],item['stockLevel'],item['storageLocationName'],item['description']])
    x.add_row(['','    Total',searchdata['response']['totalCount'],'',''])
    print x

def part(partid):
    part = prtkpr.part(partid)
    stock = prtkpr.stockhistory(partid)
    x = PrettyTable(["Name","Value"])
    x.align = "l"
    x.add_row(['ID',part['id']])
    x.add_row(['Name',part['name']])
    x.add_row(['Description',part['description']])
    x.add_row(['Comment',part['comment']])
    x.add_row(['Location',part['storageLocationName']])
    x.add_row(['Category',part['categoryName']])
    x.add_row(['Footprint',part['footprint']])
    x.add_row(['Stock',part['stockLevel']])
    print x

    print "Stock history:"
    x = PrettyTable(["+|-","Date","User","Amount","Price","Comment"])
    for log in stock:
        if log['direction'] == 'in':
            direction = "+"
        else:
            direction = "-"
        x.add_row([direction,log['dateTime'],log['username'],log['stockLevel'],log['price'],log['comment']])
    print x

if __name__ == '__main__':
    arguments = docopt(__doc__)
#    print(arguments)
    if arguments['--version']:
        print "prtkpr CLI %s"%__version__
        sys.exit(0) 

    prtkpr = partkeepr(config.get('partkeepr', 'hostname'),config.get('partkeepr', 'username'),config.get('partkeepr', 'password'),int(config.get('partkeepr','method')))

    if arguments['search']:
        search(arguments['<query>'])
    elif arguments['part']:
        part(arguments['<id>'])
    elif arguments['stockadd']:
        prtkpr.stockadd(arguments['<id>'],arguments['<amount>'],arguments['<price>'])
    elif arguments['stockrm']:
        prtkpr.stockremove(arguments['<id>'],arguments['<amount>'])
