import datetime as datetime
from datetime import time
from datetime import timedelta
import math

class LogNormAction:
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

  def values_at(self, dates, values, at_dates):
    dtv = list(zip(dates, values))
    dtv.sort(key=lambda dtv: dtv[0])
    at_dates = sorted(at_dates)
    w = []
    MAX_AGE = timedelta(hours=5)

    for at in at_dates:
      # Remove everything older than 4h from the current window, since that has
      # no effect anymore.
      while len(w) > 0 and at-w[0][0] > MAX_AGE:
        w.pop(0)
      # Add new events that happened before at
      while len(dtv) > 0 and at-dtv[0][0] > MAX_AGE:
        dtv.pop(0)
      while len(dtv) > 0 and (at-dtv[0][0]).total_seconds() > 0:
        w.append(dtv.pop(0))
      # Compute the value at at by summing up the effect at at of all events
      # in the window.
      total = 0.0
      for dt, v in w:
        td = at - dt
        x = td.total_seconds() / 3600
        # print("x %f %s" % (x, str(td)))
        exp = -math.pow(math.log(x) - self.mu, 2) / (2 * self.sigma**2)
        y = 1 / (x * self.sigma * math.sqrt(2 * math.pi)) * math.exp(exp)
        total += v * y
      yield total

  def value_at(self, dates, values, at):
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
    start = datetime(2020, 1, 1)
    end = start + time
    dates = pd.date_range(start, end, freq='min')
    values = self.valuesAt([start], [1], dates)
    df = pd.DataFrame({'date': dates, 'values': values})
    ax = df.plot(ax=ax, x='date', y='values',
                 figsize=(5, 2) if ax is None else None,
                 color=color, label=label)
    ax.set_xticks(pd.date_range(start, end, freq='10min'), minor=True)
    ax.grid(which='both', axis='both', ls=':')