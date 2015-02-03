#2015.1.27

from twisted.internet.defer import Deferred
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.python import log
import sys, time, logging
import virtualProber

class ProberProtocol(Protocol):

    def connectionMade(self):
        log.msg("connection made")
        self.deferred = None

    def processData(self, data):
        def canceler(d):
            log.msg("cancelling deffered")

        def cancelerErr(err):
            log.msg("err: %s" %(err,))
            pass
        
        if self.deferred is not None:
            log.msg("is not none")
            deferred, self.deferred = self.deferred, None
            deferred.cancel()
        
        log.msg("new deferred")
        self.deferred = Deferred(canceler)
        #self.deferred.addErrback(cancelerErr)
        self.deferred.addCallbacks(self.factory.service.receiveCommand, cancelerErr)
        self.deferred.addCallback(self.factory.service.processCommand)
        self.deferred.addCallback(self.transport.write)

        self.deferred.callback(data)

    def conncetionLost(self, reason):
        log.msg("connection lost for %s" %(reason,))
        if self.deffered is not None:
            deferred, self.deferred = self.deferred, None
            deferred.cancel()

    def dataReceived(self, data):
        log.msg("recived data: %s" %(data,))
        #self.factory.service.receiveCommand(data)
        self.processData(data)


class ProberFactory(ServerFactory):

    protocol = ProberProtocol

    def __init__(self, service):
        self.service = service

class ProberService(object):

    commandList = []

    def receiveCommand(self, command):
        self.commandList.append(command)

   #the format of command:
   #command var1 var2 ... varn;
    def parseCommand(self, res):
        if res is not None:
            data = res.split(';')
            if data is not None:
                f = data[0].split(' ')
                log.msg("command %s" %(f,))
                if f is not None:
                    attrs = [x for x in dir(virtualProber) if '__' not in x]
                    if f[0] in attrs:
                        processFunction = getattr(virtualProber, f[0])
                        print attrs
                        kw ={'name':'x', 'distence':2000}
                        print processFunction(**kw)
                        log.msg("process fuction")
                    else:
                        log.msg("err command")
                else:
                    log.msg("err command")
                    
            else:
                log.msg("err command")
        else:
            log.msg("err command")
    
    def processCommand(self, res):
        processedCommand = None
        if len(self.commandList) > 0:
            processedCommand = self.commandList[0]
            del self.commandList[0]
        log.msg("processedCommand %s" %(processedCommand,))
        self.parseCommand(processedCommand)
        return'rec:'+ processedCommand
    
    def getPosition():
        return "fake position"
    
def configLog():

    logging.basicConfig(level = logging.DEBUG, 
                            format = '%(filename)s [%(lineno)d] %(levelname)s %(message)s',
                            datefmt = '%Y %m %d,%H:%M:%S',
                            filename = 'remote-prober.log',
                            filemode = 'w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%H:%M:%S %(levelname)-8s %(message)s')    
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)



def main():
    #configLog()
    service = ProberService()
    factory = ProberFactory(service)

    log.startLogging(sys.stdout)
    

    from twisted.internet import reactor

    port = reactor.listenTCP(1000, factory, interface = 'localhost')

    print 'prober server on %s:%s' %(port.getHost(), port)
    
    #pos = vitualProber.getChuckPosition()
    #log.msg("pos: %s" %(pos,))
    reactor.run()

if __name__ == '__main__':
    main()
