import unittest
from datetime import datetime
from datetime import time
from datetime import timedelta
from DateTimeInsulin import DateTimeInsulin
from DateTimeInsulin import TimeInsulin
from Profile import Profile

class ProfileTest(unittest.TestCase):
  dt1 = datetime(2020, 3, 1)
  dt2 = datetime(2020, 3, 2)
  end = datetime(2020, 3, 3)

  def test_oneValue(self):
    profile = Profile("t", [TimeInsulin(time(), 0.8)])
    self.assertEqual('00:00#0.80', str(profile.basal[0]))
    self.assertEqual('t[00:00#0.80]', str(profile))
    self.assertEqual(list(profile.series(self.dt1, self.end)),
                     [DateTimeInsulin(self.dt1, 0.8),
                      DateTimeInsulin(self.dt2, 0.8)])

  def test_twoValues(self):
    profile = Profile("t", [TimeInsulin(time(), 0.8), TimeInsulin(time(hour=8), 1.1)])
    self.assertEqual(list(profile.series(self.dt1, self.end)),
                     [DateTimeInsulin(self.dt1, 0.8),
                      DateTimeInsulin(self.dt1 + timedelta(hours=8), 1.1),
                      DateTimeInsulin(self.dt2, 0.8),
                      DateTimeInsulin(self.dt2 + timedelta(hours=8), 1.1)])

  def test_twoValues2(self):
    profile = Profile("t", [TimeInsulin(time(), 0.8), TimeInsulin(time(hour=8), 1.1)])
    self.assertEqual(list(profile.series(self.dt1, self.dt1 + timedelta(hours=12))),
                    [DateTimeInsulin(self.dt1, 0.8),
                     DateTimeInsulin(self.dt1 + timedelta(hours=8), 1.1)])
