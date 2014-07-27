# -*- coding: cp936 -*- 
import win32serviceutil 
import win32service 
import win32event 

from hbimserver import ChatFactory
from twisted.internet import reactor
from config import SERVER_PORT

class hbimserver(win32serviceutil.ServiceFramework): 
    _svc_name_ = "HBIMServer" 
    _svc_display_name_ = "HBIMServer" 
    def __init__(self, args): 
        win32serviceutil.ServiceFramework.__init__(self, args) 

        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None) 

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        reactor.callFromThread(reactor.stop)
        self._stopped.wait(5)
        
    def SvcDoRun(self):
        reactor.listenTCP(int(SERVER_PORT),ChatFactory())
        reactor.run()

if __name__=='__main__': 
    win32serviceutil.HandleCommandLine(hbimserver)
