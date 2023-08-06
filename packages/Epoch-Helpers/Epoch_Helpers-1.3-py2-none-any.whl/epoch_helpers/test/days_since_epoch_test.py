from unittest import TestCase
from epoch_helpers.days_since_epoch import *
from freezegun import freeze_time

class DaysSinceEpochTests(TestCase):

    def test_days_since_epoch(self):
        self.assertEqual(days_since_epoch(2016, 8, 30), 17043)

    def test_days_since_epoch_date(self):
        self.assertEqual(days_since_epoch_from_date('2016-08-30', '%Y-%m-%d'), 17043)

    def test_days_since_epoch_to_date(self):
        self.assertEqual(days_since_epoch_to_date(17043), datetime(2016, 8, 30))

    @freeze_time("2016-08-31")
    def test_days_since_from_date(self):
        self.assertEqual(days_since_from_date('2016-08-30', '%Y-%m-%d'), 1)

    @freeze_time("2016-08-31")
    def test_days_since(self):
        self.assertEqual(days_since(2016, 8, 30), 1)

    @freeze_time("2016-08-31")
    def test_days_ago(self):
        self.assertEqual(days_ago(1), datetime(2016, 8, 30))
