from fake_useragent import UserAgent
import requests
from lxml import etree
ua = UserAgent().random
from multiprocessing import Pool

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
        """如要提取更多信息，自己可在此处加"""
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

    pool = Pool(processes=6)
    pool.map(main,[i for i in range(0,1840,20)])