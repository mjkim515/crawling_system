
# - 전남일보 [jnilbo] - 
# 1 page 20 articles
# https://www.jnilbo.com/
# https://www.jnilbo.com/opinion?page=2


import scrapy

from crawler.items import Headline

class JnilboSpider(scrapy.Spider):
    name = 'jnilbo'
    allowed_domains = ['www.jnilbo.com']
    start_urls = ['http://www.jnilbo.com/']

    def start_requests(self):

        for i in range(1, 3): 
            for part in ["opinion", "politics", "admin_parliament", "society&education", "jeonnam", "weeklyissue"]:
                yield scrapy.Request("http://www.jnilbo.com/"+ part + "?page=" + str(i))
                # https://www.jnilbo.com/opinion?page=2
            
    
    def parse(self, response):
        """
        메인 페이지의 토픽 목록에서 링크를 추출하고 출력합니다.
        """
        link = response.css('div.box a::attr("href")').extract()
        
        for urla in link:
            url = "https://www.jnilbo.com"+ urla;
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
        item['body'] = " ".join(response.css('.article_content p').xpath('string()').extract())
        #//*[@id="culture_section_list"]/li[1]/div/p[1]
        #//*[@id="culture_section_list"]/li[3]/div[2]/p[1]/a
        yield item 
