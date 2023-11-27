import unittest
import LogNormAction as lna
import datetime as dt

class LogNormActionAction(unittest.TestCase):

  def test_create(self):
    a = lna.LogNormAction(3)
    t = dt.datetime(2023, 11, 1)
    self.assertEqual( 0.0, a.value_at([t], [10.0], t))
    self.assertLess( 0.0, a.value_at([t], [10.0], t + dt.timedelta(hours=1)))

