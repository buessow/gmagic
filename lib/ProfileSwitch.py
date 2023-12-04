from datetime import datetime

class ProfileSwitch:
  def __init__(self, dt, profile):
    self.timestamp = dt
    self.profile = profile

  def __str__(self): return repr(self)
  def __repr__(self):
    return '[%s: %s]' % (self.timestamp.isoformat(), str(self.profile))

  def next(self, dt):
    return self.profile.at(dt + timedelta(0, 0, 1))

  def merge_series(profile_switches, end=datetime.now()):
    profile_switches = iter(profile_switches)
    ps = next(profile_switches, None)
    while ps is not None:
      psn = next(profile_switches, None)
      next_end = end if psn is None else psn.timestamp
      for dti in ps.profile.series(ps.timestamp, next_end): yield dti
      ps = psn
