

proscan_control is a python interface to the Prior Scientific
ProScan III motorized microscope stage.  It used most often
to run through a sequence of positions in a set of cultures.
Another use is to remember positions visited and plot them.


__________________________________________________________________
Source.

2021 ipro 0412v12a.
2022 ipro 0211v12a.

__________________________________________________________________
Documentation.

On the Chapel Hill UNC network, see the mtorpedi server:
  http://152.19.58.31/prs-proscan_control/main.html



__________________________________________________________________
m system.

Do this to start:
>>> from modules.m import *


__________________________________________________________________
locup system.

Do this to start:
>>> from modules.c_locup import locup
>>> locup.run()

          N
        -----
      /       \
   W |         |  E
      \       /
        -----
          S


__________________________________________________________________
arec system.


Do this to start:
>>> from modules.c_arec import arec


