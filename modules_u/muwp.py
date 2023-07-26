#!/usr/bin/python3

from modules.m2 import muwp

# muwp>> load all
muwp.load_config()
muwp.load_plate()

# muwp>> create lps
muwp.create_locups()

# run.
muwp.run()


