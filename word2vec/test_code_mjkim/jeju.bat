@echo off


echo ==============================================================================================
echo [ %date% %time% ] Crawl and Generate Word2vec model > crawl_jejulog_%date%.txt
echo ==============================================================================================

echo scrapy crawl [input spyder_filename] -o [output jl_filename] 
echo python word_count_word2vec.py [input jl_filename] [output word2vec_model_name] 


echo    1. [ %time% - Jeju Start ] >> crawl_jejulog_%date%.txt
scrapy crawl jeju -o jeju_%date%.jl
scrapy crawl jejusori -o jeju_%date%.jl
scrapy crawl halla -o jeju_%date%.jl

python word_count_word2vec.py jeju_%date%.jl jeju_%date%

echo ==============================================================================================
echo [ %date% %time% ] Word2vec model generation end !!! >> crawl_jejulog_%date%.txt
echo ==============================================================================================
echo    Related word search and extraction !!!
echo    setting : max_related_words = 5
echo    python word_word2vec_extracion.py jeju_%date%
echo ==============================================================================================
echo [ %date% %time% ] Related word extraction start!! >> crawl_jejulog_%date%.txt
echo ==============================================================================================

python word_word2vec_extraction.py jeju_%date%

echo ==============================================================================================
echo [ %date% %time% ] Related words saved!! >> crawl_jejulog_%date%.txt
echo ==============================================================================================

move *.jl ./../data
move *.csv ./../data
move *.model ./../data
move *.txt ./../data

del *.morpho