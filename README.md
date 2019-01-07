# CNVD
爬取CNVD网站的部分信息
## 前言
本文中如有错误，请指正。本文的正文部分来自书籍《从零开始学python网络爬虫》。
## 背景
&ensp;&ensp;&ensp;&ensp;刚开始学习爬虫的时候学习python的urllib库，那时会简单的下载一些网页啊，一些图片。后来学习的爬虫框架scrapy，几乎只要是写爬虫的程序就是用框架写的，但是慢慢感觉，有些内容用框架来写程序显得太重了，不是那么的方便，于是又开始学习第三方库requests和lxml。
&ensp;&ensp;&ensp;&ensp;当掉的数量越来越多时，就会考虑到爬虫的速度问题，因为Scrapy是多线程的，用requests只能写了串行爬取的。考虑到python中的Multiprocessing库，打算用python实现多进程的爬虫。
## 正文
&ensp;&ensp;&ensp;&ensp;当计算机运行时，就会创建包括代码和状态的进程。这些进程通常会通过计算机的一个或多个CPU执行。不过同一时刻每个CPU只会执行一个进程的程序，然后在不同的进行之间快速的切换，这样就给人一种同时进行的错觉，
在一个进程中，程序的执行也是在不同线程间切换的，每个线程执行程序的不同部分。
Python进行多进程掉使用了multiprocessing库，使用进程池方法进行多进程爬虫，使用方法的代码如下：
```
from multiprocessing import Pool
pool = Pool(processes=4)
pool.map(func,iterable[,chunksize])
```
代码说明：
（1）第一行导入multiprocessing库的Pool模块。
（2）第二行创建进程池，processes参数为设置进程的个数。
（3）第三行利用map()函数运行进程，func参数为需要运行的函数，在爬虫实战中为爬虫函数。iterable为迭代参数，在爬虫实战中可为多个URL列表。
## 码上行动
以爬取 http://ics.cnvd.org.cn 上的部分信息为例说明。
爬取信息为文章标题、点击数以及二级页面中的弹框内的信息。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190107142525828.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190107142536597.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)
网页的具体爬取方面些处不再详细介绍，因为本例是想说明多进程库的用法。用到的库有requests和lxml库。
```
from fake_useragent import UserAgent
import requests
from lxml import etree
from multiprocessing import Pool

ua = UserAgent().random
header = {  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': ua,
            'Accept-Encoding': 'gzip,deflate',
            'Connection': 'keep-alive',
}

def get_info(link):
    text = requests.get(link,headers=header).text
    html = etree.HTML(text)

    bigtag = html.xpath('//div[@class="list"]/table/tbody[@id="tr"]/tr')
    for per in bigtag:
        bt = per.xpath('./td[1]/a/@title')[0]
        dj = per.xpath('./td[3]/text()')[0]
        result = per.xpath('./td[1]/a/@href')[0]

        text2 = requests.get(result,headers=header).text
        html2 = etree.HTML(text2)
        gjtj = html2.xpath('//div[@id="showDiv"]/table/tbody/tr[1]/td[1]/text()')
        gjfzd = html2.xpath('//div[@id="showDiv"]/table/tbody/tr[1]/td[2]/text()')
        rz = html2.xpath('//div[@id="showDiv"]/table/tbody/tr[2]/td[1]/text()')
        jmx = html2.xpath('//div[@id="showDiv"]/table/tbody/tr[2]/td[2]/text()')
        wzx = html2.xpath('//div[@id="showDiv"]/table/tbody/tr[3]/td[1]/text()')
        kyx = html2.xpath('//div[@id="showDiv"]/table/tbody/tr[3]/td[2]/text()')
        ldpf = html2.xpath('//div[@id="showDiv"]/div/text()')

        d1 = gjtj[0] if gjtj else '-'
        d2 = gjfzd[0] if gjfzd else '-'
        d3 = rz[0] if rz else '-'
        d4 = jmx [0]if jmx else '-'
        d5 = wzx[0] if wzx else '-'
        d6 = kyx[0] if kyx else '-'
        d7 = ldpf[0] if ldpf else '-'
        print(bt,dj,d1,d2,d3,d4,d5,d6,d7)

def main(num):
    fake_link = 'http://ics.cnvd.org.cn/?tdsourcetag=s_pctim_aiomsg&max=20&offset={}'
    true_link = fake_link.format(num)
    get_info(true_link)

if __name__=="__main__":

    pool = Pool(processes=6)    #此处进程数可以自己按情况设置
    pool.map(main,[i for i in range(0,1840,20)])
```
结果如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190107143320645.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)
