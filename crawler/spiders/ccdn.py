#
# 충청매일 [ccdn] - 1page 20
# http://www.ccdn.co.kr
# https://www.ccdn.co.kr/news/articleList.html?page=1
# 

import scrapy

from crawler.items import Headline

class CcdnSpider(scrapy.Spider):
    name = 'ccdn'
    allowed_domains = ['www.ccdn.co.kr']
    start_urls = ['http://www.ccdn.co.kr/']

    def start_requests(self):

        for i in range(1, 6): 
          
            yield scrapy.Request("https://www.ccdn.co.kr/news/articleList.html?page=" + str(i))
                #https://www.ccdn.co.kr/news/articleList.html?page=2
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('div.list-titles a::attr("href")').extract()
        #/news/articleView.html?idxno=744923

        for urla in link:
            url = "https://www.ccdn.co.kr"+ urla;
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
        item['body'] = " ".join(response.css('.user-content p').xpath('string()').extract())
        yield item 