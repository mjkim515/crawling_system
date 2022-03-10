@echo off


echo ==============================================================================================
echo [ $(date "+%Y-%m-%d %H:%M:%S") ] Crawl and Generate Word2vec model > crawl_jejulog_$(date "+%Y-%m-%d").txt
echo ==============================================================================================


echo scrapy crawl [input spyder_filename] -o [output jl_filename] 
echo python count_word2vec.py [input jl_filename] [output word2vec_model_name] 


echo    1. [ %time% - Jeju Start ] >> crawl_log_$(date "+%Y-%m-%d").txt
scrapy crawl jeju -o jeju_$(date "+%Y-%m-%d").jl
scrapy crawl jejusori -o jeju_$(date "+%Y-%m-%d").jl
scrapy crawl halla -o jeju_$(date "+%Y-%m-%d").jl

python count_word2vec.py jeju_%date%.jl jeju_$(date "+%Y-%m-%d")

echo ==============================================================================================
echo [ $(date "+%Y-%m-%d %H:%M:%S") ] End !!! >> crawl_jejulog_$(date "+%Y-%m-%d").txt
echo ==============================================================================================