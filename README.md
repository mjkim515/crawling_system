# crawling_system


## 코드 작성 및 테스트

1. **Spider 생성**
    1. **scrapy genspider** [spider이름] [target address]
        - 예) scrapy genspider donga donga.com
        
2. **Spider 작성** : **신문사 기사 추출 방법**
    1. **F12 or 오른쪽 마우스 클릭 -> 검사를 통해 HTML 소스코드 분석요**
        
        
        | 제주일보
        Jejunews.com
         
        python code : 
        ../spider/jeju.py | start_urls = ['http://www.jejunews.com/news/articleList.html']
         
        parse:
        def start_requests(self):
             for i in range(1, 100, 20):
                 yield scrapy.Request("http://www.jejunews.com/news/articleList.html?page=" + str(i))
         
        parse topic:
        item['body'] = " ".join(response.css('.user-content p')\
              .xpath('string()')\
              .extract())
         
        link = response.css('div.list-titles a::attr("href")').extract()
         |
        | --- | --- |
3. **scrapy shell test 방법 [예: 제주일보 ]**
    1. **scrapy shell** [http://www.jejunews.com/news/articleView.html?idxno=2189206](http://www.jejunews.com/news/articleView.html?idxno=2189206)
        - response.css('.user-content p::text').extract()
        - response.css('.user-content p').xpath('string()').extract())
        - response.url
        
4. **Spider 실행 – 뉴스기사 crawling**
    1. **scrapy crawl** [spider 이름] -o [scrapy output]
        - 예) scrapy crawl donga -o donga.jl
    2. **Output file :** { 기사제목, 기사 URL, 기사내용 }을 포함하는 jl파일
    
5. **형태소 분석 실행 및 csv 파일 생성: word_frequency.py**
    1. python **word_frequency.py** [ input jl file ] [ output csv ]
        - python word_frequency.**py** donga.jl donga.csv
        - python word_frequency.**py** jeju.jl jeju.csv
        
6. **형태소 분석 후, Word 빈도수 top 20 추출: word_count.py**
    1. python **word_count.py [ input jl ] [ newspaper name ]**
        - python word_count.**py** jeju.jl jeju
        - python word_count.**py** jeolla.jl jeolla
    2. 키워드 개수 변경 방법
        - **frequency.most_common(20):**
        - 위의 20을 원하는 숫자로 변경
        
7. **Word2Vec을 통해 model 생성: word_word2vec.py**
    1. **모델링 생성 방법 ( output => ***.model, morpho)**
        - python **word_word2vec.py** [ input.jl ] [ outputmodel_name ]
        - python **word_word2vec.py** hani.jl hani
        - input.jl은 **word_word2vec.py를 먼저 실행하여 생성**
    2. **Top 키워드 추출과 모델 생성 동시진행**
        - Python **count_word2vec.py** [ input jl file ] [ output model name]****
        - Python **count_word2vec.py** gyeongsang.jl gyeongsang
        - **Output files : 1)***.csv,  2)model, 3)txt**
        
8. **Word2Vec을 통해 유사단어 검출 테스트: word_word2vec_test.py**
    1. **python word_word2vec_test.py** [ input model name ] [ keyword ]
        - python **word_word2vec_test.py** jeju.model 사업
        - python **word_word2vec_test.py** hani300.model 후보
