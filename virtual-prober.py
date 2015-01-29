#virtual prober
import sys, time

class axis:
    '''the unit of length is um
    speed : um/s
    s1: speed = 1000um/s
    s2: speed = 5000um/s
    s3: speed = 10000um/s
    s4: speed = 100000um/s'''

    def __init__(limit = 10000):
        self.limit = limit
        self.enableAxis()
        self.speed = 1000
        self.startTime= 0#the time start moving 
        self.estimateStopTime = 0#based on the startTime, distence, movingSpeed,if == 0 means the position aready caculated
        self.movingSpeed = 1000
        self.isMoving= False#

    def enableAxis(self):
        self.enableFlag = True

    def disableAxis(self):
        self.enableFlag = False

    def getPosition(self):
        if self.isMoving:
        #if the axis is moving ,we have to caculate positon
            t = time.time()
            d = t - self.startTime
            self.startTime = t
            l = d*self.movingSpeed
            self.position = self.position + l
            if self.position <= 0:
                self.position = 0
            elif self.position > self.getLimit():
                self.position = self.getLimit()
            if t >= self.estimateStopTime:
                self.isMoving = False
                self.estimateStopTime = 0
        elif self.estimateStopTime > 0:#isMoving == false,but the position not unpdated
            d = self.estimateStopTime - self.startTime
            l = d*self.movingSpeed
            self.position = self.position +l
            self.estimateStopTime = 0
        return self.position

    def getLimit(self):
        return self.limit
    
    def setSpeed(self, speedFlag = 's1'):
        if speedFlag == 's4':
            self.speed = 100000
        elif speedFlag == 's3':
            self.speed = 10000
        elif speedFlag == 's2':
            self.speed = 5000
        else:
            self.speed = 1000

    def getSpeed(self):
        return self.speed

    def move(self, distence):
        l = distence 
        if self.getPosition()+l > self.getLimit():
            l = self.getLimit()-l
        self.startTime = time.time()
        self.movingSpeed = self.getSpeed()
        self.estimateStopTime = self.startTime + l/self.movingSpeed
        self.isMoving = True

    def stop(self):
        if self.isMoving:
            self.isMoving = False
            self.estimateStopTime = time.time()
           
    def getStatus(self):
        isLimit = False
        isZero = False
        p = self.getPosition()
        if p <= 0:
            isZero = True
        if p >= self.getLimit():
            isLimit = True
        return self.isMoving, isLimit, isZero



        




