
import sys

##################################################################
class Cc00_config:
  ###
  def __init__(self):
    self.well6_holder_fiducial_n = 0
    self.well6_holder_fiducial_name = []
    self.well6_holder_fiducial_x    = []
    self.well6_holder_fiducial_y    = []
    #
    self.fname_plate_6well_inspos_lis = None
  ###
  def load(self):
    f = open('c00.config')
    for l in f:
      if not l.startswith('!'):  continue
      l = l.strip()
      ll = l.split(' ')
      key = ll[0]
      ###
      if key == '!well6_holder_fiducial':
        for l in f:
          l = l.strip()
          if len(l) == 0:  break
          if l[0] == '#':  continue
          ll = l.split(' ')
          self.well6_holder_fiducial_name.append( ll[0] )
          self.well6_holder_fiducial_x.append(    ll[1] )
          self.well6_holder_fiducial_y.append(    ll[2] )
      elif key == '!fname_plate_6well_inspos_list':
        self.fname_plate_6well_inspos_lis = ll[1]
      else:
        print("Error.  Unrecognized key in c00.config.")
        print("  key: ", key)
        sys.exit(1)
    f.close()
    self.well6_holder_fiducial_n = len( self.well6_holder_fiducial_name )
  ###
  def print_loaded_config(self):
    print("!well6_holder_fiducial:")
    for i in range( self.well6_holder_fiducial_n ):
      print("  ",
        self.well6_holder_fiducial_name[i],
        self.well6_holder_fiducial_x[i],
        self.well6_holder_fiducial_y[i]
        )
  ###
  def get_fidu(self, fidu_name):
    #
    # status:  0 ok, 1 error
    status = 0
    found = False
    ##############
    for i in range(self.well6_holder_fiducial_n):
      if fidu_name == self.well6_holder_fiducial_name[i]:
        found = True
        x = self.well6_holder_fiducial_x[i]
        y = self.well6_holder_fiducial_y[i]
    ##############
    if not found:
      print("Error:  Unrecognized name.")
      status = 1
      return status, 0, 0
    #
    return status, x, y
  ###
  ###
##################################################################




