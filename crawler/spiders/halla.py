# 
# 한라일보 [halla] 
# 1 page 15 articles
# http://www.ihalla.com/
# https://www.ihalla.com/articles.php?&page=1….n
# 
import scrapy


from crawler.items import Headline

class HallaSpider(scrapy.Spider):
    name = 'halla'
    allowed_domains = ['www.ihalla.com']
    start_urls = ['http://www.ihalla.com']

    def start_requests(self):
        for i in range(1, 8): 
            yield scrapy.Request("http://www.ihalla.com/articles.php?&page=" + str(i))
            #https://www.ihalla.com/articles.php?&page=3 -by mjkim
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        #같은 URL이 3개씩 포함되어 있어서 a.subtile의 URL을 참조하게 함...  -by mkim
        #css :  body > div.wrap > div.container > div.cont_left > table > tbody > tr:nth-child(1) > td > a.subtitle
        link = response.css('div.cont_left a.subtitle::attr("href")').extract()
        #/article.php?aid=1644479251720698136 - by mjkim

        for urla in link:
            url = "http://www.ihalla.com"+ urla;
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
      

        item['body'] = response.css('.article_txt::text').extract()
        #item['body'] =" ".join(response.css('.article_txt::text').xpath('string()').extract())
        

        yield item 