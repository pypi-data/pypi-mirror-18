from datetime import datetime, timedelta

EPOCH = datetime(1970, 1, 1)

def days_since_epoch(year, month, day):
    return (datetime(year, month, day) - EPOCH).days

def days_since_epoch_from_date(date, date_format):
    return (datetime.strptime(date, date_format) - EPOCH).days

def days_since_epoch_to_date(days):
    return datetime(1970, 1, 1) + timedelta(days)

def days_ago(days):
    return datetime.now() - timedelta(days)

def days_since(year, month, day):
    return (datetime.now() - datetime(year, month, day)).days

def days_since_from_date(date, date_format):
    return (datetime.now() - datetime.strptime(date, date_format)).days
