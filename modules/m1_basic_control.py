


import math

from modules.m99_sim_serial import spo





#######################################################
def send(s):
  ss = s.strip()
  ouline = ss + "\r\n"
  send = bytes(ouline.encode())
  spo.write( send )
  i = 0
  while True:
    serda = spo.readline()
    slen = len(serda)
    if slen == 0:  break
    dade = serda.decode("Ascii")
    print("  serda "+str(i)+" (L"+str(slen)+"):  ["+dade+"]")
    i += 1
#######################################################

#######################################################
def cbuf():  # clear the buffer.
  serda = ""
  ###############
  ### For testing cbuf()
  # for i in range(4):
  #   serda = spo.readline()
  #   slen = len(serda)
  #   dade = serda.decode("Ascii")
  #   print("serda "+str(i)+" (L"+str(slen)+"):  ["+dade+"]")
  ###############
  print("cbuf:")
  i = 0
  while True:
    serda = spo.readline()
    slen = len(serda)
    if slen == 0:  break
    dade = serda.decode("Ascii")
    print("  serda "+str(i)+" (L"+str(slen)+"):  ["+dade+"]")
    i += 1
  print("  Clear.")
#######################################################


#######################################################
# Reports the current stage position.
def p():
  ouline = "p\r\n"
  send = bytes(ouline.encode())
  # spo.write(b"p\r\n")  # ask for the Prior stage current position
  spo.write( send )
  serda = spo.readline()
  print("serda :  ", end='', flush=True)
  print(serda.decode("Ascii"))
#######################################################


def get_p():
  cbuf()  # Make sure the current buffer is clear.
  #
  ouline = "p\r\n"
  send = bytes(ouline.encode())
  # spo.write(b"p\r\n")  # ask for the Prior stage current position
  spo.write( send )
  serda = spo.readline()
  # print("serda :  ", end='', flush=True)
  # print(serda.decode("Ascii"))
  #
  l = serda.decode("Ascii")
  ll = l.split(',')
  x = int( ll[0] )
  y = int( ll[1] )
  return x, y


#######################################################
# Zeroes the stage at the current position.
def p0():
  spo.write(b"px 0\r\n")
  spo.write(b"py 0\r\n")
#######################################################

#######################################################
# Zeroes just the x position of the stage.
def px0():
  spo.write(b"px 0\r\n")
#######################################################

#######################################################
# Zeroes just the y position of the stage.
def py0():
  spo.write(b"py 0\r\n")
#######################################################


#######################################################
# Move 1000 pru to the left (pru is positive to left)
def grx1000():
  spo.write(b"gr 1000 0\r\n")
#######################################################


#######################################################
class Cgofov():
  # Added 2021-04-26.
  def __init__(self):
    self.fov_w = 307
    self.fov_h = 230
    self.fov_d = 384   # one diagonal, about 25% longer than 1 FOV width.
    #
    # self.Brit = bytes( 'gr -307 0\r\n'.encode() )
    # self.Blef = bytes( 'gr 307 0\r\n'.encode()  )
    # self.Bup  = bytes( 'gr 0 230\r\n'.encode()  )
    # self.Bdow = bytes( 'gr 0 -230\r\n'.encode() )
  ###
  def mcode(self, x, y):
    s = 'gr'
    s += ' {0:d}'.format( int(x * self.fov_w) )
    s += ' {0:d}'.format( int(y * self.fov_h) )
    s += '\r\n'
    return bytes( s.encode() )
  ###
  def isomcode(self, x, y):
    s = 'gr'
    s += ' {0:d}'.format( int(x * self.fov_d) )
    s += ' {0:d}'.format( int(y * self.fov_d) )
    s += '\r\n'
    return bytes( s.encode() )
  ###
  def r(self, a=1):
    spo.write( self.mcode(-a,0) )
  ###
  def l(self, a=1):
    spo.write( self.mcode(a,0) )
  ###
  def u(self, a=1):
    spo.write( self.mcode(0,a) )
  ###
  def d(self, a=1):
    spo.write( self.mcode(0,-a) )
  ###
  # isotropic motions, ie motions that move one FOV diagonal
  # This ensures same amount of motion up/down versus left/right.
  def ir(self, a=1):
    spo.write( self.isomcode(-a,0) )
  ###
  def il(self, a=1):
    spo.write( self.isomcode(a,0) )
  ###
  def iu(self, a=1):
    spo.write( self.isomcode(0,a) )
  ###
  def id(self, a=1):
    spo.write( self.isomcode(0,-a) )
  ###
#######################################################




