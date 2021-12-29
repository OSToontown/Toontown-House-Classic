# Cleanse the directory of all files with a .pyc extension, and remove any
# files "copy" files (file names that match the pattern '*/*(*').

import glob
import os

for f in (glob.glob('*/*.pyc') + glob.glob('*/*(*')):
    print "Removing '%s'..." % f
    os.unlink(f)

print 'Done.'
os.system('pause')