

import sys
import os
import winsound
import time

from modules.m1_basic_control import *
from modules.m99_sim_serial import spo
from modules.c_locup import c_locup



#######################################################
class c_muwp:
  #
  def __init__(self):
    #
    # Assume that the stage coordinates have been set
    # from a previous run.
    self.psx0 = 0
    self.psy0 = 0
    # For now, allow resetting of these in the config file.
    #
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
  def create_locups(self):
    self.mlocup = []
    for i in range(self.n_well):
      self.mlocup.append( c_locup() )
      self.mlocup[i].load_config()
      self.mlocup[i].load_pattern_data()
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
      if key == '!fname_plate': self.fname_plate = ll[1]
      elif key == '!psx0':  self.psx0 = int(ll[1])
      elif key == '!psy0':  self.psy0 = int(ll[1])
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
  def set_fidu(self, fiduname):
    # Sets the origin of our plate coordinates using the
    # current fiducial marker position.
    ifidu = None
    for i in range(self.n_fidu):
      if fiduname == self.fidu_name[i]:
        ifidu = i
        break
    if ifidu == None:
      print("Error.  Couldn't find fidu name.")
      print("  Name: ", fiduname)
      return
    ################## 
    fidx = self.fidu_x[ifidu]
    fidy = self.fidu_y[ifidu]
    ################## 
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    psx = int(ll[0])
    psy = int(ll[1])
    ################## 
    self.psx0 = psx - fidx
    self.psy0 = psy - fidy
  #
  def go_well_center(self, iw):
    if iw < 0 or iw >= self.n_well:
      print("Error.  iw out of range.")
      print("  iw =     ", iw, " (So well #"+str(iw+1)+")")
      print("  n_well = ", self.n_well)
      return
    gx, gy = self.well_center_x[iw], self.well_center_y[iw]
    psx, psy = gx+self.psx0, gy+self.psy0
    ouline = "g"
    ouline += " {0:d}".format( psx )
    ouline += " {0:d}".format( psy )
    print("Going to:   ["+ouline+"]")
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  #
  def go_fidu(self, ifidu):
    if ifidu < 0 or ifidu >= self.n_fidu:
      print("Error.  ifidu out of range.")
      print("  ifidu =     ", ifidu, " (So fidu #"+str(ifidu+1)+")")
      print("  n_fidu = ", self.n_fidu)
      return
    gx, gy = self.fidu_x[ifidu], self.fidu_y[ifidu]
    psx, psy = gx+self.psx0, gy+self.psy0
    ouline = "g"
    ouline += " {0:d}".format( psx )
    ouline += " {0:d}".format( psy )
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
      uline = input("muwp>> ")
      if uline == 'q':
        print()
        return
      elif uline == 'info':
        print("fname_plate: ", self.fname_plate)
        print("psx0:  ", self.psx0)
        print("psy0:  ", self.psy0)
        print("well centers:")
        for i in range(self.n_well):
          print("  ", i+1, self.well_center_x[i], self.well_center_y[i])
      elif uline == 'load all':
        self.load_config()
        self.load_plate()
      elif uline == 'load config':  self.load_config()
      elif uline == 'load plate':  self.load_plate()
      elif uline == 'create locups':
        self.create_locups()
      elif uline == 'print pos':
        p()
        print("TO IMPLEMENT:  These are psx psy (prior stage).")
        print("  We would also like muwp internal plate coordinates.")
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
      elif uline.startswith('set fidu'):
        ll = uline.split(' ')
        if len(ll)!=3:
          print("Strange uline split length.")
          continue
        fiduname = ll[2]
        self.set_fidu(fiduname)
      elif uline.startswith('go fidu'):
        ll = uline.split(' ')
        if len(ll)!=3:
          print("Strange uline split length.")
          continue
        fiduname = ll[2]
        ifidu = None
        for i in range(self.n_fidu):
          if fiduname == self.fidu_name[i]:
            ifidu = i
        if ifidu == None:
          print("Error.  Couldn't find fiduname.")
          print("  fiduname: ", fiduname)
        else:
          self.go_fidu(ifidu)
      else:
        print("Unrecognized input.")
  #
  #
#######################################################


muwp = c_muwp()




