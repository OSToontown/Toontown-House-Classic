"""
File: Blob.py
    Module: tth.datahnd
Author: Nacib
Date: JULY/25/2013
Description: Blob for storing data, a VFS into a single file
FROM COGTOWN
"""

import zlib

class Blob:
    def __init__(self,file):
        self.file = file
        self.reload()

    def reload(self):
        self.files = self.__readFile()
        
    def __readFile(self):
        f = open(self.file,"rb")
        data = f.read()
        f.close()
        
        return Blob.debake(data)
       
    @staticmethod   
    def debake(data,decompress=True):
        if decompress:
            data = zlib.decompress(data).split(chr(1))[1:]
            
        return dict(map(lambda a:(a[0],a[1].decode('base64')),[data[i:i+2] for i in xrange(0,len(data),2)]))
        
    def bake(self):
        o=''
        for file in self.files.keys():
            o+=chr(1)+file+chr(1)+str(self.files[file]).encode('base64')
        return zlib.compress(o)
    
    def read(self,file):
        if not file in self.files:
            return ""
        return self.files[file]
    
    def write(self,file,data,append=True):
        data = str(data)
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
            
        self.reload()
            
    def all(self): return self.files
    
    def newToon(self,*a): return "0"
    def delToon(self,*a): pass
            
def newBlob(file):
    with open(file,"w") as f:pass #create
    return Blob(file)
    