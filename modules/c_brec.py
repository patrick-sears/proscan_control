#!/usr/bin/python3

from modules.c_vec3 import *
from modules.c_matrix33 import *

import sys

class c_brec:
  def __init__(self):
    #
    # S0:  local coord system
    # S1:  stage coord system
    self.init_fid(2)
    #
    # Init S1 to be the same as S0.
    self.e1_S0 = c_vec3(1,0,0)
    self.e2_S0 = c_vec3(0,1,0)
    self.e1_S1 = c_vec3(1,0,0)
    self.e2_S1 = c_vec3(0,1,0)
    self.S01_tra = c_vec3(0,0,0)
    #
    self.fov_S0 = []
    self.fov_S1 = []
    self.n_fov = 0
    #
  def init_fid(self, n):
    self.fid_S0 = []
    self.fid_S1 = []
    self.n_fid = n
    for i in range(self.n_fid):
      self.fid_S0.append( c_vec3() )
      self.fid_S1.append( c_vec3() )
    #
  def set_ic(self, ic):
    self.ic = ic
    #
  def add_fov_S1(self, x, y, z):
    self.fov_S1.append( c_vec3(x,y,z) )
    #
    # Get S0 values from S1.
    # Temporary, just use S1 values.
    xx = x; yy = y; zz = z;
    self.fov_S0.append( c_vec3(xx,yy,zz) )
    #
    self.n_fov += 1
    #
  def set_fid_S1(self, ifid, x,y,z):
    if ifid < 0 or ifid >= self.n_fid:  return -1
    self.fid_S1[ifid].set(x,y,z)
    return 0
    #
  def get_fid_S1(self, ifid):
    x = self.fid_S1[ifid].x
    y = self.fid_S1[ifid].y
    z = self.fid_S1[ifid].z
    return x,y,z
    #
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
  def get_save1(self):
    ou = ''
    ou += '!brec ; '+str(self.ic)+'\n'
    ou += '!n_fid ; '+str(self.n_fid)+'\n'
    ou += '!n_fov ; '+str(self.n_fov)+'\n'
    for i in range(self.n_fid):
      ou += '!fid_S0 ; '+str(i)
      ou += ' ; {:6.1f}'.format( self.fid_S0[i].x )
      ou += ' ; {:6.1f}'.format( self.fid_S0[i].y )
      ou += ' ; {:6.1f}'.format( self.fid_S0[i].z )
      ou += '\n'
    for i in range(self.n_fov):
      ou += '!fov_S0 ; '+str(i)
      ou += ' ; {:6.1f}'.format( self.fov_S0[i].x )
      ou += ' ; {:6.1f}'.format( self.fov_S0[i].y )
      ou += ' ; {:6.1f}'.format( self.fov_S0[i].z )
      ou += '\n'
    return ou
    #
  def read_f(self, f):
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      key = mm[0]
      if key == '!n_fid':
        n_fid = int(mm[1])
        self.init_fid( n_fid )
      elif key == '!fid_S0':
        fidi = int(mm[1])
        x = float(mm[2])
        y = float(mm[3])
        z = float(mm[4])
        self.fid_S0[fidi].set(x,y,z)
      elif key == '!fov_S0':
        i_fov = int(mm[1])
        x = float(mm[2])
        y = float(mm[3])
        z = float(mm[4])
        self.fov_S0[i_fov].set(x,y,z)
      else:
        print("Error e301.  c_brec.py")
        print("  key: ", key)
        sys.exit(1)
    #
  def pro1(self):
    # Using fids found in S1, determine the transformation
    # needed to go to positions defined in S0.
    #
    self.generate_S01_matrix()
    #
    # Calculate new basis vectors.
    self.e1_S1 = self.m01.mult_vec3( self.e1_S0 )
    self.e2_S1 = self.m01.mult_vec3( self.e2_S0 )
    #
  def generate_S01_matrix(self):
    #
    aS0 = c_vec3( self.fid_S0[0] )
    bS0 = c_vec3( self.fid_S0[1] )
    aS1 = c_vec3( self.fid_S1[0] )
    bS1 = c_vec3( self.fid_S1[1] )
    #
    u0 = aS0.minus( bS0 )
    u0.make_uvec()
    u1 = aS1.minus( bS1 )
    u1.make_uvec()
    #
    costhe = u0.dot( u1 )
    sinthe = u1.cross_xy_k_mag( u1 )
    #
    # Find translations 1 and 2.
    dv1 = c_vec3( aS0 )
    dv2 = c_vec3( aS1 )
    #
    self.m01 = c_matrix33()
    self.m01.set_costhe( costhe )
    self.m01.set_sinthe( sinthe )
    self.m01.set_trans_1( dv1.x, dv1.y )
    self.m01.set_trans_2( dv2.x, dv2.y )
    self.m01.pro1()
    #


