#! /usr/local/bin/python
#-*- coding:utf-8 -*-

"""
@author: weber.juche@gmail.com
@time: 2016/12/5 20:47

Redis客户端订阅封装

"""

import sys
import redis
import os
import time

from weberFuncs import PrintTimeMsg

#--------------------------------------
def GetRedisClient(sRedisParam):
    import redis
    # sRedisParam = '192.168.2.209:6379:6'
    # sRedisParam = '192.168.2.209:6379:6:password'
    redisHOST = '127.0.0.1'
    redisPORT = 6379
    redisDB = 1
    redisPASS = None # WeiYF.20160414 Redis参数支持密码
    lsP = sRedisParam.split(':')
    if len(lsP)>=2:
        redisHOST = lsP[0]
        redisPORT = int(lsP[1])
        if len(lsP)>=3:
            redisDB = int(lsP[2])
            if len(lsP)>=4:
                redisPASS = int(lsP[3])
    oRedis = redis.StrictRedis(host=redisHOST, port=redisPORT, db=redisDB,
                               password=redisPASS,
                               socket_timeout=30) #WeiYF.20160606 新增超时参数
    sRedisParamHint = '%s:%s:%s' % (redisHOST, redisPORT, redisDB)
    PrintTimeMsg("GetRedisClient(%s)ReturnOK..." % (sRedisParamHint))
    return oRedis

#--------------------------------------
class CRedisClientBase:

    def __init__(self, sRedisParam=''):
        self.oRedis = GetRedisClient(sRedisParam)

    def __del__(self):
        if self.oRedis:
            self.oRedis.connection_pool.disconnect()
            PrintTimeMsg("CRedisClientBase.disconnect()!!!")

    def TryConnect(self):
        if not self.oRedis:
            self.oRedis = redis.StrictRedis(host=self.redisHOST, port=self.redisPORT, db=self.redisDB, password=self.redisPASS)
            sMsg = "{%d}TryConnect.connect(%s)..." % (os.getpid(),self.sRedisParamHint)
            PrintTimeMsg(sMsg)

class CRedisSubscribe(CRedisClientBase):

    def __init__(self, sRedisParam=''):
        CRedisClientBase.__init__(self, sRedisParam)
        self.oPubSub = None
        self.bLoopRunFlag = True  # WeiYF.20150514 循环运行标记，为False时退出订阅循环

    def __del__(self):
        if self.oPubSub:
            self.oPubSub.close()
        CRedisClientBase.__del__(self)

    def SubscribeAndLoop(self, sSubKey, ftCallBack, iTimeOutSeconds=60, ftCBTimeOut=None):
        self.oPubSub = None
        iLoopCnt = 0
        tmLastGetMsg = 0
        tmLastTimeOut = time.time() #订阅后首次超时也退出
        while self.bLoopRunFlag:
            if not self.oPubSub:
                self.TryConnect()
                self.oPubSub = self.oRedis.pubsub()
                sK = sSubKey
                self.oPubSub.subscribe(sK)
                sMsg = 'Subscribe(%s)' % str(sK)
                # LogCriticalMsg(sMsg)
                PrintTimeMsg('oPubSub.'+sMsg+'...')
            if not self.oPubSub.connection:
                PrintTimeMsg('oPubSub.connection=None...')
                if self.oPubSub:
                    self.oPubSub.close()
                    self.oPubSub = None
                time.sleep(0.001)  # be nice to the system :)
                continue
            iLoopCnt += 1
            # msg = ''
            try:
                # if self.oPubSub and self.oPubSub.connection:
                # WeiYF.20150608 应该是不判断链接状态，才会出异常
                # WeiYF.20150609 经测试，不判断链接状态，不会出异常
                msg = self.oPubSub.get_message() # No Block 不阻塞
            except Exception as e:
                PrintTimeMsg('oPubSub.Exception.e=(%s)Continue...' % (str(e)))
                if self.oPubSub:
                    self.oPubSub.close()
                    self.oPubSub = None
                time.sleep(0.001)  # be nice to the system :)
                continue
            if msg:
                # print msg
                sType = msg.get('type','')
                if sType=='subscribe':
                    PrintTimeMsg('oPubSub.SubscribeReturn=(%s)' % str(msg))
                elif sType=='message':
                    sData = msg.get('data','')
                    # print "sData=",sData
                    if sData and type(sData)==str:
                        # PrintTimeMsg("SubscribeAndLoop.iLoopCnt=%s,RcvData=(%s)" % (iLoopCnt,str(sData)) )
                        ftCallBack(sData)
                        tmLastTimeOut = time.time()
                    else:
                        PrintTimeMsg("SubscribeAndLoop.iLoopCnt=%s,Receive=(%s)" % (iLoopCnt,str(msg)) )
                time.sleep(0.01)  # be nice to the system :)
                continue
            else:
                if ftCBTimeOut and time.time()-tmLastTimeOut>iTimeOutSeconds: #超时回调 #and tmLastTimeOut>0
                    # 调用 ftCBTimeOut 首次也要调用，否则会出现没有数据情况下吊死
                    ftCBTimeOut()
                    tmLastTimeOut = time.time()
                if time.time()-tmLastGetMsg>60: # 60秒主动检查一次
                    if type(sSubKey)==str and sSubKey.startswith('LIST_'): #若是列表型，则主动去查询列表
                        lsData = self.oRedis.lrange(sSubKey,0,0) #取第一个
                        if len(lsData)>=1:
                            sData = lsData[0]
                            PrintTimeMsg("SubscribeAndLoop.iLoopCnt=%s,GetData=(%s)" % (iLoopCnt,str(sData)) )
                            ftCallBack(sData)
                            tmLastTimeOut = time.time()
                            tmLastGetMsg = tmLastTimeOut
                sleepSeconds = 0.1 #0.01
                time.sleep(sleepSeconds)  # be nice to the system :)

def testCRedisSubscribe():
    o = CRedisSubscribe()
    def cbPrint(sData):
        PrintTimeMsg("cbPrint.GetData=(%s)" % (str(sData)) )
    o.SubscribeAndLoop('ME:TEST',cbPrint)


#-------------------------------
if __name__ == '__main__':
    testCRedisSubscribe()