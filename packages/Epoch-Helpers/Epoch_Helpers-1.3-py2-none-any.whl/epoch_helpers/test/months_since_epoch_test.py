from unittest import TestCase
from epoch_helpers.months_since_epoch import *
from freezegun import freeze_time

class MonthsSinceEpochTests(TestCase):

    def test_months_since_epoch(self):
        self.assertEqual(months_since_epoch(2016, 8, 30), 559)

    def test_months_since_epoch_date(self):
        self.assertEqual(months_since_epoch_from_date('2016-08-30', '%Y-%m-%d'), 559)

    def test_months_since_epoch_to_date(self):
        self.assertEqual(months_since_epoch_to_date(559), datetime(2016, 8, 1))

    @freeze_time("2016-08-31")
    def test_months_since_from_date(self):
        self.assertEqual(months_since_from_date('2016-07-30', '%Y-%m-%d'), 1)

    @freeze_time("2016-08-31")
    def test_months_since(self):
        self.assertEqual(months_since(2016, 7, 30), 1)

    @freeze_time("2016-08-31")
    def test_months_ago(self):
        self.assertEqual(months_ago(1), datetime(2016, 7, 31))
