
import sys

from m1_basic_control import *
from m99+sim_serial import spo



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
    f = open("config/locup.config")
    for l in f:
      if not l.startswith('!'):  continue
      l = l.strip()
      ll = l.split(' ')
      key = ll[0]
      ###
      if key == '!culture_diam':
        self.culture_diam = int(ll[1])
        self.culture_r = culture_diam / 2
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
    #
    if self.get_y0():  return  # quit on 'q'
    self.go_N_to_W_edge_rough()
    if self.get_x0():  return  # quit on 'q'
    #
    print("Culture coordinates are set.")
    print("Running patterns...")
    #
    while 1:
      if run_pattern():  return  # quit on 'q'
    #
  #
  def run_pattern(self):
    pline = "In run_pattern()."
    pline += "  Nothing implemented here yet."
    pline += "  Hit q to quit."
    print(pline)
    uline = input("in<< ")
    if uline == 'q':  return 1
    return 0
  #
  def get_y0(self):
    pline = "Go to culture "+str(self.cnum)
    pline += " North edge and hit e[enter]\n"
    #####
    while True:
      print(pline)
      uline = input("in<< ")
      if uline == 'q':  return 1
      if uline == 'e':  break
    #####
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.y0 = culture_diam - int(ll[1])  # 0 x, 1 y
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
      if uline == 'q':  return 1
      if uline == 'e':  break
    #####
    cbuf()
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.x0 = culture_diam - int(ll[0])  # 0 x, 1 y
    #####
    return 0
  #
  def go_N_to_W_edge_rough():
    dx =   int(self.culture_r)
    dy = - int(self.culture_r)
    ##
    ouline = "g"
    ouline += " {0:d}".format( dx )
    ouline += " {0:d}".format( dy )
    # print(self.fovname[i]+":   ["+ouline+"]")
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  #
  def load_pattern_data(self):
    print("Loading pattern data...")
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
      if len(lla>1):  self.pam.append( lla[1].strip() )
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






