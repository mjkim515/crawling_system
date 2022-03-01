# -  대구일보[dgilbo] 
# 1 page 15 articles
# https://www.idaegu.com/
# https://www.idaegu.com/newsList/?page=1


import scrapy

from crawler.items import Headline

class DgilboSpider(scrapy.Spider):
    name = 'dgilbo'
    allowed_domains = ['www.idaegu.com']
    start_urls = ['http://www.idaegu.com/']

    def start_requests(self):
        for i in range(1, 8):       
            yield scrapy.Request("https://www.idaegu.com/newsList/?page=" + str(i))
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """

        #xpath = //*[@id="container"]/div/div[1]/div[1]/ul/li/a[1]/@href
        #1 article 당 a href tag 3개 존재 a[1]으로 지정하지 않을 시 중복 된 article이 scrapped...
        link = response.xpath('//*[@id="container"]/div/div[1]/div[1]/ul/li/a[1]/@href').extract()
        # link = /newsView/idg202202100034 
        # https://www.idaegu.com/newsView/idg202202100034
        
        for urla in link:
            url = "https://www.idaegu.com"+ urla;
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
        
        #//*[@id="articleContent"]/p/text()
        #//*[@id="articleContent"]/text()
        item['body'] =" ".join(response.xpath('//*[@id="articleContent"]/text()').extract())
    
        yield item 