import os
f = raw_input('name of account to reset:')+'.blob'
assert os.path.exists(f)
open(f,'w').close()