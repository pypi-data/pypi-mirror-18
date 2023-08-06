import argparse
from epoch_helpers.days_since_epoch import *

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ds', '--days-since-epoch', action='store_true', help='Use --days-since-epoch if you want to convert a date string or year, month, day to the number of days since January 1st, 1970')
    parser.add_argument('-ms', '--millis-since-epoch', action='store_true', help='Use millis since epoch when you want the milliseconds since January 1st, 1970 for a specific date')
    parser.add_argument('-y', '--year', type=int, help='The year to convert from. Example: --year 1996')
    parser.add_argument('-m', '--month', type=int, help='The month to convert from. Example: --month 12')
    parser.add_argument('-d', '--day', type=int, help='The day to convert from. Example: --day 24')
    parser.add_argument('-da', '--date', help='The date to convert from. Example: --date 2016-09-01')
    parser.add_argument('-df', '--date-format', help='The date format used when converting a date string', default='%Y-%m-%d')
    parser.add_argument('-dtd', '--days-to-date', action='store_true', help='Use --days-to-date when you would like to convert the number of days since January 1st, 1970 to a date. Example: --days-to-date')
    parser.add_argument('-nd', '--days', type=int, help='The number of days since January 1st, 1970. Example: --days 17043')
    parser.add_argument('-dg', '--days-ago', type=int, help='The date that is X number of days ago from the current date. Example: --days-ago 7')
    parser.add_argument('-di', '--days-since', action='store_true', help='The number of days since a specific date. Example: --days-since --date 2016-08-01.')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.days_ago:
        print(days_ago(args.days_ago))
    elif args.days_since:
        if args.date:
            print(days_since_from_date(args.date, args.date_format))
        elif all([args.year, args.month, args.day]):
            print(days_since(args.year, args.month, args.day))
        else:
            raise Exception("Incorrect usage of --days-since. See -h for examples")
    elif args.days_since_epoch:
        if args.date:
            print(days_since_epoch_from_date(args.date, args.date_format))
        elif all([args.year, args.month, args.day]):
            print(days_since_epoch(args.year, args.month, args.day))
        else:
            raise Exception("Incorrect usage of --days-since-epoch. See -h for examples")
    elif args.days_to_date:
        if args.days:
            print(days_since_epoch_to_date(args.days))
        else:
            raise Exception('Incorrect usage of --days-to-date. See -h for examples')


if __name__ == '__main__':
    main()

