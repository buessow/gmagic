import unittest
from datetime import datetime
from datetime import time
from datetime import timedelta
from .DateTimeInsulin import DateTimeInsulin
from .DateTimeInsulin import TimeInsulin
from .Profile import Profile
from .ProfileSwitch import ProfileSwitch

class MergeProfileSeriesTest(unittest.TestCase):
  dt1 = datetime(2020, 3, 1)
  dt2 = datetime(2020, 3, 2)
  dt3 = datetime(2020, 3, 3)
  end = datetime(2020, 3, 4)

  def test_empty(self):
    dtis = list(ProfileSwitch.merge_series([], self.end))
    self.assertEqual(dtis, [])

  def test_oneProfileOneValue(self):
    profile = Profile('t', [TimeInsulin(time(), 0.8)])
    dtis = list(ProfileSwitch.merge_series([ProfileSwitch(self.dt1, profile)], self.end))
    self.assertEqual(
        dtis,
        [DateTimeInsulin(self.dt1, 0.8),
         DateTimeInsulin(self.dt2, 0.8),
         DateTimeInsulin(self.dt3, 0.8)])

  def test_oneProfileOneValue(self):
    profile = Profile('t', [TimeInsulin(time(), 0.8), TimeInsulin(time(hour=10), 1.8)])
    dtis = list(ProfileSwitch.merge_series([ProfileSwitch(self.dt1, profile)], self.end))
    self.assertEqual(
        dtis,
        [DateTimeInsulin(self.dt1, 0.8),
         DateTimeInsulin(self.dt1 + timedelta(hours=10), 1.8),
         DateTimeInsulin(self.dt2, 0.8),
         DateTimeInsulin(self.dt2 + timedelta(hours=10), 1.8),
         DateTimeInsulin(self.dt3, 0.8),
         DateTimeInsulin(self.dt3 + timedelta(hours=10), 1.8)])

  def test_twoProfilesOneValue(self):
    ps1 = ProfileSwitch(self.dt1, Profile('t', [TimeInsulin(time(), 0.8)]))
    ps2 = ProfileSwitch(self.dt1 + timedelta(hours=11), Profile('t', [TimeInsulin(time(), 1.8)]))
    dtis = list(ProfileSwitch.merge_series([ps1, ps2], self.end))
    self.assertEqual(
        dtis,
        [DateTimeInsulin(self.dt1, 0.8),
         DateTimeInsulin(ps2.timestamp, 1.8),
         DateTimeInsulin(self.dt2, 1.8),
         DateTimeInsulin(self.dt3, 1.8)])

  def test_twoProfilesTwoValues(self):
    ps1 = ProfileSwitch(
        self.dt1,
        Profile('t', [TimeInsulin(time(), 0.8), TimeInsulin(time(hour=10), 1.4)]))
    ps2 = ProfileSwitch(
        self.dt1 + timedelta(hours=11),
        Profile('t', [TimeInsulin(time(), 1.8), TimeInsulin(time(hour=9), 2.0)]))
    dtis = list(ProfileSwitch.merge_series([ps1, ps2], self.end))
    self.assertEqual(
        dtis,
        [DateTimeInsulin(self.dt1, 0.8),
         DateTimeInsulin(self.dt1 + timedelta(hours=10), 1.4),
         DateTimeInsulin(self.dt1 + timedelta(hours=11), 2.0),
         DateTimeInsulin(self.dt2, 1.8),
         DateTimeInsulin(self.dt2 + timedelta(hours=9), 2.0),
         DateTimeInsulin(self.dt3, 1.8),
         DateTimeInsulin(self.dt3 + timedelta(hours=9), 2.0)])
