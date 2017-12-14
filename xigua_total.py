#!/usr/bin/env python
#!coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib
import random
import os
import logging
import json
import six
import pymysql
import urlparse
import binascii
import base64
from threading import Thread
import requests
import re
import commands


file_name = __file__.split('/')[-1].replace(".py","")
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='%s.log'%file_name,
                filemode='a')

#将日志打印到标准输出（设定在某个级别之上的错误）
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


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

def text(string, encoding='utf8'):
    if isinstance(string, six.text_type):
        return string
    elif isinstance(string, six.binary_type):
        return string.decode(encoding)
    else:
        return six.text_type(string)

#接收一个(blob型)字符串并将其转成utf8
def blob2utf8(blob):
    fk = text(blob)
    fk = json.loads(fk,strict=False)
    return fk

def db_connetionSS(ip,port,user,pwd,db):
    conn = pymysql.connect(host=ip,
                           port=port,
                           user=user,
                           password=pwd,
                           db=db,
                           charset='utf8'
                           )
    cursor = pymysql.cursors.SSCursor(conn)
    return conn,cursor


#将取出来来的taskid和url作为下载对象和视频文件名字
def download(filename,url,platform):
    try:
        path = os.getcwd()
        platform = platform
        file_name = filename+'.mp4'
        if os.path.exists(path+"/"+platform):
            local_path=os.path.join(path+"/"+platform,file_name)
            urllib.urlretrieve(url , local_path)
        else:
            os.mkdir(path + "/" + platform)
            local_path = os.path.join(path + "/" + platform, file_name)
            urllib.urlretrieve(url , local_path)
    except Exception,e:
        print e
        print '\tError retrieving the URL:', local_path

#按条件获取 {taskid : url}
def get_map_video(platform):
    res = []
    conn, cursor = db_connetionSS("192.168.218.10", 3306, "root", "taihe123", "resultdb")
    sql = "select taskid,result from %s"%platform
    cursor.execute(sql)
    while cursor:
        try:
            row = cursor.fetchone()
            taskid = row[0]
            video_link = blob2utf8(row[1]).get('url')
            temp = {
                "taskid":taskid,
                "video_link":video_link,
                "platform":platform,
                    }
            res.append(temp)
        except Exception, e:
            # logging.info(e)
            break
    conn.close()
    return res


#for crc32
def right_shift(val, n):
    return val >> n if val >= 0 else (val + 0x100000000) >> n

#get videoid with a requests
#get videoid with a requests
def getVideoid(url):
    try:
        html = requests.get(url,headers={
        "user-agent":random.choice(user_agent),
    },proxies={"http":"http:192.168.0.205:8888"},verify=False)
    except Exception,e:
        logging.warning("get video play url failed , please check function named getVideoid !")
        logging.warning(e)
        exit()
    if html.status_code == 404:
        logging.warning("the retrun code is 404, the page is not exists !")
        return "404"
    else:
        res_id = ""
        try:
                videolist = re.findall("(?<=videoId: \').*(?=\')", html.content)
                res_id = videolist[0]
        except Exception,e:
                logging.warning(e)
                logging.warning(url)
                logging.warning("get video_id failed , please check function named getVideoid !")
                exit()
        return res_id


#下载链接，一般有三个，我们选高清的那个video_3
def parseVideoJson(url):
    fk = True
    while fk:
        #由于url动态生成的问题，这里可能会出现失败，我们不断进行重试即可
        try:
            html = requests.get(url,headers={
                "Host":"i.snssdk.com",
                "User-Agent":random.choice(user_agent),
            },proxies={"http":"http:192.168.0.205:8888"})
            fk = False
        except Exception,e:
            logging.warning("parse video json failed , please check function named parseVideoJson !")
            logging.warning(url)
            logging.warning(e)
            #exit()
            continue
    htmlstr = html.json()
    #res = json.loads(htmlstr)
    res = htmlstr
    videotype = res.get('data').get('video_list').keys()
    #清晰度从前到后降低，取第一个，最清晰的
    if videotype:
        final_key = videotype[0]
        main_url = res.get('data').get('video_list').get(final_key).get('main_url')
        return main_url
    else:
        logging.warning("此视频解析出现问题....地址为:%s"%url)
        exit()

def get_realtime_url(url):
    videoid = getVideoid(url)
    if videoid == "404":
        return None
    else:
        r = str(random.random())[2:]
        url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/%s' % videoid
        n = urlparse.urlparse(url).path + '?r=' + r
        c = binascii.crc32(n)
        s = right_shift(c, 0)
        mainvideourl = parseVideoJson(url + '?r=%s&s=%s' % (r, s))
        videourl = base64.b64decode(mainvideourl)
        return videourl

def run():
    downed_str =commands.getstatusoutput("ls ./%s"%"test_for_xigua")
    downed =downed_str[1]
    res = get_map_video("test_for_xigua")
    for i in res[:2]:
        if not re.search(str(i['taskid']),downed):
            video_link = get_realtime_url(i['video_link'])
            if video_link is None:
                continue
            else:
                download(i['taskid'],get_realtime_url(i['video_link']),i['platform'])
        else:
            logging.warning("video has been downloaded !")

if __name__ == '__main__':
    run()

