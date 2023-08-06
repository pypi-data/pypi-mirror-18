from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

EPOCH = datetime(1970, 1, 1)

def months_between_dates(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def months_since_epoch(year, month, day):
    return months_between_dates(datetime(year, month, day), EPOCH)

def months_since_epoch_from_date(date, date_format):
    return months_between_dates(datetime.strptime(date, date_format), EPOCH)

def months_since_epoch_to_date(months):
    return datetime(1970, 1, 1) + relativedelta(months=months)

def months_ago(months):
    return datetime.now() - relativedelta(months=months)

def months_since(year, month, day):
    return months_between_dates(datetime.now(), datetime(year, month, day))

def months_since_from_date(date, date_format):
    return months_between_dates(datetime.now(), datetime.strptime(date, date_format))
