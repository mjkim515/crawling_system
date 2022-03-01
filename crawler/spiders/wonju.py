# • 원주투데이[kado] - finished
# 1 page 20 articles
# http://www.wonjutoday.co.kr/
# http://www.wonjutoday.co.kr/news/articleList.html?page=2


import scrapy

from crawler.items import Headline

class WonjuSpider(scrapy.Spider):
    name = 'wonju'
    allowed_domains = ['www.wonjutoday.co.kr']
    start_urls = ['http://www.wonjutoday.co.kr/']

    def start_requests(self):
        for i in range(1, 6):       
            yield scrapy.Request("http://www.wonjutoday.co.kr/news/articleList.html?page=" + str(i))
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """

        #xpath = //*[@id="ND_Warp"]/table[1]/tbody/tr/td[1]/table[1]/tbody/tr/td/table/tbody/tr/td[1]/a
        #css =  ND_Warp > table:nth-child(1) > tbody > tr > td:nth-child(1) > table:nth-child(1) > tbody > \
        #       tr > td > table > tbody > tr:nth-child(4) > td.ArtList_Titl
        link = response.css('td.ArtList_Title a::attr("href")').extract()
        # link = articleView.html?idxno=124670, articleView.html?idxno=124669, ...
        # http://www.wonjutoday.co.kr/news/articleView.html?idxno=124670
        
        for urla in link:
            url = "http://www.wonjutoday.co.kr/news/"+ urla;
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
        
        #//*[@id="articleBody"]/p[1]/text()
        item['body'] = response.xpath('//*[@id="articleBody"]/p/text()').extract()
    
        yield item 