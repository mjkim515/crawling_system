# - 강원도민일보 : www.kado.net - #
# 
# 1 page 20 articles

import scrapy
import time

from crawler.items import Headline

class KadoSpider(scrapy.Spider):
    name = 'kado'
    allowed_domains = ['www.kado.net']
    start_urls = ['http://www.kado.net/']

    def start_requests(self):

        for i in range(1, 9):  
            yield scrapy.Request("http://www.kado.net/news/articleList.html?page=" + str(i)) # +"&total=1027548&box_idxno=&view_type=sm")
            #http://www.kado.net/news/articleList.html?page=2&total=1027548&box_idxno=&view_type=sm
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.xpath('//*[@id="section-list"]/ul/li/h4/a/@href').extract()
                               #//*[@id="section-list"]/ul/li/h4/a
        #/news/articleView.html?idxno=1112184', '/news/articleView.html?idxno=1112183',...  -by mjkim

        for urla in link:
            url = "http://www.kado.net"+ urla;
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
        item['body'] = " ".join(response.css('.article-body p').xpath('string()').extract())
        
        time.sleep(1)

        yield item
        
