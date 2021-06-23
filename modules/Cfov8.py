
import math
import os
from modules.m import *

from modules.m99_sim_serial import spo



##################################################################
##################################################################
class Cfov8:
  def __init__(self,cid):  # cid = culture id
    self.cid = str(cid)
    self.fname_zero_c = 'config/fov8_'+self.cid+'.data'
    self.fname_zero_u = 'user/fov8_'+self.cid+'.data'
    self.n_pos = 8
    self.fovname = 'N;NW;W;SW;S;SE;E;NE'.split(';')
    # self.init_fovs()  # Can only be done after x0 and y0 are set.
    #
    # x0 and y0 are the center of each cultures.
    # Inserts are 23000 um wide.  So edges are at
    # So edges (not fovs) are here:
    # W and E edges:  x0 +/- 11500
    # N and S edges:  y0 +/- 11500
    self.x0 = None
    self.y0 = None
    self.zeroed = False
    #
    # fovs are at self.x1 self.y1.
    # edges are at self.x2 self.y2
    #
    # side = r / sqrt(2) = 11500 / sqrt(2) = 8132.
  ###
  def show_zero(self):
    ux0 = "not_set" if self.x0==None else str(self.x0)
    uy0 = "not_set" if self.y0==None else str(self.y0)
    # ux0 = "not_set"
    # uy0 = "not_set"
    # if self.x0 != None:  ux0 = self.x0
    # if self.y0 != None:  uy0 = self.y0
    # print("x0, y0:  "+str(ux0)+", "+str(uy0) )
    print("x0, y0:  "+ux0+", "+uy0 )
  ###
  def adjust_zero(self, dx, dy):
    self.x0 += dx
    self.y0 += dy
    self.init_fovs()
  ###
  def rel_top2lef(self):
    # Used after doing selef() to go roughly from the top of the
    # culutre to the left side.
    send = bytes( "gr 11500 -11500\r\n".encode() )
    spo.write( send )
  ###
  def rel_lef2top(self):
    # Used after doing selef() to go roughly from the top of the
    # culutre to the left side.
    send = bytes( "gr -11500 11500\r\n".encode() )
    spo.write( send )
  ###
  def selef(self):
    # Set center x0 using the left edge.
    # Then set fovs if possilbe.
    # Set the left edge of the track.  Ie, set x0.
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.x0 = int(ll[0]) - 11500
    self.init_fovs()
  ###
  def serit(self):
    # Set center x0 using the right edge.
    # Then set fovs if possilbe.
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.x0 = int(ll[0]) + 11500
    self.init_fovs()
  ###
  def setop(self):
    # Set center y0 using the top edge.
    # Then set fovs if possilbe.
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.y0 = int(ll[1]) - 11500
    self.init_fovs()
  ###
  def sebot(self):
    # Set center y0 using the bottom edge.
    # Then set fovs if possilbe.
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.y0 = int(ll[1]) + 11500
    self.init_fovs()
  ###
  def init_fovs(self):  # and edges
    if self.x0 != None and self.y0 != None:
      print("Initiating FOVs...")
    else:
      return;
    #
    diam1 = 12.0 * 1000
    diam2 = 23.0 * 1000
    rad1 = diam1/2
    rad2 = diam2/2
    radc = (rad1+rad2) / 2.0  # rad c:  center
    radedge = 11500
    self.x1 = []  # fov
    self.y1 = []  # fov
    self.x2 = []  # edge
    self.y2 = []  # edge
    for i in range(self.n_pos):
      # print("FOV ", fovname[i])
      theta = (i+2) * math.pi * 2 / self.n_pos
      # Using (i_2) because we want to start at the top (N).
      self.x1.append( self.x0 - radc * math.cos(theta) )
      self.y1.append( self.y0 + radc * math.sin(theta) )  # neg because prior
      #
      self.x2.append( self.x0 - radedge * math.cos(theta) )
      self.y2.append( self.y0 + radedge * math.sin(theta) )
    self.zeroed = True
    print("  Done.")
  ###
  def gofov(self, ifov):
    if not self.zeroed:
      print("Error:  Culture not zeroed.")
      return
    if not str(ifov).isnumeric():
      print("Error:  Needs an integer.")
      return
    if ifov < 0 or ifov > 7:
      print("Error:  Needs to be in range [0,7]")
      return
    i = ifov
    cx = int( self.x1[i] )
    cy = int( self.y1[i] )
    ouline = "g"
    ouline += " {0:d}".format( cx )
    ouline += " {0:d}".format( cy )
    print(self.fovname[i]+":   ["+ouline+"]")
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  ###
  def goed(self, ifov):  # Go to the edge, but use fov numbers
    # 0 N, 1 NW, 2 W...
    if not self.zeroed:
      print("Error:  Culture not zeroed.")
      return
    if not str(ifov).isnumeric():
      print("Error:  Needs an integer.")
      return
    if ifov < 0 or ifov > 7:
      print("Error:  Needs to be in range [0,7]")
      return
    i = ifov
    cx = int( self.x2[i] )
    cy = int( self.y2[i] )
    ouline = "g"
    ouline += " {0:d}".format( cx )
    ouline += " {0:d}".format( cy )
    print(self.fovname[i]+":   ["+ouline+"]")
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  ###
  def goN(self):
    self.gofov(0)
  ###
  def goW(self):
    self.gofov(2)
  ###
  def goS(self):
    self.gofov(4)
  ###
  def goE(self):
    self.gofov(6)
  ###
  def goedN(self):
    self.goed(0)
  ###
  def goedW(self):
    self.goed(2)
  ###
  def goedS(self):
    self.goed(4)
  ###
  def goedE(self):
    self.goed(6)
  ###
  def run(self):
    if not self.zeroed:
      print("Error:  Culture not zeroed.")
      return
    self.goN()
    print("Ready.  At N FOV.")
    print("  x to exit.")
    # print("uline: ["+uline+"]")
    for i in range(1, self.n_pos):
      uline = input("u>> ")
      if uline == 'x':
        print("Early exit.")
        break
      ####
      cx = int( self.x1[i] )
      cy = int( self.y1[i] )
      ouline = "g"
      ouline += " {0:d}".format( cx )
      ouline += " {0:d}".format( cy )
      print(self.fovname[i]+":   ["+ouline+"]")
      ouline += "\r\n"
      send = bytes( ouline.encode() )
      spo.write( send )
    print("Done.  At NE FOV.")
  ###
  def load_zero(self):
    #########
    fname_zero = self.fname_zero_u
    if not os.path.isfile( fname_zero ):
      fname_zero = self.fname_zero_c
    if not os.path.isfile( fname_zero ):
      print("The culture "+self.cid+" has no saved zero file.")
      return
    #########
    print("Loading culture "+self.cid+" zero file.")
    f = open( fname_zero )
    ll = f.readline().strip().split(' ')
    self.x0 = int(ll[1])
    ll = f.readline().strip().split(' ')
    self.y0 = int(ll[1])
    f.close()
    #
    self.init_fovs()  # this also inits the edges.
  ###
  def save_zero(self):
    if not self.zeroed:
      print("The culture "+self.cid+" is not zeroed.")
      return
    print("Saving culture "+self.cid+" zero file.")
    # Only allow saving to the user dir, not the config dir.
    fz = open(self.fname_zero_u, 'w')
    line = ""
    line += "x0: " + str(self.x0) + '\n'
    line += "y0: " + str(self.y0) + '\n'
    fz.write(line)
    fz.close()
  ###
##################################################################


