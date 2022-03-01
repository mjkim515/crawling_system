import scrapy

from crawler.items import Headline

class MkSpider(scrapy.Spider):
    name = 'mk'
    allowed_domains = ['mk.co.kr']
    start_urls = ['http://mk.co.kr/']


    # 크롤링을 시작할 URL 리스트
    def start_requests(self):
        for part in ["economy", "business", "society", "world", "realestate"]: # "Culture"]:        
            for i in range(0, 3): #page 1 == 0, page2 = 1, page3 = 2, page4 = 3, page5 = 4, page 6 = 5....
                yield scrapy.Request("http://www.mk.co.kr/news/" + part + "/?page=" + str(i))
                # https://www.mk.co.kr/news/economy/?page=0
                # ...
                # https://www.mk.co.kr/news/economy/?page=2        
                # https://www.mk.co.kr/news/business/?page=0         
                
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('dl.article_list a::attr("href")').extract()
        
        for url in link:
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
        # item['body'] = " ".join(response.css('.o-article_block p')\
        #     .xpath('string()')\
        #     .extract())
        item['body'] = response.css('.art_txt::text').extract()
        yield item
        

# robots.txt forbidden...... so failed.... by mjkim