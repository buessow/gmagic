import numpy as np
from datetime import datetime
from datetime import time
from datetime import timedelta
from .DateTimeInsulin import DateTimeInsulin

class TempBasal:
  def __init__(self, start, duration, insulin):
    self.start = start
    self.end = start + duration
    self.duration = duration
    self.insulin = None if insulin is None or np.isnan(insulin) else insulin

  def __repr__(self):
    return ('%s-%dmin ' % (str(self.start.strftime), self.duration // timedelta(minutes=1)) +
            ('-' if self.insulin is None else ('%.01f' % self.insulin)))

  def remove_zero_duration_temp_basals(tbs):
    tbs = iter(tbs)
    tb = next(tbs, None)
    while tb is not None:
      tb_next = next(tbs, None)
      if tb_next is None or tb_next.start > tb.start + timedelta(seconds=10):
        yield tb
      tb = tb_next

  def merge_temp_basal(dtis, tbs):
    dtis, tbs = iter(dtis), iter(tbs)
    dti = next(dtis, None)
    if dti is None: return
    tb = next(tbs, None)
    profile_basal = dti.insulin
    while dti is not None:
      if tb is not None and tb.start <= dti.timestamp:
        if tb.insulin is not None:
          yield DateTimeInsulin(tb.start, tb.insulin)
        tb_end = tb.end
        tb = next(tbs, None)
        while tb is not None and tb.start <= tb_end:
          if tb.insulin is not None:
            yield DateTimeInsulin(tb.start, tb.insulin)
          tb_end = tb.end
          tb = next(tbs, None)
        # skip regular profile switches that happened before end ot temp basal
        while dti is not None and dti.timestamp < tb_end:
          profile_basal = dti.insulin
          dti = next(dtis, None)
        # resume regular profile basal
        if profile_basal is not None:
          yield DateTimeInsulin(tb_end, profile_basal)

      else:
        yield dti
        profile_basal = dti.insulin
        dti = next(dtis, None)
