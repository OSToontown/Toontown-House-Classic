def GetDept(n):

        sell = ["coldcaller","telemarketer","namedropper","gladhander","movershaker","twoface","mingler","mrhollywood"]
        cash = ["shortchange","pennypincher","tightwad","beancounter","numbercruncher","moneybags","loanshark","robberbaron"]
        law = ["bottomfeeder","bloodsucker","doubletalker","ambulancechaser","backstabber","spindoctor","legaleagle","bigwig"]
        boss = ["flunky","pencilpusher","yesman","micromanager","downsizer","headhunter","corporateraider","bigcheese"]

        if n in sell: return 3
        if n in cash: return 2
        if n in law:  return 1
        if n in boss: return 0
        return -1
        
BasicAnims = ('walk','neutral','anvil-drop','drop','sidestep-left',
              'sidestep-right','squirt-large','landing','walknreach',
              'rake','hypnotize','soak',"walk","neutral","flailing",
              "lose","pie-small","squirt-small","slip-forward",
              "slip-backward","tug-o-war")

SpecificAnims = (
    #dept 0: boss
    (        (('throw-paper',3.5), ('phone',3.5), ('shredder', 3.5)),        (('pencil-sharpener', 5),('pen-squirt', 5),('hold-eraser', 5),('finger-wag', 5),('hold-pencil', 5)),        (('throw-paper', 5),('golf-club-swing', 5),('magic3', 5),('rubber-stamp', 5),('smile', 5)),        (('speak', 5),('effort', 5),('magic1', 5),('fountain-pen', 5),('finger-wag', 5)),        (('magic1', 5),('magic2', 5),('throw-paper', 5),('magic3', 5)),        (('fountain-pen', 7),('glower', 5),('throw-paper', 5),('magic1', 5),('roll-o-dex', 5)),        (('pickpocket', 5), ('throw-paper', 3.5), ('glower', 5)),        (('cigar-smoke', 8),('glower', 5),('song-and-dance', 8),('golf-club-swing', 5)),    ),
    #dept 1: law
    (
        (('pickpocket', 5),('rubber-stamp', 5),('shredder', 3.5),('watercooler', 5),),
        (('effort', 5),('throw-paper', 5),('throw-object', 5),('magic1', 5),),
        (('rubber-stamp', 5),('throw-paper', 5),('speak', 5),('fingerwag', 5),('throw-paper', 5),),
        (('throw-object', 5),('roll-o-dex', 5),('stomp', 5),('phone', 5),('throw-paper', 5),),
        (('magic1', 5),('throw-paper', 5),('fingerwag', 5),),
        (('magic2', 5),('jump', 6),('stomp', 5),('magic3', 5),('hold-pencil', 5),('throw-paper', 5),),
        (('speak', 5),('throw-object', 5),('glower', 5),('throw-paper', 5),),
        (('fingerwag', 5),('cigar-smoke', 8),('gavel', 8),('magic1', 5),('throw-object', 5),('throw-paper', 5),),
    ),
    #dept 2: cash
    (        (('throw-paper', 3.5),('watercooler', 5),('pickpocket', 5),),        (('throw-paper', 5),('glower', 5),('fingerwag', 5),),        (('throw-paper', 3.5),('glower', 5),('magic2', 5),('finger-wag', 5),),        (('phone', 5),('hold-pencil', 5),),        (('phone', 5),('throw-object', 5),),        (('magic1', 5),('throw-paper', 3.5),),        (('throw-paper', 5),('throw-object', 5),('hold-pencil', 5),),        (('glower', 5),('magic1', 5),('golf-club-swing', 5),),    ),
    #dept 3: sell        (
        (('speak', 5),('glower', 5),('phone', 3.5),('finger-wag', 5)),
        (('speak', 5),('throw-paper', 5),('pickpocket', 5),('roll-o-dex', 5),('finger-wag', 5),),
        (('pickpocket', 5),('roll-o-dex', 5),('magic3', 5),('smile', 5),),
        (('speak', 5),('fountain-pen', 5),('rubber-stamp', 5),),
        (('effort', 5),('throw-paper', 5),('stomp', 5),('jump', 6),),
        (('phone', 5),('smile', 5),('throw-object', 5),('glower', 5),),
        (('speak', 5),('magic2', 5),('magic1', 5),('golf-club-swing', 5),),
        (('magic1', 5),('smile', 5),('golf-club-swing', 5),('song-and-dance', 5),),
    ),)

