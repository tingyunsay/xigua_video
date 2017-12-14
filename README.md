# xigua_video
西瓜(头条)视频下载

### author tingyun 
参考:  
[fourbrother](https://github.com/fourbrother/python_toutiaovideo)  
[在路上](http://blog.csdn.net/facekbook/article/details/77675537)  
[fourbrother的博客](http://blog.csdn.net/jiangwei0910410003/article/details/54092364)

### 方法一
直接获取头条官方接口，不使用中间人解密  
见xigua_total.py中

#### updated 2017-12-14
由于西瓜视频的播放链接是算法加密过的，并且其是动态的，只有短时间有效。所以我们保存其播放链，在真正需要下载时再生成实时的资源链下载  
更新下载到本地，从pyspider抓取到的结果中取出播放链接，生成短期有效的播放链

### 方法二
使用service.iiilab.com中间人转换视频并下载  
见xigua_middle.py中
