# - 강원지방신문  - 
# 1 page 20 article
# http://www.gwunion.co.kr/
# http://www.gwunion.co.kr/news/articleList.html?page=1
#


import scrapy

from crawler.items import Headline

class GwunionSpider(scrapy.Spider):
    name = 'gwunion'
    allowed_domains = ['www.gwunion.co.kr']
    start_urls = ['http://www.gwunion.co.kr/news/articleList.html']

    def start_requests(self):
        for i in range(1, 11): 
            yield scrapy.Request("http://www.gwunion.co.kr/news/articleList.html?page=" + str(i))
            
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('td.ArtList_Title a::attr("href")').extract()
        #link -> 'articleView.html?idxno=14554', 'articleView.html?idxno=14553', ...
        
        # http://www.gwunion.co.kr/news/articleView.html?idxno=14554
        for urla in link:
            url = "http://www.gwunion.co.kr/news/"+ urla;

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
        item['body'] = " ".join(response.xpath('//*[@id="articleBody"]/p/text()').extract())

        yield item 