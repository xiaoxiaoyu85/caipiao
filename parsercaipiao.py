
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import re
import urllib
import urllib2
import cookielib
import socket
import datetime
reload(sys) 
sys.setdefaultencoding("utf-8")
import logging
import os
from logging.handlers import RotatingFileHandler

from httpComm import *

handler = RotatingFileHandler(filename= os.environ["APPDATA"] + "\\" + "stock.log", mode="a", maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
handler.setFormatter(formatter)
g_logger = logging.getLogger("stock")
g_logger.setLevel(logging.DEBUG)
g_logger.addHandler(handler)

STR_SUCESS = 'sucess'
STR_FAIL = 'fail'
STR_OK = '1000'
STR_UNKNOW_CMD = '1001'
STR_NET_ERR = '1002'               #http请求失败
STR_PARSE_ERR = '1003'             #请求结果分析失败
STR_NEEDLOGIN_ERR = '1004'
STR_SERVER_DATA_ERR = '1005'

#strDataFileName = 'caipiao.data'
strUrl = "http://caipiao.baidu.com/lottery/draw/sorts/ajax_get_draw_data.php?"

#import calendar
#cal = calendar.month(2015, 12)
#print cal



def GetCurrentTimeStr():
    '''
              根据time类型时间获得时间字符串
    '''
    dictSrcTime = time.localtime(time.time())
    strTaskTime = time.strftime("%Y-%m-%d %H:%M:%S", dictSrcTime)
    return strTaskTime






def GetCaiPiaoData(fhandle, strUrl, strDate):
    #SetCook('')
    Httplib2SetCook('')
    strResult = "success"
    listPara = []
    listPara.append(("lottery_type", '200'))
    listPara.append(("date", strDate))
    rspheader, resp = Httplib2Get(strUrl, listPara)
    if ("" == resp):
        g_logger.info("未获取到请求数据")
        strResult = "fail"
        strResCode = STR_NET_ERR
        return strResult,strResCode  
    resp = resp.strip()
    dataJson = json.loads(resp)
    iRows = dataJson["data"]["rows"]
    strPerCP = ''
    strPhase = ''
    dictEveryCP = {}
    dictEveryCP['date'] = strDate
    listPerData = []    
    while iRows > 0:
        iRows = iRows - 1
        dictPerCP = dataJson["data"]["data"][iRows]
        strPhase = dictPerCP["phase"]
        strNo = strPhase[8 : len(strPhase)]
        listCode = (dictPerCP["result"]["result"][0]["data"])
        strCode = ''.join(listCode)
        dictPer = {}
        dictPer[strNo] = strCode
        listPerData.append(dictPer)
        #strPerCP = strPerCP + strCode + '|'

    dictEveryCP["phase"] = listPerData
    strPerCP = json.dumps(dictEveryCP, ensure_ascii=False)
    strPerCP = strPerCP + '\n'
    fhandle.write(strPerCP)
    fhandle.flush()
    #print strPerCP
    #print '%s ---------------------------------------------------' %GetCurrentTimeStr()
    return dataJson

def GetDateSpan(strFrom):
    listSpan = []
    iDaySpan = 0
    d = datetime.datetime.now()    
    if '' == strFrom:        
        iDaySpan = 365
    else:
        listFromStr = strFrom.split('-')
        dtFrom = datetime.datetime(int(listFromStr[0]), int(listFromStr[1]), int(listFromStr[2]), 0, 0, 0)
        iDaySpan = (d - dtFrom).days
        #if 0 == iDaySpan:
        #    iDaySpan = 1


    while iDaySpan >= 0:
        dayscount = datetime.timedelta(iDaySpan)
        dtDay = d - dayscount
        taskDay = datetime.datetime(dtDay.year, dtDay.month, dtDay.day, 0, 0, 0)
        strDay = str(taskDay)
        strDay = strDay[0 : 10]
        listSpan.append(strDay)
        iDaySpan = iDaySpan - 1
    return listSpan

def UpdateCaiPiaoData(strDataFileName):
    fhandle = open(strDataFileName, 'r+')
    listCaiPiao = fhandle.readlines()
    iLen = len(listCaiPiao)
    listSpan = []
    if 0 == iLen:
        listSpan = GetDateSpan('')
    else:        
        strLastCP = listCaiPiao[iLen - 1]
        iOffSet = (len(strLastCP) + 1) * -1
        fhandle.seek(iOffSet, 2)
        #fhandle.write("china")
        #fhandle.close()
        strLastCP = strLastCP.replace('\n', '')
        dictLastCP = json.loads(strLastCP)
        strLastCPDate = dictLastCP["date"]
        listSpan = GetDateSpan(strLastCPDate)
    for strDate in listSpan:
        GetCaiPiaoData(fhandle, strUrl, strDate)
        if len(listSpan) >= 3:
            time.sleep(1)
    fhandle.close()
    return STR_SUCESS, STR_OK


def ParserCaiPiaoCmd(strCmdJson):
    g_logger.info("cmd json:" + strCmdJson)
    dictRes = {}
    strRes = ''
    listResInfo = []
    strResCode = ''
    try:
        inputDict = json.loads(strCmdJson)
        if inputDict.has_key('Cookie'):
            SetCook(inputDict['Cookie'])
        if 'UpdateCaiPiaoData' == inputDict['Cmd']:
            strRes, strResCode = UpdateCaiPiaoData(inputDict['datafilepath'])
        else:
            strRes = STR_FAIL
            strResCode = STR_UNKNOW_CMD
    except Exception , e:
        strRes = STR_FAIL
        strResCode = STR_PARSE_ERR
        exc_type, exc_value, exc_traceback = sys.exc_info()
        errinfo  = exc_traceback
        while(errinfo):  #进入到最内层出错的函数模块
            strerr = 'errorinfo: '
            strerr = strerr + "  filename: " + errinfo.tb_frame.f_code.co_filename[ errinfo.tb_frame.f_code.co_filename.rfind("\\") + 1: ]
            strerr = strerr + "  functionname: " + errinfo.tb_frame.f_code.co_name
            strerr = strerr + "  lineno: " + str(errinfo.tb_lineno)
            errinfo = errinfo.tb_next
            g_logger.info(strerr)

    dictRes['result'] = strRes
    dictRes['rescode'] = strResCode
    dictRes['info'] = listResInfo
    resultjson = json.dumps(dictRes, ensure_ascii = False)
    g_logger.debug("result " + inputDict['Cmd'] + " json:" + resultjson)
    return resultjson

if __name__ == "__main__":
    dictCmd = {}
    dictCmd["Cmd"] = "UpdateCaiPiaoData"
    dictCmd['datafilepath'] = "E:\study\web\caipiaoparser\caipiao.data"
    strCmdJson = json.dumps(dictCmd, ensure_ascii = False)
    print ParserCaiPiaoCmd(strCmdJson)
    



