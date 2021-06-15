



# from m0_c00_config import *
from modules.m1_basic_control import *
# from m2_plate_6well import *
# from m3_mctd_8fov import *
# from m4_center_fovs import *

# from xxx import xxx
from modules.Cc00_config import Cc00_config
from modules.Cfov8 import Cfov8
from modules.Cmculture import Cmculture
from modules.Cplate_6well import Cplate_6well


c00 = Cc00_config()
c00.load()
c00.print_loaded_config()





c1 = Cfov8(1)
c2 = Cfov8(2)
c3 = Cfov8(3)
c4 = Cfov8(4)
c5 = Cfov8(5)
c6 = Cfov8(6)

def load_all_zeros():
  c1.load_zero()
  c2.load_zero()
  c3.load_zero()
  c4.load_zero()
  c5.load_zero()
  c6.load_zero()

def save_all_zeros():
  c1.save_zero()
  c2.save_zero()
  c3.save_zero()
  c4.save_zero()
  c5.save_zero()
  c6.save_zero()

wp = Cplate_6well()   # wp:  well plate
#################################
def wp_sefidu(fidu_name):
  status, x, y = c00.get_fidu(fidu_name)
  if status != 0:  return
  wp.sefidu(x,y)
#################################
def wp_load_inspos():
  wp.fname_inspos = c00.fname_plate_6well_inspos_lis
  wp.load_inspos()
#################################

# general culture
gc = Cmculture()



gf = Cgofov();


#######################################################
def tour_fovN():
  print("Starting tour of N FOVs.")
  ##########
  c1.goN()
  pline = "At c1 N.  [enter] when done, q to quit."
  while True:
    print(pline)
    uline = input("in<< ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c2.goN()
  pline = "At c2 N.  [enter] when done, q to quit."
  while True:
    print(pline)
    uline = input("in<< ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c3.goN()
  pline = "At c3 N.  [enter] when done, q to quit."
  while True:
    print(pline)
    uline = input("in<< ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c4.goN()
  pline = "At c4 N.  [enter] when done, q to quit."
  while True:
    print(pline)
    uline = input("in<< ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c5.goN()
  pline = "At c5 N.  [enter] when done, q to quit."
  while True:
    print(pline)
    uline = input("in<< ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c6.goN()
  pline = "At c6 N."
  # pline = "At c6 N.  [enter] when done, q to quit."
  # while True:
  #   print(pline)
  #   uline = input("in<< ")
  #   if uline == 'q':  return
  #   if uline == '':  break
  ##########
  print("Done with tour of N FOVs.")
  return
#######################################################






