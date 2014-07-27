import threading
#from buffer import MsgBuffer
#from msg import MsgFactory
#from constant import MSG_HEAD_LEN
#from twisted.internet import defer

#class dataProduce(threading.Thread):
#    def __init__(self,msgbuf):
#        self.buf = msgbuf 
#        self.msg = Msg(self.buf)
#
#        threading.Thread.__init__(self)
#    def run(self):
#        def dataproduce():
#            if self.buf.getLen() >= MSG_HEAD_LEN :
#                msgLen=self.msg.getLen()
#                msg=self.msg.getMsg(msgLen)
#                if len(msg) < msgLen:
#                    msg=self.msg.getMsg(msgLen)
#                    print msg
#                msgType=self.msg.get(msg,'Type')
#                self.msgHandle.get(msgType,self.errHandle)(msg,msgLen)
#                self.buf.clearBuffer(msgLen)
#                if self.buf.getLen() > 0:
#                    dataproduce()
#        dataproduce()   
#

class setOnLineMsg(threading.Thread):
    def __init__(self,*args):
        threading.Thread.__init__(self)

        self.type=args[0]
        self.body=args[1]
        self.created=args[2]
        self.sid=args[3]
        self.rid=args[4]
        self.mysql=args[5]
	self.run()
    def run(self):
 	self.mysql.setOnLineMsg(self.type,self.body,self.created,self.sid,self.rid)


#class setOnLineMsg(object):
#    def __init__(self,*args):
#        self.type=args[0]
#        self.body=args[1]
#        self.created=args[2]
#        self.sid=args[3]
#        self.rid=args[4]
#        self.mysql=args[5]
#	self.run()
#    def run(self):
# 	defer.succeed(self.mysql.setOnLineMsg(self.type,self.body,self.created,self.sid,self.rid))


class setOffLineMsg(threading.Thread):
    def __init__(self,*args):
        threading.Thread.__init__(self)

        self.type=args[0]
        self.body=args[1]
        self.created=args[2]
        self.sid=args[3]
        self.rid=args[4]
        self.mysql=args[5]
    	self.run()    
    def run(self):
        self.mysql.setOffLineMsg(self.type,self.body,self.created,self.sid,self.rid)


#class setOffLineMsg(object):
#    def __init__(self,*args):
#        self.type=args[0]
#        self.body=args[1]
#        self.created=args[2]
#        self.sid=args[3]
#        self.rid=args[4]
#        self.mysql=args[5]
#    	self.run()    
#    def run(self):
#        defer.succeed(self.mysql.setOffLineMsg(self.type,self.body,self.created,self.sid,self.rid))

class setSendFileMsg(threading.Thread):
    def __init__(self,*args):
        threading.Thread.__init__(self)

	self.type=args[0]
	self.created=args[1]
	self.displayname=args[2]
	self.rid=args[3]
	self.sid=args[4]
	self.length=args[5]
	self.nid=args[6]
	self.ip=args[7]
	self.mysql=args[8]
        self.run()
    def run(self):
	self.mysql.setSendFileMsg(self.type,self.sid,self.rid,self.created,self.displayname,self.length,self.nid,self.ip)
