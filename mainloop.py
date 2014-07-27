#!/usr/bin/env python2.7

from twisted.internet.epollreactor import EPollReactor
from log import logger

class MainLoop(EPollReactor):
    def __init__(self):
        EPollReactor.__init__(self)
    def sigInt(self,*args):
        logger.info("Shutdown HBIM Server...")
        self.stop()
        logger.info("Done")
    def sigTerm(self,*args):
        logger.info("Shutdown HBIM Server...")
        self.stop()
        logger.info("Done")
def install():
    p = MainLoop() 
    from twisted.internet.main import installReactor
    installReactor(p)



