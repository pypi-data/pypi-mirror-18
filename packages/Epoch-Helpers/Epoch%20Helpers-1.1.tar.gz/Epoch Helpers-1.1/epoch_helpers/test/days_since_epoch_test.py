from unittest import TestCase
from epoch_helpers.days_since_epoch import *

class DaysSinceEpochTests(TestCase):

    def test_days_since_epoch(self):
        self.assertEqual(days_since_epoch(2016, 8, 30), 17043)

    def test_days_since_epoch_date(self):
        self.assertEqual(days_since_epoch_from_date('2016-08-30', '%Y-%m-%d'), 17043)

    def test_days_since_epoch_to_date(self):
        self.assertEqual(days_since_epoch_to_date(17043), datetime(2016, 8, 30))