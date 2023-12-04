from datetime import datetime
from datetime import timedelta

class TimeInsulin:
  def __init__(self, time, insulin):
    self.time = time
    self.insulin = insulin
  def __eq__(self, other):
    return (type(self) == type(other) and
            self.time == other.time and
            self.insulin == other.insulin)
  def __repr__(self):
    return '%s#%.2f' % (self.time.strftime('%H:%M'), self.insulin)

class DateTimeInsulin:
  def __init__(self, timestamp, insulin):
    self.timestamp = timestamp
    self.insulin = insulin
  def __eq__(self, other):
    return (type(self) == type(other) and
            self.timestamp == other.timestamp and
            self.insulin == other.insulin)
  def __str__(self): return repr(self)
  def __repr__(self):
    return '%s#%.2f' % (self.timestamp.strftime('%Y-%m-%dT%H:%M:%S'), self.insulin)

  def to_data(dtis):
    dates = [dti.timestamp for dti in dtis]
    values = [dti.insulin for dti in dtis]
    return {'dates': dates, 'values': values}

  def minutely(dtis, end=datetime.now(), interval=timedelta(minutes=1)):
    def safeNext():
      dti0 = next(dtis, None)
      return DateTimeInsulin(end, 0) if dti0 is None else dti0
    dtis = iter(dtis)
    dti = safeNext()
    dti_next = safeNext()
    dt = dti.timestamp.replace(second=0, microsecond=0)

    while dt < end:
      dt_sub = dt
      insulin = 0
      while True:
        sub_interval = min(dti_next.timestamp, dt + interval) - dt_sub
        insulin += dti.insulin * sub_interval.total_seconds() / 3600
        if dt_sub < end and dt + interval > dti_next.timestamp:
          dt_sub = dti_next.timestamp
          dti = dti_next
          dti_next = safeNext()
        else:
          break
      yield DateTimeInsulin(dt, insulin)
      dt += interval

    def mergeDateTimeInsulins(dtis1, dtis2):
      dtis1, dtis2 = iter(dtis1), iter(dtis2)
      dti1 = next(dtis1, None)
      dti2 = next(dtis2, None)
      while dti1 is not None or dti2 is not None:
        if dti1 is not None and dti2 is None or dti1.timestamp < dti2.timestamp:
          yield dti1
          dti1 = next(dtis1, None)
        elif dti1 is None or dti2.timestamp < dti1.timestamp:
          yield dti2
          dti2 = next(dtis2, None)
        else:
          yield DateTimeInsulin(dti1.timestamp, dti1.insulin + dti2.insulin)
          dti1 = next(dtis1, None)
          dti2 = next(dtis2, None)

  def removeNoneInsulin(dtis):
    for dti in dtis:
      if dti.insulin is not None:
        yield dti
