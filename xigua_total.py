#!/usr/bin/env python
#!coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib3
import certifi
import json, time, re, os, sys
import json
import random
import urlparse
import binascii
import base64
import requests
import logging
import urllib

user_agent = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",\
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",\
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",\
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",\
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",\
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",\
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",\
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",\
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",\
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",\
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",\
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",\
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",\
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",\
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",\
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
		]

#for crc32
def right_shift(val, n):
    return val >> n if val >= 0 else (val + 0x100000000) >> n

#get videoid with a requests
def getVideoid(url):
    try:
        html = requests.get(url,headers={
        "user-agent":random.choice(user_agent),
    },proxies={"http":"http:192.168.0.205:8888"}).content
    except Exception,e:
        logging.warning("get video play url failed , please check function named getVideoid !")
        logging.warning(e)
        exit()
    videolist = re.findall("(?<=videoId: \').*(?=\')", html)
    return videolist[0]

#下载链接，一般有三个，我们选高清的那个video_3
def parseVideoJson(url):
    try:
        html = requests.get(url, headers={
            "Host": "i.snssdk.com",
            "User-Agent": random.choice(user_agent),
        }, proxies={"http": "http:192.168.0.205:8888"})
    except Exception, e:
        logging.warning("parse video json failed , please check function named parseVideoJson !")
        logging.warning(e)
        exit()
    htmlstr = html.content
    res = json.loads(htmlstr)
    videtype = res.get('data').get('video_list').keys()
    if "video_3" in videtype:
        main_url = res.get('data').get('video_list').get('video_3').get('main_url')
        return main_url
    else:
        logging.warning("此视频没有高清版本....地址为:%s"%url)
        exit()

def run(url):
    videoid = getVideoid(url)
    r = str(random.random())[2:]
    url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/%s' % videoid
    n = urlparse.urlparse(url).path + '?r=' + r
    c = binascii.crc32(n)
    s = right_shift(c, 0)
    mainvideourl = parseVideoJson(url + '?r=%s&s=%s' % (r, s))
    videourl = base64.b64decode(mainvideourl)
    return videourl


if __name__ == '__main__':
    print run("http://www.ixigua.com/a6475182873170149901/#mid=5450442017")


