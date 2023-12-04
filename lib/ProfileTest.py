import unittest
from datetime import datetime
from datetime import time
from datetime import timedelta
from .DateTimeInsulin import DateTimeInsulin
from .DateTimeInsulin import TimeInsulin
from .Profile import Profile

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
                    
  def test_from_json(self):
    json = """{"dia":"5","carbratio":[{"time":"00:00","value":"10","timeAsSeconds":"0"},{"time":"16:00","value":"8","timeAsSeconds":"57600"}],"carbs_hr":"15","delay":"20","sens":[{"time":"00:00","value":"2","timeAsSeconds":"0"}],"timezone":"Europe\/Zurich","basal":[{"time":"00:00","value":"0.56","timeAsSeconds":"0"},{"time":"01:00","value":"0.64","timeAsSeconds":"3600"},{"time":"02:00","value":"0.64","timeAsSeconds":"7200"},{"time":"03:00","value":"0.68","timeAsSeconds":"10800"},{"time":"04:00","value":"0.68","timeAsSeconds":"14400"},{"time":"05:00","value":"0.72","timeAsSeconds":"18000"},{"time":"06:00","value":"0.84","timeAsSeconds":"21600"},{"time":"07:00","value":"0.88","timeAsSeconds":"25200"},{"time":"08:00","value":"0.8","timeAsSeconds":"28800"},{"time":"09:00","value":"0.96","timeAsSeconds":"32400"},{"time":"10:00","value":"0.96","timeAsSeconds":"36000"},{"time":"11:00","value":"0.96","timeAsSeconds":"39600"},{"time":"12:00","value":"1.05","timeAsSeconds":"43200"},{"time":"13:00","value":"1.05","timeAsSeconds":"46800"},{"time":"14:00","value":"1.5","timeAsSeconds":"50400"},{"time":"15:00","value":"1.45","timeAsSeconds":"54000"},{"time":"16:00","value":"1.2","timeAsSeconds":"57600"},{"time":"17:00","value":"0.88","timeAsSeconds":"61200"},{"time":"18:00","value":"0.8","timeAsSeconds":"64800"},{"time":"19:00","value":"0.8","timeAsSeconds":"68400"}],"target_low":[{"time":"00:00","value":"4.5","timeAsSeconds":"0"}],"target_high":[{"time":"00:00","value":"7.5","timeAsSeconds":"0"}],"startDate":"1970-01-01T00:00:00.000Z","units":"mmol"}"""
    p = Profile.from_json('test', json)
    self.assertEquals('test', p.name)
    self.assertEquals(20, len(p.basal))
    self.assertEquals(TimeInsulin(time(0), 0.56), p.basal[0])
    self.assertEquals(TimeInsulin(time(6), 0.84), p.basal[6])

