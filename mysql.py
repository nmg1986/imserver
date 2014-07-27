#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

import MySQLdb
from constant import ONLINE_MSG,OFFLINE_MSG,GOOD_FRIEND,BLACKLIST
from sys import stdout
import time
from log import logger
import traceback
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from custom import doubleQuoteDict

from config import DB_HOST,DB_USER,DB_PASSWD,DB_NAME,DB_PORT

class MySql(object):
    def __init__(self):
        try:
	    logger.info('Connect to database...')
            self.conn=MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASSWD,db=DB_NAME,port=int(DB_PORT))
	    if os.name == 'nt':
                try:
                    self.conn.set_character_set('utf8')
                except:
                    pass
            self.cur=self.conn.cursor()
	    logger.info('Done')
        except MySQLdb.Error as e:
            logger.error('Mysql Error {}:{!s}'.format(e.args[0],e.args[1]))
	    logger.error("{}".format(traceback.format_exc()))	
    def setOffLineMsg(self,type,content,time,sid,rid):
        if hasattr(self,'cur'):
            content=content.encode('utf-8')
            value=[type,content,time,sid,rid]
            self.cur.execute('insert into offlinemsgs(MsgType,MsgContent,CreatedTime,SendGuid,RecvGuid) values(%s,%s,%s,%s,%s)',value)
            self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    def delOffLineMsg(self,msgID):
        if hasattr(self,'cur'):
            self.cur.execute("delete from offlinemsgs where MsgID='%s'" % msgID)
            self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    def setOnLineMsg(self,type,content,sendtime,sid,rid):
        if hasattr(self,'cur'):
            try:
                content=content.encode('utf-8')
            except UnicodeDecodeError:
                content=content
            year=time.localtime(sendtime)[0]
            month=time.localtime(sendtime)[1]
            table='msgs' + str(year) + str(month)
            value=[table,type,content,sendtime,sid,rid]
            try:
                sql='''insert into {!s}(MsgType,MsgContent,CreatedTime,SendGuid,RecvGuid) 
                       values('{!s}','{!s}','{!s}','{!s}','{!s}')
                    '''.format(table,type,content,sendtime,sid,rid)
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as error:
                logger.debug(error)
                if error[0] == 1146 :
                    logger.debug("Table {!s} is not exist,create it !".format(table))
                    sql_1="create table {!s} like msgs".format(table)
                    self.cur.execute(sql_1)
                    logger.debug("Insert msg into {!s}".format(table))
                    sql='''insert into {!s}(MsgType,MsgContent,CreatedTime,SendGuid,RecvGuid) 
                           values('{!s}','{!s}','{!s}','{!s}','{!s}')
                        '''.format(table,type,content,sendtime,sid,rid)
                    self.cur.execute(sql)
                    self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    def getOffLineMsg(self,rid):
        if hasattr(self,'cur'):
            value=(rid)
            #self.cur.execute("select MsgType,MsgContent,CreatedTime,SendGuid,RecvGuid from offlinemsg where RecvGuid='%s' and Flag='%s'" % value)
            self.cur.execute("select MsgType,MsgContent,CreatedTime,SendGuid,RecvGuid,MsgID from offlinemsgs where RecvGuid='%s'" % value)
            self.conn.commit()
            #self.cur.execute("update offlinemsg set Flag='1' where RecvGuid = '%s'" % rid)
            results=self.cur.fetchall()
            return results
        else:
            logger.error("Database does not connected!!!")
    def setOnLineUser(self,sid):
	''' online is 1 '''
        if hasattr(self,'cur'):
            #self.cur.execute("update onlineuser set Online='1' where UserID='%s'" % sid)
	    self.cur.execute("insert into onlineuser(UserID,Online) values ('%s',1) on duplicate key update Online=1" % sid)
            self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    #def getOnLineUser(self):
    #    if hasattr(self,'cur'):
    #        self.cur.execute("update users set Online='1' where UserID='%s'" % sid)
    #        self.conn.commit()
    #        results=self.cur.fetchall()
    #        return results
    def getOnlineUser(self,gid):
        if hasattr(self,'cur'):
            user_list=[]
            sql='''select uid from group_users,onlineuser where group_users.uid=onlineuser.UserID 
                   and group_users.gid='%s' 
                   and onlineuser.Online=0; 
                ''' % gid
            self.cur.execute(sql)
            self.conn.commit()
            results=self.cur.fetchall()
            if results is not None:
                for result in results:
                    uid=result[0]
                    user_list.append(uid)
                return user_list
            if results is None:
                return user_list
        else:
            logger.error("Database does not connected!!!")
    def delOnLineUser(self,sid):
	''' offline is 0 '''
        if hasattr(self,'cur'):
            self.cur.execute("update onlineuser set Online='0' where UserID='%s'" % sid)
            self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    def setSendFileMsg(self,*args):
	if hasattr(self,'cur'):
	    '''
		self.type,self.sid,self.rid,self.created,self.displayname,self.length,self.nid,self.ip '''
	    value=[args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7]]
            sql=''' insert into sendfilemsgs(Type,SendGuid,RecvGuid,Created,DisplayName,Length,NodeID,SendIP)
                    value('{!s}','{!s}','{!s}','{!s}','{!s}',{},{},'{!s}')
                '''.format(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7])
	    self.cur.execute(sql)
	    self.conn.commit()
    def getGroups(self,sid,gname='ALL'):
        if hasattr(self,'cur'):
            groups_list=[]
            if gname == 'ALL':
                self.cur.execute("select gid,gname,created,weight from groups where uid='%s'" % sid)
                self.conn.commit()
            else :
                gname=gname.decode('utf8')
                self.cur.execute("select gid,gname,created,weight from groups where gname='%s' and uid='%s'" % (gname,sid))
                self.conn.commit()
            groups=self.cur.fetchall()
            if groups is not None:
                for group in groups :
                    gid=group[0]
                    self.cur.execute("select gid,uid,created from group_users where gid='%s'" % gid)
                    self.conn.commit()
                    users=self.cur.fetchall()
                    user_list=list()
                    if users is not None:
                        for user in users:
                            uid=user[1]
                            #print "uid=%s"%uid
                            #self.cur.execute("select Sex,DisplayName,Photo from users where UserID='%s'" % uid)
                            self.cur.execute("select Sex,DisplayName,Photo,Online,SignContent,FontSetting from users,onlineuser where users.UserID=onlineuser.UserID and users.UserID='%s'"% uid)
                            self.conn.commit()
                            result=self.cur.fetchone()
                            logger.debug(result)
			    if result is not None :
                                Sex=result[0]
                                DisplayName=result[1]
                                if not result[2]:
                                    Photo=''
                                else:
                                    Photo=result[2]
                                Online=result[3]
                                user_item={}
                                user_item['UserGuid']=uid
                                user_item['Sex']=Sex
                                user_item['DisplayName']=DisplayName
                                user_item['Photo']=Photo
                                user_item['Online']=Online
                                user_item['SignContent']=result[4]
                                user_item['FontSetting']=result[5]
                                user_item=doubleQuoteDict(user_item)
                                user_list.append(user_item)
			    else : 
                                Sex='1'
                                DisplayName=''
                                Photo=''
                                Online='0'
                                user_item={}
                                user_item['UserGuid']=uid
                                user_item['Sex']=Sex
                                user_item['DisplayName']=DisplayName
                                user_item['Photo']=Photo
                                user_item['Online']=Online
                                user_item['SignContent']=''
                                user_item['FontSetting']=''
                                user_item=doubleQuoteDict(user_item)
                                user_list.append(user_item)

                    group_item={}
                    group_item["gid"]=gid
                    group_item["gname"]=group[1]
                    group_item["users"]=user_list
                    group_item["created"]=group[2]
                    group_item["weight"]=group[3]
                    groups_list.append(group_item)
            return groups_list
        else:
            logger.error("Database does not connected!!!")
    def delGroup(self,gid,uid):
        if hasattr(self,'cur'):
            self.cur.execute("delete from groups where gid='%s' and uid='%s'" % (gid,uid))
            self.cur.execute("delete from group_users where gid='%s'" % gid)
            self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    def addGroup(self,uid,gname,weight):
        if hasattr(self,'cur'):
            value=[uid,gname,int(time.time()),weight]
            self.cur.execute("insert into groups(uid,gname,created,weight) values(%s,%s,%s,%s)",value)
            try:
                self.conn.commit()
            except MySQLdb.IntegrityError as error:
                logger.error(error)
        else:
            logger.error("Database does not connected!!!")
    def renameGroup(self,gid,gname):
        if hasattr(self,'cur'):
            self.cur.execute("update groups set gname='%s' where gid='%s'" % (gname,gid))
            self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    def addUser(self,gid,uid):
        if hasattr(self,'cur'):
            value=[gid,uid,int(time.time())]
            self.cur.execute("insert into group_users(gid,uid,created) values(%s,%s,%s)",value)
            self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    def delUser(self,gid,uid):
        if hasattr(self,'cur'):
            self.cur.execute("delete from group_users where gid='%s' and uid='%s'" % (gid,uid))
            self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    def getUsers(self,sid):
        if hasattr(self,'cur'):
            ''' generator object '''
            #user_list=[]
            try:
                self.cur.execute("select gid from groups where uid='%s'" % sid)
            except AttributeError:
                return
            gids=self.cur.fetchall()
	    #print gids
            if not gids:
                return
            #gid=gids[0]
	    for gid in gids:
            	self.cur.execute("select uid from group_users where gid='%s'" % gid[0])
            	users=self.cur.fetchall()
            	if users:
            	    for user in users:
            	        #user_list.append(user[0])
            	        yield user[0]
            	#return user_list
        else:
            logger.error("Database does not connected!!!")
    def getUserInfo(self,uname):
        if hasattr(self,'cur'):
            self.cur.execute("select UserID,PassWord,DisplayName from users where UserName='%s'" % uname)
            self.conn.commit()
            uid=self.cur.fetchone()
            return uid
        else:
            logger.error("Database does not connected!!!")
    def getUserBasicInfo(self,uids):
        user_list=list()
        if hasattr(self,'cur'):
            for uid in uids: 
                self.cur.execute("select Sex,DisplayName,Photo,Online,SignContent,FontSetting from users,onlineuser where users.UserID=onlineuser.UserID and users.UserID='%s'"% uid)
                self.conn.commit()
                result=self.cur.fetchone()
                #logger.debug(result)
	        if result is not None :
                    Sex=result[0]
                    DisplayName=result[1]
                    if not result[2]:
                        Photo=''
                    else:
                        Photo=result[2]
                    Online=result[3]
                    user_item={}
                    user_item['UserGuid']=uid
                    user_item['Sex']=Sex
                    user_item['DisplayName']=DisplayName
                    user_item['Photo']=Photo
                    user_item['Online']=Online
                    user_item['SignContent']=result[4]
                    user_item['FontSetting']=result[5]
                    user_item=doubleQuoteDict(user_item)
                    user_list.append(user_item)
	        else : 
                    Sex='1'
                    DisplayName=''
                    Photo=''
                    Online='0'
                    user_item={}
                    user_item['UserGuid']=uid
                    user_item['Sex']=Sex
                    user_item['DisplayName']=DisplayName
                    user_item['Photo']=Photo
                    user_item['Online']=Online
                    user_item['SignContent']=''
                    user_item['FontSetting']=''
                    user_item=doubleQuoteDict(user_item)
                    user_list.append(user_item)
        else:
            logger.error("Database does not connected!!!")

        return user_list

    def getPassWord(self,uname):
        if hasattr(self,'cur'):
            self.cur.execute("select PassWord from users where UserName='%s'" % uname)
            self.conn.commit()
            password=self.cur.fetchone()
            return password
        else:
            logger.error("Database does not connected!!!")
    def getBlackList(self,rid):
        if hasattr(self,'cur'):
            self.cur.execute("select gid from groups where weight='%d' and uid='%s'" % (99999,rid))  
            self.conn.commit()
            gid=self.cur.fetchone()
            if gid is not None:
                self.cur.execute("select uid from group_users where gid='%s'" % gid[0])
                self.conn.commit()
                uid=self.cur.fetchone()
                if uid is not None:
                    return uid
                else:
                    logger.debug("user {!s} has no blacklist...".format(rid))
                    return ()
            else:
                logger.debug("user {!s} has no blacklist...".format(rid))
                return () 
        else:
            logger.error("Database does not connected!!!")
    def setDefaultGroups(self,sid):
        if hasattr(self,'cur'):
            "good friend"
            logger.debug("create my-good-friends group of {}".format(sid))
            value=[sid,GOOD_FRIEND,int(time.time()),0]
            self.cur.execute("insert into groups(uid,gname,created,weight) values(%s,%s,%s,%s)",value)
            self.cur.execute("select gid from groups where uid='%s'" % sid)
            gid=self.cur.fetchone()[0]
            value=[gid,sid,int(time.time())]
            self.cur.execute("insert into group_users(gid,uid,created) values(%s,%s,%s)",value)
            "blacklist"
            logger.debug('create blacklist       group of {}' .format(sid))
            value=[sid,BLACKLIST,int(time.time()),99999]
            self.cur.execute("insert into groups(uid,gname,created,weight)  values(%s,%s,%s,%s)",value)

            self.conn.commit()
        else:
            logger.error("Database does not connected!!!")
    def updatePhoto(self,uid,photo):
	if hasattr(self,'cur'):
	    logger.debug("Update user photo : {}".format(uid))
	    self.cur.execute("update users set Photo='{}' where UserID='{}'".format(photo,uid))
	    self.conn.commit()
	    logger.debug("Done")
        else:
            logger.error("Database does not connected!!!")
    def updateSignature(self,uid,sign):
        if hasattr(self,'cur'):
            logger.debug("Update user signature : {}".format(uid))
            sign=sign.encode('utf-8')
            self.cur.execute("update users set SignContent='{}' where UserID='{}'".format(sign,uid))
            self.conn.commit()
            logger.debug("Done")
        else:
            logger.error("Database does not connected!!!")
    def changeFontSetting(self,uid,settings):
        if hasattr(self,'cur'):
            logger.debug("Set user font-seting : {}".format(uid))
            self.cur.execute("update users set FontSetting='{}' where UserID='{}'".format(settings,uid))
            self.conn.commit()
            logger.debug("Done")
        else:
            logger.error("Database does not connected!!!")

    def close(self):
        if hasattr(self,'cur'):
            self.cur.close()
            self.conn.close()
        else:
            logger.error("Database does not connected!!!")
