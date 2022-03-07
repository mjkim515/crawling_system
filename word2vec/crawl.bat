@echo off


echo =============================================================================
echo [ %date% %time% ] Crawl and Generate Word2vec model > crawl_log_%date%..txt
echo =============================================================================

echo scrapy crawl [input spyder_filename] -o [output jl_filename] 
echo python count_word2vec.py [input jl_filename] [output word2vec_model_name] 


echo    1. [ %time% - Jeju Start ] >> crawl_log_%date%.txt
scrapy crawl jeju -o jeju.jl
scrapy crawl jejusori -o jeju.jl
scrapy crawl halla -o jeju.jl

python count_word2vec.py jeju.jl jeju


echo    2. [ %time% - Chungcheong Start ]  >> crawl_log_%date%.txt
scrapy crawl cbilbo -o chungcheong.jl 
scrapy crawl ccdn -o chungcheong.jl
scrapy crawl gmcc -o chungcheong.jl 
scrapy crawl ccnnews -o chungcheong.jl 

python count_word2vec.py chungcheong.jl chungcheong

	
echo    3. [ %time% - Jeolla Start ]  >> crawl_log_%date%.txt
scrapy crawl jbdomin -o jeolla.jl
scrapy craw jjan -o  jeolla.jl
scrapy crawl jnilbo -o jeolla.jl

python count_word2vec.py jeolla.jl jeolla

echo    4. [ %time% - Gyeongsang Start ] >> crawl_log_%date%.txt
scrapy crawl kbilbo -o gyeongsang.jl 
scrapy crawl dgilbo  -o gyeongsang.jl 
scrapy crawl imaeil -o gyeongsang.jl
scrapy crawl idaegu -o gyeongsang.jl
scrapy crawl hidomin -o gyeongsang.jl

python count_word2vec.py gyeongsang.jl gyeongsang

echo    5. [ %time% - Gangwon Start ] >> crawl_log_%date%.txt
scrapy crawl wonju -o gangwon.jl
scrapy crawl kado -o gangwon.jl
scrapy crawl gwunion -o gangwon.jl

python count_word2vec.py gangwon.jl gangwon

echo    6. [ %time% - Gyeonggi Start ]  >> crawl_log_%date%.txt
scrapy crawl incheon -o gyeonggi.jl
scrapy crawl kyeongin -o gyeonggi.jl
scrapy crawl kbnews -o gyeonggi.jl

python count_word2vec.py gyeonggi.jl gyeonggi


echo ==========================================================================
echo [ %date% %time% ] End !!! >> crawl_log_%date%.txt
echo ==========================================================================