ModelDict = {'a': ('/models/char/suitA-', 4),
             'b': ('/models/char/suitB-', 4),
             'c': ('/models/char/suitC-', 3.5)}
     
HeadModelDict = {'a': ('/models/char/suitA-', 4),
                 'b': ('/models/char/suitB-', 4),
                 'c': ('/models/char/suitC-', 3.5)}

HeadData = (  
	(
		('c', [('flunky', None),('glasses',None)]),
		('b', [('pencilpusher', None)]),
		('a', [('yesman', None)]),
		('c', [('micromanager', None)]),
		('b', [('beancounter', None)]),
		('a', [('headhunter', None)]),
		('c', [('flunky', 'corporate-raider.jpg')]),
		('a', [('bigcheese', None)]),
	),
	(
		('c', [('flunky', 'bottom-feeder.jpg')]),
		('b', [('movershaker', 'blood-sucker.jpg')]),
		('a', [('twoface', 'double-talker.jpg')]),
		('b', [('ambulancechaser', None)]),
		('a', [('backstabber', None)]),
		('b', [('telemarketer', 'spin-doctor.jpg')]),
		('a', [('legaleagle', None)]),
		('a', [('bigwig', None)]),
	),
    (
		('c', [('coldcaller', None)]),
		('a', [('pennypincher', None)]),
		('c', [('tightwad', None)]),
		('b', [('beancounter', None)]),
		('a', [('numbercruncher', None)]),
		('c', [('moneybags', None)]),
		('b', [('loanshark', None)]),
		('a', [('yesman', 'robber-baron.jpg')]),
	),
	(
		('c', [('coldcaller', None)]),
		('b', [('telemarketer', None)]),
		('a', [('numbercruncher', 'name-dropper.jpg')]),
		('a', [('yesman', None)]),
		('b', [('movershaker', None)]),
		('a', [('twoface', None)]),
		('a', [('twoface', 'mingler.jpg')]),
		('a', [('yesman', None)]),
	)
)

def getBodyType(dept, index):
    return (('c','b','a','c','b','a','c','a'),('c','b','a','b','a','b','a','a'),('c','a','c','b','a','c','b','a'),('c','b','a','c','b','a','a','a'))[dept][index]
    
def getHeadColor(dept, index):
    if dept == 3 and index == 0:
        return (0.25, 0.35, 1.0, 1.0)
        
def getHandColor(dept, index):
    c = ((0.95, 0.75, 0.75, 1.0),(0.75, 0.75, 0.95, 1.0),(0.65, 0.95, 0.85, 1.0),(0.95, 0.75, 0.95, 1.0))[dept]
    
    if dept == 0:
        if index == 6: c = (0.85, 0.55, 0.55, 1.0)
        elif index == 7: c = (0.75, 0.95, 0.75, 1.0)
        
    elif dept == 1:
        if index == 1: c = (0.95, 0.95, 1.0, 1.0)
        elif index == 5: c = (0.5, 0.8, 0.75, 1.0)
        elif index == 6: c = (0.25, 0.25, 0.5, 1.0)
        
    elif dept == 2:
        if index == 1: c = (1.0, 0.5, 0.6, 1.0)
    
    elif dept == 3:
        if index == 0: c = (0.55, 0.65, 1.0, 1.0)
        
    return c
    
ScalesAndHeights = (
                    ((0.97, 4.88), (0.63, 5.0), (0.68, 5.28), (0.6, 3.25), (0.85, 6.08), (1.07, 7.45), (1.63, 8.23), (1.16, 9.34)),
                    ((0.97, 4.81), (0.83, 6.17), (0.7, 5.63), (0.82, 6.39), (0.74, 6.71), (1.07, 7.9), (1.18, 8.27), (1.16, 8.69)),
                    ((0.87, 4.77), (0.59, 5.26), (1.09, 5.41), (0.83, 5.95), (0.87, 7.22), (1.28, 6.97), (1.23, 8.58), (1.16, 8.95)),
                    ((0.85, 4.63), (0.71, 5.24), (0.72, 5.98), (1.15, 6.4), (0.9, 6.7), (0.87, 6.95), (0.95, 7.61), (1.16, 8.95))
                   )
                   
def getHpByLevel(l):
    if l == 12: return 200
    return l**2+3*l+2
    
def getMedallionColor(dept,index):
    c = ((0.863, 0.776, 0.769, 1.0),(0.843, 0.745, 0.745, 1.0),(0.749, 0.776, 0.824, 1.0),(0.749, 0.769, 0.749, 1.0))[dept]
    
    return c