import argparse
import datetime
import dateutils
import grants


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Summary information about your AppDynamics stock awards.')
    parser.add_argument('price', type=float, default=25.0, nargs='?', help='The current stock price in dollars.')
    parser.add_argument('-d', '--date', type=dateutils.parse_iso8601_date_string, default=datetime.date.today(),
                        help='An ISO-8601 formatted date e.g. 1999-12-31.  Defaults to today\'s date.')
    args = parser.parse_args()
    date = args.date
    price = args.price

    total_shares = 0
    vested_options = 0
    vested_rsus = 0
    total_net_value = 0.
    total_cost = 0.

    for award in grants.parse():
        total_shares += award.shares
        vested = award.number_vested(date)
        if award.strike_price:
            vested_options += vested
        else:
            vested_rsus += vested
        total_cost += award.cost_to_purchase(date)
        total_net_value += award.net_value(price, date)

    print('Based on a stock price of $%.2f on %s...' % (price, date))
    print(' - %d/%d shares vested' % (vested_options + vested_rsus, total_shares))
    print(' - %d vested RSUs at a value of %.2f' % (vested_rsus, vested_rsus * price))
    if total_cost:
        print(' - cost to purchase available options: $%.2f' % total_cost)
    print(' - total net value of all awards (pre-tax): $%.2f' % total_net_value)
