@echo off


echo ==============================================================================================
echo Date=$(date "+%Y-%m-%d")
echo
echo [ $(date "+%Y-%m-%d %H:%M:%S")] Crawl and Generate Word2vec model > crawl_log_$(date "+%Y-%m-%d").txt
echo ==============================================================================================

echo scrapy crawl [input spyder_filename] -o [output jl_filename] 
echo python count_word2vec.py [input jl_filename] [output word2vec_model_name] 


echo    1. [ %time% - Jeju Start ] >> crawl_log_$(date "+%Y-%m-%d").txt
scrapy crawl jeju -o jeju_$(date "+%Y-%m-%d").jl
scrapy crawl jejusori -o jeju_$(date "+%Y-%m-%d").jl
scrapy crawl halla -o jeju_$(date "+%Y-%m-%d").jl

python count_word2vec.py jeju_%date%.jl jeju_$(date "+%Y-%m-%d")


echo    2. [ %time% - Chungcheong Start ]  >> crawl_log_$(date "+%Y-%m-%d").txt
scrapy crawl cbilbo -o chungcheong_$(date "+%Y-%m-%d").jl 
scrapy crawl ccdn -o chungcheong_$(date "+%Y-%m-%d").jl 
scrapy crawl gmcc -o chungcheong_$(date "+%Y-%m-%d").jl  
scrapy crawl ccnnews -o chungcheong_$(date "+%Y-%m-%d").jl  

python count_word2vec.py chungcheong_%date%.jl  chungcheong_$(date "+%Y-%m-%d")

	
echo    3. [ %time% - Jeolla Start ]  >> crawl_log_$(date "+%Y-%m-%d").txt
scrapy crawl jbdomin -o jeolla_$(date "+%Y-%m-%d").jl
scrapy craw jjan -o  jeolla_$(date "+%Y-%m-%d").jl
scrapy crawl jnilbo -o jeolla_$(date "+%Y-%m-%d").jl

python count_word2vec.py jeolla_%date%.jl jeolla_$(date "+%Y-%m-%d")


echo    4. [ %time% - Gyeongsang Start ] >> crawl_log_$(date "+%Y-%m-%d").txt
scrapy crawl kbilbo -o gyeongsang_$(date "+%Y-%m-%d").jl 
scrapy crawl dgilbo  -o gyeongsang_$(date "+%Y-%m-%d").jl 
scrapy crawl imaeil -o gyeongsang_$(date "+%Y-%m-%d").jl
scrapy crawl idaegu -o gyeongsang_$(date "+%Y-%m-%d").jl
scrapy crawl hidomin -o gyeongsang_$(date "+%Y-%m-%d").jl

python count_word2vec.py gyeongsang_%date%.jl gyeongsang_$(date "+%Y-%m-%d")


echo    5. [ %time% - Gangwon Start ] >> crawl_log_$(date "+%Y-%m-%d").txt
scrapy crawl wonju -o gangwon_$(date "+%Y-%m-%d").jl
scrapy crawl kado -o gangwon_$(date "+%Y-%m-%d").jl
scrapy crawl gwunion -o gangwon_$(date "+%Y-%m-%d").jl

python count_word2vec.py gangwon_%date%.jl gangwon_$(date "+%Y-%m-%d")


echo    6. [ %time% - Gyeonggi Start ]  >> crawl_log_$(date "+%Y-%m-%d").txt
scrapy crawl incheon -o gyeonggi_$(date "+%Y-%m-%d").jl
scrapy crawl kyeongin -o gyeonggi_$(date "+%Y-%m-%d").jl
scrapy crawl kbnews -o gyeonggi_$(date "+%Y-%m-%d").jl

python count_word2vec.py gyeonggi_%date%.jl gyeonggi_$(date "+%Y-%m-%d")


echo ==============================================================================================
echo [ $(date "+%Y-%m-%d %H:%M:%S") ] End !!! >> crawl_log_$(date "+%Y-%m-%d").txt
echo ==============================================================================================

rm *.morpho
