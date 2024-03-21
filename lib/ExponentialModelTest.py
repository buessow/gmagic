import unittest
import datetime as dt
import numpy as np
from .ExponentialModel import ExponentialModel

class ExponentialModelTest(unittest.TestCase):
    """
    Test cases for the Fiasp insulin model's insulinOnBoard function.
    """

    def setUp(self):
        self.fiasp = ExponentialModel(peak=dt.timedelta(minutes=55), total=dt.timedelta(hours=6))

    def test_insulin_on_board(self):
        self.assertAlmostEqual(self.fiasp.insulin_on_board(dt.timedelta(minutes=-1)), 1.0)
        self.assertAlmostEqual(self.fiasp.insulin_on_board(dt.timedelta()), 1.0)
        self.assertAlmostEqual(self.fiasp.insulin_on_board(dt.timedelta(minutes=45)), 0.788, delta=1e-3)
        self.assertAlmostEqual(self.fiasp.insulin_on_board(dt.timedelta(minutes=55)), 0.717, delta=1e-3)
        self.assertAlmostEqual(self.fiasp.insulin_on_board(dt.timedelta(minutes=120)), 0.314, delta=1e-3)
        self.assertAlmostEqual(self.fiasp.insulin_on_board(dt.timedelta(minutes=360)), 0.0, delta=1e-3)
        self.assertAlmostEqual(self.fiasp.insulin_on_board(dt.timedelta(minutes=420)), 0.0, delta=1e-3)

    def test_values_at(self):
        """
        Test the valuesAt function for calculating cumulative insulin values.
        """

        t = dt.datetime.fromisoformat("2013-12-13T20:00:00Z").astimezone(dt.timezone.utc)

        # Create a list of timestamps with offsets
        timestamps = [t + dt.timedelta(minutes=m) for m in [5, 30, 55, 120, 180, 230, 360]]

        results = self.fiasp.values_at([t], [5], t, timestamps)
        expected_values = [0.021, 0.537, 0.860, 2.011, 0.999, 0.372, 0.202]
        np.testing.assert_almost_equal(results, expected_values, 2)

        # Verify total insulin delivered matches initial dose
        self.assertAlmostEqual(sum(results), 5.0, delta=1e-2)

        double_results = self.fiasp.values_at([t], [10], t, timestamps)
        double_expected = [value * 2 for value in expected_values]
        np.testing.assert_almost_equal(double_results, double_expected, 2)
        self.assertAlmostEqual(sum(double_results), 10.0, delta=1e-2)

    def test_str(self):
      self.assertEqual('Exponential(0:55:00, 6:00:00)', str(self.fiasp))

