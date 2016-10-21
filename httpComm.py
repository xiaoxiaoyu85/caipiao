#!/usr/bin/python
from binascii import b2a_base64
import json
import re
import urllib
import urllib2
import httplib2
import cookielib
import socket
import time
#from parsercaipiao import g_logger

def SetCook(strCookie):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('Accept', 'application/json, text/javascript, */*; q=0.01'),
                        ('Accept-Language', 'zh-CN'),
                        #('Content-Type', 'application/x-www-form-urlencoded'),
                        ('X-Requested-With', 'XMLHttpRequest'),
                        #('Accept-Encoding', 'deflate'),
                        ('Connection', 'Keep-Alive'),
                        ('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)'),
                        #('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; EmbeddedWB 14.52 from: http://www.bsalsa.com/ EmbeddedWB 14.52; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'),
                        ('Referer', 'https://caipiao.baidu.com/lottery/draw/view/200?qq-pf-to=pcqq.c2c'),
                        ('DNT', '1'),
                        ('Cookie', 'BAIDUID=81C36ADA26E5E63B0DAC30874D51D511:FG=1')
                        ]
    urllib2.install_opener(opener)

def HttpGet(strUrl, listPara, strMethod = 'GET'):
    #print 'begin'
    timeout = socket._GLOBAL_DEFAULT_TIMEOUT
    #timeout = 60
    #socket.setdefaulttimeout(timeout)
    request = None
    if ('GET' == strMethod):
        strParamData = urllib.urlencode(listPara)
        strUrl = strUrl + strParamData
        request = urllib2.Request(strUrl)
    else:
        strPostData = urllib.urlencode(listPara)
        request = urllib2.Request(strUrl, strPostData)
    rsp = urllib2.urlopen(request)   
    strRsp = ""
    rspHeader = rsp.info()
    #contextType = rspHeader.get("Cookie")
    strRsp = rsp.read()
    #print 'end'
    return strRsp


dictHeaders = {'Accept' : 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language' : 'zh-CN',
                        #'Content-Type' : 'application/x-www-form-urlencoded',
                        'X-Requested-With' : 'XMLHttpRequest',
                        #'Accept-Encoding' : 'deflate',
                        'Connection' : 'Keep-Alive',
                        'User-Agent' : 'Mozilla/5.0 compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0',
                        'Referer' : 'https://caipiao.baidu.com/lottery/draw/view/200?qq-pf-to=pcqq.c2c',
                        'DNT' : '1',
                        'Cookie' : 'BAIDUID=81C36ADA26E5E63B0DAC30874D51D511:FG=1'
                        }


def Httplib2SetCook(strCookie):
    dictHeaders['Cookie'] = strCookie

def Httplib2Get(strUrl, listPara, strMethod = 'GET'):
    http = httplib2.Http()
    
    if ('GET' == strMethod):
        strParamData = urllib.urlencode(listPara)
        strUrl = strUrl + strParamData
        strRsp = ""
        #g_logger.info(strUrl)
        response, content = http.request(strUrl, strMethod, body=None, headers = dictHeaders)
        strRsp = content
        #contextType = response.get("content-type")        
    else:
        response, content = http.request(strUrl, strMethod, body = urllib.urlencode(listPara), headers = dictHeaders)
    return response, content
