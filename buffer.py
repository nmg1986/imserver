#!/usr/bin/env python2.7

''' no use current '''
class MsgBuffer(object):
    def __init__(self):
        self.buf=''
    def pushMsg(self,msg):
        self.buf += msg
    def getLen(self):
        return len(self.buf)
    def popMsg(self,left,right):
        return self.buf[left:right]
    def clearBuffer(self,msglen):
	    self.buf = self.buf[msglen+5:] 

        


