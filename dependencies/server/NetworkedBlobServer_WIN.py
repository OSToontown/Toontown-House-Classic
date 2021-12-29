"""
This file runs on server.
"""

import zlib, random, hashlib, cPickle, os, sys, glob
from socket import *
from thread import start_new_thread as snt
from base64 import *

import __builtin__
__builtin__.tracker = {}

class Blob:
    def __init__(self,file):
        self.file = file
        try:
            with open(file,"rb") as f: 
                self.data=f.read()
                if self.data: self.data=zlib.decompress(self.data)
        except Exception,e: raise Exception, e
        self.data = self.data.split(chr(1))[1:]
        self.files={}
        for i in range(0,len(self.data),2):
            key = self.data[i]
            val = self.data[i+1]
            decodedval = b64decode(val)
            self.files[key] = decodedval
        del self.data
        
    def bake(self):
        o=''
        for file in self.files.keys():
            o+=chr(1)+file+chr(1)+b64encode(self.files[file])
        return zlib.compress(o)
    
    def read(self,file):
        if not file in self.files:
            return ""
        return self.files[file]
    
    def write(self,file,data,append=True):
        if not file in self.files: 
            self.files[file]=data
            return
        if append:
            self.files[file]+=data
        else:
            self.files[file]=data
            
    def exists(self,file): return file in self.files
    
    def flush(self):
        with open(self.file,"wb") as f:
            f.write(self.bake())

def hs(s):
	_items = ','.join(map(str,[random.randint(1,11) for i in xrange(5)]))
	_key = hashlib.md5(os.urandom(128)).hexdigest()[:8]
	expect = hashlib.md5(zlib.compress(cPickle.dumps({_key[::-1]:','.join(list(reversed(_items.split(','))))}))).hexdigest()[:8]
	s.send(zlib.compress(cPickle.dumps({_key:_items})).encode('base64'))
	return s.recv(8) == expect
    
def getTargetUser(sock):
    user = sock.recv(100).split('\0',1)[0]
    print '\t',sock,'SETUSER',user
    if not os.path.isfile('./data/blobs/{0}.blob'.format(user)):
        return False
    if user in tracker:
        print 'WTF! USER ALREADY CONNECTED!',user
        return False
        
    #tracker[user] = sock
    return user

s = socket()
s.bind(("0.0.0.0",36911))
s.listen(1000)

def newToon(acc,name,ia,spot,nToAp = None):
    _id = -1
    _toons = [int(t.replace('\\','/').split('/')[-1].split('.',1)[0]) for t in glob.glob('./data/toons/*.toon')]
    _toons.sort()
    if len(_toons): _id = _toons[-1]+1
    else: _id = 0
    del _toons
    _id = str(_id)
    
    if not ia and nToAp:
        with open('./data/toons/'+_id+'.nta','wb') as f:
            f.write('!'.join([nToAp,acc,spot]))
    
    with open('./data/toons/'+_id+'.toon','wb') as f:
        f.write('!'.join([name,acc,spot]))
        
    return _id

def handler(sock,addr):
    shouldRun = True
    if not hs(sock):
        print '\t',addr,'BAD HANDSAKE! Exiting...'
        shouldRun = False
        
    if shouldRun:
        user = getTargetUser(sock)
        if not user:
            print '\t',addr,'Error getting target user! Exiting...'
            shouldRun = False
        
    if not shouldRun:
        sock.close()
        return
        
    ublob = Blob('./data/blobs/{0}.blob'.format(user))
        
    while shouldRun:
        try: query = sock.recv(1024*50).split('\0',1)[0].split(' ',1) #20kb buffer
        except Exception as e:
            print '\t',addr,'left (1)!',e
            break
            
        msg = 'ok'
        
        cmd = query[0]
        
        if not cmd:
            print '\t',addr,'left (3)!'
            break
        
        args = []
        if len(query)>1: args = query[1:]
        
        #print '\t',addr,' SENT CMD!'
        #print '\t\t',cmd
        #print '\t\t',args
        
        if cmd == 'get': #ex: get file
            _name = args[0]
            msg = ublob.read(_name).encode('base64')
            if not msg: msg='NO_SUCH_FILE'
            
        elif cmd == 'set': #ex: set file data
            _name,_data = args[0].split('\x12')
            ublob.write(_name,_data,False)
            ublob.flush()
            
        elif cmd == 'newToon': #ex: newToon NAME IS_APPROVED SPOT
            msg = newToon(user,*args[0].split('%'))
        
        elif cmd == 'all': #ex: all
            msg = ublob.bake().encode('base64')
         #   print '!!! SENDING "all" to',addr,' SIZE=',len(msg)
         
        elif cmd == 'delToon': #ex: delToon SPOT
            #remove data about that spot
            spot = args[0]
            
            of = ublob.files
            nf = {}
            
            for f,c in of.items():
                if not f.endswith(str(spot)): nf[f]=c
                
            ublob.files = nf
            ublob.flush()

        try: sock.send(msg+'\0')
        except Exception as e:
            print '\t',addr,'left (2)!',e
            break
            
    sock.close()
    #del tracker[user]

print 'RUNNING...'

while True:
    sock,addr = s.accept()
    print 'New connection!',addr
    snt(handler,(sock,addr))