import random

ShadowSpeed = 3.0
ShadowMoveTime = (7,20)
MinShadowDelta = 2.5

DOCK_Z = 1.9 #1.73
__targetInfoDict = {
                    #ttc
                    1000:(2,-81,31,-4.8,14,-1.4),
                    1100:(2,20,-664,-1.4,14,-1.4-0.438),
                    1200:(2,-234,175,-1.4,14,-1.4-0.462),
                    1300:(2,529,-70,-1.4,13,-1.4-0.486),
                    
                    #docks
                    2000:(2,-17,130,DOCK_Z,15,1.73-3.615),
                    2100:(2,381,-350,-2,14,-2-0.482),
                    2200:(2,-395,-226,-2,14,-2-0.482),
                    2300:(2,350,100,-2,14,-2-0.482),
                    
                    #garden
                    3000:(2,50,47,-1.48,13,-1.48-0.345),
                    3100:(2,149,44,-1.43,13,-1.43-0.618),
                    3200:(2,176,100,-1.43,13,-1.43-0.618),
                    3300:(2,134,-70.5,-1.5,13,-1.5-0.377),
                    
                    #mml
                    4000:(2,-0.2,-20.2,-14.65,14,-14.65--12),
                    4100:(2,-580,-90,-0.87,14,-0.87-1.844),
                    4200:(2,-214,250,-0.87,14,-0.87-1.844),
                    4300:(2,715,-15,-0.87,14,-0.87-1.844),
                    
                    #brrgh
                    5000:(2,-58,-26,1.7,10,-0.8),
                    5100:(2,460,29,-2,13,-2-0.4),
                    5200:(2,340,480,-2,13,-2-0.4),
                    5300:(2,45.5,90.86,-2,13,-2-0.4),
                    
                    #dreamland
                    6000:(2,159,0.2,-17.1,14,-17.1--14.6),
                    6100:(2,118,-185,-2.1,14,-2.1-0.378),
                    6200:(2,241,-348,-2.1,14,-2.1-0.378),
                    
                    "estate":(3,30,-126,-0.3,16,-0.83)
                    }
                    
def getNumTargets(zone):
    info = __targetInfoDict.get(zone)
    if info:
        return info[0]
    else:
        return 2


def getTargetCenter(zone):
    info = __targetInfoDict.get(zone)
    if info:
        return info[1:4]
    else:
        return (0, 0, 0)


def getTargetRadius(zone):
    info = __targetInfoDict.get(zone)
    if info:
        return info[4]
    else:
        return 10

def getWaterLevel(zone):
    info = __targetInfoDict.get(zone)
    if info:
        return info[5]
    else:
        return 0
        
FishMask = 4

RodFileDict = {0: 'phase_4/models/props/pole_treebranch-mod',
 1: 'phase_4/models/props/pole_bamboo-mod',
 2: 'phase_4/models/props/pole_wood-mod',
 3: 'phase_4/models/props/pole_steel-mod',
 4: 'phase_4/models/props/pole_gold-mod'}
 
Species = {}

FishAudioFileDict = {
                     0: ('Clownfish.mp3',1,1.5,1.0),
                     1:('BalloonFish.mp3',1,0,1.23),
                     2:('CatFish.mp3',1,0,1.26),
                     3:('DevilRay.mp3',0,0,1.0),
                     4:('Frozen_Fish.mp3',1,0,1.0),
                     5:('Starfish.mp3',0,0,1.25),
                     6:('Holy_Mackerel.mp3',1,0.9,1.0),
                     7:('Dog_Fish.mp3',1,0,1.25),
                     8:('AmoreEel.mp3',1,0,1.0),
                     9:('Nurse_Shark.mp3',0,0,1.0),
                     10:('King_Crab.mp3',0,0,1.0),
                     11:('Moon_Fish.mp3',0,1.0,1.0),
                     12:('Seahorse.mp3',1,0,1.26),
                     13:('Pool_Shark.mp3',1,2.0,1.0),
                     14:('Bear_Acuda.mp3',1,0,1.0),
                     15:('CutThroatTrout.mp3',1,0,1.0),
                     16:('Piano_Tuna.mp3',0,0,1.0),
                     17:('PBJ_Fish.mp3',1,0,1.25),
                    }
