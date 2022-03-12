@echo off

echo ==============================================================================================
echo [ %date% %time% ] Crawl and Generate Word2vec model > crawl_log_%date%..txt
echo ==============================================================================================

echo scrapy crawl [input spyder_filename] -o [output jl_filename] 
echo python word_count_word2vec.py [input jl_filename] [output word2vec_model_name] 


echo    1. [ %time% - Jeju Start ] >> crawl_log_%date%.txt
scrapy crawl jeju -o jeju_%date%.jl
scrapy crawl jejusori -o jeju_%date%.jl
scrapy crawl halla -o jeju_%date%.jl

python word_count_word2vec.py jeju_%date%.jl jeju_%date%


echo    2. [ %time% - Chungcheong Start ]  >> crawl_log_%date%.txt
scrapy crawl cbilbo -o chungcheong_%date%.jl 
scrapy crawl ccdn -o chungcheong_%date%.jl 
scrapy crawl gmcc -o chungcheong_%date%.jl  
scrapy crawl ccnnews -o chungcheong_%date%.jl  

python word_count_word2vec.py chungcheong_%date%.jl  chungcheong_%date%

	
echo    3. [ %time% - Jeolla Start ]  >> crawl_log_%date%.txt
scrapy crawl jbdomin -o jeolla_%date%.jl
scrapy craw jjan -o  jeolla_%date%.jl
scrapy crawl jnilbo -o jeolla_%date%.jl

python word_count_word2vec.py jeolla_%date%.jl jeolla_%date%

echo    4. [ %time% - Gyeongsang Start ] >> crawl_log_%date%.txt
scrapy crawl kbilbo -o gyeongsang_%date%.jl 
scrapy crawl dgilbo  -o gyeongsang_%date%.jl 
scrapy crawl imaeil -o gyeongsang_%date%.jl
scrapy crawl idaegu -o gyeongsang_%date%.jl
scrapy crawl hidomin -o gyeongsang_%date%.jl

python word_count_word2vec.py gyeongsang_%date%.jl gyeongsang_%date%

echo    5. [ %time% - Gangwon Start ] >> crawl_log_%date%.txt
scrapy crawl wonju -o gangwon_%date%.jl
scrapy crawl kado -o gangwon_%date%.jl
scrapy crawl gwunion -o gangwon_%date%.jl

python word_count_word2vec.py gangwon_%date%.jl gangwon_%date%

echo    6. [ %time% - Gyeonggi Start ]  >> crawl_log_%date%.txt
scrapy crawl incheon -o gyeonggi_%date%.jl
scrapy crawl kyeongin -o gyeonggi_%date%.jl
scrapy crawl kbnews -o gyeonggi_%date%.jl

python word_count_word2vec.py gyeonggi_%date%.jl gyeonggi_%date%


echo ==============================================================================================
echo [ %date% %time% ] Word2vec model generation end !!! >> crawl_log_%date%.txt
echo ==============================================================================================


echo ==============================================================================================
echo    Related word search and extraction !!!
echo 
echo    setting : max_related_words = 10
echo    python word_word2vec_extracion.py jeju_%date%
echo ==============================================================================================
echo ==============================================================================================
echo [ %date% %time% ] Related word extraction start!! >> crawl_log_%date%.txt
echo ==============================================================================================

python word_word2vec_extraction.py  jeju_%date%
python word_word2vec_extraction.py  chungcheong_%date%
python word_word2vec_extraction.py  jeolla_%date%
python word_word2vec_extraction.py  gyeongsang_%date%
python word_word2vec_extraction.py  gangwon_%date%
python word_word2vec_extraction.py  gyeonggi_%date%

echo ==============================================================================================
echo [ %date% %time% ] Related words saved!! >> crawl_log_%date%.txt
echo ==============================================================================================

move *.jl ./../data
move *.csv ./../data
move *.model ./../data
move *.txt ./../data

del *.morpho