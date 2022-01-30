import scrapy

from crawler.items import Headline


class JejuSpider(scrapy.Spider):
    name = 'jeju'
    allowed_domains = ['jejunews.com']
    #start_urls = ['http://jejunews.com/']
    start_urls = ['http://www.jejunews.com/news/articleList.html']

    def start_requests(self):
        # range (1, n) --> page=1 ~ page=(n-1)
        # 1 page is including 20 articles
        # ex) range(1, 3) => page=1, page=2, total articles = 40
        # by mjkim
        for i in range(1, 6):  #total 40 articles
            yield scrapy.Request("http://www.jejunews.com/news/articleList.html?page=" + str(i))
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('div.list-titles a::attr("href")').extract()
        
        for urla in link:
            url = "http://www.jejunews.com/"+ urla;
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
        item['body'] = " ".join(response.css('.user-content p')\
             .xpath('string()')\
             .extract())
        #item['body'] = response.css('.user-content p::text').extract()
        #item['body'] = response.css('.user-content p').xpath('string()').extract()
        yield item
        

