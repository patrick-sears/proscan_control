

import sys
import os
import winsound
import time

from modules.m1_basic_control import *
from modules.m99_sim_serial import spo



#######################################################
class c_muwp:
  #
  def __init__(self):
    self.x0 = None
    self.y0 = None
    self.fname_plate = None
  #
  def load_config(self):
    print("Loading config...")
    #
    fname_base =  "muwp.config"
    fname_default = "config/"+fname_base
    fname_user = "user/"+fname_base
    if os.path.isfile( fname_user ):
      fname = fname_user
      print("Found user file.")
    else:
      fname = fname_default
      print("Using default file.")
    #
    print("  Loading: ", fname )
    f = open(fname)
    for l in f:
      if not l.startswith('!'):  continue
      l = l.strip()
      ll = l.split(' ')
      key = ll[0]
      ###
      if key == '!fname_plate':
        self.fname_plate = ll[1]
      else:
        print("Error.  Unrecognized key in config file.")
        print("  key: ", key)
        sys.exit(1)
    f.close()
    print("  Done.")
  #
  def beep(self, u):
    if u == 1:
      winsound.Beep(1600,200)  # (freq in Hz, duration in ms)
      time.sleep(0.1)
      winsound.Beep(1600,200)  # (freq in Hz, duration in ms)
      # os.system('\a')
      # sys.stdout.write('\a')
      # sys.stdout.flush()
    elif u == 2:
      winsound.Beep(1600,200)  # (freq in Hz, duration in ms)
  #
  def run(self):   # run the hui (human user interface)
    self.beep(2)
    print()
    print("Entering muwp hui.")
    print("  Use q to quit.")
    while( 1 ):
      print()
      uline = input("u>> ")
      if uline == 'q':
        print()
        return
      elif uline == 'info':
        print("fname_plate: ", self.fname_plate)
        print("x0:  ", self.x0)
        print("y0:  ", self.y0)
      elif uline == 'load config':  self.load_config()
      elif uline == 'print pos':
        p()
      else:
        print("Unrecognized input.")
  #
  #
#######################################################


muwp = c_muwp()




