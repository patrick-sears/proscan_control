

import platform
import socket


############################################
print('platform.system(): ', platform.system())
hostname = socket.gethostname()
print('hostname: ', hostname)
############################################


##################################################################
class C_sim_serial:
  ###
  def __init__(self):
    self.x = 0
  ###
  def write(self, s):
    print("> ", s)
  ###
  def readline(self):
    return bytes( "101,102,103\r\n".encode() )
  ###
# module serial
##################################################################


############################################
if hostname == 'shiva2':
  #
  import serial
  #
  # Starts serial port when module is loaded.
  # spo:  serial port
  ### spo = serial.Serial(
  ###   port='COM5', baudrate=9600, bytesize=8,
  ###   timeout=2, stopbits=serial.STOPBITS_ONE
  ###   )
  spo = serial.Serial(
    port='COM5', baudrate=9600, bytesize=8,
    timeout=1, stopbits=serial.STOPBITS_ONE
    )
  #
else:
  # from m99_sim_serial import *
  spo = C_sim_serial();
############################################





