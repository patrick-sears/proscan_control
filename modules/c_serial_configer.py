#!/usr/bin/env python3

import sys

class c_serial_configer:
  def __init__(self):
    self.timeout = 1.0
    pass
  def load(self, funame):
    f = open(funame)
    for l in f:
      l = l.strip()
      if len(l) == 0:  continue
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      key = mm[0]
      if key == '!timeout':  self.timeout = float(mm[1])
      elif key == '!port':  self.port = mm[1]
      elif key == '!serial_mode':  self.serial_mode = mm[1]
      elif key == '!xxx':  self.xxx = mm[1]
      else:
        print("Error.  Unrecognized key in c_serial_configer.")
        print("  funame: ", funame)
        print("  key:    ", key)
        sys.exit(1)
    f.close()
    # print("Using timeout: ", self.timeout)
    self.check_vals()
    #
  def check_vals(self):
    ok = False
    if self.serial_mode == 'hardware':  ok = True
    if self.serial_mode == 'simulation':  ok = True
    if not ok:
      print("Error.  Unrecognized serial_mode.")
      print("  serial_mode: ", serial_mode)
      sys.exit(1)



