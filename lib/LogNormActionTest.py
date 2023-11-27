import unittest
import LogNormAction as lna
import datetime as datetime

class LogNormActionAction(unittest.TestCase):

  def test_create(self):
    lna.LogNormAction(3)

  def test_plot(self):
    lna.LogNormAction(3).plot(datetime.timedelta(hours(1))
