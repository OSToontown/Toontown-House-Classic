from BookPage import *
from tth.fishing.Fish import *

PageMode_Bucket = 1
PageMode_History = 2
PageMode_Trophies = 3

class FishingPage(BookPage):
    def __init__(self, book):
        BookPage.__init__(self,book)
        self.activeTab = 0
        self.progressTitle = None
        
    def setup(self):
        gui = loader.loadModel("phase_3.5/models/gui/fishingBook")
        self.frame = DirectFrame(parent=self.frame, relief=None)
        self.buck = DirectFrame(parent=self.frame, geom=gui.find('**/bucket'), relief=None, scale=.035, pos=(0,0,0.05))
        self.tabs = []
        #self.pageFrame = DirectFrame(parent=self.frame, relief=None)
        self.buck.ls()