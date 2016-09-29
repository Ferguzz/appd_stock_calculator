import argparse
import datetime
import dateutils
import json
from stock_award import StockAward
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Summary information about your AppDynamics stock awards.')
    parser.add_argument('price', type=float, default=15.0, nargs='?', help='The current stock price in dollars.')
    parser.add_argument('-d', '--date', type=dateutils.parse_iso8601_date_string, default=datetime.date.today(),
                        help='An ISO-8601 formatted date e.g. 1999-12-31.  Defaults to today\'s date.')
    args = parser.parse_args()
    date = args.date
    price = args.price

    with open('grants.json') as f:
        try:
            grants = json.load(f)
        except ValueError as e:
            print('There was a fomattting error in your \'grants.json\': %s.  Please correct it and try again.' % e)
            sys.exit(1)

    net_value = 0.
    cost = 0.
    for grant in grants:
        try:
            award = StockAward(**grant)
        except TypeError as e:
            print('There was an unexpected value in your \'grants.json\': %s.  Please correct it and try again.'
                  % str(e).split('unexpected keyword argument ')[1])
            sys.exit(1)
        cost += award.cost_to_purchase(date)
        net_value += award.net_value(price, date)

    print('Based on a stock price of $%.2f on %s...' % (price, date))
    print('total cost to purchase: $%.2f' % cost)
    print('total net value (pre-tax): $%.2f' % net_value)
