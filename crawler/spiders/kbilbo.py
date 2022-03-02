# - 경북일보[kbilbo] - 
# 1 page 20 articles
# https://www.kyongbuk.co.kr/
# https://www.kyongbuk.co.kr/news/articleList.html?page=2



import scrapy

from crawler.items import Headline

class KbilboSpider(scrapy.Spider):
    name = 'kbilbo'
    allowed_domains = ['www.kyongbuk.co.kr']
    start_urls = ['http://www.kyongbuk.co.kr/']

    def start_requests(self):
        for i in range(1, 4): 
            yield scrapy.Request("https://www.kyongbuk.co.kr/news/articleList.html?page=" + str(i))
                #https://www.kyongbuk.co.kr/news/articleList.html?page=1
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('div.list-titles a::attr("href")').extract()
        #'/news/articleView.html?idxno=2093870'

        for urla in link:
            url = "https://www.kyongbuk.co.kr"+ urla;
            #https://www.domin.co.kr/news/articleView.html?idxno=1371215&sc_section_code=S1N4

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
        #//*[@id="article-view-content-div"]/p/text()[1]
        item['body'] = "".join(response.xpath('//*[@id="article-view-content-div"]/p/text()').extract())
        if not (item['body']):
            item['body'] = " ".join(response.xpath('//*[@id="article-view-content-div"]/text()').extract())
        #item['body'] = " ".join(response.css('.user-content p').xpath('string()').extract())
        yield item 