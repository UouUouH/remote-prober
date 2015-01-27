#2015.1.26

from twisted.internet.defer import Deferred
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.python import log
import sys

class ProberProtocol(Protocol):

    def connectionMade(self):
        log.msg("connection made")

    def conncetionLost(self, reason):
        log.msg("connection lost for %s" %(reason,))

    def dataReceived(self, data):
        log.msg("recived data: %s" %(data,))
        self.factory.service.receiveCommand(data)


class ProberFactory(ServerFactory):

    protocol = ProberProtocol

    def __init__(self, service):
        self.service = service

class ProberService(object):

    commandList = []

    def receiveCommand(self,command):
        self.commandList.append(command)

    def processCommand():
        processedCommand = None
        if len(self.commandList) > 0:
            processedCommand = self.commandList[0]
            del self.commandList[0]
        return processedCommand

def main():
    service = ProberService()
    factory = ProberFactory(service)

    log.startLogging(sys.stdout)

    from twisted.internet import reactor


    port = reactor.listenTCP(1000, factory, interface = 'localhost')

    print 'prober server on %s:%s' %(port.getHost(), port)

    reactor.run()

if __name__ == '__main__':
    main()
