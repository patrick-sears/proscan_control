



# from m0_c00_config import *
from m1_basic_control import *
# from m2_plate_6well import *
# from m3_mctd_8fov import *
# from m4_center_fovs import *

# from xxx import xxx
from Cc00_config import Cc00_config
from Cfov8 import Cfov8
from Cmculture import Cmculture
from Cplate_6well import Cplate_6well


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
  wp.load_inspos( c00.fname_plate_6well_inspos_lis )
#################################

# general culture
gc = Cmculture()



gf = Cgofov();


