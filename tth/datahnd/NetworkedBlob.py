"""
File: NetworkBlob.py
    Module: tth.datahnd
Author: Nacib
Date: JULY/25/2013
Description: Blob for storing data, a VFS into a single file, pushed to a server
BASED ON FILE FROM COGTOWN
"""

import zlib, os, hashlib, cPickle, random
from socket import *
from base64 import *

def hs(s):
        hash1 = cPickle.loads(zlib.decompress(b64decode(s.recv(2048))))
        _key,_items = hash1.items()[0]
        hash2 = hashlib.md5(zlib.compress(cPickle.dumps({_key[::-1]:','.join(list(reversed(_items.split(','))))}))).hexdigest()[:8]
        
        s.send(hash2)

class NetworkedBlob:
    def __init__(self,server,port,user):
        self.s = socket()
        self.s.connect((server,port))
        
        hs(self.s)
        
        self.s.send(user+'\0')
        
    def write(self,file,data,*ignore):
        self.s.send('set {}\x12{}'.format(file,data))
        self.s.recv(10) #ignore
    
    def read(self,file):
        self.s.send('get '+file)
        return self.s.recv(1024*50).split('\0',1)[0]
        
    def newToon(self,*args):
        self.s.send('newToon '+'%'.join(args))
        return self.s.recv(1024**1).split('\0',1)[0]
        
    def delToon(self,spot):
        self.s.send('delToon '+str(spot))
        return self.s.recv(1024**1).split('\0',1)[0]
        
    def allToon(self,verbose=0):
        if verbose:print ':SrvData: Contacting server for "all"...'
        self.s.send('all')
        data = zlib.decompress(b64decode(self.s.recv(1024*500).split('\0',1)[0])).split(chr(1))[1:]
        if verbose:print ':SrvData: "all" sent by server!',data
        files={}
        
        if len(data)>1:
            for i in range(0,len(data),2):
                key = data[i]
                val = data[i+1]
                decodedval = b64decode(val)
                files[key] = decodedval
            
        if verbose:print ':SrvData: "all" READ!'
        return files
        
    def bake(self): pass
    def flush(self): pass
    
#i had put a handler for mgs
#put stupid git got rid of it
#also fault of the guy that
#did the allToon shit
