class EstatePlane:
 
    def loop(self):
        self.airplane = None
        self.theta = 0
        self.phi = 0
        self.loadAirplane()
        self.__startAirplaneTask()
 
    def loadAirplane(self):
        self.font = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        self.airplane = loader.loadModel('phase_4/models/props/airplane.bam')
        self.airplane.reparentTo(self.np)
        self.airplane.setScale(4)
        self.airplane.setPos(0, 0, 1)
        self.banner = self.airplane.find('**/*banner')
        bannerText = TextNode('bannerText')
        bannerText.setTextColor(1, 0, 0, 1)
        bannerText.setAlign(bannerText.ACenter)
        bannerText.setFont(self.font)
        bannerText.setText('I\'m back!!!')
        self.bn = self.banner.attachNewNode(bannerText.generate())
        self.bn.setHpr(180, 0, 0)
        self.bn.setPos(-5.8, 0.1, -0.25)
        self.bn.setScale(0.95)
 
    def __startAirplaneTask(self):
        self.theta = 0
        self.phi = 0
        taskMgr.remove('estate-airplane')
        taskMgr.add(self.airplaneFlyTask, 'estate-airplane')

    def __pauseAirplaneTask(self):
        pause = 45
        self.phi = 0
        self.theta = (self.theta + 10) % 360
        taskMgr.remove('estate-airplane')
        taskMgr.doMethodLater(pause, self.airplaneFlyTask, 'estate-airplane')

    def __killAirplaneTask(self):
        taskMgr.remove('estate-airplane')

    def airplaneFlyTask(self, task):
        rad = 300.0
        amp = 80.0
        self.theta += 0.25
        self.phi += 0.005
        sinPhi = math.sin(self.phi)
        if sinPhi <= 0:
            self.__pauseAirplaneTask()
        angle = math.pi * self.theta / 180.0
        x = rad * math.cos(angle)
        y = rad * math.sin(angle)
        z = amp * sinPhi
        self.airplane.reparentTo(render)
        self.airplane.setH(90 + self.theta)
        self.airplane.setPos(x, y, z)
        return Task.cont