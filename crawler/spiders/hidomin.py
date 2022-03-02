# 
# 경북도민일보 [hidomin] 
# 1 page 20 articles
# http://www.hidomin.com/
#https://www.hidomin.com/news/articleList.html?page=1….n
# 

import scrapy

from crawler.items import Headline

class HidominSpider(scrapy.Spider):
    name = 'hidomin'
    allowed_domains = ['www.hidomin.com']
    start_urls = ['http://www.hidomin.com/']

    def start_requests(self):
        for i in range(1, 3):       
            yield scrapy.Request("https://www.hidomin.com/news/articleList.html?page=1" + str(i))
            
    #https://www.hidomin.com/news/articleList.html?page=1

    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """

        #xpath = //*[@id="container"]/div/div[1]/div[1]/ul/li/a[1]/@href
      
        link = response.css('div.list-titles a::attr("href")').extract()
        # link = '/news/articleView.html?idxno=477652'
        # http://www.hidomin.com/news/articleView.html?idxno=477652'
        
        for urla in link:
            url = "http://www.hidomin.com"+ urla;
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
    
        item['body'] = " ".join(response.css('.article::text').extract())
        
        if not (item['body']):
           item['body'] = " ".join(response.xpath('//*[@id="article-view-content-div"]/text()').extract())
        
        #if not (item['body']):
        #   item['body'] = " ".join(response.xpath('//*[@id="article-view-content-div"]/p/text()').extract())
   
        yield item 

