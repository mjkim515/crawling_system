#  - 경남신문[knnews] - 
# 1 page 15 articles
# https://www.knnews.co.kr/autoi/index.html
# https://www.knnews.co.kr/news/articleList.php
# 적게 scrapped...

import scrapy

from crawler.items import Headline

class KnnewsSpider(scrapy.Spider):
    name = 'knnews'
    allowed_domains = ['www.knnews.co.kr']
    start_urls = ['http://www.knnews.co.kr/']

    def start_requests(self):

        for i in range(1, 8):  #1page =15 articles  -by mjkim
            yield scrapy.Request("http://www.knnews.co.kr/news/articleList.php?sxno=&seldate=&gubun=&page=" + str(i))
            #https://www.knnews.co.kr/news/articleList.php?sxno=&seldate=&gubun=&page=1
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        #A little special method was needed to get the href tag.   - by mjkim
        
        #//*[@id="index"]/div[1]/div[3]/div[4]/ul/li[1]/span[3]/a
        #//*[@id="index"]/div[1]/div[3]/div[4]/ul/li[3]/span[3]/a
        link = response.xpath('//*[@id="index"]/div[1]/div[3]/div[4]/ul/li/span[3]/a/@href').extract()
        #link = response.xpath('//div[@class="list_cont02"]/ul/li/span[@class="cont02_tit"]/a/@href').extract() -bug fixed by mjkim
        #link = ../news/articleView.php?idxno=1369702&gubun=, ../news/articleView.php?idxno=1369701&gubun=, ...     -by mjkim

        for urla in link:
            #urla = '../news/articleView.php?idxno=1369702&gubun='  -by mjkim
            urls = urla.replace("..","") #remove '..'form urla    -by mjkim
            url = "http://www.knnews.co.kr"+ urls;
            #https://www.knnews.co.kr/news/articleView.php?idxno=1369702&gubun=    -by mjkim

            print ("URL : " + url)
            # 광고 페이지 제외
            if url.find("products") == 1: 
                continue
            # 의미 없는 페이지 제외
            if url == "#": 
                continue
            # 기사 페이지
            # yield scrapy.Request(response.urljoin(url), self.parse_topics)
            yield scrapy.Request(url, self.parse_topics)

    def parse_topics(self, response):
        item = Headline()
        item['title'] = response.css('head title::text').extract_first()
        item['url'] = response.url
        item['body'] = " ".join(response.css('.cont_cont p').xpath('string()').extract())

        yield item
        