FishFileDict = {
                0:(4,'clownFish-zero','clownFish-swim','clownFish-swim',None,(0.12,0,-0.15),0.38,-35,20),
                1:(4,'balloonFish-zero','balloonFish-swim','balloonFish-swim',None,(0.0,0,0.0),1.0,0,0),
                2:(4,'catFish-zero','catFish-swim','catFish-swim',None,(1.2,-2.0,0.5),0.22,-35,10),
                3:(4,'devilRay-zero','devilRay-swim','devilRay-swim',None,(0,0,0),0.4,-35,20),
                4:(4,'frozenFish-zero','frozenFish-swim','frozenFish-swim',None,(0,0,0),0.5,-35,20),
                5:(4,'starFish-zero','starFish-swim','starFish-swimLOOP',None,(0,0,-0.38),0.36,-35,20),
                6:(4,'holeyMackerel-zero','holeyMackerel-swim','holeyMackerel-swim',None,None,0.4,0,0),
                7:(4,'dogFish-zero','dogFish-swim','dogFish-swim',None,(0.8,-1.0,0.275),0.33,-38,10),
                8:(4,'amoreEel-zero','amoreEel-swim','amoreEel-swim',None,(0.425,0,1.15),0.5,0,60),
                9:(4,'nurseShark-zero','nurseShark-swim','nurseShark-swim',None,(0,0,-0.15),0.3,-40,10),
                10:(4,'kingCrab-zero','kingCrab-swim','kingCrab-swimLOOP',None,None,0.4,0,0),
                11:(4,'moonFish-zero','moonFish-swim','moonFish-swimLOOP',None,(-1.2,14,-2.0),0.33,0,-10),
                12:(4,'seaHorse-zero','seaHorse-swim','seaHorse-swim',None,(-0.57,0.0,-2.1),0.23,33,-10),
                13:(4,'poolShark-zero','poolShark-swim','poolShark-swim',None,(-0.45,0,-1.8),0.33,45,0),
                14:(4,'BearAcuda-zero','BearAcuda-swim','BearAcuda-swim',None,(0.65,0,-3.3),0.2,-35,20),
                15:(4,'cutThroatTrout-zero','cutThroatTrout-swim','cutThroatTrout-swim',None,(-0.2,0,-0.1),0.5,35,20),
                16:(4,'pianoTuna-zero','pianoTuna-swim','pianoTuna-swim',None,(0.3,0,0.0),0.6,40,30),
                17:(4,'PBJfish-zero','PBJfish-swim','PBJfish-swim',None,(0,0,0.72),0.31,-35,10),
                }
  
