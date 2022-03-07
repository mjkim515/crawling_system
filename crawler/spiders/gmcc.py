import scrapy

from crawler.items import Headline

class GmccSpider(scrapy.Spider):
    name = 'gmcc'
    allowed_domains = ['www.goodmorningcc.com']
    start_urls = ['http://www.goodmorningcc.com/']

    def start_requests(self):
        for i in range(1, 3): 
            yield scrapy.Request("http://www.goodmorningcc.com/news/articleList.html?page=" + str(i))
             
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('div.list-titles a::attr("href")').extract()
        #link ->'/news/articleView.html?idxno=265568'

        # http://www.goodmorningcc.com/news/articleView.html?idxno=265547

        for urla in link:
            url = "http://www.goodmorningcc.com"+ urla;

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
        item['body'] = response.xpath('//*[@id="article-view-content-div"]/p/text()').extract()

        yield item 
