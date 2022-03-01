
#
# - 충청뉴스 [ccnnews] - 
# 1 page 20 articles
# http://www.ccnnews.co.kr/
# http://www.ccnnews.co.kr/news/articleList.html?page=1
#

import scrapy

from crawler.items import Headline

class CcnnewsSpider(scrapy.Spider):
    name = 'ccnnews'
    allowed_domains = ['www.ccnnews.co.kr']
    start_urls = ['http://www.ccnnews.co.kr/']

    def start_requests(self):

        for i in range(1, 6):  
            yield scrapy.Request("http://www.ccnnews.co.kr/news/articleList.html?page=" + str(i))

    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('div.list-titles a::attr("href")').extract()
        #/news/articleView.html?idxno=247412', '/news/articleView.html?idxno=247410' .... - by mjkim

        for urla in link:
            url = "http://www.ccnnews.co.kr"+ urla;
            #http://www.ccnnews.co.kr/news/articleView.html?idxno=247392  - by mjkim

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
        #item['body'] = " ".join(response.css('.user-content p').xpath('string()').extract())
        item['body'] = " ".join(response.xpath('//*[@id="article-view-content-div"]/p/text()').extract())
  
        yield item
        
