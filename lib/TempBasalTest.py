import unittest
from datetime import datetime
from datetime import time
from datetime import timedelta
from DateTimeInsulin import DateTimeInsulin
from DateTimeInsulin import TimeInsulin
from TempBasal import TempBasal

class TempBasalTest(unittest.TestCase):
  dt1 = datetime(2020, 3, 1)
  dt2 = datetime(2020, 3, 2)
  dt3 = datetime(2020, 3, 3)

  def test_empty(self):
    tis = list(TempBasal.merge_temp_basal([], []))
    self.assertEqual(tis, [])

  def test_oneProfile(self):
    tis = list(TempBasal.merge_temp_basal([DateTimeInsulin(self.dt1, 1.1)], []))
    self.assertEqual(tis, [DateTimeInsulin(self.dt1, 1.1)])

  def test_twoProfiles(self):
    tis = list(TempBasal.merge_temp_basal([DateTimeInsulin(self.dt1, 1.1), DateTimeInsulin(self.dt3, 1.4)], []))
    self.assertEqual(tis, [DateTimeInsulin(self.dt1, 1.1), DateTimeInsulin(self.dt3, 1.4)])

  def test_twoProfilesWithTemp(self):
    tis = list(TempBasal.merge_temp_basal([DateTimeInsulin(self.dt1, 1.1), DateTimeInsulin(self.dt3, 1.4)],
                              [TempBasal(self.dt2, timedelta(hours=1), 0.5)]))
    self.assertEqual(tis, [DateTimeInsulin(self.dt1, 1.1),
                           DateTimeInsulin(self.dt2, 0.5),
                           DateTimeInsulin(self.dt2 + timedelta(hours=1), 1.1),
                           DateTimeInsulin(self.dt3, 1.4)])

  def test_twoProfilesWithCanceledTemp(self):
    tis = list(TempBasal.merge_temp_basal([DateTimeInsulin(self.dt1, 1.1), DateTimeInsulin(self.dt3, 1.4)],
                              [TempBasal(self.dt2, timedelta(hours=3), 0.5),
                               TempBasal(self.dt2 + timedelta(minutes=10), timedelta(), None)]))
    self.assertEqual(tis, [DateTimeInsulin(self.dt1, 1.1),
                           DateTimeInsulin(self.dt2, 0.5),
                           DateTimeInsulin(self.dt2 + timedelta(minutes=10), 1.1),
                           DateTimeInsulin(self.dt3, 1.4)])

  def test_twoProfilesWithTempOverlapping(self):
    tis = list(TempBasal.merge_temp_basal([DateTimeInsulin(self.dt1, 1.1), DateTimeInsulin(self.dt3, 1.4)],
                              [TempBasal(self.dt2, timedelta(hours=25), 0.5)]))
    self.assertEqual(tis, [DateTimeInsulin(self.dt1, 1.1),
                           DateTimeInsulin(self.dt2, 0.5),
                           DateTimeInsulin(self.dt2 + timedelta(hours=25), 1.4)])

  def test_twoProfilesWithTempOverlapping(self):
    tis = list(TempBasal.merge_temp_basal([DateTimeInsulin(self.dt1, 1.1), DateTimeInsulin(self.dt2, 1.4)],
                              [TempBasal(self.dt2, timedelta(hours=25), 0.5)]))
    self.assertEqual(tis, [DateTimeInsulin(self.dt1, 1.1),
                           DateTimeInsulin(self.dt2, 0.5),
                           DateTimeInsulin(self.dt2 + timedelta(hours=25), 1.4)])

  def test_twoProfilesWithTwoTemp(self):
    tis = list(TempBasal.merge_temp_basal(
        [DateTimeInsulin(self.dt1, 1.1), DateTimeInsulin(self.dt3, 1.4)],
        [TempBasal(self.dt2, timedelta(hours=25), 0.5),
         TempBasal(self.dt2 + timedelta(minutes=10), timedelta(hours=25, minutes=1), 0.6)]))
    self.assertEqual(
        tis,
        [DateTimeInsulin(self.dt1, 1.1),
         DateTimeInsulin(self.dt2, 0.5),
         DateTimeInsulin(self.dt2 + timedelta(minutes=10), 0.6),
         DateTimeInsulin(self.dt2 + timedelta(hours=25, minutes=11), 1.4)])
