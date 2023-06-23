
import sys
import os
import winsound
import time

from modules.m1_basic_control import *
from modules.m99_sim_serial import spo



#######################################################
class c_locup:
  #
  def __init__(self):
    print("Remember, use q to quit any time.")
    # center of insert:  cx cy
    self.cx = None
    self.cy = None
    self.cnum = 1    # the culture number
    self.pattern_file = "locup_pattern.data"
  #
  def load_config(self):
    print("Loading config...")
    #
    fname_base =  "locup.config"
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
      print("Warning w33.  Missing config file.")
      print("  In c_locup::load_config().")
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
      if key == '!culture_diam':
        self.culture_diam = int(ll[1])
        self.culture_r = int(self.culture_diam / 2)
      elif key == '!pattern_file':
        self.pattern_file = ll[1]
      else:
        print("Error.  Unrecognized key in config file.")
        print("  key: ", key)
        sys.exit(1)
    f.close()
    print("  culture diam: ", self.culture_diam)
    print("  Done.")
  #
  def run(self):
    self.load_config()
    self.load_pattern_data()
    ##############
    while( 1 ):
      #
      if self.get_edges() == -1:  return  # quit on 'q'
      #
      ######################################
      # This section is here to make sure the human doesn't
      # keep moving to edges and hitting enter when they
      # should be taking videos using the pattern.
      pline = "Ready to start pattern run (y for yes / q to quit):"
      while True:
        print(pline)
        uline = input("u>> ")
        if uline == 'q':  return
        if uline == 'y':  break
      ######################################
      #
      debug_run = 0
      if debug_run == 1:
        if self.debug_run() == -1:  return # quit of 'q'
      else:
        print("Culture "+str(self.cnum)+" coordinates are set.")
        print("Running pattern...")
        if self.run_pattern() == -1:  return  # quit on 'q'
        print("Culture "+str(self.cnum)+" done.")
        print()
      #
      self.cnum += 1
    ##############
  #
  def debug_run(self):
    pline = '\n'
    pline += "Debug run...\n"
    #####
    while True:
      print(pline)
      uline = input("u>> ")
      if uline == 'q':  return -1
      if uline == 'p':
        p()
      elif uline == 'xy':
        print("n_pattern = ", self.n_pattern)
        print("xc,yc = ", int(self.xc), int(self.yc))
        for i in range(self.n_pattern):
          x = self.cx + self.pax[i]
          y = self.cy + self.pay[i]
          print("  i,x,y: ", i+1, int(x), int(y))
    #####
    return 0
  #
  def go_fov(self, i1o_fov):
    i = i1o_fov-1
    if i < 0 or i >= self.n_pattern:
      print("Error.  locup asked for OOR FOV.")
      print("  i1o_fov: ", i1o_fov)
      print("  n_pattern:  ", self.n_pattern)
      return
    #########
    x = self.cx + self.pax[i]
    y = self.cy + self.pay[i]
    ouline = "g"
    ouline += " {0:d}".format( x )
    ouline += " {0:d}".format( y )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
    #########
  #
  def run_pattern(self):
    ######################
    print()
    for i in range(self.n_pattern):
      #########
      pline = ""
      if self.pam[i] != "":
        pline += self.pam[i]
      pline += " : c"+str(self.cnum)
      pline += " : "+self.paname[i]  # +'\n'
      print(pline)
      #########
      x = self.cx + self.pax[i]
      y = self.cy + self.pay[i]
      ouline = "g"
      ouline += " {0:d}".format( x )
      ouline += " {0:d}".format( y )
      ouline += "\r\n"
      send = bytes( ouline.encode() )
      spo.write( send )
      #########
      # uline = input("  Hit [enter] when done (q=quit):  \n")
      uline = input("  Hit [enter] when done (q=quit):  ")
      if uline == 'q':  return -1
    ######################
    self.beep(1)
    return 0
  #
  def go_edge(self, capo):  # capo:  "cardinal point"
    #  self.culture_r = int(self.culture_diam / 2)
    if capo == 'N' or capo == 'n':
      x = self.cx
      y = self.cy + self.culture_r
    elif capo == 'S' or capo == 's':
      x = self.cx
      y = self.cy - self.culture_r
    elif capo == 'W' or capo == 'w':
      x = self.cx + self.culture_r
      y = self.cy
    elif capo == 'E' or capo == 'e':
      x = self.cx - self.culture_r
      y = self.cy
    else:
      print("Error.  Unrecognized cardinal point.")
      print("  capo: ", capo)
      print("  Expected on of:  N W S E n w s e.")
      return
    ouline = "g"
    ouline += " {0:d}".format( x )
    ouline += " {0:d}".format( y )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  #
  def beep(self, n_beep):
    for i in range(n_beep):
      if i != 0:  time.sleep(0.1)
      winsound.Beep(1600,200)  # (freq in Hz, duration in ms)
      # os.system('\a')
      # sys.stdout.write('\a')
      # sys.stdout.flush()
  #
  def get_edges(self):
    #####
    #
    # 0 E, 1 N, 2 W, 3 S
    edvalx = [0,0,0,0]
    edvaly = [0,0,0,0]
    edi = None
    #
    # Get the first edge ----------------------->
    pline =  "Go to the N edge of culture "+str(self.cnum)+'\n'
    pline += "  Then hit [enter].\n"
    pline += "  Or q[enter] to quit.\n"
    while True:
      print(pline)
      uline = input("u>> ")
      if uline == 'q':  return -1
      elif uline == 'E' or uline == 'e':
        edi = 0
        break
      elif uline == 'N' or uline == 'n' or uline == '':
        edi = 1
        break
      elif uline == 'W' or uline == 'w':
        edi = 2
        break
      elif uline == 'S' or uline == 's':
        edi = 3
        break
      else:
        print("Unrecognized input.")
    ######################################
    # Get the edge values.
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    edvalx[edi] = int(ll[0])  # 0 x, 1 y
    edvaly[edi] = int(ll[1])  # 0 x, 1 y
    ######################################
    #
    # Get the second edge ----------------------->
    self.go_ccw_edge_rough(edi)
    #
    edi = edi+1 if edi<3 else 0
    if   edi == 0:  ped = 'E'
    elif edi == 1:  ped = 'N'
    elif edi == 2:  ped = 'W'
    elif edi == 3:  ped = 'S'
    pline = "Go to "+ped+" and hit [enter], q to quit.\n"
    while True:
      print(pline)
      uline = input("u>> ")
      if uline == 'q':  return -1
      break
    ######################################
    # Get the edge values.
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    edvalx[edi] = int(ll[0])  # 0 x, 1 y
    edvaly[edi] = int(ll[1])  # 0 x, 1 y
    ######################################
    #
    # Get the third edge ----------------------->
    self.go_ccw_edge_rough(edi)
    #
    edi = edi+1 if edi<3 else 0
    if   edi == 0:  ped = 'E'
    elif edi == 1:  ped = 'N'
    elif edi == 2:  ped = 'W'
    elif edi == 3:  ped = 'S'
    pline = "Go to "+ped+" and hit m[enter].\n"
    while True:
      print(pline)
      uline = input("u>> ")
      if uline == 'q':  return -1
      break
    ######################################
    # Get the edge values.
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    edvalx[edi] = int(ll[0])  # 0 x, 1 y
    edvaly[edi] = int(ll[1])  # 0 x, 1 y
    ######################################
    #
    # Get the fourth edge ----------------------->
    self.go_ccw_edge_rough(edi)
    #
    edi = edi+1 if edi<3 else 0
    if   edi == 0:  ped = 'E'
    elif edi == 1:  ped = 'N'
    elif edi == 2:  ped = 'W'
    elif edi == 3:  ped = 'S'
    pline = "Go to "+ped+" and hit m[enter].\n"
    while True:
      print(pline)
      uline = input("u>> ")
      if uline == 'q':
        # No beep needed.  If the user hit 'q', he's looking
        # at the interface.
        return -1
      break
    ######################################
    # Get the edge values.
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    edvalx[edi] = int(ll[0])  # 0 x, 1 y
    edvaly[edi] = int(ll[1])  # 0 x, 1 y
    ######################################
    #
    # Set the center.
    self.cx = int((edvalx[0] + edvalx[2]) / 2)
    self.cy = int((edvaly[1] + edvaly[3]) / 2)
    #
    self.beep(1)
    #
    return 0
    #
  #
  def get_edges_2(self, start_fov):
    # start fov:  N S E W
    #####
    #
    # 0 E, 1 N, 2 W, 3 S
    edvalx = [0,0,0,0]
    edvaly = [0,0,0,0]
    edi = None
    #
    # Get the first edge ----------------------->
    pline =  "Getting edges in culture "+str(self.cnum)+'\n'
    print(pline)
    if start_fov == 'E':
      edi = 0
    elif start_fov == 'N':
      edi = 1
    elif start_fov == 'W':
      edi = 2
    elif start_fov == 'S':
      edi = 3
    else:
      print("Unrecognized get_edges_2() start_fov..")
      print("  start_fov: ", start_fov)
      return -2
    ######################################
    #
    # Get the first edge ----------------------->
    self.go_edge(start_fov)
    #
    # Do not incremente edit here because it's already set.
    if   edi == 0:  ped = 'E'
    elif edi == 1:  ped = 'N'
    elif edi == 2:  ped = 'W'
    elif edi == 3:  ped = 'S'
    pline = "Go to "+ped+" and hit [enter], q to quit.\n"
    while True:
      print(pline)
      uline = input("u>> ")
      if uline == 'q':  return -1
      break
    ######################################
    # Get the edge values.
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    edvalx[edi] = int(ll[0])  # 0 x, 1 y
    edvaly[edi] = int(ll[1])  # 0 x, 1 y
    ######################################
    #
    # Get the second edge ----------------------->
    self.go_ccw_edge_rough(edi)
    #
    edi = edi+1 if edi<3 else 0
    if   edi == 0:  ped = 'E'
    elif edi == 1:  ped = 'N'
    elif edi == 2:  ped = 'W'
    elif edi == 3:  ped = 'S'
    pline = "Go to "+ped+" and hit [enter], q to quit.\n"
    while True:
      print(pline)
      uline = input("u>> ")
      if uline == 'q':  return -1
      break
    ######################################
    # Get the edge values.
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    edvalx[edi] = int(ll[0])  # 0 x, 1 y
    edvaly[edi] = int(ll[1])  # 0 x, 1 y
    ######################################
    #
    # Get the third edge ----------------------->
    self.go_ccw_edge_rough(edi)
    #
    edi = edi+1 if edi<3 else 0
    if   edi == 0:  ped = 'E'
    elif edi == 1:  ped = 'N'
    elif edi == 2:  ped = 'W'
    elif edi == 3:  ped = 'S'
    pline = "Go to "+ped+" and hit [enter].\n"
    while True:
      print(pline)
      uline = input("u>> ")
      if uline == 'q':  return -1
      break
    ######################################
    # Get the edge values.
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    edvalx[edi] = int(ll[0])  # 0 x, 1 y
    edvaly[edi] = int(ll[1])  # 0 x, 1 y
    ######################################
    #
    # Get the fourth edge ----------------------->
    self.go_ccw_edge_rough(edi)
    #
    edi = edi+1 if edi<3 else 0
    if   edi == 0:  ped = 'E'
    elif edi == 1:  ped = 'N'
    elif edi == 2:  ped = 'W'
    elif edi == 3:  ped = 'S'
    pline = "Go to "+ped+" and hit [enter].\n"
    while True:
      print(pline)
      uline = input("u>> ")
      if uline == 'q':
        # No beep needed.  If the user hit 'q', he's looking
        # at the interface.
        return -1
      break
    ######################################
    # Get the edge values.
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    edvalx[edi] = int(ll[0])  # 0 x, 1 y
    edvaly[edi] = int(ll[1])  # 0 x, 1 y
    ######################################
    #
    # Set the center.
    self.cx = int((edvalx[0] + edvalx[2]) / 2)
    self.cy = int((edvaly[1] + edvaly[3]) / 2)
    #
    # Print with this culture.
    self.beep(1)
    #
    return 0
    #
  #
  #
  def go_ccw_edge_rough(self, in_edi):
    if   in_edi == 0:  self.go_E_to_N_edge_rough()
    elif in_edi == 1:  self.go_N_to_W_edge_rough()
    elif in_edi == 2:  self.go_W_to_S_edge_rough()
    elif in_edi == 3:  self.go_S_to_E_edge_rough()
  #
  def go_E_to_N_edge_rough(self):
    dx =   int(self.culture_r)
    dy =   int(self.culture_r)
    ##
    ouline = "gr"  # the "r" is to go relative to current position
    ouline += " {0:d}".format( dx )
    ouline += " {0:d}".format( dy )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  #
  def go_N_to_W_edge_rough(self):
    dx =   int(self.culture_r)
    dy = - int(self.culture_r)
    ##
    ouline = "gr"  # the "r" is to go relative to current position
    ouline += " {0:d}".format( dx )
    ouline += " {0:d}".format( dy )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  #
  def go_W_to_S_edge_rough(self):
    dx = - int(self.culture_r)
    dy = - int(self.culture_r)
    ##
    ouline = "gr"  # the "r" is to go relative to current position
    ouline += " {0:d}".format( dx )
    ouline += " {0:d}".format( dy )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  #
  def go_S_to_E_edge_rough(self):
    dx = - int(self.culture_r)
    dy =   int(self.culture_r)
    ##
    ouline = "gr"  # the "r" is to go relative to current position
    ouline += " {0:d}".format( dx )
    ouline += " {0:d}".format( dy )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  #
  def load_pattern_data(self):
    print("Loading pattern data...")
    #
    fname_base = self.pattern_file
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
      print("Warning w34.  Missing pattern file.")
      print("  In c_locup::load_pattern_data().")
      print("  File not loaded.")
      print("  fname: ", fname)
      return
    #
    self.pam = []  # pattern message
    self.pax = []  # pattern x
    self.pay = []  # pattern y
    self.paname = []  # a short name for that item in the pattern list
    # several items can have the same name.
    next_pam = ""
    f = open(fname)
    for l in f:
      l = l.strip()
      if len(l) == 0:  continue
      if l[0] == '#':  continue
      ll = l.split(' ')
      lla = l.split(':')
      key = ll[0]
      ###
      if key == '!culture_diam':
        # This allows the pattern file to override the culture diameter
        # from the config file.
        self.culture_diam = int(ll[1])
        self.culture_r = int(self.culture_diam / 2)
        continue
      elif key == '!m':
        next_pam = lla[1].strip()
        continue
      if len(lla) > 1:
        # This overrides next_pam.
        self.pam.append( lla[1].strip() )
        next_pam = ""
      else:
        self.pam.append( next_pam )
        next_pam = ""
      llb = lla[0].strip().split(' ')
      self.paname.append( llb[0] )
      self.pax.append( int(llb[1]) )
      self.pay.append( int(llb[2]) )
    f.close()
    self.n_pattern = len(self.paname)
    print("  Done.")
    #
  #
  #
#######################################################


locup = c_locup()



