import pandas as pd
import math
import datetime as dt

class ExponentialModel:
  name = 'Exponential'
  def __init__(self, peak, total):
    self.peak = peak
    self.total = total

    self.tp = peak / dt.timedelta(minutes=1)
    self.td = total / dt.timedelta(minutes=1)

    self.tau = self.tp * (1 - self.tp / self.td) / (1 - 2 * self.tp / self.td)
    self.a = 2 * self.tau / self.td
    self.S = 1 / (1 - self.a + (1 + self.a) * math.exp(-self.td / self.tau))

  def insulin_action(self, t):
      """
      Calculates the insulin action at a given time (in minutes).

      Args:
          t (float): Time (in minutes).

      Returns:
          float: The insulin action value.
      """
      return (self.S / (self.tau * self.tau)) * t * (1 - t / self.td) * math.exp(-t / self.tau)

  @property
  def args(self):
    return dict(name=self.name, peak=self.tp, total=self.td)

  def insulin_on_board(self, duration):
      """
      Calculates the amount of insulin remaining active (on board) at a given
      duration after injection.

      Args:
          t (TimeDelta): 

      Returns:
          float: The amount of insulin on board.
      """
      if duration < dt.timedelta():
          return 1.0
      elif duration > self.total:
          return 0.0
      else:
          t = duration / dt.timedelta(minutes=1)
          return 1 - self.S * (1 - self.a) * (
              ((t * t) / (self.tau * self.td * (1 - self.a)) - t / self.tau - 1)
              * math.exp(-t / self.tau)
              + 1
          )

  def insulin_used(self, injection, start, upto):
    r = self.insulin_on_board(start - injection) - self.insulin_on_board(upto - injection)
    return r

  def values_at(self, dates, values, start, times):
    """
    Calculates the cumulative value within a time window for each timestamp.

    Args:
        values: List of data points containing timestamp and value.
        start: Starting timestamp for the window.
        times: Iterable of timestamps for which to calculate the value.

    Returns:
        List of doubles representing the cumulative value at each timestamp.
    """
    results = []

    last = start
    win_start = 0
    for t in times:
      # Move the first element in the window
      while win_start < len(values) and t - self.total > dates[win_start]:
        win_start += 1

      total = 0.0
      i = win_start
      while i < len(values):
        timestamp, value = dates[i], values[i]
        if timestamp > t: break
        # Calculate insulin used within the window
        insulin_ratio = self.insulin_used(timestamp, last, t)
        total += value * insulin_ratio
        i += 1
      
      last = t
      results.append(total)
    return results    

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

