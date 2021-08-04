

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
    self.clear_fidu()
    self.clear_well_center()
    self.clear_ins_center()
  #
  def clear_fidu(self):
    self.fidu_name = []
    self.fidu_x = []
    self.fidu_y = []
    self.n_fidu = 0
  #
  def clear_well_center(self):
    self.well_center_x = []
    self.well_center_y = []
    self.n_well = 0
  #
  def clear_ins_center(self):
    self.ins_center_x = []
    self.ins_center_y = []
    self.n_ins = 0
  #
  def load_plate(self):
    print("Loading plate data...")
    fname_base = self.fname_plate
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
      if key == '!fidu':
        self.clear_fidu()
        for l in f:
          l = l.strip()
          ll = l.split(' ')
          if len(l) == 0:  break
          if l[0] == '#':  continue
          self.fidu_name.append( ll[0] )
          self.fidu_x.append( int(ll[1]) )
          self.fidu_y.append( int(ll[2]) )
        self.n_fidu = len(self.fidu_x)
      elif key == '!well_center':
        self.clear_well_center()
        for l in f:
          l = l.strip()
          ll = l.split(' ')
          if len(l) == 0:  break
          if l[0] == '#':  continue
          self.well_center_x.append( int(ll[1]) )
          self.well_center_y.append( int(ll[2]) )
        self.n_well = len(self.well_center_x)
      elif key == '!ins_center':
        self.clear_ins_center()
        for l in f:
          l = l.strip()
          ll = l.split(' ')
          if len(l) == 0:  break
          if l[0] == '#':  continue
          self.ins_center_x.append( int(ll[1]) )
          self.ins_center_y.append( int(ll[2]) )
        self.n_ins = len(self.ins_center_x)
      else:
        print("Error.  Unrecognized key in config file.")
        print("  key: ", key)
        sys.exit(1)
    f.close()
    print("  Done.")
  #
  def load_config(self):
    print("Loading config...")
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
  def go_well_center(self, iw):
    if iw < 0 or iw >= self.n_well:
      print("Error.  iw out of range.")
      print("  iw =     ", iw, " (So well #"+str(iw+1)+")")
      print("  n_well = ", self.n_well)
      return
    gx, gy = self.well_center_x[iw], self.well_center_y[iw]
    ouline = "g"
    ouline += " {0:d}".format( gx )
    ouline += " {0:d}".format( gy )
    print("Going to:   ["+ouline+"]")
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  #
  def run(self, amode=0):   # run the hui (human user interface)
    self.beep(2)
    print()
    print("Entering muwp hui.")
    print("  Use q to quit.")
    if amode == 1:
      self.load_config()
      self.load_plate()
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
        print("well centers:")
        for i in range(self.n_well):
          print("  ", i+1, self.well_center_x[i], self.well_center_y[i])
      elif uline == 'load all':
        self.load_config()
        self.load_plate()
      elif uline == 'load config':  self.load_config()
      elif uline == 'load plate':  self.load_plate()
      elif uline == 'print pos':
        p()
      elif uline.startswith('go well'):
        ll = uline.split(' ')
        if len(ll)!=4:
          print("Strange uline split length.")
          continue
        iw = int( uline.split(' ')[2] ) - 1
        ppos = ll[3]
        if ppos == 'center':  self.go_well_center(iw)
        else:
          print("Unrecognized ppos: ", ppos)
      else:
        print("Unrecognized input.")
  #
  #
#######################################################


muwp = c_muwp()




