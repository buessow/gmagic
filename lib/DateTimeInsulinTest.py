import unittest
from datetime import datetime
from datetime import timedelta
from DateTimeInsulin import DateTimeInsulin

class DateTimeTest(unittest.TestCase):
  def test_equals(self):
    dt1 = DateTimeInsulin(datetime(2023, 12, 4, 12, 0, 10), 10)
    dt2 = DateTimeInsulin(datetime(2023, 12, 4, 12, 0, 10), 10)
    dt3 = DateTimeInsulin(datetime(2023, 12, 4, 12, 0, 10), 11)
    dt4 = DateTimeInsulin(datetime(2023, 12, 4, 12, 0, 11), 10)
    self.assertTrue(dt1 == dt2)
    self.assertFalse(dt1 == dt3)
    self.assertFalse(dt1 == dt4)

  def test_str(self):
    dt1 = DateTimeInsulin(datetime(2023, 12, 4, 12, 0, 10), 10)
    self.assertEqual("2023-12-04T12:00:10#10.00", str(dt1))
    
class MinutelyTest(unittest.TestCase):
  dt1 = datetime(2020, 3, 1)
  dt2 = datetime(2020, 3, 1, 0, 3)
  dt3 = datetime(2020, 3, 1, 0 ,6)
  end = datetime(2020, 3, 1, 0 ,8)

  def test_minutely(self):
    dtis = list(DateTimeInsulin.minutely(
        [DateTimeInsulin(self.dt1, 6),
         DateTimeInsulin(self.dt2, 0.6),
         DateTimeInsulin(self.dt3, 1.2)],
        self.end))
    self.assertEqual(
        dtis,
        [DateTimeInsulin(datetime(2020, 3, 1, 0, 0), 0.1),
         DateTimeInsulin(datetime(2020, 3, 1, 0, 1), 0.1),
         DateTimeInsulin(datetime(2020, 3, 1, 0, 2), 0.1),
         DateTimeInsulin(datetime(2020, 3, 1, 0, 3), 0.01),
         DateTimeInsulin(datetime(2020, 3, 1, 0, 4), 0.01),
         DateTimeInsulin(datetime(2020, 3, 1, 0, 5), 0.01),
         DateTimeInsulin(datetime(2020, 3, 1, 0, 6), 0.02),
         DateTimeInsulin(datetime(2020, 3, 1, 0, 7), 0.02)])

  def test_5minutely(self):
    dtis = list(DateTimeInsulin.minutely(
        [DateTimeInsulin(self.dt1, 6),
         DateTimeInsulin(self.dt2, 0.6),
         DateTimeInsulin(self.dt3, 1.2)],
        self.end,
        timedelta(minutes=5)))
    self.assertEqual(
        dtis,
        [DateTimeInsulin(datetime(2020, 3, 1, 0, 0), 0.32),
         DateTimeInsulin(datetime(2020, 3, 1, 0, 5), 0.05)])

