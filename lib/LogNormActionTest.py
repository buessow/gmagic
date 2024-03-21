import unittest
import datetime as dt
from .LogNormAction import LogNormAction

class LogNormActionAction(unittest.TestCase):

  def test_create(self):
    a = LogNormAction(3)
    self.assertEquals(dict(name='LogNorm', mu=3, sigma=1.0), a.args)
    t = dt.datetime(2023, 11, 1)
    self.assertAlmostEqual(0.0, a.value_at([t], [10.0], t, t))
    self.assertLess(0.0, a.value_at([t], [10.0], t, t + dt.timedelta(hours=1)))
    
  def test_values_at(self):
    a = LogNormAction(mode=dt.timedelta(hours=3))
    t = dt.datetime(2023, 11, 1)
    self.assertAlmostEqual(0.0, a.value_at([t], [5.0], t, t))
    self.assertAlmostEqual(0.08099936958648521, a.value_at([t], [5.0], t, t + dt.timedelta(minutes=30)))
    self.assertAlmostEqual(0.3714600764604711, a.value_at([t], [5.0], t, t + dt.timedelta(hours=2)))
    self.assertAlmostEqual(0.4032845408652389, a.value_at([t], [5.0], t, t + dt.timedelta(hours=3)))
    self.assertAlmostEqual(0.39134904494144485, a.value_at([t], [5.0], t, t + dt.timedelta(hours=3, minutes=50)))

  def test_str(self):
    a = LogNormAction(mode=dt.timedelta(hours=2), sigma=0.3)
    self.assertEqual('LogNorm(120, 0.3)', str(a))
    self.assertEqual('LogNorm(120, 0.3)', repr(a))


