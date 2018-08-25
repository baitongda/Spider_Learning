# 主要是学习爬虫期间做的一些东西，有待完善



## 1 . CookiePool_Weibo
    - 模拟登录微博获取Cookies
    - 通过Redis构建一个Cookies池
    - 将获取的Cookies存入Cookies池中


## 2  . ProxyPool_Wechat
    - 从各大代理网站抓取免费代理，每隔一段时间获取一次，存入到Redis的有序集合中，构建一个代理池
    - 测试一下代理的可用性，给其设置一下score。
    - 本地开启一个Flask接口，通过一个HTTP接口获取可用代理
    - 抓取搜狗微信站点的微信文章，对接代理池
 
 ## 3 . Complie_Priniple 
    - 获取中国MOOC上编译原理课程中每个视频的URL
    - 通过异步方式下载视频
