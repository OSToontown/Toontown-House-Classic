import struct, zlib

class HouseDatagramError(Exception): pass
class NumberTooLarge(HouseDatagramError): pass
class UnpackableObjectError(HouseDatagramError): pass

def testInt(theint):
    if int(theint) != theint:
        return "d"
        
    if theint < 0:
        if theint > -2**15: return "h"
        elif theint > -2**31: return "i"
        else: raise NumberTooLarge(str(theint))
        
    else:
        if theint < 2**16: return "H"
        elif theint < 2**32: return "I"
        else: raise NumberTooLarge(str(theint))
    
class HouseDatagram:
    symbols = {
               str:'S',
               
               int:'N',
               long:'N',
               float:'N',
               
               list:'C',
               tuple:'C',
               set:'C',
               
               dict:'D',
               
               bool:'B',
               type(None):'V'
              }
                
    conjuncts = {
                 list:'l',
                 tuple:'t',
                 set:'s',
                }
                
    def packString(self,string):
        return ('S',string.encode('base64'))
        
    def packNumber(self,numb):
        stx = testInt(numb)
        return ('N',stx+'\0'+struct.pack("<"+stx,numb).encode('base64'))
        
    def packConjunct(self,conj):
        stx = self.conjuncts.get(type(conj))
        if not stx:
            raise UnpackableObjectError(str(type(conj)))
        
        index = ""
        data = ""
        for item in conj:
            i,d = self.packObject(item).split('\1')
            index += i
            data += '\0'+d.encode('base64')
            
        return ('C',stx+'\0'+index+'\0'+data.encode('base64'))
        
    def packBool(self,b):
        return ('B',chr(int(b)+65))
        
    def packNone(self,_):
        return ('V','v')
        
    def packObject(self,obj):
        stx = self.symbols.get(type(obj))
        if stx is None:
            raise UnpackableObjectError(str(type(obj)))
                  
        if stx == 'N': data = self.packNumber(obj)
        elif stx == 'S': data = self.packString(obj)
        elif stx == 'C': data = self.packConjunct(obj)
        elif stx == 'D': data = self.packDict(obj)
        elif stx == 'B': data = self.packBool(obj)
        elif stx == 'V': data = self.packNone(obj)
        
        return '\1'.join(data)
        
    def packDict(self,obj):
        its = obj.items()
        keys = self.packObject(map(lambda x:x[0],its))
        values = self.packObject(map(lambda x:x[1],its))
        
        return ('D','\2'.join((keys,values)).encode('base64'))
        
    def unpackObject(self,string):
        stx,data = string.split('\1')
        
        if stx == 'S': return self.unpackString(data)
        elif stx == 'N': return self.unpackNumber(data)
        elif stx == 'C': return self.unpackConjunct(data)
        elif stx == 'D': return self.unpackDict(data)
        elif stx == 'B': return self.unpackBool(data)
        elif stx == 'V': return self.unpackNone(data)
        
    def unpackString(self,data):
        return data.decode('base64')
        
    def unpackNumber(self,data):
        stx,d = data.split('\0')
        return struct.unpack('<'+stx,d.decode('base64'))[0]
        
    def unpackConjunct(self,data):
        stx,index,d = data.split('\0')
        finalType = dict((v,k) for k, v in self.conjuncts.iteritems())[stx]
        
        fr = []
        d = d.decode('base64')
        for x in zip(index,map(lambda x:x.decode('base64'),d.split('\0')[1:])):
            fr.append(self.unpackObject('\1'.join(x)))
            
        return finalType(fr)
        
    def unpackDict(self,obj):
        keys, values = obj.decode('base64').split('\2')
        keysU = self.unpackObject(keys)
        valuesU = self.unpackObject(values)
        
        return dict(zip(keysU,valuesU))
        
    def unpackNone(self,_):
        return None
       
    def unpackBool(self,d):
        return bool(ord(d)-65)
        
globalDg = HouseDatagram()
def packs(obj):
    return zlib.compress(globalDg.packObject(obj)).encode('base64')
    
def unpacks(string):
    return globalDg.unpackObject(zlib.decompress(string.decode('base64')))
    
loads = unpacks
dumps = packs
