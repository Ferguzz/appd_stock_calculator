import calendar
import datetime


def parse_iso8601_date_string(date):
    return datetime.date(*map(int, date.split('-')))


def add_months(date, months):
    """Return the date some number of months from now.

    e.g. add_months(2016-01-30, -3) -> 2015-10-30
         add_months(2016-01-30, 1)  -> 2016-02-29  # February 30th doesn't exist.

    """

    # Convert the month to a number between 0 and 11 then add the required number of months.
    month = date.month - 1 + months
    # Handle year overflow.
    year = date.year + (month // 12)
    # Convert the month back to number between 1 and 12.
    month = (month % 12) + 1
    # Create the new date, ensuring the day exists in the new month.
    return datetime.date(year, month, min(date.day, calendar.monthrange(year, month)[1]))


def months_between(older_date, newer_date):
    """Return the number of months between older_date and newer_date.

    """

    months = 0
    while True:
        older_date = add_months(older_date, 1)
        if older_date <= newer_date:
            months += 1
        else:
            break
    return months
