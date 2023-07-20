

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
    self.n_well = 0
    #
    self.fname_plate = None
    #
    self.clear_fidu()
    self.clear_well_center()
    self.clear_ins_center()
    #
    self.n_remulti = 0
    #
    self.run_mode = 'a'
    #
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
    if not os.path.exists( fname ):
      print("Warning w33.  Missing plate file.")
      print("  In c_muwp::load_plate().")
      print("  File not loaded.")
      print("  fname: ", fname)
      return
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
      elif key == '!reset_multi_edges':
        self.remulti_i = []   # index of ins
        self.remulti_fe = []  # fe:  first edge
        # The "first edge" is the one to start with.
        #
        for l in f:
          l = l.strip()
          ll = l.split(' ')
          if len(l) == 0:  break
          if l[0] == '#':  continue
          idx = int(ll[0])-1
          data_ok = True
          if idx < 0 or idx >= self.n_ins:
            print("Error reading plate data.")
            print("  idx out of range: ", idx)
            print("  fname: ", fname) 
            print("  !reset_multi_edges is incomplete.")
            data_ok = False
          a = ll[1]
          if a!='N' and a!='S' and a!='W' and a!='E':
            print("Error reading plate data.")
            print("  Bad fov: ", a)
            print("  fname: ", fname) 
            print("  !reset_multi_edges is incomplete.")
            data_ok = False
          #
          self.remulti_i.append( idx )
          self.remulti_fe.append( a )
          #
        #
        self.n_remulti = len(self.remulti_i)
        #
      else:
        print("Error.  Unrecognized key in config file.")
        print("  key: ", key)
        sys.exit(1)
    f.close()
    print("  Done.")
  #
  def save_plate(self):
    #
    stime = datetime.now().strftime("%Y%m%d_%H%M%S")
    fz_name = 'user/muwp_plate_'+stime+'.data'
    #
    ou = '\n'
    ou += '\n'
    ou += '# Created from:  '+self.fname_plate+'\n'
    ou += '\n'
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
    if not os.path.exists( fname ):
      print("Warning w32.  Missing config file.")
      print("  In c_muwp::load_config().")
      print("  File not loaded.")
      print("  fname: ", fname)
      return
    f = open(fname)
    for l in f:
      if not l.startswith('!'):  continue
      l = l.strip()
      ll = l.split(' ')
      mm = [m.strip() for m in l.split(';')]
      key = mm[0]
      ###
      if key == '!fname_plate': self.fname_plate = mm[1]
      elif key == '!psx0':      self.psx0 = int(mm[1])
      elif key == '!psy0':      self.psy0 = int(mm[1])
      elif key == '!run_mode':  self.run_mode = mm[1]
      else:
        print("Error.  Unrecognized key in config file.")
        print("  key: ", key)
        sys.exit(1)
    f.close()
    #
    if self.run_mode != 'a' and self.run_mode != 'b':
      print("Error during muwp load config.")
      print("  Unrecognized run mode.")
      print("  run_mode: ", run_mode)
      sys.exit(1)
    print("  Done.")
  #
  def beep(self, n_beep):
    for i in range(n_beep):
      if i != 0:  time.sleep(0.1)
      winsound.Beep(1600,200)  # (freq in Hz, duration in ms)
      # os.system('\a')
      # sys.stdout.write('\a')
      # sys.stdout.flush()
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
  def send(self, s):
    cbuf() # Make sure the buffer is clear.
    ss = s.strip()
    ouline = ss+'\r\n'
    send = bytes(ouline.encode())
    spo.write( send )
    while True:
      serda = spo.readline()
      slen = len(serda)
      if slen == 0:  break
      dade = serda.decode("Ascii")
      print("  serda:  ["+dade+"]")
  #
  def user_send(self, uline):
    # Expect:  send "something in here"
    # Or:      send 'something in here'
    ll = uline.split("'")
    if len(ll) != 3:
      ll = uline.split('"')
    if len(ll) != 3:
      print("Didn't find a message.")
      return
    self.send( ll[1] )
  #
  def run(self, amode=0):   # run the hui (human user interface)
    self.beep(2)
    print()
    print("Entering muwp hui.")
    print("  Use q to quit.")
    if amode == 1:
      self.load_config()
      self.load_plate()
    ############################ Start of hui while(1)...
    while( 1 ):
      print()
      uline = input("muwp>> ")
      uline = uline.strip()
      uline = ' '.join( uline.split() )  # remove duplicate spaces
      ull = uline.split(' ')
      n_ull = len(ull)
      if n_ull == 0:  continue  # Handle just hitting enter.
      action = ull[0]
      if action == '0':
        print("No action.")
      elif action == 'create':
        if n_ull != 2:
          print("uError.  Bad uline.")
          ac2 = ull[1]
          if ac2 == 'lps':  self.create_locups()
          else:
            print("uError.")
      elif action == 'go':
        if n_ull < 2:
          print("uError")
          continue
        ac2 = ull[1]
        if ac2.startswith('c'):
          if n_ull != 3:
            print("uError")
            print("  Need 3 words.")
            print("  Examples:")
            print("    go c2 center")
            print("    go c2 N-edge")
            print("    go c3 fov1")
            continue
          if len(ac2) < 2:
            print("uError.")
            continue
          iws = ac2[1:]
          if not iws.isdigit():
            print("uError.")
            print("  c not followed by a digit.")
            continue
          iw = int( iws ) - 1   # iw is the lp index
          ac3 = ull[2]
          # DANGER:  The following might cause a crash if
          # the user input is bad.  I need to investigate
          # this.
          if ac3 == 'center':  self.go_ins_center(iw)
          elif ac3.endswith('-edge'):
            capo = ac3[0]  # N W S E
            self.mlocup[iw].go_edge( capo )
          elif ac3.startswith('fov'):
            i1o_fov = int( ac3[3:] )  # the fov number
            self.mlocup[iw].go_fov(i1o_fov)
          else:
            print("Unrecognized ac3: ", ac3)
        elif ac2 == 'fidu':
          if n_ull != 3:
            print("uError.")
            continue
          fiduname = ull[2]
          ifidu = None
          for i in range(self.n_fidu):
            if fiduname == self.fidu_name[i]:
              ifidu = i
          if ifidu == None:
            print("Error.  Couldn't find fiduname.")
            print("  fiduname: ", fiduname)
          else:
            self.go_fidu(ifidu)
        if ac2.startswith('w'):
          if n_ull != 3:
            print("uError")
            print("  Need 3 words.")
            print("  Examples:")
            print("    go w2 center")
            print("    go w2 N-edge")
            continue
          if len(ac2) < 2:
            print("uError.")
            continue
          iws = ac2[1:]
          if not iws.isdigit():
            print("uError.")
            print("  w not followed by a digit.")
            continue
          iw = int( iws ) - 1   # iw is the lp index
          ac3 = ull[2]
          if ac3 == 'center':  self.go_well_center(iw)
          else:
            print("Unrecognized ac3: ", ac3)
        else:
          print("uError.  Unrecognized ac2.")
        #
      elif action == 'load':
        if n_ull != 2:
          print("uError.  Bad uline.")
          continue
        if ll[1] == 'all':
          self.load_config()
          self.load_plate()
        elif ll[1] == 'config':  self.load_config()
        elif ll[1] == 'plate':   self.load_plate()
        else:
          print("uError.  Bad uline.")
      elif action == 'print':
        if n_ull != 3:
          print("uError.")
          continue
        ac2 = ull[1]
        if ac2 == 'pos':
          p()
          print("TO IMPLEMENT:  These are psx psy (prior stage).")
          print("  We would also like muwp internal plate coordinates.")
        elif ac2 == 'info':
          self.print_info()
        else:
          print("uError.")
      elif action == 'q':
        if n_ull != 1:
          print("uError.")
          continue
        print()
        return
      elif action == 'save':
        if n_ull != 2:
          print("uError.")
          continue
        ac2 = ull[1]
        if ac2 == 'plate':  self.save_plate()
        else:
          print("uError.")
      elif action == 'reset':
        if n_ull != 3:
          print("uError.")
          continue
        ac2 = ull[1]
        ac3 = ull[2]
        if ac3 != 'edges':
          print("uError.")
          continue
        if ac2.startswith('c'):
          if len(ac2) < 2:
            print("uError.")
            continue
          iws = ac2[1:]
          if not iws.isdigit():
            print("uError.")
            print("  c not followed by a digit.")
            continue
          iw = int(iws) - 1
          if iw < 0 or iw >= self.n_ins:
            print("uError.  c number out of range.")
            continue
          rv = self.mlocup[iw].get_edges()
          if rv == 0:
            print("Resetting muwp ins",iw+1,"center.")
            self.ins_center_x[iw] = self.mlocup[iw].cx
            self.ins_center_y[iw] = self.mlocup[iw].cy
          else:
            print("locup get_edges() didn't return 0.")
            print("  So not resetting muwp ins center.")
        elif ac2 == 'multi':
          self.reset_multi_edges()
        else:
          print("uError.")
          print("  ac2 not recognized.")
        #
      elif ac2 == 'rme':
          self.reset_multi_edges()
      elif action == 'run':
        if n_ull != 2:
          print("Strange uline split length.")
          print("  Need 2 words.")
          print("  Example:  run c2")
          continue
        ac2 = ull[1]  # Expect:  c1 c2 ... c11 c12 ...
        if len(ac2) < 2:
          print("uError.  Bad culture format.")
          continue
        if ac2[0] != 'c':
          print("uError.")
          print("  Missing c.")
          continue
        iws = ac2[1:]
        if not iws.isdigit():
          print("uError.")
          print("  c not followed by a digit.")
          continue
        iw = int(iws)-1
        if iw < 0 or iw >= len(self.mlocup):
          print("Entered number is out of range.")
          print("  n_well:      ", self.n_well)
          print("  len(mlocup): ", len(self.mlocup))
          continue
        ###
        if   self.run_mode == 'a':   self.mlocup[iw].run_pattern()
        elif self.run_mode == 'b':
          self.mlocup[iw].go_edge( 'N' )
          rv = self.mlocup[iw].get_edges()
          if rv == 0:
            # all is ok
            print("Resetting muwp ins",iw+1,"center.")
            self.ins_center_x[iw] = self.mlocup[iw].cx
            self.ins_center_y[iw] = self.mlocup[iw].cy
          else:
            print("locup get_edges() didn't return 0.")
            print("  So not resetting muwp ins center.")
            print("  Running patter...")
          self.mlocup[iw].run_pattern()
        #
      elif action == 'send':
        self.user_send(uline)
      elif action == 'set':
        if n_ull < 2:
          print("uError.  Bad uline.")
          continue
        ac2 = ll[1]
        if ac2 == 'fidu':
          ll = uline.split(' ')
          if n_ull != 3:
            print("Strange uline split length.")
            print("  Need 3 words.")
            print("  Example:  set fidu x1")
            continue
          fiduname = ll[2]
          self.set_fidu(fiduname)
        elif ac2 == 'run_mode':
          if n_ull != 3:
            print("Strange uline split length.")
            print("  Need 3 words.")
            print("  Example:  set run_mode a")
            continue
          ac3 = ll[2]
          ok = False
          if   ac3 == 'a':  ok = True
          elif ac3 == 'b':  ok = True
          if ok:
            self.run_mode = ac3
          else:
            print("uError.  Bad set run_mode.")
        else:
          print("uError.  Unrecognized ac2.")
      else:
        print("uError.  Unrecognized action.")
  #
  def hui_reset_multi_edges(self):
    if self.n_remulti == 0:
      print("The multi edges have not been configured.")
    #
    for i in range(self.n_remulti):
      rv = self.reset_edges_2(self.remulti_i[i], self.remulti_fe[i])
      if rv != 0:  break
    #
    if rv == 0:
      print("All edges reset.")
    else:
      print("Some edges not reset.")
    self.beep(2)
  #
  def print_info(self):
    if self.fname_plate == None:
      print("fname_plate:  None.")
    else:
      print("fname_plate: ", self.fname_plate)
      if os.path.isfile( "config/"+self.fname_plate):
        print("  File exists in config/")
      else:
        print("  File does not exist in config/")
      if os.path.isfile( "user/"+self.fname_plate):
        print("  File exists in user/")
      else:
        print("  File does not exist in user/")
    print("psx0:  ", self.psx0)
    print("psy0:  ", self.psy0)
    print("well centers:")
    for i in range(self.n_well):
      print("  ", i+1, self.well_center_x[i], self.well_center_y[i])
  #
  def reset_edges_2(self, iw, start_edge):
    rv = self.mlocup[iw].get_edges_2(start_edge)
    if rv == 0:
      self.ins_center_x[iw] = self.mlocup[iw].cx
      self.ins_center_y[iw] = self.mlocup[iw].cy
    return rv
  #
#######################################################


muwp = c_muwp()




