
import sys
import os
import winsound
import time
from datetime import datetime

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
    self.name_prefix = 'a'
    #
    self.n_area = 0
    #
    print("DANGER:  Backup system not implemented yet.")
    print("  If you set areas and then load, you will loose your data.")
  #
  def prefix(self,p=None):
    if p != None:
      self.name_prefix = p
    print("Using new prefix'"+self.name_prefix+"'")
    print("  Next area name will be: ",self.next_name())
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
  def next_name(self):
    auto_n = len(self.name_prefix)+3
    next_i = 0   # The first possible will actually be 1
    n0 = len(self.name_prefix)
    for i in range(self.n_area):
      if len(self.name[i]) != auto_n:  continue
      if not self.name[i].startswith( self.name_prefix ):  continue
      # print("::> ", self.name[i])
      oor = 0  #  index out of range
      for j in range(3):  # 3 digits
        acode = ord(self.name[i][n0+j])
        if acode < 48:  oor = 1    # ascii 0
        if acode > 57:  oor = 1    # ascii 9
      if oor == 1:  continue
      cunum = int(self.name[i][n0:])
      if cunum > next_i:  next_i = cunum
    next_i += 1
    return self.name_prefix+'{0:03d}'.format( next_i )
  #
  def set(self, name=None):
    #
    i = self.n_area
    self.name.append( self.next_name() )
    self.n_area += 1
    #
    # self.name.append( self.name_prefix+str(i) )
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
  def save(self, ufname=None):
    if self.n_area == 0:
      print("Nothing to save.")
      return
    fname_base =  "arec.data"
    if ufname != None:
      fname_base = ufname
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
  #
  def backup(self):
    ts_dto = datetime.now()
    ts = ts_dto.strftime("%Y%m%d_%H%M%S")
    ufname = "arec_"+ts+".data"
    self.save( ufname )
  #
  def run(self):   # human user system
    ####################################
    while( 1 ):
      #########################
      print()
      print("Entering arec user run.")
      print("  Use q to quit.")
      while True:
        print()
        uline = input("u>> ")
        if uline == 'q':
          print()
          return
        elif uline == 'ls':  self.ls()
        elif uline == 'load':  self.load()
        elif uline == 'save':  self.save()
        elif uline == 'backup':  self.backup()
        elif uline.startswith('go '):
          if len(uline) <= len('go '):
            print("No entered entered.")
          else:
            # go abc
            # 01234567
            aname = uline[3:]
            self.go( aname )
        elif uline.startswith('prefix'):
          if uline == 'prefix':
            self.prefix()  # Just show the current prefix.
          elif len(uline) <= len('prefix '):  # note the extra space
            print("No prefix entered.")
            self.prefix()
          else:
            # prefix abc
            # 01234567
            pre = uline[7:]
            self.prefix( pre )
        else:
          print("Unrecognized input.")
      #########################
    ####################################
  #
#######################################################


arec = c_arec()



