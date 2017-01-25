import json
from stock_award import StockAward
import sys


def parse(grant_file='grants.json'):
    with open(grant_file) as f:
        try:
            grants = json.load(f)
        except ValueError as e:
            print('ERROR: There was a fomattting error in your \'grants.json\': %s.  Please correct it and try again.'
                  % e)
            sys.exit(1)

    for grant in grants:
        try:
            yield StockAward(**grant)
        except TypeError as e:
            print('ERROR: There was an unexpected value in your \'grants.json\': %s.  Please correct it and try again.'
                  % str(e).split('unexpected keyword argument ')[1])
            sys.exit(1)
