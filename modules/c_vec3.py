#!/usr/bin/python3

import sys
import math


class c_vec3:
  def __init__(self, a1=None, a2=None, a3=None):
    self.set(a1,a2,a3)
  def set(self, a1, a2, a3):
    if a1 == None:
      self.x = 0
      self.y = 0
      self.z = 0
    elif type(a1)==int or type(a1)==float:
      self.x = a1
      self.y = a2
      self.z = a3
    elif type(a1) == c_vec3:
      self.x = a1.x
      self.y = a1.y
      self.z = a1.z
    else:
      print("Error e1 c_vec3.")
      print("  Unrecognized type.")
      sys.exit(1)
  def minus(self, v):
    w = c_vec3( self.x, self.y, self.z )
    w.x -= v.x
    w.y -= v.y
    w.z -= v.z
    return w
  def mag2(self):
    return self.x**2 + self.y**2 + self.z**2
  def mag(self):
    return math.sqrt(self.mag2())
  def make_uvec(self):
    mag = self.mag()
    self.x /= mag
    self.y /= mag
    self.z /= mag
  def dot(self, v):
    return self.x*v.x + self.y*v.y + self.z*v.z
  def cross_xy_k_mag(self, v):
    #   | i   j   k |
    #   | ax  ay  0 |
    #   | bx  by  0 |
    return self.x * v.y - self.y * v.y