#{id:((<sub>),((minw,maxw,rarity),(<places>)))
FishLocationDict = {
                    0:((1,3,1,(-1,)),(1,1,4,(1000,-1)),(3,5,5,(1300,5000)),(3,5,3,(1100,3000)),(1,5,2,(1200,1000))),
                    1:((2,6,1,(3000,-1)),(2,6,9,(3100,3000)),(5,11,4,(9100,)),(2,6,3,(3000,"estate")),(5,11,2,(6000,"estate"))),
                    2:((2,8,1,(1000,-1)),(2,8,4,(1000,-1)),(2,8,2,(1000,-1)),(2,8,6,(1000,4000))),
                    3:((1,20,10,(6000,-1)),),
                    4:((8,12,1,(5000,)),),
                    5:((1,5,1,(-1,)),(2,6,2,(4000,-1)),(5,10,5,(4000,-1)),(1,5,7,("estate",-1)),(1,5,10,("estate",-1))),
                    6:((6,10,9,("estate",-1)),),
                    7:((7,15,1,(2000,-1)),(18,20,6,(2000,"estate")),(1,5,5,(2000,"estate")),(3,7,4,(2000,"estate")),(1,2,2,(2000,-1))),
                    8:((2,6,1,(3000,"estate",-1)),(2,6,3,(3000,"estate"))),
                    9:((4,12,5,(4000,-1)),(4,12,7,(4200,4000)),(4,12,8,(4300,4000))),
                    10:((2,4,3,(2000,-1)),(5,8,7,(5000,)),(4,6,8,(2300,))),
                    11:((4,6,1,(6000,)),(14,18,10,(6000,)),(6,10,8,(9100,)),(1,1,3,(6000,)),(2,6,6,(9100,)),(10,14,4,(6000,3000))),
                    12:((12,16,2,("estate",3000,-1)),(14,18,3,("estate",3000,-1)),(14,20,5,("estate",3000)),(14,20,7,("estate",3000))),
                    13:((9,11,3,(-1,)),(8,12,5,(3000,2000)),(8,12,6,(3000,2000)),(8,16,7,(3000,2000))),
                    14:((10,18,2,(5000,)),(10,18,3,(5000,)),(10,18,4,(5000,)),(10,18,5,(5000,)),(12,20,6,(5000,)),(14,20,7,(5000,)),(14,20,8,(5200,5000)),(16,20,10,(5100,5000))),
                    15:((2,10,2,(2000,-1)),(4,10,6,(2100,2000)),(4,10,7,(2200,2000))),17:((13,17,5,(4000,-1)),(16,20,10,(4100,4000)),(12,18,9,(4300,4000)),(12,18,6,(4000,)),(12,18,7,(4000,))),
                    16:((13,17,5,(4000,-1)),(16,20,10,(4100,4000)),(12,18,9,(4300,4000)),(12,18,6,(4000,)),(12,18,7,(4000,))),
                    17:((1,5,2,(1000,"estate",-1)),(1,5,3,(5000,"estate",-1)),(1,5,4,(3000,"estate")),(1,5,5,(6000,"estate")),(1,5,10,(5000,6000))),
                    }
       
def getFishData(species,subIndex):
    audio = FishAudioFileDict.get(species,('',0,0,0))
    model = FishFileDict.get(species,(0,'','','',None,None,0,0))
    location = FishLocationDict.get(species,())[subIndex]
    return (audio,model,location)
    
RARITY_VALUE_SCALE = 0.2
WEIGHT_VALUE_SCALE = 0.05 / 16.0
OVERALL_VALUE_SCALE = 15
    
def getValue(species, subIndex, weight):
    rarity = FishLocationDict[species][subIndex][2]
    rarityValue = pow(RARITY_VALUE_SCALE * rarity, 1.5)
    weightValue = pow(WEIGHT_VALUE_SCALE * weight, 1.1)
    value = OVERALL_VALUE_SCALE * (rarityValue + weightValue)
    finalValue = int(value)
    return finalValue
    
def getRandomWeight(species, subIndex, rod = None):
    weightRange = FishLocationDict[species][subIndex][:2]
    delta = weightRange[1]-weightRange[0]
    final = weightRange[0]+random.random()*delta
    
    if rod:
        final = min(4*(rod+1),final)
        
    return final * 16
   
def canRodCatch(wRange,rod):
    return 4*(rod+1) >= wRange[0]
  
def getRandomFish(area,rod):   
    def __key(x):
        return FishLocationDict[x[0]][x[1]][2]
    possible = []
    for index,subs in FishLocationDict.items():
        for sub in subs:
            locations = sub[-1]
            for location in locations:
                if location in (area,-1):
                    possible.append((index,subs.index(sub)))

    st = []
    for fish in possible:
        wr = FishLocationDict[fish[0]][fish[1]][:2]
        cc = canRodCatch(wr,rod)
        if cc:
            print 'can catch', L10N.FishNames[fish[0]][fish[1]]
            st.append(fish)
        
    st = sorted(st,key=__key)
    
    rt = random.random()*11
    if random.random() < .4: rt /= 1.5
    rt = min(10,max(1,int(rt)))
    
    selected = random.choice([x for x in st if __key(x)<=rt])
    
    return (rt,selected)