import argparse
from epoch_helpers.days_since_epoch import *
from epoch_helpers.months_since_epoch import *

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dse', '--days-since-epoch', nargs='?', const='', help='Use --days-since-epoch if you want to convert a date string or year, month, day to the number of days since January 1st, 1970')
    parser.add_argument('-y', '--year', type=int, help='The year to convert from. Example: --year 1996')
    parser.add_argument('-m', '--month', type=int, help='The month to convert from. Example: --month 12')
    parser.add_argument('-d', '--day', type=int, help='The day to convert from. Example: --day 24')
    parser.add_argument('-df', '--date-format', help='The date format used when converting a date string', default='%Y-%m-%d')
    parser.add_argument('-dtd', '--days-to-date', type=int, help='Use --days-to-date when you would like to convert the number of days since January 1st, 1970 to a date.')
    parser.add_argument('-da', '--days-ago', type=int, help='The date that is X number of days ago from the current date. Example: --days-ago 7')
    parser.add_argument('-ds', '--days-since', nargs='?', const='', help='The number of days since a specific date. Example: --days-since 2016-08-01.')

    parser.add_argument('-mse', '--months-since-epoch', nargs='?', const='', help='Use --months-since-epoch if you want to convert a date string or year, month, day to the number of months since January 1st, 1970')
    parser.add_argument('-mtd', '--months-to-date', type=int, help='Use --months-to-date when you would like to conver the number of months since January 1st, 1970 to a date.')
    parser.add_argument('-ma', '--months-ago', type=int, help='The date that is X number of months ago from the current date.')
    parser.add_argument('-ms', '--months-since', nargs='?', const='', help='The number of months since a specific date.')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    ymd_args = [args.year, args.month, args.day]
    has_ymd = all(ymd_args)
    if args.days_ago:
        print(days_ago(args.days_ago))
    elif args.days_since is not None:
        if has_ymd:
            print(days_since(*ymd_args))
        else:
            print(days_since_from_date(args.days_since, args.date_format))
    elif args.days_since_epoch is not None:
        if has_ymd:
            print(days_since_epoch(*ymd_args))
        else:
            print(days_since_epoch_from_date(args.days_since_epoch, args.date_format))
    elif args.days_to_date:
        print(days_since_epoch_to_date(args.days_to_date))
    elif args.months_since is not None:
        if has_ymd:
            print(months_since(*ymd_args))
        else:
            print(months_since_from_date(args.months_since, args.date_format))
    elif args.months_since_epoch is not None:
        if has_ymd: 
            print(months_since_epoch(*ymd_args))
        else:
            print(months_since_epoch_from_date(args.months_since_epoch, args.date_format))
    elif args.months_to_date:
        print(months_since_epoch_to_date(args.months_to_date))
    elif args.months_ago:
        print(months_ago(args.months_ago))


if __name__ == '__main__':
    main()

