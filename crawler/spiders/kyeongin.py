import scrapy

from crawler.items import Headline

class KyeonginSpider(scrapy.Spider):
    name = 'kyeongin'
    allowed_domains = ['www.kyeongin.com']
    start_urls = ['http://www.kyeongin.com/']

    def start_requests(self):
        for i in range(1, 3): 
            yield scrapy.Request("http://www.kyeongin.com/main/news.php?page=" + str(i))
             
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('h4.news-title a::attr("href")').extract()
        #link ->' view.php?key=20220304010000862'

        # http://www.kyeongin.com/main/view.php?key=20220304010000862

        for urla in link:
            url = "http://www.kyeongin.com/main/"+ urla;

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
        item['body'] = response.css('.article::text').extract()

        yield item 