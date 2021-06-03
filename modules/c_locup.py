
from m1_basic_control import p

#######################################################
class c_locup:
  #
  def __init__(self):
    self.x0 = None
    self.y0 = None
    self.cnum = 1    # the culture number
  #
  def run(self):
    pline = "Go to culture "+str(self.cnum)
    pline += " North edge. and hit e[enter]\n"
    while True:
      print(pline)
      uline = input("in<< ")
      if uline == 'q':  return
      if uline == 'e':  break
    p()
#######################################################






