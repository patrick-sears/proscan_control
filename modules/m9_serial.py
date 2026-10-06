#!/usr/bin/env python3

from modules.c_serial_configer import *

import sys, os
import platform
# import socket


############################################
# print('platform.system(): ', platform.system())
# hostname = socket.gethostname()
# print('hostname: ', hostname)
############################################


ser_config = c_serial_configer()
ser_config.load('config/serial.config')
user_ser_config_fname = 'user/serial.config'
if os.path.exists(user_ser_config_fname):
  ser_config.load(user_ser_config_fname)


############################################
#if hostname == 'shiva2':
if ser_config.serial_mode == 'hardware':
  #
  import serial
  #
  # Starts serial port when module is loaded.
  # spo:  serial port
  ### spo = serial.Serial(
  ###   port='COM5', baudrate=9600, bytesize=8,
  ###   timeout=2, stopbits=serial.STOPBITS_ONE
  ###   )
  try:
    print("Using timeout: ", ser_config.timeout)
    spo = serial.Serial(
      # port='COM5', baudrate=9600, bytesize=8,
      port=ser_config.port,
      baudrate=9600, bytesize=8,
      # timeout=1, stopbits=serial.STOPBITS_ONE
      timeout=ser_config.timeout,
      stopbits=serial.STOPBITS_ONE
      )
  except:
    print("Error.  An exception was raised by the")
    print("  call to serial.Serial().")
    print("  - Do you have two programs trying to")
    print("    access the serial port maybe?")
    sys.exit(1)
  #
else:
  from modules.c_sim_serial import *
  spo = c_sim_serial()
############################################





