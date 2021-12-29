from panda3d.core import *
from CogGlobals import *

class CogHead(NodePath):
    def __init__(self,dept,level):
        self.dept, self.level = dept, level
        
        data = HeadData[dept][level]
        letter,parts = data
        
        path,phase = HeadModelDict[letter]
        path = 'phase_'+str(phase)+path+'heads'
        
        __m = loader.loadModel(path)
        
        NodePath.__init__(self,"cogHead-"+str(dept)+"_"+str(level))
        for part,tex in parts:
            p = __m.find('**/'+part)
            if tex: p.setTexture(loader.loadTexture(self.__findTex(tex)),1)
            p.reparentTo(self)
            
        __m.removeNode()
        
    def __findTex(self,tex):
        phase = "3.5"
        fixes = {"blood-sucker.jpg":"4","double-talker.jpg":"4","robber-baron.jpg":"4",
                 "spin-doctor.jpg":"4","mingler.jpg":"4","name-dropper.jpg":"4",}
        if tex in fixes: phase=fixes[tex]
        path = "phase_"+phase+"/maps/"+tex
        return path