file = "to_process.txt"

startId = 113

import sys
sys.stdout = open("cogs_EN.l10n","ab")

def pc(x):
    index,name = x.split(' ',1)
    
    return map(int,index.split(',')),name

for x in filter(None,map(lambda x:x.strip(),open("to_process.txt","rb").read().replace('\r','\n').replace('\n\n','\n').split('\n'))):
    if x[1]==",":
        (a,b),name = pc(x)
        print 
        print "#",name
        print 
        base = "BATTLE_ACCEPT_%s_%s" % (a,b)
        
    else:
        print base,startId,x.strip('"')
        startId+=1