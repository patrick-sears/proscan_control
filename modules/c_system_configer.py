#!/usr/bin/env pyton3

import sys, os, subprocess

class c_system_configer:
  def __init__(self):
    self.load('config/system.config')
    uname = 'user/system.config'
    if os.path.isfile(uname):
      self.load(uname)
    #
    self.init_sound()
    #
  def load(self, fname):
    f = open(fname)
    for l in f:
      l = l.strip()
      if len(l) == 0:  continue
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      key = mm[0]
      if key == '!sound_mode':
        self.sound_mode = mm[1]
      elif key == '!sound_wav1':  self.sound_wav1 = mm[1]
      elif key == 'xxx':  self.xxx = mm[1]
      elif key == 'xxx':  self.xxx = mm[1]
      elif key == 'xxx':  self.xxx = mm[1]
      else:
        print("Error.  Unrecognized key.")
        print("  key: ", key)
        print("  fname: ", fname)
        sys.exit(1)
    f.close()
    #
    self.check_values()
    #
  def check_values(self):
    ok = False
    if self.sound_mode == 'no-sound':  ok=True
    if self.sound_mode == 'aplay-wav':  ok=True
    if self.sound_mode == 'winsound':  ok=True
    if not ok:
      print("Error.  Unrecognized sound mode.")
      print("  sound_mode: ", sound_mode)
      sys.exit(1)
    #
    if self.sound_mode == 'aplay-wav':
      if not os.path.isfile(self.sound_wav1):
        print("Error.")
        print("  Using sound_mode aplay-wav but the")
        print("  wav file is missing.")
        print("  sound_wav1: ", self.sound_wav1)
        sys.exit(1)
    #
  def init_sound(self):
    sm = self.sound_mode
    if sm == 'winsound':
      import winsound
      self.ws_beep = winsound.Beep
    #
  def beep1(self):
    sm = self.sound_mode
    if sm == 'no-sound':  return
    if sm == 'winsound':
      # winsound.Beep(1600,200)  # (freq in Hz, duration in ms)
      self.ws_beep(1600,200)  # (freq in Hz, duration in ms)
      return
    if sm == 'aplay-wav':
      sloc = self.sound_wav1
      cmd = ['aplay', sloc]
      subprocess.call( cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
            )
      return
    #





