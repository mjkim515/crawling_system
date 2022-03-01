# - 인천일보 -
# http://www.incheonilbo.com
# http://www.incheonilbo.com/news/articleList.html?page=1


import scrapy

from crawler.items import Headline

class IncheonSpider(scrapy.Spider):
    name = 'incheon'
    allowed_domains = ['www.incheonilbo.com']
    start_urls = ['http://www.incheonilbo.com/']

    def start_requests(self):
        for i in range(1, 6): 
            yield scrapy.Request("http://www.incheonilbo.com/news/articleList.html?page=" + str(i))
            
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('div.list-titles a::attr("href")').extract()
        #link -> '/news/articleView.html?idxno=1131543', '/news/articleView.html?idxno=1131542
        
        # http://www.incheonilbo.com/news/articleView.html?idxno=1131576
        for urla in link:
            url = "http://www.incheonilbo.com"+ urla;

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
        item['body'] = " ".join(response.xpath('//*[@id="article-view-content-div"]/p/text()').extract())

        yield item 