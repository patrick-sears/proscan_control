
import sys
import os

from m1_basic_control import *
from m99_sim_serial import spo



#######################################################
class c_locup:
  #
  def __init__(self):
    print("Remember, use q to quit any time.")
    self.x0 = None
    self.y0 = None
    self.cnum = 1    # the culture number
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
      else:
        print("Error.  Unrecognized key in config file.")
        print("  key: ", key)
        sys.exit(1)
    f.close()
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
      ##########################
      # Old system...............
      # if self.get_y0() == -1:  return  # quit on 'q'
      # self.go_N_to_W_edge_rough()
      # if self.get_x0() == -1:  return  # quit on 'q'
      ##########################
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
      uline = input("in<< ")
      if uline == 'q':  return -1
      if uline == 'p':
        p()
      elif uline == 'xy':
        print("n_pattern = ", self.n_pattern)
        print("x0,y0 = ", int(self.x0), int(self.y0))
        for i in range(self.n_pattern):
          x = self.x0 + self.pax[i]
          y = self.y0 + self.pay[i]
          print("  i,x,y: ", i+1, int(x), int(y))
    #####
    return 0
  #
  def run_pattern(self):
    ######################
    for i in range(self.n_pattern):
      #########
      pline = ""
      if self.pam[i] != "":
        pline += "\n"+self.pam[i]+"\n"
      pline += "c"+str(self.cnum)
      pline += " : "+self.paname[i]+'\n'
      print(pline)
      #########
      x = self.x0 + self.pax[i]
      y = self.y0 + self.pay[i]
      ouline = "g"
      ouline += " {0:d}".format( x )
      ouline += " {0:d}".format( y )
      ouline += "\r\n"
      send = bytes( ouline.encode() )
      spo.write( send )
      #########
      uline = input("  Hit [enter] when done (q=quit):  \n")
      if uline == 'q':  return -1
    ######################
    return 0
  #
  def get_y0(self):
    pline = "Go to culture "+str(self.cnum)
    pline += " North edge and hit e[enter]\n"
    #####
    while True:
      print(pline)
      uline = input("in<< ")
      if uline == 'q':  return -1
      if uline == 'e':  break
    #####
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.y0 = int(ll[1]) - self.culture_diam  # 0 x, 1 y
    #####
    return 0
  #
  def get_x0(self):
    pline = "Go to culture "+str(self.cnum)
    pline += " West edge and hit e[enter]\n"
    #####
    while True:
      print(pline)
      uline = input("in<< ")
      if uline == 'q':  return -1
      if uline == 'e':  break
    #####
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.x0 = int(ll[0]) - self.culture_diam  # 0 x, 1 y
    #####
    return 0
  #
  def get_edges(self):
    #
    # 0 E, 1 N, 2 W, 3 S
    edvalx = [0,0,0,0]
    edvaly = [0,0,0,0]
    edi = None
    #
    # Get the first edge ----------------------->
    pline =  "Go to and edge in culture "+str(self.cnum)+'\n'
    pline += "  Then hit N or S or E or W, and [enter]\n"
    pline += "  n s e w also ok.\n"
    pline += "  Or q to quit.\n"
    while True:
      print(pline)
      uline = input("in<< ")
      if uline == 'q':  return -1
      elif uline == 'E' or uline == 'e':
        edi = 0
        break
      elif uline == 'N' or uline == 'n':
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
    pline = "Go to "+ped+" and hit m[enter].\n"
    while True:
      print(pline)
      uline = input("in<< ")
      if uline == 'q':  return -1
      elif uline == 'm':  break
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
      uline = input("in<< ")
      if uline == 'q':  return -1
      elif uline == 'm':  break
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
      uline = input("in<< ")
      if uline == 'q':  return -1
      elif uline == 'm':  break
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
    # Figure out x0 y0 ----------------------->
    ### # Reset culture diam.
    ### self.culture_diam = int(edvalx[2] - edvalx[0])
    ### alt_diam = int(edvaly[1] - edvaly[3])
    ### if alt_diam < self.culture_diam:  self.culture_daim = alt_diam
    ### self.culture_r = int(self.culture_diam / 2)
    #
    # Set the center.
    self.cx = int((edvalx[0] + edvalx[2]) / 2)
    self.cy = int((edvaly[1] + edvaly[3]) / 2)
    #
    # Set x0 and y0
    self.x0 = self.cx - self.culture_r
    self.y0 = self.cy - self.culture_r
    #
    return 0
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
    fname_base =  "locup_pattern.data"
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
    #
    self.pam = []  # pattern message
    self.pax = []  # pattern x
    self.pay = []  # pattern y
    self.paname = []  # a short name for that item in the pattern list
    # several items can have the same name.
    f = open("config/locup_pattern.data")
    for l in f:
      l = l.strip()
      if len(l) == 0:  continue
      if l[0] == '#':  continue
      lla = l.split(':')
      if len(lla) > 1:  self.pam.append( lla[1].strip() )
      else:           self.pam.append( "" )
      llb = lla[0].strip().split(' ')
      self.paname.append( llb[0] )
      self.pax.append( int(llb[1]) )
      self.pay.append( int(llb[2]) )
    f.close()
    self.n_pattern = len(self.paname)
    print("  Done.")
  #
  #
#######################################################






