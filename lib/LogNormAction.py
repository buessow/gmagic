import datetime as dt
import pandas as pd
import numpy as np
import math
from datetime import time
from datetime import timedelta

class LogNormAction:
  name = 'LogNorm'
  def __init__(self, mu=None, sigma=1.0, mode=None):
    """Constructor.
    Args:
      mu: mean for log norm computation
      sigma: standard deviation for log norm computation
    """
    if mode is not None and sigma is not None:
      if isinstance(mode, timedelta):
        mode = mode.total_seconds() / 3600
      self.mu = math.log(mode) + sigma**2
    else:
      self.mu = mu
    self.sigma = sigma
    print("mode %f" % math.exp(self.mu - self.sigma**2))

  @property
  def args(self):
    return dict(name=self.name, mu=self.mu, sigma=self.sigma)

  def approx_error_function(x):
    """Computes an approximation of the error function (erf).
       https://en.wikipedia.org/wiki/Error_function#Bürmann_series
    """
    PI_SQRT = math.sqrt(math.pi)
    C1 = 31.0 / 200.0
    C2 = 341.0 / 8000.0
    e_x2 = math.exp(-x * x)
    e_2x2 = math.exp(-2 * x * x)
    return 2 / PI_SQRT * math.signum(x) * math.sqrt(1 - e_x2) * (PI_SQRT / 2 + C1 * e_x2 - C2 * e_2x2)

  def quantity_until(self, at, until):
    """Computes the cumulative value until date.
       {@linktourl https://en.wikipedia.org/wiki/Log-normal_distribution#Cumulative_distribution_function}
    """
    x = (date - at).total_seconds() / 3600
    if x <= 0.0:
      return 0.0
    return 0.5 * (1 + approx_error_function((math.log(x) - self.mu) / (self.sigma * math.sqrt(2))))

  def quantity_within(self, dates, values, start, end):
    total = 0.0;
    for dt, v in zip(dates, values):
      total += v * (quantity_until(dt, end) - quantity_until(dt, start))
    return total


  def values_at(self, dates, values, start, at_dates):
    dtv = list(zip(dates, values))
    dtv.sort(key=lambda dtv: dtv[0])
    at_dates = sorted(at_dates)
    MAX_AGE = np.timedelta64(5, 'h')
    win_start = 0
    win_end = 0
      
    for at in at_dates:
      # Ignore everything older than 4h from the current window, since that has
      # no effect anymore.
      while win_start < len(dtv) and at-dtv[win_start][0] > MAX_AGE:
        win_start += 1
      # Move window end to 'at'
      win_end = max(win_start, win_end)
      while win_end < len(dtv) and dtv[win_end][0] < at:
        win_end += 1

      # Sum up action at 'at' from all events in the window
      total = 0.0
      for i in range(win_start, win_end):
        dt, v = dtv[i]
        td = at - dt
        x = td / np.timedelta64(1, 'h')
        exp = -math.pow(math.log(x) - self.mu, 2) / (2 * self.sigma**2)
        y = 1 / (x * self.sigma * math.sqrt(2 * math.pi)) * math.exp(exp)
        total += v * y
      yield total

  def value_at(self, dates, values, start, at):
    total = 0.0
    for dt, v in zip(dates, values):
      td = at - dt
      if td <= timedelta(): break
      if td > timedelta(hours=4): continue 
      x = td.total_seconds() / 3600.0
      exp = -math.pow(math.log(x) - self.mu, 2) / (2 * self.sigma**2)
      y = 1 / (x * self.sigma * math.sqrt(2 * math.pi)) * math.exp(exp)
      total += v * y
    return total

  def plot(self, time, color='red', label='', ax=None):
    """Plots the action curve over given amount of time.
    Args:
        time: timedelta amount of time
        color: string color of the graph
        label: string label of the graph
        ax: axis to use for plotting."""
    start = dt.datetime(2020, 1, 1)
    end = start + time
    dates = pd.date_range(start, end, freq='min')
    values = self.values_at([start], [1], start, dates)
    df = pd.DataFrame({'date': dates, 'values': values})
    ax = df.plot(ax=ax, x='date', y='values',
                 figsize=(5, 2) if ax is None else None,
                 color=color, label=label)
    ax.set_xticks(pd.date_range(start, end, freq='10min'), minor=True)
    ax.grid(which='both', axis='both', ls=':')
