#!/usr/bin/env python3

from modules.c_muwp import *

muwp  = c_muwp()
muwp.load_config()
muwp.load_plate()

muwp.create_locups()
muwp.create_brecs()

muwp.hui_main()



