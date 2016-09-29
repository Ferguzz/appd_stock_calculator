import calendar
import dateutils


class StockAward(object):
    def __init__(self, shares, commencement_date, strike_price=0, vesting_schedule_in_years=4, monthly=False,
                 number_purchased=0, one_year_cliff=True):
        self.shares = shares
        self.commencement_date = dateutils.parse_iso8601_date_string(commencement_date)
        self.strike_price = strike_price
        self.vesting_schedule_in_years = vesting_schedule_in_years
        self.monthly = monthly
        self.number_purchased = number_purchased
        assert one_year_cliff
        self.first_vesting_date = self.commencement_date.replace(year=self.commencement_date.year + 1)
        self.number_vested_cache = {}

    def cost_to_purchase(self, date):
        return (self.number_vested(date) - self.number_purchased) * self.strike_price

    def gross_value(self, price, date):
        return self.number_vested(date) * price

    def net_value(self, price, date):
        return (self.number_vested(date) * price) - (self.number_vested(date) * self.strike_price)

    def last_vesting_date(self, date):
        # If we haven't hit the requisite day of the month yet, go back a month.
        if date.day < self.commencement_date.day:
            date = dateutils.add_months(date, -1)

        # If the award vests quarterly we might have to go back even further.
        if not self.monthly:
            # Quarterly vesting schedules vest in March, June, September, and
            # December.  Subtracting (month % 3) always takes us back to one of
            # those months.  e.g. May (5) % 3 = 2 and 5 - 2 = 3 (March).
            date = dateutils.add_months(date, -(date.month % 3))

        # The vesting day is the same as the award day unless the award day
        # doesn't exist in the given month.
        try:
            date = date.replace(day=self.commencement_date.day)
        except ValueError:  # day is out of range for month
            date = date.replace(day=calendar.monthrange(date.year, date.month)[1])
        return date

    def number_vested(self, date):
        try:
            return self.number_vested_cache[date]
        except KeyError:
            last_vesting_date = self.last_vesting_date(date)

            # Awards which haven't reached their cliff are worthless.
            if last_vesting_date < self.first_vesting_date:
                number_vested = 0
            else:
                shares_vesting_per_month = self.shares / float(12 * self.vesting_schedule_in_years)
                number_vested = min(self.shares, int(dateutils.months_between(
                    self.commencement_date, last_vesting_date) * shares_vesting_per_month))

            self.number_vested_cache[date] = number_vested
            return number_vested
