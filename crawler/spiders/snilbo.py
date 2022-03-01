# - 성남일보 -
# http://snilbo.co.kr
# http://snilbo.co.kr/sub_view.html?page=1

import scrapy

from crawler.items import Headline

class SnilboSpider(scrapy.Spider):
    name = 'snilbo'
    allowed_domains = ['snilbo.co.kr']
    start_urls = ['http://snilbo.co.kr/']

    def start_requests(self):
        for i in range(1, 6): 
            yield scrapy.Request("http://snilbo.co.kr/sub_view.html?page=" + str(i))
            
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link =  response.css('dd.title a::attr("href")').extract()
        #link -> '['/44499', '/44498', '/44497', ....]
        
        # http://snilbo.co.kr/44519
        for urla in link:
            url = "http://snilbo.co.kr"+ urla;

            # 광고 페이지 제외
            if url.find("products") == 1: 
                continue
            # 의미 없는 페이지 제외
            if url == "#": 
                continue
            
            print ("URL : " + url)
            yield scrapy.Request(url, self.parse_topics)


    def parse_topics(self, response):

        item = Headline()
        item['title'] = response.css('head title::text').extract_first()
        item['url'] = response.url


        #//*[@id="articleBody"]/p[5]/text()[2]
        item['body'] = " ".join(response.xpath('//*[@id="textinput"]/p/text()').extract())

        yield item 