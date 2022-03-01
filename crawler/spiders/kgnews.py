# - 경기신문 - 
# 1 page - 10 articles
# https://www.kgnews.co.kr
# https://www.kgnews.co.kr/news/section_list_all.html?sec_no=0&page=1…n


import scrapy

from crawler.items import Headline

class KgnewsSpider(scrapy.Spider):
    name = 'kgnews'
    allowed_domains = ['www.kgnews.co.kr']
    start_urls = ['http://www.kgnews.co.kr/']

    def start_requests(self):
        for i in range(1, 11): 
            yield scrapy.Request("https://www.kgnews.co.kr/news/section_list_all.html?sec_no=0&page=" + str(i))
            
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('ul.art_list_all a::attr("href")').extract()
        #link -> '/news/article.html?no=689075', '/news/article.html?no=689106',...
        
        # https://www.kgnews.co.kr/news/article.html?no=689255
        for urla in link:
            url = "https://www.kgnews.co.kr"+ urla;

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
        item['body'] = " ".join(response.xpath('//*[@id="news_body_area"]/p/text()').extract())

        yield item 