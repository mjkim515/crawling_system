# - 한겨레 : http://www.hani.co.kr/ = #

import scrapy


from crawler.items import Headline

class HaniSpider(scrapy.Spider):
    name = 'hani'
    allowed_domains = ['hani.co.kr']
    start_urls = ['http://www.hani.co.kr/']


    def start_requests(self):
        for i in range(1, 21):  #total 40 articles
            yield scrapy.Request("http://www.hani.co.kr/arti/list" + str(i) + ".html")


    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('div.list a::attr("href")').extract()

        for urla in link:
            # 광고 페이지 제외
            url =  "http://www.hani.co.kr/"+ urla;
         
            if url.find("products") == 1: 
                continue
            # 의미 없는 페이지 제외
            if url == "#": 
                continue

            yield scrapy.Request(url, self.parse_topics)


    def parse_topics(self, response):
        item = Headline()
        item['title'] = response.css('head title::text').extract_first()
        item['url'] = response.url

        item['body'] = " ".join(response.css('.text').xpath('string()').extract())
        #response.css('.text::text').extract()
        #response.css('.text').xpath('string()').extract()
  
        yield item
        
