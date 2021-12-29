from tth.cogs import Cog, CogDNA, CogGlobals
from panda3d.core import Point3
for x in render.findAllMatches('**/suit*'): x.removeNode()

import random,math

av = gamebase.curArea.avatar
avPos = av.getPos()

cogs = []

for i in xrange(32):

	dna = CogDNA.CogDNA()
	dna.dept = i//8
	dna.leader = i%8
	dna.isWaiter = random.random() > .5 
	dna.isSkel = random.random() > .7 

	data = dna.make()
	#print data.encode('hex')

	c = Cog.Cog(data)
	c.reparentTo(render)
	
	ang = (360.0/32*i)
	y = 25*math.sin(ang*(math.pi/180))
	x = 25*math.cos(ang*(math.pi/180))
	c.setPos(Point3(x,y,0)+avPos)
	c.lookAt(av)

	anim = random.choice(CogGlobals.BasicAnims)
	c.loop(anim)

	cogs.append(c)