#!/usr/bin/python3

from modules.c_vec3 import *

class c_brec:
  def __init__(self):
    #
    # S0:  local coord system
    # S1:  stage coord system
    self.init_fid()
    #
    # Init S1 to be the same as S0.
    self.e1_S0 = c_vec3(1,0,0)
    self.e2_S0 = c_vec3(0,1,0)
    self.e1_S1 = c_vec3(1,0,0)
    self.e2_S1 = c_vec3(0,1,0)
    self.S01_tra = c_vec3(0,0,0)
    #
  def init_fid(self):
    self.fid_S0 = []
    self.fid_S1 = []
    self.n_fid = 2
    for i in range(self.n_fid):
      self.fid_S0.append( c_vec3() )
      self.fid_S1.append( c_vec3() )
    #
  def set_ic(self, ic):
    self.ic = ic
    #
  def set_fid_S1(self, ifid, x,y,z):
    if ifid < 0 or ifid >= self.n_fid:  return -1
    self.fid_S1[ifid].set(x,y,z)
    return 0
  def define_S0(self, S1x0, S1y0, S1z0):
    self.S01_tra.set(S1x0, S1y0, S1z0)
    #
    # Reset S1 basis vectors to be same as for S0.
    # Note that these are S1 vectors in SO.
    self.e1_S1.set(1,0,0)
    self.e2_S1.set(0,1,0)
    #
    for i in range(self.n_fid):
      self.fid_S0[i].set(
        self.fid_S1[i].x - self.S01_tra.x,
        self.fid_S1[i].y - self.S01_tra.y,
        self.fid_S1[i].z - self.S01_tra.z
        )
    #




