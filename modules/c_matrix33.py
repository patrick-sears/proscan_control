#!/usr/bin/python3

from modules.c_vec3 import *

import sys
import math


class c_matrix33:
  def __init__(self,
        a11=None, a12=None, a13=None,
        a21=None, a22=None, a23=None,
        a31=None, a32=None, a33=None,
        ):
    self.set(a11,a12,a13,a21,a22,a23,a31,a32,a33)
    #
  def set(self, a11,a12,a13,a21,a22,a23,a31,a32,a33):
    if a11 == None:
      self.make_zero()
    elif type(a11)==int or type(a11)==float:
      self.m11=a11;  self.m12=a12;  self.m13=a13;
      self.m21=a21;  self.m22=a22;  self.m23=a23;
      self.m31=a31;  self.m32=a32;  self.m33=a33;
    elif type(a11) == c_matrix33:
      self.m11=a11.m11;  self.m12=a11.m12;  self.m13=a11.m13;
      self.m21=a11.m21;  self.m22=a11.m22;  self.m23=a11.m23;
      self.m31=a11.m31;  self.m32=a11.m32;  self.m33=a11.m33;
    else:
      print("Error e2 c_matrix33.")
      print("  Unrecognized type.")
      sys.exit(1)
  def make_zero(self):
    self.m11=0; self.m12=0; self.m13=0;
    self.m21=0; self.m22=0; self.m23=0;
    self.m31=0; self.m32=0; self.m33=0;
  def make_identity(self):
    self.make_zero()
    self.m11=1; self.m22=1; self.m33=1;
  def set_costhe(self, c):
    self.costhe = c
  def set_sinthe(self, s):
    self.sinthe = s
  def set_trans_1(self, dx, dy):
    self.dx1 = dx
    self.dy1 = dy
  def set_trans_2(self, dx, dy):
    self.dx2 = dx
    self.dy2 = dy
  def pro1(self):
    self.m11 =  self.costhe
    self.m12 = -self.sinthe
    self.m21 =  self.sinthe
    self.m22 =  self.costhe
    #
    self.m13 =  -self.dx1 * self.costhe
    self.m13 +=  self.dy1 * self.sinthe
    self.m13 +=  self.dx2
    #
    self.m23 =  -self.dx1 * self.sinthe
    self.m23 += -self.dy1 * self.costhe
    self.m23 +=  self.dy2
    #
  def mult_vec3(self, v):
    q = c_vec3()
    q.x = self.m11*v.x + self.m12*v.y + self.m13*v.z
    q.y = self.m21*v.x + self.m22*v.y + self.m23*v.z
    q.z = self.m31*v.x + self.m32*v.y + self.m33*v.z
    return q


