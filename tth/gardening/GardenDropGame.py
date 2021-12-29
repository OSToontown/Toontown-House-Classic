import math
from math import pi
from direct.distributed.ClockDelta import *
from tth.gardening.GameSprite import GameSprite
from tth.gardening.GardenProgressMeter import GardenProgressMeter
 
class GardenDropGame:
 
    def __init__(self):
        self.levelNumber = 1
        self.inHelp = False
        self.acceptErrorDialog = 0
        self.doneEvent = 'game Done'
        self.sprites = []
        self.playGardenDrop()
        self.colorRed = (1, 0, 0, 1)
        self.colorBlue = (0, 0, 1, 1)
        self.colorGreen = (0, 1, 0, 1)
        self.colorGhostRed = (1, 0, 0, 0.5)
        self.colorGhostBlue = (0, 0, 1, 0.5)
        self.colorGhostGreen = (0, 1, 0, 0.5)
        self.colorWhite = (1, 1, 1, 1)
        self.colorBlack = (0.5, 0.5, 0.5, 1.0)
        self.colorShadow = (0, 0, 0, 0.5)
        self.lastTime = []
        self.running = 0
        self.massCount = 0
        self.foundCount = 0
        self.maxX = 0.46999999999999997
        self.minX = -0.46999999999999997
        self.maxZ = 0.75000000000000002
        self.minZ = -0.00000000000000001
        self.newBallX = 0.0
        self.newBallZ = 0.69999999999999998
        self.rangeX = (self.maxX - self.minX)
        self.rangeZ = (self.maxZ - self.minZ)
        size = 0.085000000000000006
        sizeZ = (size * 0.80000000000000004)
        gX = int((self.rangeX / size))
        gZ = int((self.rangeZ / sizeZ))
        self.maxX = (self.minX + (gX * size))
        self.maxZ = (self.minZ + (gZ * sizeZ))
        self.controlOffsetX = 0.0
        self.controlOffsetZ = 0.0
        self.queExtent = 3
        print ('Grid Dimensions X%s Z%s' % (gX,
         gZ))
        self.grid = []
        self.gridDimX = gX
        self.gridDimZ = gZ
        self.gridBrick = False
 
        base.gardenGame = self
 
        self.controlSprite = None
        self.matchList = []
        self.newBallTime = 1.0
        self.newBallCountUp = 0.0
        self.cogX = 0
        self.cogZ = 0
 
        return None
 
    def __init2__(self):
        self.acceptErrorDialog = 0
        self.doneEvent = 'game Done'
        self.sprites = []
        self.lastTime = []
        self.running = 0
        self.massCount = 0
        self.foundCount = 0
        self.maxX = 0.46999999999999997
        self.minX = -0.46999999999999997
        self.maxZ = 0.65000000000000002
        self.minZ = -0.00000000000000001
        self.newBallX = 0.0
        self.newBallZ = 0.69999999999999998
        self.rangeX = (self.maxX - self.minX)
        self.rangeZ = (self.maxZ - self.minZ)
        size = 0.085000000000000006
        sizeZ = (size * 0.80000000000000004)
        gX = int((self.rangeX / size))
        gZ = int((self.rangeZ / sizeZ))
        self.maxX = (self.minX + (gX * size))
        self.maxZ = (self.minZ + (gZ * sizeZ))
        self.controlOffsetX = 0.0
        self.controlOffsetZ = 0.0
        self.queExtent = 3
        print ('Grid Dimensions X%s Z%s' % (gX,
         gZ))
        self.grid = []
        self.gridDimX = gX
        self.gridDimZ = gZ
        self.gridBrick = False
 
        base.gardenGame = self
 
        self.controlSprite = None
        self.matchList = []
        self.newBallTime = 1.0
        self.newBallCountUp = 0.0
        self.cogX = 0
        self.cogZ = 0
 
        return None
 
    def load(self):
        model = loader.loadModel('phase_5.5/models/gui/package_delivery_panel.bam')
        model1 = loader.loadModel('phase_3.5/models/gui/matching_game_gui.bam')
 
        self.model = model
        self.model1 = model1
 
        background = model.find('**/bg')
        itemBoard = model.find('**/item_board')
 
        self.frame = DirectFrame(scale=1.1000000000000001, relief=DGG.FLAT, frameSize=(-0.5,
         0.5,
         -0.45000000000000001,
         -0.050000000000000003), frameColor=(0.73699999999999999, 0.57299999999999995, 0.34499999999999997, 1.0))
 
        self.background = DirectFrame(self.frame, image=background, image_scale=0.050000000000000003, relief=None, pos=(0, 1, 0))
        self.itemBoard = DirectFrame(parent=self.frame, image=itemBoard, image_scale=0.050000000000000003, image_color=(0.92200000000000004, 0.92200000000000004, 0.753, 1), relief=None, pos=(0, 1, 0))
        gui2 = loader.loadModel('phase_3/models/gui/quit_button.bam')
 
        self.font = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        self.gardenDropText = OnscreenText(parent=self.frame, text="Garden Drop",scale=(0.17,0.17,0.17), font=self.font, pos=(0,0.685,0), fg=(1,1,1,1))
 
        self.quitButton = DirectButton(parent=self.frame, relief=None, image=(gui2.find('**/QuitBtn_UP'),
         gui2.find('**/QuitBtn_DN'),
         gui2.find('**/QuitBtn_RLVR')), pos=(0.5,
         1.0,
         -0.41999999999999998), scale=0.90000000000000002, text='Exit Mini Game', text_font=self.font, text0_fg=(1, 1, 1, 1), text1_fg=(1, 1, 1, 1), text2_fg=(1, 1, 1, 1), text_scale=0.044999999999999998, text_pos=(0,
         -0.01), command=self._GardenDropGame__handleExit)
 
        if self.level == 1:
            self.helpButton = DirectButton(parent=self.frame, relief=None, image=(gui2.find('**/QuitBtn_UP'),
             gui2.find('**/QuitBtn_DN'),
             gui2.find('**/QuitBtn_RLVR')), pos=(-0.5,
             1.0,
             -0.41999999999999998), scale=0.90000000000000002, text='How To Play', text_font=self.font, text0_fg=(1, 1, 1, 1), text1_fg=(1, 1, 1, 1), text2_fg=(1, 1, 1, 1), text_scale=0.044999999999999998, text_pos=(0,
             -0.01), command=self._GardenDropGame__openHelp)
 
    def help(self):
        self.inHelp = True
        helpMessage = 'How To Play:'
        helpMessage2 = "Match the ghost balls with the normal balls! But beware of the cog ball, it will try to block you off!"
 
        frameGui = loader.loadModel('phase_3/models/gui/dialog_box_gui.bam')
        self.helpFrame = DirectFrame(scale=1.1, relief=None, image=frameGui, image_scale=(1.75, 1, 0.75), image_color=(1,1,1,1), frameSize=(-0.5,
         0.5,
         -0.45,
         -0.05))#GardenDropGame.help()
 
        self.font = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        self.helpText = DirectLabel(scale=1.1, relief=None, text_pos=(0, 0.2), text_wordwrap=16, text=helpMessage, text_font=self.font, pos=(0.0, 0.0, 0.0), text_scale=0.1, text0_fg=(1, 1, 1, 1), parent=self.helpFrame)
 
        self.font2 = loader.loadFont("phase_3/models/fonts/Comedy.bam")
        self.helpText2 = DirectLabel(scale=1.1, relief=None, text_pos=(-0.6, 0.1), text_wordwrap=15, text=helpMessage2, text_font=self.font2, pos=(0.0, 0.0, 0.0), text_scale=0.085, text0_fg=(0, 0, 0, 1), parent=self.helpFrame, text_align=TextNode.ALeft)
 
        gui2 = loader.loadModel('phase_3/models/gui/quit_button.bam')
        self.backButton = DirectButton(parent=self.helpFrame, relief=None, image=(gui2.find('**/QuitBtn_UP'), gui2.find('**/QuitBtn_DN'), gui2.find('**/QuitBtn_RLVR')), pos=(0.5, 1.0, -0.32), scale=0.9, text='Back to Game', text_font=self.font, text0_fg=(1, 1, 1, 1), text1_fg=(1, 1, 1, 1), text2_fg=(1, 1, 1, 1), text_scale=0.045, text_pos=(0, -0.01), command=self.__handlePlay)
 
        return True
 
    def addSprite(self, image, size = 0.5, posX = 0, posZ = 0, found = 0):
        nodeObj = DirectLabel(parent=self.frame, relief=None, image=image, pos=(posX, 0.0, posZ), scale=size, image_color=(1.0, 1.0, 1.0, 1))
        if self.levelNumber == 1 or self.levelNumber == 2:
            colorChoice = random.choice(range(0, 3))
        if self.levelNumber == 3 or self.levelNumber == 4:
            colorChoice = random.choice(range(0, 4))
        if self.levelNumber == 5:
            colorChoice = random.choice(range(0, 5))
 
        newSprite = GameSprite(nodeObj, colorChoice, found)
        self.sprites.append(newSprite)
 
        if found:
            self.foundCount += 1
 
        return newSprite
 
    def addUnSprite(self, image, size = 0.5, posX = 0, posZ = 0):
        nodeObj = DirectLabel(parent=self.frame, relief=None, image=image, pos=(posX, 0.0, posZ), scale=size, image_color=(1.0, 1.0, 1.0, 1))
 
        newSprite = GameSprite(nodeObj)
        newSprite = GameSprite(nodeObj)
 
        return newSprite
 
    def testPointDistanceSquare(self, x1, z1, x2, z2):
        distX = x1 - x2
        distZ = z1 - z2
        distC = distX * distX + distZ * distZ
 
        if distC == 0:
            distC = 1e-10
 
        return distC

    def testDistance(self, nodeA, nodeB):
        distX = nodeA.getX() - nodeB.getX()
        distZ = nodeA.getZ() - nodeB.getZ()
        distC = distX * distX + distZ * distZ
        dist = math.sqrt(distC)
 
        return dist
 
    def testGridfull(self, cell):
        if not cell:
            return 0
 
        elif cell[0] != None:
            return 1
 
        else:
            return 0
 
        returnTrue

    def getValidGrid(self, x, z):
        if x < 0 or x >= self.gridDimX:
            return None
 
        elif z < 0 or z >= self.gridDimZ:
            return None
 
        else:
            return self.grid[x][z]
 
        return None

    def getColorType(self, x, z):
        if x < 0 or x >= self.gridDimX:
            return -1
 
        elif z < 0 or z >= self.gridDimZ:
            return -1
 
        elif self.grid[x][z][0] == None:
            return -1
 
        else:
            return self.grid[x][z][0].colorType
 
        return True
 
    def getSprite(self, spriteIndex):
        if spriteIndex >= len(self.sprites) or self.sprites[spriteIndex].markedForDeath:
            return None
 
        else:
            return self.sprites[spriteIndex]
 
        return None
 
    def findGrid(self, x, z, force = 0):
        currentClosest = None
        currentDist = 10000000
 
        for countX in range(self.gridDimX):
            for countZ in range(self.gridDimZ):
                testDist = self.testPointDistanceSquare(x, z, self.grid[countX][countZ][1], self.grid[countX][countZ][2])
                if self.grid[countX][countZ][0] == None and testDist < currentDist and (force or self.hasNeighbor(countX, countZ)):
                    currentClosest = self.grid[countX][countZ]
                    self.closestX = countX
                    self.closestZ = countZ
                    currentDist = testDist

        return currentClosest
 
    def findGridCog(self):
        self.cogX = 0
        self.cogZ = 0
        self.massCount = 0
 
        for row in self.grid:
            for cell in row:
                if cell[0] != None:
                    self.cogX += cell[1]
                    self.cogZ += cell[2]
                    self.massCount += 1

        if self.massCount > 0:
            self.cogX = (self.cogX / self.massCount)
            self.cogZ = (self.cogZ / self.massCount)
            self.cogSprite.setX(self.cogX)
            self.cogSprite.setZ(self.cogZ)
        else:
            self.doOnClearGrid()
 
        return True
 
    def stickInGrid(self, sprite, force = 0):
        if sprite.isActive and not sprite.isQue:
            gridCell = self.findGrid(sprite.getX(), sprite.getZ(), force)
 
            if gridCell:
                gridCell[0] = sprite
                sprite.setActive(0)
                sprite.setX(gridCell[1])
                sprite.setZ(gridCell[2])
                self.createMatchList(self.closestX, self.closestZ)
 
                if len(self.matchList) >= 3:
                    self.clearMatchList()
                self.findGridCog()
 
    def fillMatchList(self, cellX, cellZ):
        if (cellX, cellZ) in self.matchList:
            return True
 
        self.matchList.append((cellX, cellZ))
        colorType = self.grid[cellX][cellZ][0].colorType
 
        if cellZ % 2 == 0:
            if self.getColorType(cellX - 1, cellZ) == colorType:
                self.fillMatchList(cellX - 1, cellZ)

            if self.getColorType(cellX + 1, cellZ) == colorType:
                self.fillMatchList(cellX + 1, cellZ)
 
            if self.getColorType(cellX, cellZ + 1) == colorType:
                self.fillMatchList(cellX, cellZ + 1)
 
            if self.getColorType(cellX + 1, cellZ + 1) == colorType:
                self.fillMatchList(cellX + 1, cellZ + 1)
 
            if self.getColorType(cellX, cellZ - 1) == colorType:
                self.fillMatchList(cellX, cellZ - 1)
 
            if self.getColorType(cellX + 1, cellZ - 1) == colorType:
                self.fillMatchList(cellX + 1, cellZ - 1)
 
        else:
            if self.getColorType(cellX - 1, cellZ) == colorType:
                self.fillMatchList(cellX - 1, cellZ)
 
            if self.getColorType(cellX + 1, cellZ) == colorType:
                self.fillMatchList(cellX + 1, cellZ)
 
            if self.getColorType(cellX, cellZ + 1) == colorType:
                self.fillMatchList(cellX, cellZ + 1)
 
            if self.getColorType(cellX - 1, cellZ + 1) == colorType:
                self.fillMatchList(cellX - 1, cellZ + 1)
 
            if self.getColorType(cellX, cellZ - 1) == colorType:
                self.fillMatchList(cellX, cellZ - 1)
 
            if self.getColorType(cellX - 1, cellZ - 1) == colorType:
                self.fillMatchList(cellX - 1, cellZ - 1)
 
    def createMatchList(self, x, z):
        self.matchList = []
        self.fillMatchList(x, z)
 
    def clearMatchList(self):
        for entry in self.matchList:
            gridEntry = self.grid[entry[0]][entry[1]]
            sprite = gridEntry[0]
            gridEntry[0] = None
            sprite.markedForDeath = 1

        return True
 
    def hasNeighbor(self, cellX, cellZ):
        gotNeighbor = 0
 
        if cellZ % 2 == 0:
            if self.testGridfull(self.getValidGrid(cellX - 1, cellZ)):
                gotNeighbor = 1
 
            elif self.testGridfull(self.getValidGrid(cellX + 1, cellZ)):
                gotNeighbor = 1
 
            elif self.testGridfull(self.getValidGrid(cellX, cellZ + 1)):
                gotNeighbor = 1
 
            elif self.testGridfull(self.getValidGrid(cellX + 1, cellZ + 1)):
                gotNeighbor = 1
 
            elif self.testGridfull(self.getValidGrid(cellX, cellZ - 1)):
                gotNeighbor = 1
 
            elif self.testGridfull(self.getValidGrid(cellX + 1, cellZ - 1)):
                gotNeighbor = 1
 
        elif self.testGridfull(self.getValidGrid(cellX - 1, cellZ)):
            gotNeighbor = 1
 
        elif self.testGridfull(self.getValidGrid(cellX + 1, cellZ)):
            gotNeighbor = 1
 
        elif self.testGridfull(self.getValidGrid(cellX, cellZ + 1)):
            gotNeighbor = 1
 
        elif self.testGridfull(self.getValidGrid(cellX - 1, cellZ + 1)):
            gotNeighbor = 1
 
        elif self.testGridfull(self.getValidGrid(cellX, cellZ - 1)):
            gotNeighbor = 1
 
        elif self.testGridfull(self.getValidGrid(cellX - 1, cellZ - 1)):
            gotNeighbor = 1
 
        return gotNeighbor
 
    def __colTest(self):
        if not hasattr(self, 'tick'):
            self.tick = 0
 
        self.tick += 1
 
        if self.tick > 5:
            self.tick = 0
        sizeSprites = len(self.sprites)
 
        for movingSpriteIndex in range(len(self.sprites)):
            for testSpriteIndex in range(movingSpriteIndex, len(self.sprites)):
                movingSprite = self.getSprite(movingSpriteIndex)
                testSprite = self.getSprite(testSpriteIndex)
 
                if testSprite and movingSprite:
                    if movingSpriteIndex != testSpriteIndex and (movingSprite.isActive or testSprite.isActive):
                        if movingSprite.isQue or testSprite.isQue:
                            if self.testDistance(movingSprite.nodeObj, testSprite.nodeObj) < self.queExtent * (movingSprite.size + testSprite.size):
                                self.push(movingSprite, testSprite)
 
                        elif self.testDistance(movingSprite.nodeObj, testSprite.nodeObj) < movingSprite.size + testSprite.size:
                            if movingSprite.isActive:
                                testSprite.isActive or self.__collide(movingSprite, testSprite)
 
                        if self.testDistance(self.cogSprite.nodeObj, testSprite.nodeObj) < (self.cogSprite.size + testSprite.size):
                            if movingSprite.isActive:
                                self.stickInGrid(testSprite, 1)
 
                        if self.tick == 5:
                            pass
 
    def __collide(self, move, test):
        queHit = 0
 
        if move.isQue:
            que = move
            hit = test
            queHit = 1
 
        elif test.isQue:
            que = test
            hit = move
            queHit = 1
 
        else:
            test.velX = 0
            test.velZ = 0
            move.velX = 0
            move.velZ = 0
            test.collide()
            move.collide()
            self.stickInGrid(move,1)
            self.stickInGrid(test,1)
 
        if queHit:
            forceM = 0.1
            distX = que.getX() - hit.getX()
            distZ = que.getZ() - hit.getZ()
            self.stickInGrid(move,1)
            self.stickInGrid(test,1)

    def push(self, move, test):
        queHit = 0
 
        if move.isQue:
            que = move
            hit = test
            queHit = 1
 
        elif test.isQue:
            que = test
            hit = move
            queHit = 1
 
        if queHit:
            forceM = 0.1
            dist = self.testDistance(move.nodeObj, test.nodeObj)
 
            if abs(dist) < self.queExtent * que.size and abs(dist) > 0:
                scaleSize = self.queExtent * que.size * 0.5
                distFromPara = abs(abs(dist) - scaleSize)
                force = (scaleSize - distFromPara) / scaleSize * (dist / abs(dist))
                angle = self.angleTwoSprites(que, hit)
 
                if angle < 0:
                    angle = angle + 2 * pi
 
                if angle > pi * 2.0:
                    angle = angle - 2 * pi
 
                newAngle = pi * 1.0
 
                if angle > pi * 1.5 or angle < pi * 0.5:
                    newAngle = pi * 0.0
 
                hit.addForce(forceM * force, newAngle)
 
    def angleTwoSprites(self, sprite1, sprite2):
        x1 = sprite1.getX()
        z1 = sprite1.getZ()
        x2 = sprite2.getX()
        z2 = sprite2.getZ()
        x = x2 - x1
        z = z2 - z1
        angle = math.atan2(-x, z)
 
        return angle + pi * 0.5
 
    def doOnClearGrid(self):
        secondSprite = self.addSprite(self.block, posX=self.newBallX, posZ=0.0, found=1)
        secondSprite.addForce(0, 1.55 * pi)
        self.stickInGrid(secondSprite, 1)
 
    def __run(self, cont = 1):
        if self.lastTime == None:
             self.lastTime = globalClock.getRealTime()
 
        timeDelta = 0.025
        self.lastTime = globalClock.getRealTime()
        self.newBallCountUp += timeDelta
 
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
            self.queBall.setX(x)
            self.queBall.setZ(y)
 
        for sprite in self.sprites:
            sprite.run(timeDelta)
            if sprite.getX() > self.maxX:
                sprite.setX(self.maxX)
                sprite.velX = -sprite.velX
 
            if sprite.getX() < self.minX:
                sprite.setX(self.minX)
                sprite.velX = -sprite.velX
 
            if sprite.getZ() > self.maxZ:
                sprite.setZ(self.maxZ)
                sprite.velZ = -sprite.velZ
 
            if sprite.getZ() < self.minZ:
                self.stickInGrid(sprite, 1)
 
            if sprite.isActive:
                sprite.addForce(timeDelta * 0.9, pi * 1.5)

        self.queBall.velX = (self.queBall.getX() - self.queBall.prevX) / timeDelta
        self.queBall.velZ = (self.queBall.getZ() - self.queBall.prevZ) / timeDelta
        self.__colTest()
 
        for sprite in self.sprites:
            if sprite.markedForDeath:
                if sprite.foundation:
                    self.foundCount -= 1
 
                self.sprites.remove(sprite)
                sprite.delete()
 
        if self.controlSprite == None:
            self.addControlSprite(self.newBallX, self.newBallZ)
            self.newBallCountUp = 0.0
 
        if self.newBallCountUp >= self.newBallTime:
            self.addControlSprite(self.newBallX, self.newBallZ)
            self.newBallCountUp = 0.0
 
        if not self.controlSprite.isActive:
            self.controlSprite = None
 
        if self.foundCount <= 0:
            self.__handleWin()
 
        return Task.cont
 
    def loadStartingSprites(self, levelNum):
        self.queBall = self.addSprite(self.block, posX=0.25, posZ=0.5, found=0)
        self.queBall.setColor(self.colorWhite)
        self.queBall.isQue = 1
 
        self.controlSprite = None
        self.cogSprite = self.addUnSprite(self.block, posX=0.25, posZ=0.5)
        self.cogSprite.setColor(self.colorBlack)
 
        for ball in range(0, levelNum):
            place = random.random() * self.rangeX
            self.newSprite = self.addSprite(self.block, size=0.5, posX=self.minX + place, posZ=0.0, found=1)
            self.stickInGrid(self.newSprite, 1)
 
    def __handlePlay(self):
        self.__init2__()
        self.load()
 
        self.itemboard = self.model.find('**/item_board')
        self.block = self.model1.find('**/minnieCircle')
 
        size = 0.085
        sizeZ = size * 0.8
 
        for countX in range(self.gridDimX):
            newRow = []
            for countZ in range(self.gridDimZ):
                offset = 0
                if countZ % 2 == 0:
                    offset = size / 2
                newRow.append([None, countX * size + self.minX + offset, countZ * sizeZ + self.minZ])

            self.grid.append(newRow)
 
        if self.levelNumber == 1:
            self.loadStartingSprites(3)
        elif self.levelNumber == 2:
            self.loadStartingSprites(5)
        elif self.levelNumber == 3:
            self.loadStartingSprites(7)
        elif self.levelNumber == 4:
            self.loadStartingSprites(10)
        elif self.levelNumber == 5:
            self.loadStartingSprites(15)
        base.taskMgr.add(self._GardenDropGame__run,"MouseCheck")
 
        if hasattr(GardenProgressMeter, 'frame'):
            return GardenProgressMeter.frame.removeNode()
 
        if self.inHelp == True:
            self.helpFrame.removeNode()
            self.inHelp = False
            if hasattr(self, 'GardenGameButton'):
                self.GardenGameButton.removeNode()
        else:
            self.GardenGameButton.removeNode()
 
    def addControlSprite(self, x = 0.0, z = 0.0):
        newSprite = self.addSprite(self.block, posX=x, posZ=z)
        self.controlSprite = newSprite
 
    def playGardenDrop(self):
        self.GDButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
        self.font = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        self.yellowButton = (self.GDButtonImage.find('**/QuitBtn_UP'), self.GDButtonImage.find('**/QuitBtn_DN'), self.GDButtonImage.find('**/QuitBtn_RLVR'))
 
        self.GardenGameButton = DirectButton(frameSize=(0), text="Garden\nDrop", image=self.yellowButton, text_pos=(0,0.01), relief=None, text_fg=(1, 1, 1, 1), \
        geom=None, pad=(0.01, 0.01), suppressKeys=0, command=self.__handlePlay, pos=(-.62,0,-.89), text_font=self.font, text_scale=(0.083,0.040,0.049), borderWidth=(0.13, 0.01), scale=(0.8,1,1.8))
 
    def __openHelp(self):
        self.unload()
        self.help()
        base.taskMgr.remove('MouseCheck')
 
    def unload(self):
        self.frame.destroy()
        del self.frame
 
        if (self.acceptErrorDialog and self.acceptErrorDialog.cleanup()):
            self.acceptErrorDialog = 1
 
    def __handleExit(self):
        self._GardenDropGame__acceptExit()
 
    def __acceptExit(self, buttonValue = None):
        self.playGardenDrop()
        if (hasattr(self, 'frame') and self.frame.hide()):
            self.unload()
            messenger.send(self.doneEvent)
 
        self.levelNumber = 1
        base.taskMgr.remove('MouseCheck')
 
    def __handleWin(self):
        self.unload()
        GardenProgressMeter.load()
        self.levelNumber += 1
        base.taskMgr.remove('MouseCheck')