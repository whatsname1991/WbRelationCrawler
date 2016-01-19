#!/usr/bin/env python
# -*- coding: gb2312 -*-

import os
import sys
import urllib
import urllib2
import cookielib
import base64
import re
import hashlib
import json
import binascii
import string
import traceback
import random
import time
import threading
import threadpool

successusers = []

def CrwalUserFollowsByPages(userid,pageid):
    cookie_jar     = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
    opener         = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    #POST data per LOGIN WEIBO, these fields can be captured using httpfox extension in FIrefox
    login_data = {'uid': userid,'page': pageid, 'currentuid': '','page_size': '32'}
    login_url = 'http://tw.weibo.com/api/user/follow'

    login_data = urllib.urlencode(login_data)

    ContentLength = ""
    if(pageid > 9):
        ContentLength = '47'
    else:
        ContentLength = '46'
    http_headers = {}
    http_headers['Accept'] = 'text/html, */*; q=0.01'
    http_headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
    http_headers['Connection'] = 'keep-alive'
    http_headers['Content-Length'] = ContentLength
    http_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    http_headers['Cookie'] = 'SINAGLOBAL=6734201726503.67.1450690458300; _s_tentry=www.baidu.com; Apache=3834941124077.886.1451963952063; ULV=1451963952071:2:1:1:3834941124077.886.1451963952063:1450690458309; __gads=ID=1b769cf25d60815e:T=1452496487:S=ALNI_MY9sXARmxWrN9r_6p6v1c79BFdiHg; wvr=6; CNZZDATA1254954382=1145982714-1452493836-http%253A%252F%252Fbindog.github.io%252F%7C1452493836; UOR=search.damai.cn,widget.weibo.com,sports.sina.com.cn; SUHB=0u5Qtl8fLSPjJu; _gat=1; showPopAd=1; SUB=_2AkMhypGMdcPhrAFRmvEcxGnlaIxRllGn4YeuehaZSFNRaWkLwlsD3QoJ2hF-Xtyj2Ea60VI2Qk99b9AWPDKc0Y16-74mKGBWuJ9FVOIICbc.; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFLSXdjpu3Ai.XZm_ciuTxZ5JpV8JpDqcyydNDQUgv5qrH7UF4L9G-VqcRt; laravel_session=37b758389ec896657594daaa1ef64822445e8024%2B2Qjl02k4Pw5X4i1H0zDnzSksyecKtU3hJbd35Pm4; _ga=GA1.2.1390947069.1452496486; crtg_rta=; Hm_lvt_50f34491c9065a59f87d0d334df29fa4=1452496754,1452496789,1452498021,1452498031; Hm_lpvt_50f34491c9065a59f87d0d334df29fa4=1452678962'
    http_headers['Host'] = 'tw.weibo.com'
    http_headers['Origin'] = 'http://tw.weibo.com'
    http_headers['Referer'] = 'http://tw.weibo.com/fans/follow/' + str(userid) + '/p/' + str(pageid)
    http_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    http_headers['X-Requested-With'] = 'XMLHttpRequest'

    req_login  = urllib2.Request(url = login_url,data = login_data,headers = http_headers)


    result = urllib2.urlopen(req_login,timeout=20)
    text = result.read()
    ss = text.split('<div class="addFollow none" uid=\'')
    ids = []
    for i in range(1,len(ss)):
        ids.append(ss[i].split("'>")[0])
    return ids

def CrawlUserFollowCount(userid):
    url = "http://tw.weibo.com/" + str(userid)
    result = urllib2.urlopen(url,timeout=20)
    text = result.read()
    followCount = text.split('<li class="followNum">')[1].split("<strong>")[1].split("</strong>")[0]
    return int(followCount)

def threadFun(userid):
    allids = []
    errorTime = 0
    flag = 0
    print(userid + " Begin")
    while flag == 0 and errorTime <= 2:
        try:
            followCOunt = CrawlUserFollowCount(userid)
            pages = followCOunt / 32
            for pageid in range(1,pages + 2):
                followIds = CrwalUserFollowsByPages(userid,pageid)
                for fid in followIds:
                    allids.append(fid)
            file_object = open('D:\users\\v-zhaozl\Weibo\\' + userid, 'w')
            for useridss in allids:
                file_object.write(useridss + "\n")
            file_object.close()
            flag = 1
        except Exception as e:
            print(userid + "****" + "Error!!! " + e.message + "\n")
            errorTime += 1
            time.sleep(10)
    if flag == 1:
        successusers.append(userid)
    if len(successusers) % 25 == 0:
        writer = open('D:\users\\v-zhaozl\Weibo\\' + "Success", 'w')
        for s in successusers:
            writer.write(s + "\n")
        writer.close()
    print(userid + " End")

all_the_text = []
file_object = open('D:\users\\v-zhaozl\Weibo\weiboids.txt','r')
try:
     all_the_text = file_object.read()
finally:
     file_object.close( )

userids = []
for text in all_the_text.split("\n"):
    userids.append(text.split("\t")[1])




pool = threadpool.ThreadPool(10)
requests = threadpool.makeRequests(threadFun, userids)
[pool.putRequest(req) for req in requests]
pool.wait()
