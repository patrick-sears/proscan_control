
import sys
import os
import winsound
import time

from modules.m1_basic_control import *
from modules.m99_sim_serial import spo






#######################################################
class c_arec:
  #
  def __init__(self):
    print("Remember, use q to quit any time.")
    self.name = []  # area name
    self.px = []    # x pos
    self.py = []    # y pos
    self.notes = [] 
    #
    self.n_area = 0
    #
    print("DANGER:  Backup system not implemented yet.")
    print("  If you set areas and then load, you will loose your data.")
  #
  def clear_areas(self):
    self.name = []  # area name
    self.px = []    # x pos
    self.py = []    # y pos
    self.notes = [] 
    #
    self.n_area = 0
  #
  def ls(self):  # list
    for i in range(self.n_area):
      line = str(i)+'. '
      line += "("+str(self.px[i])+','+str(self.py[i])+")"
      line += "  ["+self.name[i]+"]"
      line += "  - " + self.notes[i]
      print(line)
    print("n_area: ", self.n_area)
  #
  def set(self, name=None):
    #
    i = self.n_area
    self.n_area += 1
    #
    self.name.append( "a"+str(i) )
    self.px.append( 0 )
    self.py.append( 0 )
    self.notes.append( "" )
    #
    if name != None: self.name[i] = name
    ###
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.px[i] = int(ll[0])
    self.py[i] = int(ll[1])
  #
  def go(self,name):
    j = -1
    for i in range(self.n_area):
      if name == self.name[i]:
        j = i
    if j == -1:
      print("Couldn't find area.")
      return
    ###
    x = self.px[j]
    y = self.py[j]
    ouline = "g"
    ouline += " {0:d}".format( x )
    ouline += " {0:d}".format( y )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  #
  def load(self):
    print("Loading data...")
    #
    fname_base =  "arec.data"
    fname_default = "config/"+fname_base
    fname_user = "user/"+fname_base
    if os.path.isfile( fname_user ):
      fname = fname_user
      print("Found user file.")
    else:
      fname = fname_default
      print("Using default file.")
    #
    self.clear_areas()
    #
    print("  Loading: ", fname )
    f = open(fname)
    for l in f:
      l = l.strip()
      if len(l) == 0:  continue
      if l[0] == '#':  continue
      ###
      ll = l.split(';')
      self.px.append( int(ll[1].strip()) )
      self.py.append( int(ll[2].strip()) )
      self.name.append( ll[3].strip() )
      if len(ll) > 4:
        self.notes.append( ll[4].strip() )
      else:
        self.notes.append("")
      ###
    f.close()
    self.n_area = len(self.name)
    print("  Done.")
  #
  def save(self):
  #
    if self.n_area == 0:
      print("Nothing to save.")
      return
    fname_base =  "arec.data"
    fname_user = "user/"+fname_base
    fname = fname_user
    print("Saving "+fname+" ...")
    #
    fz = open(fname, 'w')
    for i in range(self.n_area):
      ou = str(i)
      ou += " ; " + str(self.px[i])
      ou += " ; " + str(self.py[i])
      ou += " ; " + self.name[i]
      if len(self.notes[i])>0:
        ou += " ; " + self.notes[i]
      ou += '\n'
      fz.write(ou)
    fz.close()
#######################################################


arec = c_arec()



