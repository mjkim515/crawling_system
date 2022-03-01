# 충북일보 [cbilbo] 
# 1page = 25 article
# http://www.inews365.com
# https://www.inews365.com/news/article_list_all.html?page=1

import scrapy

from crawler.items import Headline

class CbilboSpider(scrapy.Spider):
    name = 'cbilbo'
    allowed_domains = ['www.inews365.com']
    start_urls = ['http://www.inews365.com/']

    def start_requests(self):

        for i in range(1, 5):       
            yield scrapy.Request("https://www.inews365.com/news/article_list_all.html?page=" + str(i))
            #https://www.inews365.com/news/article_list_all.html?page=1
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """

        #xpath = //*[@id="alt1"]/ul/li/a
        link = response.xpath('//*[@id="alt1"]/ul/li/a/@href').extract()
        # link = article.html?no=702242      
        # https://www.inews365.com/news/article.html?no=702242
        
        for urla in link:
            url = "https://www.inews365.com/news/"+ urla;
            # 광고 페이지 제외
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
        item['body'] = response.css('.article::text').extract()
        #item['body'] = response.xpath('//*[@id="news_body_area"]/div/text()').extract()
    
        yield item 