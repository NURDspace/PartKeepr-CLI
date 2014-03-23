"""PartKeepr CLI

Usage:
  prtkpr.py search <query>
  prtkpr.py -h | --help
  prtkpr.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from partkeepr import partkeepr
from prettytable import PrettyTable
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('partkeepr.conf')

prtkpr = partkeepr(config.get('partkeepr', 'hostname'),config.get('partkeepr', 'username'),config.get
('partkeepr', 'password'),int(config.get('partkeepr','method')))

def search(query):
    x = PrettyTable(["ID","Part", "Stock", "Location","Description"])
    x.align = "l"
    x.max_width['Description']=30
    searchdata = prtkpr.search(query)
    for item in searchdata['response']['data']:
        x.add_row([item['id'],item['name'],item['stockLevel'],item['storageLocationName'],item['description']])
    x.add_row(['','    Total',searchdata['response']['totalCount'],'',''])
    print x
    

if __name__ == '__main__':
    arguments = docopt(__doc__)
#    print(arguments)
    if arguments['search']:
        search(arguments['<query>']) 
