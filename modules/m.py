



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

def print_zeros():
  print("c1:  ", c1.x0, c1.y0)
  print("c2:  ", c2.x0, c2.y0)
  print("c3:  ", c3.x0, c3.y0)
  print("c4:  ", c4.x0, c4.y0)
  print("c5:  ", c5.x0, c5.y0)
  print("c6:  ", c6.x0, c6.y0)


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
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c2.goN()
  pline = "At c2 N.  [enter] when done, q to quit."
  while True:
    print(pline)
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c3.goN()
  pline = "At c3 N.  [enter] when done, q to quit."
  while True:
    print(pline)
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c4.goN()
  pline = "At c4 N.  [enter] when done, q to quit."
  while True:
    print(pline)
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c5.goN()
  pline = "At c5 N.  [enter] when done, q to quit."
  while True:
    print(pline)
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':  break
  ##########
  c6.goN()
  pline = "At c6 N."
  # pline = "At c6 N.  [enter] when done, q to quit."
  # while True:
  #   print(pline)
  #   uline = input("u>> ")
  #   if uline == 'q':  return
  #   if uline == '':  break
  ##########
  print("Done with tour of N FOVs.")
  return
#######################################################




#######################################################
def fov8_adjust():
  print("Starting tour of edges to adjust culture positions.")
  print("  Just hit [enter] if ok.")
  print("  Hit a[enter] if adjustment has been made.")
  print("  Any time, q[enter] quits.")
  ##########
  c1.goedW()
  while True:
    print("At c1 W edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c1.selef()
  ##########
  c1.goedN()
  while True:
    print("At c1 N edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c1.setop()
  ##########
  c2.goedW()
  while True:
    print("At c2 W edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c2.selef()
  ##########
  c2.goedN()
  while True:
    print("At c2 N edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c2.setop()
  ##########
  c3.goedW()
  while True:
    print("At c3 W edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c3.selef()
  ##########
  c3.goedN()
  while True:
    print("At c3 N edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c3.setop()
  ##########
  ################################### new order
  ##########
  c6.goedN()
  while True:
    print("At c6 N edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c6.setop()
  ##########
  c6.goedW()
  while True:
    print("At c6 W edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c6.selef()
  ##########
  c5.goedN()
  while True:
    print("At c5 N edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c5.setop()
  ##########
  c5.goedW()
  while True:
    print("At c5 W edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c5.selef()
  ##########
  c4.goedN()
  while True:
    print("At c4 N edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c4.setop()
  ##########
  c4.goedW()
  while True:
    print("At c4 W edge.")
    uline = input("u>> ")
    if uline == 'q':  return
    if uline == '':   break
    if uline == 'a':  c4.selef()
  ##########
  print("Done with adjustments.")
  return
#######################################################


