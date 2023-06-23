
from modules.c_muwp import muwp

# muwp>> load all
muwp.load_config()
muwp.load_plate()

# muwp>> create lps
muwp.create_locups()

# run.
muwp.run()



