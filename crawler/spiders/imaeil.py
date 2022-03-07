# 
# 매일신문 [imaeil] 
# 1 page 30 articles
# http://news.imaeil.com/
# http://news.imaeil.com/latest_article?page=1….n
# 


import scrapy

from crawler.items import Headline

class ImaeilSpider(scrapy.Spider):
    name = 'imaeil'
    allowed_domains = ['news.imaeil.com']
    start_urls = ['http://news.imaeil.com/']

    def start_requests(self):
        for i in range(1, 3):       
            yield scrapy.Request("http://news.imaeil.com/latest_article?page=" + str(i))
            
    #http://news.imaeil.com/latest_article?page=1

    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """

        #xpath = //*[@id="container"]/div/div[1]/div[1]/ul/li/a[1]/@href
      
        link = response.xpath('//*[@id="container"]/div[2]/div[1]/div/ul/li/p[1]/a/@href').extract()
        #'/page/view/2022030213213559807', '/page/view/2022030213202801317', 

        # link = /news/articleView.html?idxno=374145'
        # https://www.idaegu.co.kr/news/articleView.html?idxno=374145'
        
        for urla in link:
            url = "http://news.imaeil.com/"+ urla;
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
        
        #item['body'] = " ".join(response.xpath('//*[@id="articlebody"]/p/text()').extract())
        item['body']  = response.xpath('//*[@id="articlebody"]/p/text()').extract()
    
        yield item 

