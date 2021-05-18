

from m99_sim_serial import spo


##################################################################
class Cplate_6well:
  ###
  def __init__(self):
    # When zeroed, this class has the prior coordinates reset so
    # that x=0 at R end of R most wells (wells 3 and 6) and y=0 at
    # the bottom of the bottom wells (wells 1 2 3).
    self.zeroed = False
    self.n_well = 7    # well[0] is the center of the plate (not a well)
    # Creating n_well = 7 was a terrible idea.  I don't want to
    # change it now but I do need an n_well that goes to 6.  So:
    # n_euwell:  n true well.
    self.n_euwell = 6
    self.init_wells()
    #
    # For each insert, we want to have position info which we can
    # save to file.  We want the ability to use N W S E edges of
    # insert membrane (pos 0 1 2 3).  We need this for each of the
    # 6 wells, 1 2 3 4 5 6 which will have indices 0 1 ... 5.
    # n_cardinal:  number of cardinal points
    self.n_cardinal = 4
    self.card_name = ['N','W','S','E']
    # inspos:  insert position[well_index][cardinal_pos_index]
    self.inscenx = []  # insert center x
    self.insceny = []  # insert center y
    self.inscenxl = []  # loaded insert center x
    self.inscenyl = []  # loaded insert center y
    self.inspos = []
    self.insposl = [] # pos set by loading a file.
    #######
    for i in range(self.n_euwell):
      self.inscenx.append(None)
      self.insceny.append(None)
      self.inscenxl.append(None)
      self.inscenyl.append(None)
      self.inspos.append([])
      self.insposl.append([])
      for j in range(self.n_cardinal):
        self.inspos[i].append(None)
        self.insposl[i].append(None)
    #######
    #
    self.fname_inspos = "z02_plate_6well_inspos.data"
  ###
  def seinsposN(self, well):
    self.seinspos(well,0)
  ###
  def seinsposW(self, well):
    self.seinspos(well,1)
  ###
  def seinsposS(self, well):
    self.seinspos(well,2)
  ###
  def seinsposE(self, well):
    self.seinspos(well,3)
  ###
  def seinspos(self, well, cp):  # cp is cardinal point
    if well < 1 or well > 6:
      print("well out of range.")
      return
    if cp < 0 or cp > 3:
      print("cp out of range.")
      return
    i = well - 1
    cbuf() # Make sure the buffer is clear.
    send = bytes( "p\r\n".encode() )
    spo.write( send )
    serda = spo.readline()
    ll = serda.decode("Ascii").split(',')
    if cp == 0 or cp == 2:  # setting y
      self.inspos[i][cp] = int(ll[1])
    else:                   # setting x
      self.inspos[i][cp] = int(ll[0])
  ###
  def save_inspos(self):
    fz = open(self.fname_inspos, 'w')
    fz.write('--------------------------\n')
    for i in range(self.n_euwell):
      ii = i + 1
      line = "w"+str(ii)
      line += " center:"
      x = self.inscenx[i]
      y = self.insceny[i]
      if x == None:  line += " ---"
      else: line += " {0:d}".format(self.inscenx[i])
      if y == None:  line += " ---"
      else: line += " {0:d}".format(self.insceny[i])
      fz.write(line+'\n')
    fz.write('--------------------------\n')
    fz.write('------\n')
    for i in range(self.n_euwell):
      ii = i + 1
      for j in range(self.n_cardinal):
        if j == 0 or j == 2:  cardtype = 'y:'
        else:                 cardtype = 'x:'
        if self.inspos[i][j] == None:  sval = '-'
        else:  sval = str( int(self.inspos[i][j]) )
        line = "w"+str(ii)
        line += ' '+self.card_name[j]
        line += ' '+cardtype
        line += ' '+sval
        fz.write(line+'\n')
      fz.write('------\n')
    fz.write('--------------------------\n')
    fz.close()
  ###
  def calc_all_inscen(self):
    for i in range(self.n_euwell):
      self.inscenx[i] = None
      self.insceny[i] = None
      ######
      val0 = self.inspos[i][0] # N
      val2 = self.inspos[i][2] # S
      if val0 != None and val2 != None:
        self.insceny[i] = int((val0 + val2) / 2)
      ######
      val1 = self.inspos[i][1] # W
      val3 = self.inspos[i][3] # E
      if val1 != None and val3 != None:
        self.inscenx[i] = int((val1 + val3) / 2)
      ######
  ###
  def load_inspos(self, fname):
    # f = open(self.fname_inspos)
    f = open(fname)
    f.readline()  # skip first line.
    for i in range(self.n_euwell):
      l = f.readline().strip()
      ll = l.split(' ')
      if ll[2] == '---':  self.inscenxl[i] = None
      else:               self.inscenxl[i] = int(ll[2])
      if ll[3] == '---':  self.inscenyl[i] = None
      else:               self.inscenyl[i] = int(ll[3])
    f.readline()  # skip line of ----------------
    for i in range(self.n_euwell):
      f.readline()  # skip line of ------
      ii = i + 1
      for j in range(self.n_cardinal):
        if j == 0 or j == 2:  cardtype = 'y:'
        else:                 cardtype = 'x:'
        #
        l = f.readline().strip()
        ll = l.split(' ')
        if ll[3] == '-': self.insposl[i][j] = None
        else:  self.insposl[i][j] = int(ll[3])
    f.close()
  ###
  def copy_insposl_to_inspos(self):
    for i in range(self.n_euwell):
      self.inscenx[i] = self.inscenxl[i]
      self.insceny[i] = self.inscenyl[i]
      for j in range(self.n_cardinal):
        self.inspos[i][j] = self.insposl[i][j]
  ###
  def ls_inspos(self):
    for i in range(self.n_euwell):
      ii = i + 1
      line = "w"+str(ii)
      line += " center:"
      x = self.inscenx[i]
      y = self.insceny[i]
      if x == None:
        line += "      ---"
      else:
        line += " {0:8d}".format(self.inscenx[i])
      if y == None:
        line += "      ---"
      else:
        line += " {0:8d}".format(self.insceny[i])
      print(line)
    for i in range(self.n_euwell):
      ii = i + 1
      for j in range(self.n_cardinal):
        if j == 0 or j == 2:  cardtype = 'y:'
        else:                 cardtype = 'x:'
        if self.inspos[i][j] == None:  sval = '-'
        else:  sval = str( int(self.inspos[i][j]) )
        line = "w"+str(ii)
        line += ' '+self.card_name[j]
        line += ' '+cardtype
        line += ' '+sval
        print(line)
  ###
  def ls_insposl(self):
    for i in range(self.n_euwell):
      ii = i + 1
      line = "w"+str(ii)
      line += " center:"
      x = self.inscenxl[i]
      y = self.inscenyl[i]
      if x == None:
        line += "      ---"
      else:
        line += " {0:8d}".format(self.inscenxl[i])
      if y == None:
        line += "      ---"
      else:
        line += " {0:8d}".format(self.inscenyl[i])
      print(line)
    for i in range(self.n_euwell):
      ii = i + 1
      for j in range(self.n_cardinal):
        if j == 0 or j == 2:  cardtype = 'y:'
        else:                 cardtype = 'x:'
        if self.insposl[i][j] == None:  sval = '-'
        else:  sval = str( int(self.insposl[i][j]) )
        line = "w"+str(ii)
        line += ' '+self.card_name[j]
        line += ' '+cardtype
        line += ' '+sval
        print(line)
  ###
  def sefidu(self, x, y):
    #
    if x != '-':
      uline = "px "+x
      print("Sending: ", uline)
      uline = uline+"\r\n"
      spo.write( bytes( uline.encode() ) )
    if y != '-':
      uline = "py "+y
      print("Sending: ", uline)
      uline = uline+"\r\n"
      spo.write( bytes( uline.encode() ) )
  ###
  def init_wells(self):
    self.well_diam = 35000
    self.well_r = self.well_diam / 2
    self.well_sep  = 39000
    #
    # [row][col], like a matrix (not like xy)
    #
    # [0(center of plate) 1 2 3 4 5 6]
    self.well_cx = []
    self.well_cy = []
    for i in range(self.n_well):
      self.well_cx.append(None)
      self.well_cy.append(None)
    #
    #
    self.well_cx[1] = int(self.well_r + 2 * self.well_sep)
    self.well_cx[2] = int(self.well_r + self.well_sep)
    self.well_cx[3] = int(self.well_r)
    #
    self.well_cy[1] = int(self.well_r + self.well_sep)
    self.well_cy[4] = int(self.well_r)
    #
    self.well_cx[4] = self.well_cx[1]
    self.well_cx[5] = self.well_cx[2]
    self.well_cx[6] = self.well_cx[3]
    #
    self.well_cy[2] = self.well_cy[1]
    self.well_cy[3] = self.well_cy[1]
    self.well_cy[5] = self.well_cy[4]
    self.well_cy[6] = self.well_cy[4]
    #
    self.well_cx[0] = self.well_cx[2]
    self.well_cy[0] = int((self.well_cy[1] + self.well_cy[4]) / 2)
  ###
  def show_well_centers(self):
    for i in range(self.n_well):
      print("> ", i, "  ("+str(self.well_cx[i])+","+str(self.well_cy[i])+")")
  ###
  def gow1N(self):
    self.gowiN(1)
  ###
  def gow6N(self):
    self.gowiN(6)
  ###
  def gowiN(self, i):
    gox = int( self.well_cx[i] )
    goy = int( self.well_cy[i] + 8750 )
    # North is roughly 8.75 mm up from center.
    ouline = "g"
    ouline += " {0:d}".format( gox )
    ouline += " {0:d}".format( goy )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  ###
  def gowiW(self, i):
    gox = int( self.well_cx[i] + 8750 )
    goy = int( self.well_cy[i] )
    # W is roughly 8.75 mm to left from center.
    ouline = "g"
    ouline += " {0:d}".format( gox )
    ouline += " {0:d}".format( goy )
    ouline += "\r\n"
    send = bytes( ouline.encode() )
    spo.write( send )
  ###
  def reset_origin(self):
    # Won't actually reset the origin unless the user accepts
    # the change.
    if not self.zeroed:
      print("Hold on there!")
      print("  You've got to set an origin first.")
      return
    n_x = 0
    n_y = 0
    dx = 0
    dy = 0
    ###############
    for i in range(self.n_euwell):
      for j in range(self.n_cardinal):
        if self.inspos[i][j]  == None:  continue
        if self.insposl[i][j] == None:  continue
        if j == 0 or j == 2:     # y
          dy += self.inspos[i][j] - self.insposl[i][j]
          n_y += 1
        else:                    # x
          dx += self.inspos[i][j] - self.insposl[i][j]
          n_x += 1
    ###############
    if n_y > 0:  dy /= n_y
    if n_x > 0:  dx /= n_x
    dy = int(dy)
    dx = int(dx)
    print("Number of matching x positions: ", n_x)
    print("Number of matching y positions: ", n_x)
    print("dx: ", dx)
    print("dy: ", dy)
    if n_x < 1 or n_y < 1:
      print("Not enogh inforamtion to reset the origin.")
    else:
      uline = input("Accept the ner origin? (N/y):<< ")
      if uline == 'y':
        # Get the current position then figure out where the
        # true origin is.
        curx, cury = get_p()
        #
        new_x0 = int( -curx - dx )
        new_y0 = int( -cury - dy )
        linex = "px "+str(new_x0)+"\r\n"
        liney = "py "+str(new_x0)+"\r\n"
        print("sending:")
        print("  "+linex)
        print("  "+liney)
        spo.write( bytes(linex.encode()) )
        spo.write( bytes(liney.encode()) )
  ###
##################################################################







