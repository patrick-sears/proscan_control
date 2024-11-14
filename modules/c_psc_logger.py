#!/usr/bin/python3

import sys
from datetime import datetime

class c_psc_logger:
  def __init__(self):
    self.fzname = 'z01a.log'
    self.logging_is_on = False
    self.oulog = ''
    #
  def clear(self):
    self.oulog = ''
    #
  def set_fzname(self, fzname):
    self.fzname = fzname
    #
  def turn_on_logging(self):
    self.logging_is_on = True
  def turn_off_logging(self):
    self.logging_is_on = False
    #
  def is_logging(self):
    return self.logging_is_on
  def add(self, m, end='\n', flush=False):
    if not self.logging_is_on:  return
    self.oulog += m+end
    if flush:  self.send()
  def add_send(self, m, end='\n'):
    if not self.logging_is_on:  return
    self.oulog += m+end
    self.send()
  def send(self):
    if not self.logging_is_on:  return
    form1 = "%Y-%m-%d %H:%M:%S"
    now = datetime.now().strftime(form1)
    ou = ''
    ou += '#_____________________________\n'
    ou += '!ts ; '+now+'\n'  # ts:  timestamp
    ou += self.oulog
    fz=open(self.fzname,'a');fz.write(ou);fz.close()
    self.oulog = ''
    #
  def send_blank_lines(self, n):
    if not self.logging_is_on:  return
    ou = ''
    for i in range(n):
      ou += '\n'
    fz=open(self.fzname,'a');fz.write(ou);fz.close()


