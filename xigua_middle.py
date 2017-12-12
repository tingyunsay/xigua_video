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
import execjs
import requests

#author : tingyun  2017-12-12
#此版本通过别人网站提供的接口去获取下载网址，不是源下载网址

#在线工具的解码方式，可参考
'''
var Base64 = {
    _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    encode: function(j) {
        var m = "";
        var d, b, g, p, c, l, k;
        var h = 0;
        j = Base64._utf8_encode(j);
        while (h < j.length) {
            d = j.charCodeAt(h++);
            b = j.charCodeAt(h++);
            g = j.charCodeAt(h++);
            p = d >> 2;
            c = (d & 3) << 4 | b >> 4;
            l = (b & 15) << 2 | g >> 6;
            k = g & 63;
            if (isNaN(b)) {
                l = k = 64
            } else {
                if (isNaN(g)) {
                    k = 64
                }
            }
            m = m + this._keyStr.charAt(p) + this._keyStr.charAt(c) + this._keyStr.charAt(l) + this._keyStr.charAt(k)
        }
        return m
    },
    decode: function(j) {
        var m = "";
        var d, b, g;
        var p, c, l, k;
        var h = 0;
        j = j.replace(/[^A-Za-z0-9+/=]/g, "");
        while (h < j.length) {
            p = this._keyStr.indexOf(j.charAt(h++));
            c = this._keyStr.indexOf(j.charAt(h++));
            l = this._keyStr.indexOf(j.charAt(h++));
            k = this._keyStr.indexOf(j.charAt(h++));
            d = p << 2 | c >> 4;
            b = (c & 15) << 4 | l >> 2;
            g = (l & 3) << 6 | k;
            m = m + String.fromCharCode(d);
            if (l != 64) {
                m = m + String.fromCharCode(b)
            }
            if (k != 64) {
                m = m + String.fromCharCode(g)
            }
        }
        m = Base64._utf8_decode(m);
        return m
    },
    _utf8_encode: function(c) {
        c = c.replace(/rn/g, "n");
        var a = "";
        for (var d = 0; d < c.length; d++) {
            var b = c.charCodeAt(d);
            if (b < 128) {
                a += String.fromCharCode(b)
            } else {
                if (b > 127 && b < 2048) {
                    a += String.fromCharCode(b >> 6 | 192);
                    a += String.fromCharCode(b & 63 | 128)
                } else {
                    a += String.fromCharCode(b >> 12 | 224);
                    a += String.fromCharCode(b >> 6 & 63 | 128);
                    a += String.fromCharCode(b & 63 | 128)
                }
            }
        }
        return a
    },
    _utf8_decode: function(c) {
        var a = "";
        var d = 0;
        var b = c1 = c2 = 0;
        while (d < c.length) {
            b = c.charCodeAt(d);
            if (b < 128) {
                a += String.fromCharCode(b);
                d++
            } else {
                if (b > 191 && b < 224) {
                    c2 = c.charCodeAt(d + 1);
                    a += String.fromCharCode((b & 31) << 6 | c2 & 63);
                    d += 2
                } else {
                    c2 = c.charCodeAt(d + 1);
                    c3 = c.charCodeAt(d + 2);
                    a += String.fromCharCode((b & 15) << 12 | (c2 & 63) << 6 | c3 & 63);
                    d += 3
                }
            }
        }
        return a
    }
};
if (typeof(Storage) !== "undefined") {
    Storage.prototype.setObject = function(a, b) {
        this.setItem(a, JSON.stringify(b))
    };
    Storage.prototype.getObject = function(a) {
        var b = this.getItem(a);
        return b && JSON.parse(b)
    }
}
Array.prototype.contains = function(b) {
    var a = this.length;
    while (a--) {
        if (this[a] === b) {
            return true
        }
    }
    return false
};
var shortUrlArr = ["url", "t", "dwz", "suo"],
    hostMap = {
        huoshan: "huoshan.iiilab.com",
        huoshanzhibo: "huoshan.iiilab.com",
        gifshow: "kuaishou.iiilab.com",
        kuaishou: "kuaishou.iiilab.com",
        kwai: "kuaishou.iiilab.com",
        miaopai: "weibo.iiilab.com",
        xiaokaxiu: "weibo.iiilab.com",
        yixia: "weibo.iiilab.com",
        weibo: "weibo.iiilab.com",
        weico: "weibo.iiilab.com",
        toutiao: "toutiao.iiilab.com",
        "365yg": "toutiao.iiilab.com",
        ixigua: "toutiao.iiilab.com",
        xiguaapp: "toutiao.iiilab.com",
        xiguavideo: "toutiao.iiilab.com",
        xiguashipin: "toutiao.iiilab.com",
        pstatp: "toutiao.iiilab.com",
        zijiecdn: "toutiao.iiilab.com",
        zijieimg: "toutiao.iiilab.com",
        toutiaocdn: "toutiao.iiilab.com",
        toutiaoimg: "toutiao.iiilab.com",
        toutiao12: "toutiao.iiilab.com",
        toutiao11: "toutiao.iiilab.com",
        neihanshequ: "toutiao.iiilab.com",
        meipai: "meipai.iiilab.com",
        douyin: "douyin.iiilab.com",
        amemv: "douyin.iiilab.com",
        tiktokv: "douyin.iiilab.com",
        tiktokcdn: "douyin.iiilab.com",
        musical: "muse.iiilab.com",
        musemuse: "muse.iiilab.com",
        muscdn: "muse.iiilab.com",
        xiaoying: "xiaoying.iiilab.com",
        vivavideo: "xiaoying.iiilab.com",
        immomo: "momo.iiilab.com",
        momocdn: "momo.iiilab.com",
        inke: "inke.iiilab.com"
    };

function parseHost(a) {
    var c = document.createElement("a");
    c.href = a;
    var b = c.hostname.split(".");
    if (b.length < 2) {
        return ""
    }
    return b[b.length - 2]
}

function parseSuffix(a) {
    var b = document.createElement("a");
    b.href = a;
    return b.pathname.split(".").pop()
}

function isMP4File(a) {
    var b = parseSuffix(a);
    return b.toUpperCase() === "MP4"
}

function detectIE() {
    var a = window.navigator.userAgent;
    if (a.indexOf("MSIE ") > 0 || a.indexOf("Trident/") > 0) {
        $("#app .row .col-md-12").prepend('<div style="text-align: center;" class="alert alert-danger" role="alert">发现您正在使用IE内核浏览器，建议使用WebKit内核浏览器访问本站获得最佳上网体验。<a target="_blank" href="http://www.jianshu.com/p/a70521aba2b3">详情>></a></div>')
    }
}
var app = new Vue({
    el: "#app",
    data: {
        link: "",
        linkFromInit: false,
        submitBtnClass: {
            disabled: false
        },
        errorTip: "",
        isMP4File: false,
        requestSuccess: false,
        showAllSupportLink: false,
        showClearBtn: false,
        requestResult: {
            video: "",
            text: "",
            cover: ""
        }
    },
    watch: {
        link: function(b, a) {
            if (b.length > 0) {
                this.showClearBtn = true;
                $(".input-group-lg .link-input").css("padding-right", "32px")
            } else {
                this.showClearBtn = false;
                $(".input-group-lg .link-input").css("padding-right", "16px")
            }
        }
    },
    methods: {
        gaga: function(a, b) {
            ga("send", "event", a, a + "-" + (b + 1))
        },
        videoDownloadLink: function(a, b) {
            if (typeof(b) === "undefined") {
                b = "video"
            }
            return "http://service.iiilab.com/video/iiilab/" + b + "_iiilab_" + new Date().getTime() + Math.random().toString(10).substring(2, 4) + ".mp4?source=" + Base64.encode(a)
        },
        toggleAllSupportLink: function() {
            this.showAllSupportLink = !this.showAllSupportLink
        },
        submit: function(b) {
            if (this.submitBtnClass.disabled) {
                return
            }
            this.removeLastResult();
            if (this.link == "") {
                this.errorTip = "请先将视频链接粘贴到上面的输入框";
                return
            }
            var c = this.link.lastIndexOf("http://");
            c = (c === -1) ? this.link.lastIndexOf("https://") : c;
            if (c === -1) {
                this.errorTip = "请输入正确的视频链接";
                return
            }
            this.link = this.link.substr(c);
            var a = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z]{2,5}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g;
            if (this.link.length < 16 || !a.test(this.link)) {
                this.errorTip = "请输入正确的视频链接";
                return
            }
            this.errorTip = "";
            if (isMP4File(this.link)) {
                this.isMP4File = true;
                return
            }
            if (shortUrlArr.contains(parseHost(this.link))) {
                this.unShortUrlAndParseVideo();
                return
            }
            this.parseVideo()
        },
        unShortUrlAndParseVideo: function() {
            this.submitBtnClass.disabled = true;
            var b = this,
                c = Math.random().toString(10).substring(2),
                a = this.generateStr(this.link + "@" + c).toString(10);
            $.ajax({
                type: "POST",
                url: "http://service.iiilab.com/url/unshort",
                xhrFields: {
                    withCredentials: true
                },
                crossDomain: true,
                data: {
                    link: b.link,
                    r: c,
                    s: a
                },
                dataType: "json",
                success: function(d) {
                    if (d.succ) {
                        b.link = d.data;
                        b.parseVideo()
                    } else {
                        b.submitBtnClass.disabled = false;
                        b.errorTip = d.retDesc
                    }
                },
                error: function() {
                    b.submitBtnClass.disabled = false;
                    b.errorTip = "处理失败,请重试!"
                }
            })
        },
        parseVideo: function() {
            var d = parseHost(this.link);
            if (hostMap.hasOwnProperty(d) && hostMap[d] != location.hostname) {
                this.redirect(hostMap[d]);
                return
            }
            if (typeof(ga) !== "undefined") {
                ga("send", "event", "analysis", "analysis-normal")
            }
            this.submitBtnClass.disabled = true;
            var b = this,
                c = Math.random().toString(10).substring(2),
                a = this.generateStr(this.link + "@" + c).toString(10);
            $.ajax({
                type: "POST",
                url: "http://service.iiilab.com" + analyzeVideoUrl,
                xhrFields: {
                    withCredentials: true
                },
                crossDomain: true,
                data: {
                    link: b.link,
                    r: c,
                    s: a
                },
                dataType: "json",
                success: function(e) {
                    b.submitBtnClass.disabled = false;
                    if (e.succ) {
                        b.requestResult = e.data;
                        b.requestSuccess = true;
                        b.cacheResult()
                    } else {
                        if (e.retCode == 300 && !b.linkFromInit) {
                            b.redirect(location.hostname);
                            return
                        }
                        b.errorTip = e.retDesc
                    }
                    b.linkFromInit = false
                },
                error: function() {
                    b.submitBtnClass.disabled = false;
                    b.errorTip = "处理失败,请重试!"
                }
            })
        },
        init: function() {
            detectIE();
            var a = "?link=";
            if (location.search.indexOf(a) != -1 && location.search.substr(a.length) != "") {
                this.link = decodeURI(location.search.substr(a.length));
                history.replaceState("", "", "/");
                this.linkFromInit = true;
                this.submit();
                return
            }
            if (typeof(Storage) == "undefined") {
                return
            }
            if (localStorage.getItem("link") != null) {
                this.link = localStorage.getItem("link")
            }
            if (localStorage.getItem("requestResult") != null) {
                this.requestResult = localStorage.getObject("requestResult");
                this.requestSuccess = true
            }
        },
        cacheResult: function() {
            if (typeof(Storage) == "undefined") {
                return
            }
            localStorage.setItem("link", this.link);
            localStorage.setObject("requestResult", this.requestResult)
        },
        removeLastResult: function() {
            if (typeof(Storage) == "undefined") {
                return
            }
            this.isMP4File = false;
            this.requestSuccess = false;
            localStorage.removeItem("link");
            localStorage.removeItem("requestResult")
        },
        clear: function() {
            this.removeLastResult();
            this.link = "";
            ga("send", "event", "clear", "clear")
        },
        clearLinkInput: function() {
            this.removeLastResult();
            this.link = "";
            ga("send", "event", "clear", "clear-input")
        },
        redirect: function(a) {
            var b = location.protocol + "//" + a + "/?link=" + encodeURI(this.link);
            window.location.replace(b)
        },
        generateStr: function(a) {
            var c = function() {
                    for (var d = 0, f = new Array(256), g = 0; 256 != g; ++g) {
                        d = g, d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1, d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1, d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1, d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1, d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1, d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1, d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1, d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1, f[g] = d
                    }
                    return "undefined" != typeof Int32Array ? new Int32Array(f) : f
                }(),
                b = function(g) {
                    for (var j, k, h = -1, f = 0, d = g.length; f < d;) {
                        j = g.charCodeAt(f++), j < 128 ? h = h >>> 8 ^ c[255 & (h ^ j)] : j < 2048 ? (h = h >>> 8 ^ c[255 & (h ^ (192 | j >> 6 & 31))], h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & j))]) : j >= 55296 && j < 57344 ? (j = (1023 & j) + 64, k = 1023 & g.charCodeAt(f++), h = h >>> 8 ^ c[255 & (h ^ (240 | j >> 8 & 7))], h = h >>> 8 ^ c[255 & (h ^ (128 | j >> 2 & 63))], h = h >>> 8 ^ c[255 & (h ^ (128 | k >> 6 & 15 | (3 & j) << 4))], h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & k))]) : (h = h >>> 8 ^ c[255 & (h ^ (224 | j >> 12 & 15))], h = h >>> 8 ^ c[255 & (h ^ (128 | j >> 6 & 63))], h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & j))])
                    }
                    return h ^ -1
                };
            return b(a) >>> 0
        }
    }
});
app.init();
'''

