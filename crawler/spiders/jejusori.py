# - 제주의소리 [jejusori] - f
# 1 page 
# http://www.jejusori.net/
# http://www.jejusori.net/news/articleList.html?view_type=sm

import scrapy

from crawler.items import Headline

class JejusoriSpider(scrapy.Spider):
    name = 'jejusori'
    allowed_domains = ['www.jejusori.net']
    start_urls = ['http://www.jejusori.net/']

    def start_requests(self):

        for i in range(1, 6): 
            yield scrapy.Request("http://www.jejusori.net/news/articleList.html?page=" + str(i))
            #http://www.jejusori.net/news/articleList.html?page=2
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('div.list-titles a::attr("href")').extract()
        #/news/articleView.html?idxno=338369

        for urla in link:
            url = "http://www.jejusori.net"+ urla;
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

        #//*[@id="article-view-content-div"]/p[1]/text()
        item['body'] = " ".join(response.xpath('//*[@id="article-view-content-div"]/p/text()').extract())

        yield item 