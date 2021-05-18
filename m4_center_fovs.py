

from m99_sim_serial import spo
import math

from m1_basic_control import cbuf

# We need to set the top, left, and right of the culture.
# The left and right together se the culture size.
# Then...
# The top is to zero the y axis.
# The left is to zero the x axis.


##################################################################
class Cmculture:
  ###
  def __init__(self):
    self.x0 = None
    self.y0 = None
    self.size = None   # diameter
    self.endlef = None
    self.endrit = None
    self.endtop = None
    self.zeroed = False
  ###
  def test_spo(self):
    send = bytes( "p\r\n".encode() )
    spo.write( send )
  ###
  def init_coordinates(self):
    if self.endlef == None or self.endrit == None or self.endtop == None:
      return;
    print("Initiating culture coordinates...")
    # Remember, prio x axis:    (+)<---------------(-)
    self.size = self.endlef - self.endrit +1
    self.radius = self.size // 2
    self.x0 = self.endrit + self.radius
    self.y0 = self.endtop - self.radius
    self.zeroed = True
  ###
  def selef(self):
    # Set the left edge of the culture.
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.endlef = int(ll[0])
    self.init_coordinates()
  ###
  def serit(self):
    # Set the right edge of the culture.
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.endrit = int(ll[0])
    self.init_coordinates()
  ###
  def setop(self):
    # Set the top edge of the culture.
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    self.endtop = int(ll[1])   # note [1], not [0] for y coord.
    self.init_coordinates()
  ###
  def gocenter(self):
    if not self.zeroed:
      print("Error:  Culture not zeroed.")
      return
    cx = int( self.x0 )
    cy = int( self.y0 )
    ouline = "g"
    ouline += " {0:d}".format( cx )
    ouline += " {0:d}".format( cy )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  ###
  def gotop(self):
    if not self.zeroed:
      print("Error:  Culture not zeroed.")
      return
    cx = int( self.x0 )
    cy = int( self.endtop )
    ouline = "g"
    ouline += " {0:d}".format( cx )
    ouline += " {0:d}".format( cy )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  ###
  def runac(self,
    n_fov = -1, margin = 1232
    ):  # run across
    if not self.zeroed:
      print("Error:  Culture not zeroed.")
      return
    w_fov = 307  # 20x:  each fov is 307.2 um wide.
    usize = self.size - margin * 2  # the width to use.
    # u_n_fov is the actual number of fovs to use.
    u_n_fov = n_fov
    n_fov_max = int(usize / (w_fov+1))
    if u_n_fov == -1:
      # Take every third FOV.
      n_av = int(usize / w_fov)
      u_n_fov = int((n_av + 2) / 3)
    if u_n_fov * w_fov > usize:
      print("Error:  Too many FOVs.")
      return
    n_if = u_n_fov - 1
    ifd = (usize - u_n_fov * w_fov) / n_if # inter fov dist
    print("FOV width:  307 um")
    print("Distance between FOV edges: ")
    print("  In um: ", int(ifd))
    print("  In FOV widths: {0:0.2f}".format(ifd/w_fov))
    print("Max number of FOVs: ", n_fov_max)
    print("n_fov to use: ", u_n_fov)
    print("Enter to run, x to exit:")
    uline = input("  in<< ")
    if uline == 'x':
      return
    dx = ifd + w_fov
    x0 = self.x0 + usize/2 - w_fov/2  # (+)<----x
    x = []
    for i in range(u_n_fov):
      x.append( x0 - i * dx )  # (+)<-----x
    #
    # cx = int( self.x0 )
    cy = int( self.y0 )
    print("Running...  Use x for early exit.")
    for i in range(u_n_fov):
      ux = int(x[i])
      ouline = "g"
      ouline += " {0:d}".format( ux )
      ouline += " {0:d}".format( cy )
      ouline += "\r\n"
      send = bytes( ouline.encode() )
      spo.write( send )
      line = "At fov "+str(i+1)+" / "+str(u_n_fov)+'.'
      if i+1 < u_n_fov:
        uline = input(line + "  in<< ")
        if uline == 'x':
          print("Early exit.")
          break
      else:
        print(line)
    print("Done.")
  ###
  ### class Cmculture
##################################################################