js_code = """
function test(a) {
            var c = function() {
                for (var d = 0,
                f = new Array(256), g = 0; 256 != g; ++g) {
                    d = g,
                    d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
                    d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
                    d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
                    d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
                    d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
                    d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
                    d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
                    d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
                    f[g] = d
                }
                return "undefined" != typeof Int32Array ? new Int32Array(f) : f
            } (),
            b = function(g) {
                for (var j, k, h = -1,
                f = 0,
                d = g.length; f < d;) {
                    j = g.charCodeAt(f++),
                    j < 128 ? h = h >>> 8 ^ c[255 & (h ^ j)] : j < 2048 ? (h = h >>> 8 ^ c[255 & (h ^ (192 | j >> 6 & 31))], h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & j))]) : j >= 55296 && j < 57344 ? (j = (1023 & j) + 64, k = 1023 & g.charCodeAt(f++), h = h >>> 8 ^ c[255 & (h ^ (240 | j >> 8 & 7))], h = h >>> 8 ^ c[255 & (h ^ (128 | j >> 2 & 63))], h = h >>> 8 ^ c[255 & (h ^ (128 | k >> 6 & 15 | (3 & j) << 4))], h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & k))]) : (h = h >>> 8 ^ c[255 & (h ^ (224 | j >> 12 & 15))], h = h >>> 8 ^ c[255 & (h ^ (128 | j >> 6 & 63))], h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & j))])
                }
                return h ^ -1
            };
            var f = b(a) >>> 0;
            return f.toString(10);
        }


      function test2(){
          return Math.random().toString(10).substring(2);
      }
"""

def run_js(func,url):
    ctx = execjs.compile(js_code)
    res = ctx.call(func,url)
    return res

def run_js2(func):
    ctx = execjs.compile(js_code)
    res = ctx.call(func)
    return res


if __name__ == '__main__':
    url = "https://www.ixigua.com/a6490210860416369166/"
    #url = "http://www.toutiao.com/a6456372102038553101/"
    r = run_js2("test2")
    param = url + "@" + r
    s = run_js("test",param)

    api = "http://service.iiilab.com/video/toutiao"
    fuck = requests.post(api,data={
        "link":url,
        "r":str(r),
        "s":str(s),
    },headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Cookie":"PHPSESSIID=675421513073; _ga=GA1.2.946294264.1512721853; _gid=GA1.2.252509210.1513072209; _gat=1",
        "Host":"service.iiilab.com",
        "Origin":"http://toutiao.iiilab.com",
    })

    print fuck.content





