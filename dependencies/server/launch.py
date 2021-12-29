import sys

helpInfo = """
I tried to make a script that would do it for us, however it doesn't work!!!!
So here I will explain how to start/launch server:

First, will you launch the devs or public version?
    DEVS is the one used by the game NOT compiled
    PUBLIC is the one used when it is compiled
    
2: Will you run Panda's (dist) or data server (data)?
    DATA server takes care of the blobs
    DIST is the server for DistributedObjects (panda stuff)
    **** A fully working server uses both ****
    
Extra info: Ports each one uses

|-------------------|
|______|DATA | DIST |
|PUBLIC|36911| 4011 |
|DEVS  |36912| 4000 |
|-------------------|
   
Now that you already know I'll explain which python shortcut you should use for each.
I set shortcuts to make it easier to find them with "ps -A"

The shortcuts are:
    py_dev_data : Data for DEVS version
    py_dev_dist : Panda's for DEVS version
    py_pub_data : Data for PUBLIC version
    py_pub_dist : Panda's for DEVS version
    
Now cd to the folder you wanna (eg: devs)
The right commands are:
    Devs: (cd devs)
        data -> nohup py_dev_data NetworkedBlobServer.py &
        dist -> nohup py_dev_dist server.py &
    Public: (cd public)
        data -> nohup py_pub_data NetworkedBlobServer.py &
        dist -> nohup py_pub_dist server.py &
    
"""

sys.exit(helpInfo)
import subprocess, sys, os
from string import split

psProc = subprocess.Popen(['ps','-A'],shell=True,stdout=subprocess.PIPE)
psProc.wait()

out,_ = psProc.communicate()
res = map(split,out.replace('\r','').split('\n')[1:-1])
running = {}
for r in res:
    if r[-1].startswith('py_'): running[r[0]] = r[-1]
    
print running
        
def open_nohup(path,cmd):
    cmd = ['nohup']+' '.join(cmd)+['&']
    print 'Nohup:',cmd,'@',path
    cpath = os.path.abspath(os.curdir)
    os.chdir(path)
    subprocess.Popen(cmd,shell=True,stdout=sys.stdout,stderr=sys.stderr).wait()
    os.chdir(cpath)
    
d = raw_input('Dist to run ("public" or "devs"):')
while not d in ["public","devs"]:
    d = raw_input('Dist to run ("public" or "devs"):')
    
_path = d
_cmd = "py_"+_path[:3]

run_data = raw_input('Run DATA (y/n):')
while not run_data in ["y","n"]:
    run_data = raw_input('Run DATA (y/n):')
    
run_distributed = raw_input('Run distributed [panda\'s] (y/n):')
while not run_distributed in ["y","n"]:
    run_distributed = raw_input('Run distributed [panda\'s] (y/n):')
    
if run_data: open_nohup(_path,[_cmd+"_data","NetworkedBlobServer.py"])
if run_distributed: open_nohup(_path,[_cmd+"_dist","server.py"])