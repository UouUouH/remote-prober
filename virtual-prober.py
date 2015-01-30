#virtual prober
import sys, time
import logging

class axis:
    '''the unit of length is um
    speed : um/s
    s1: speed = 1000um/s
    s2: speed = 5000um/s
    s3: speed = 10000um/s
    s4: speed = 100000um/s'''

    def __init__(self, name, limit = 10000):
        """
        @type limit: C{long}
        @param limit: maximum operating distance,and it's unit is um
        """
        self.name = name 
        self.limit = limit
        self.enableAxis()
        self.speed = 1000
        self.startTime= 0#the time start moving 
        self.estimateStopTime = 0#based on the startTime, distence, movingSpeed,if == 0 means the position aready caculated
        self.movingSpeed = 1000
        self.isMoving= False#
        self.position = 0
        self.enable = True
        '''
        logging.basicConfig(level = loggint.DEBUG, 
                            format = '%(filename)s [%(lineno)d] %(levelname)s %(message)s',
                            datefmt = '%Y %m %d,%H:%M:%S',
                            filename = 'remote-prober.log',
                            filemode = 'w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%H:%M:%S %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
                    '''

    def enableAxis(self):
        """
        if the axis is not enabled, it can not move
        """
        self.enableFlag = True
        logging.info("enable axis")

    def disableAxis(self):
        """
        if the axis is not enabled, it can not move
        """
        self.enableFlag = False
        logging.info("disable axis")

    def getPosition(self):
        """
        If the axis was moving(isMoving == Ture),
        it would caculate the position based on the time and speed.
        And it also update the starttime to the time right now (for the next caculation).

        if the axis was stop(estimateStopTime <=  time right now)
        if the time right now passed the estimateStopTime, it means the axis is stop.
        so, we would set estimateStopTime to 0, and isMoving to False, which are the sign of axis's moving status.
        only if those two signs are set to the correct value, it means the position aready updated. 

        if the position is out of limit, we will stop moving
        """
        logging.info("get position")
        if self.isMoving:
            t = time.time()
            if t >= self.estimateStopTime:
                self.isMoving = False
                self.estimateStopTime = 0
                d = self.estimateStopTime - self.startTime
            else:
                d = t - self.startTime
            self.startTime = t
            l = d*self.movingSpeed
            self.position = self.position + l
            if self.position <= 0:
                self.position = 0
                self.estimateStopTime = 0
                self.isMoving = False
            elif self.position > self.getLimit():
                self.position = self.getLimit()
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
        logging.info("set speed %s" %(speedFlag,))
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

    def moveStep(self, distence):
        print self.name, distence

        logging.info("move step %f" %(distence,))
        if self.enableFlag == False:
            return True
        sta = self.getStatus()
        if sta[0]:#is moving
            return True 
        l = distence 
        if self.getPosition()+l > self.getLimit():
            l = self.getLimit()-l
        self.startTime = time.time()
        self.movingSpeed = self.getSpeed()
        self.estimateStopTime = self.startTime + l/self.movingSpeed
        print self.name, self.estimateStopTime
        self.isMoving = True
        return False

    def move(self, direction):
        '''direction == 1: positive direction
           direction == -1:nagetive direction
        '''
        logging.info("move, direction: %d" %(direction,))
        if self.enableFlag == False:
            return True
        sta = self.getStatus()
        if sta[0]:#is moving
            return True
        self.getPosition()
        if direction == 1:
            distence = self.getLimit() - self.getPosition()
        elif direction  == -1:
            distence = 0 - self.getPosition()

        return self.moveStep(distence)

    def stop(self):
        logging.info("stop")
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
        #we update the value of isMoving in getPosition(),
        #so, here it can indicate if the axis was moving
        return (self.isMoving, isLimit, isZero)



        
chuck = {'x' : axis(name = 'chuck x', limit = 100000),
        'y' : axis(name = 'chuck y', limit = 100000),
        'z' : axis(name = 'chuck z', limit = 10000),
        't' : axis(name = 'chuck t', limit = 10)
        }

scope = {'x': axis(name = 'scope x',limit = 100000),
        'y': axis(name = 'scope y', limit = 100000),
        'z': axis(name = 'scope z', limit = 100000)
        }

specialPoint = {'base':[0,0],
                'separate':220,
                'align':10,
                'contact':0,
                'mark1':[0,0],
                'mark2':[0,0],
                'focus1':100,
                'focus2':200,
                'focus3':300
                }

def moveChuck(**kwargs):
    axisName = kwargs.get("name")
    direction = kwargs.get("direction", 0)
    distence = kwargs.get("distence", 0)

    if direction == 0 and distence == 0:
        return 
    if direction != 0 and distence != 0:
        return
    
    if direction != 0:
        chuck[axisName].move(direction)

    if distence != 0:
        chuck[axisName].moveStep(distence)


def stopChuck(axisName):
    chuck[axisName].stop()


def getChuckPosition():
    return (chuck['x'].getPosition(),
         chuck['y'].getPosition(),
         chuck['z'].getPosition(),
         chuck['t'].getPosition())


print getChuckPosition()
#moveChuck(name = 'x', direction = 1)
time.sleep(1)
print getChuckPosition()
time.sleep(1)
stopChuck('x')
moveChuck(name = 'x', distence = 2000)
time.sleep(3)
print getChuckPosition()

