ratio = (.25,0,0,.75)

depts = {0:8,1:6,2:2,3:10}

total = sum(depts.values())

def getNextDept():  
        r = []
        for i,rt in zip(range(4),ratio):
            R = (float(depts[i])/total)
            r.append(R-rt)
            
        m = min(r)
        return r.index(m)
        
        
for i in xrange(100):
    d = getNextDept()
    depts[d]+=1
    print depts,d
    total = sum(depts.values())