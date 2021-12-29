import os, sys
f = raw_input('name of account to explore:')+'.blob'
assert os.path.exists(f)

sys.path.append('../../../..')
from tth.datahnd import Blob

b = Blob.Blob(f)

for file,data in b.files.items():
    print '------------%s (%d bytes)------------' % (file,len(data))
    print
    print data
    print
    
raw_input('*** press enter to exit')