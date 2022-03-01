@echo off

echo ==========================================================================
echo    Crawl and Generate JL file 
echo ==========================================================================

echo scrapy crawl [input spyder_filename] -o [output jl_filename] 

echo 1. 제주 ==================================================================
scrapy crawl jeju -o jejunew.jl
scrapy crawl jejusori -o jejunew.jl
scrapy crawl halla -o jejunew.jl

echo 2. 충청 ==================================================================
scrapy crawl cbilbo -o chungcheong_new.jl 
scrapy crawl ccdn -o chungcheong_new.jl 
scrapy crawl ccnnews -o chungcheong_new.jl 
	
echo 3. 전라 ==================================================================
scrapy crawl jbdomin -o jeolla_new.jl
scrapy craw jjan -o  jeolla_new.jl
scrapy crawl jnilbo -o jeolla_new.jl(코롤링 너무 많이 됨)

echo 4. 경상 ==================================================================
scrapy crawl kbilbo -o gyeongsang_new.jl 
scrapy crawl dgilbo  -o gyeongsang_new.jl 
scrapy crawl knnews -o gyeongsang_new.jl 

echo 5. 강원 ==================================================================
scrapy crawl wonju -o gangwon_new.jl
scrapy crawl kado -o gangwon_new.jl
scrapy crawl gwunion -o gangwon_new.jl

echo 6. 경기 ==================================================================
scrapy crawl  incheon -o gyeonggi_new.jl
scrapy crawl snilboi -o gyeonggi_new.jl
scrapy crawl kbnews -o gyeonggi_new.jl