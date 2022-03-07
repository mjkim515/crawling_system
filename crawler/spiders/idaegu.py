# 
# 매일신문 [imaeil] 
# 1 page 20 articles
# http://www.idaegu.co.kr/
# https://www.idaegu.co.kr/news/articleList.html?page=1….n
# 


from pandas import notnull
import scrapy

from crawler.items import Headline

class IdaeguSpider(scrapy.Spider):
    name = 'idaegu'
    allowed_domains = ['www.idaegu.co.kr']
    start_urls = ['http://www.idaegu.co.kr/']

    def start_requests(self):
        for i in range(1, 4):       
            yield scrapy.Request("https://www.idaegu.co.kr/news/articleList.html?page=" + str(i))
            
    #https://www.idaegu.co.kr/news/articleList.html?page=1

    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """

        #xpath = //*[@id="container"]/div/div[1]/div[1]/ul/li/a[1]/@href
      
        link = response.css('div.list-titles a::attr("href")').extract()
        # link = /news/articleView.html?idxno=374145'
        # https://www.idaegu.co.kr/news/articleView.html?idxno=374145'
        
        for urla in link:
            url = "https://www.idaegu.co.kr"+ urla;
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
        # print(item['body'])

        if not (item['body']):
           item['body'] = " ".join(response.css('.article p').xpath('string()').extract())
        
        if not (item['body']):
           item['body'] = " ".join(response.xpath('//*[@id="article-view-content-div"]/p/text()').extract())
    
        yield item 
