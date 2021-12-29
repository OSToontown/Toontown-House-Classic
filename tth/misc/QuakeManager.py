from direct.interval.IntervalGlobal import *

class EarthQuake:
    def __init__(self,intensity,time,environ):
        self.initialEnvHpr = environ.getHpr()
        target = environ
        toonyscale = intensity / 0.5
        ty = toonyscale
        self.shake = Sequence(target.hprInterval(.3,(0,0,ty)),
                              target.hprInterval(.3,(0,0,-ty)))
        self.shake.loop()

        self.environ = environ

        self.duration = Sequence(Wait(time),Func(self.stop)).start()


    def stop(self):
        self.shake.finish()
        self.environ.setHpr(self.initialEnvHpr)
        
        

