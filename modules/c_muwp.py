

import sys
import os
import winsound
import time
from datetime import datetime
import shutil

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
      self.mlocup[i].cx = self.ins_center_x[i]
      self.mlocup[i].cy = self.ins_center_y[i]
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
      elif key == '!psx0':  self.psx0 = int(ll[1])
      elif key == '!psy0':  self.psy0 = int(ll[1])
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
  def save_plate(self):
    fz_name = 'user/muwp_plate.data'
    if os.path.exists( fz_name ):
      stime = datetime.now().strftime("%Y%m%d_%H%M%S")
      fbak_name = fz_name + '.'+stime+'.bak'
      shutil.copyfile(fz_name, fbak_name)
    #
    ou = '\n'
    ou += '!psx0 '+str(self.psx0)+'\n'
    ou += '!psy0 '+str(self.psy0)+'\n'
    ou += '\n'
    ou += '!fidu\n'
    for i in range(self.n_fidu):
      ou += self.fidu_name[i]
      ou += ' ' + str(self.fidu_x[i])
      ou += ' ' + str(self.fidu_y[i])
      ou += '\n'
    ou += '\n'
    ou += '!well_center\n'
    for i in range(self.n_well):
      ou += str(i+1)
      ou += ' ' + str(self.well_center_x[i])
      ou += ' ' + str(self.well_center_y[i])
      ou += '\n'
    ou += '\n'
    ou += '!ins_center\n'
    for i in range(self.n_ins):
      ou += str(i+1)
      ou += ' ' + str(self.ins_center_x[i])
      ou += ' ' + str(self.ins_center_y[i])
      ou += '\n'
    ou += '\n'
    fz = open(fz_name, 'w')
    fz.write(ou)
    fz.close()
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
  def go_ins_center(self, iw):
    if iw < 0 or iw >= self.n_ins:
      print("Error.  iw out of range.")
      print("  iw =     ", iw, " (So ins #"+str(iw+1)+")")
      print("  n_ins = ", self.n_ins)
      return
    gx, gy = self.ins_center_x[iw], self.ins_center_y[iw]
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
  def go_locup_edge(self, iw, capo):  # capo is "cardinal point"
    if iw < 0 or iw >= self.n_ins:
      print("Error.  iw out of range.")
      print("  iw =     ", iw, " (So ins #"+str(iw+1)+")")
      print("  n_ins = ", self.n_ins)
      return
    mlocup[iw].go_edge(capo)
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
      elif uline == 'save plate':  self.save_plate()
      elif uline == 'create lps':
        self.create_locups()
      elif uline.startswith('run lp'):
        ll = uline.strip().split(' ')
        if len(ll)== 2:
          iw = int(ll[1][2:])-1
        elif len(ll)==3:
          iw = int(ll[2])-1
        else:
          print("Strange uline split length.")
          print("  Need 2 or 3 words.")
          print("  Example:  run lp2")
          print("  Example:  run lp 2")
          continue
        if iw < 0 or iw >= len(self.mlocup):
          print("Entered number is out of range.")
          print("  n_well:      ", self.n_well)
          print("  len(mlocup): ", len(self.mlocup))
          continue
        self.mlocup[iw].run_pattern()
      elif uline.startswith('setrun lp '):
        ll = uline.strip().split(' ')
        if len(ll)!=3:
          print("Strange uline split length.")
          print("  Need 3 words.")
          print("  Example:  setrun lp 2")
          continue
        iw = int(ll[2]-1)
        if iw < 0 or iw >= len(self.mlocup):
          print("Entered number is out of range.")
          print("  n_well:      ", self.n_well)
          print("  len(mlocup): ", len(self.mlocup))
          continue
        self.mlocup[iw].run()
      elif uline == 'print pos':
        p()
        print("TO IMPLEMENT:  These are psx psy (prior stage).")
        print("  We would also like muwp internal plate coordinates.")
      elif uline.startswith('go well'):
        ll = uline.strip().split(' ')
        if len(ll)!=4:
          print("Strange uline split length.")
          print("  Need 4 words.")
          print("  Example:  go well 2 center")
          continue
        iw = int( ll[2] ) - 1
        ppos = ll[3]
        if ppos == 'center':  self.go_well_center(iw)
        else:
          print("Unrecognized ppos: ", ppos)
      elif uline.startswith('reset lp') and uline.endswith(' edges') and len(uline) > len('reset lpedges'):
        ll = uline.strip().split(' ')
        iw = int( ll[1][2:] ) - 1
        if iw < 0 or iw >= self.n_ins:
          print("Bad lp number.")
          continue
        rv = self.mlocup[iw].get_edges()
        if rv == 0:
          # all is ok
          print("Resetting muwp ins",iw+1,"center.")
          self.ins_center_x[iw] = self.mlocup[iw].cx
          self.ins_center_y[iw] = self.mlocup[iw].cy
        else:
          print("locup get_edges() didn't return 0.")
          print("  So not resetting muwp ins center.")
      elif uline.startswith('go ins') or uline.startswith('go lp'):
        ll = uline.strip().split(' ')
        if len(ll) == 3:
          if ll[1].startswith('lp'):
            iw = int( ll[1][2:] ) - 1
          elif ll[1].startswith('ins'):
            iw = int( ll[1][3:] ) - 1
          ppos = ll[2]
        elif len(ll)== 4:
          iw = int( ll[2] ) - 1
          ppos = ll[3]
        else:
          print("Strange uline split length.")
          print("  Need 4 words.")
          print("  Examples:")
          print("    go lp 2 center")
          print("    go lp2 center")
          print("    go lp2 N-edge")
          print("    go ins 2 center")
          print("    go ins 2 center")
          print("    go ins 2 N-edge")
          continue
        if ppos == 'center':  self.go_ins_center(iw)
        elif ppos.endswith('-edge'):
          capo = ppos[0]  # N W S E
          self.mlocup[iw].go_edge( capo )
        else:
          print("Unrecognized ppos: ", ppos)
      elif uline.startswith('set fidu'):
        ll = uline.split(' ')
        if len(ll)!=3:
          print("Strange uline split length.")
          print("  Need 3 words.")
          print("  Example:  set fidu x1")
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




