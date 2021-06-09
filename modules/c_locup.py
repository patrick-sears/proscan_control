
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
        self.culture_r = self.culture_diam / 2
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
      if self.get_y0() == -1:  return  # quit on 'q'
      self.go_N_to_W_edge_rough()
      if self.get_x0() == -1:  return  # quit on 'q'
      #
      print("Culture "+str(self.cnum)+" coordinates are set.")
      print("Running pattern...")
      #
      if self.run_pattern() == -1:  return  # quit on 'q'
      print("Culture "+str(self.cnum)+" done.")
      print()
      #
      self.cnum += 1
    ##############
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
    self.y0 = self.culture_diam - int(ll[1])  # 0 x, 1 y
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
    self.x0 = self.culture_diam - int(ll[0])  # 0 x, 1 y
    #####
    return 0
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






