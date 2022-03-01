# - 전북일보 [jjan] -
# 1 page 20 articles
# https://www.jjan.kr/
# https://www.jjan.kr/list5/110?page=1, 2,,,

import scrapy

from crawler.items import Headline

class JjanSpider(scrapy.Spider):
    name = 'jjan'
    allowed_domains = ['www.jjan.kr']
    start_urls = ['http://www.jjan.kr/']

    def start_requests(self):

        for i in range(1, 6): 
            yield scrapy.Request("https://www.jjan.kr/list5/110?page=" + str(i))
            #https://www.jjan.kr/list5/110?page=1
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        #/html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div[1]/a
        #body > div.wrapper > div.content_wrapper > div.top_contents_wrap > div.top_left_container > div.section_list > div:nth-child(1) > div > a
        link = response.xpath('/html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div/a/@href').extract()
        # /article/20220209580377'
        
        for urla in link:
            url = "https://www.jjan.kr"+ urla;
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

        #/html/body/div[1]/div[3]/div[5]/div[2]/div/p[2]
        #body > div.wrapper > div.content_wrapper > div.top_contents_wrap > div.top_left_container > div > p:nth-child(5)
    
        item['body'] = " ".join(response.css('.top_left_container > div > p').xpath('string()').extract())        

        yield item 