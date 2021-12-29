#from CannonGame import DistCannonGameAI, CannonGameZone
from RingGame import DistRingGameAI, RingGameZone
games = {
         1:(DistRingGameAI,RingGameZone,'AREA_MG_RIN'),
         #2:(DistCannonGameAI,CannonGameZone,'AREA_MG_CAN'),
}
       
players = {
            1:(1,),
            2:(1,),
            3:(1,),
            4:(1,),
           }
       
import random

def generateGame(zone, toons):
    gid = random.choice(players[len(toons)][:])
    game = games[gid][0]
    
    go = game(base.air)
    go.setToons(toons)
    go = base.air.createDistributedObject(distObj = go, zoneId = zone)
    
    return gid