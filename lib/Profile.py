from datetime import datetime
from datetime import time
from datetime import timedelta
from .DateTimeInsulin import DateTimeInsulin
from .DateTimeInsulin import TimeInsulin

class Profile:
  def __init__(self, name, basal):
    self.name = name
    self.basal = basal

  def from_json(name, profile_json):
    p = json.loads(profile_json)
    basal = []
    for b in p['basal']:
      secs = int(b['timeAsSeconds'])
      t = time(hour=secs // 3600, minute=(secs % 3600) // 60, second=secs % 60)
      basal.append(TimeInsulin(t, float(b['value'])))
    basal.sort(key=lambda ti: ti.time)
    return Profile(name, basal)

  def __str__(self): return repr(self)

  def __repr__(self):
    return self.name + '[' + (','.join(map(str, self.basal))) + "]"

  def at(self, dt):
    current = None
    for b in self.basal:
      if b.time > dt.time():
        break
      current = b
    return current.insulin

  def series(self, start, end):
    sec = 3600 * start.hour + 60 * start.minute + start.second
    i = 0
    curr = start
    while i+1 < len(self.basal) and self.basal[i+1].time < curr.time():
      i += 1
    while curr < end:
      yield DateTimeInsulin(curr, self.basal[i].insulin)
      i += 1
      if i == len(self.basal):
        i = 0
        curr = datetime.combine(curr.date(), time()) + timedelta(days=1)
      else:
        curr = datetime.combine(curr.date(), self.basal[i].time)

