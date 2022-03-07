@echo off

echo ==========================================================================
echo  [ Jeju ] Crawl and Generate JL file 
echo ==========================================================================

echo scrapy crawl [input spyder_filename] -o [output jl_filename] 
echo python count_word2vec.py [input jl_filename] [output word2vec_model_name] 


echo 1. [ Jeju Start ] =========================================================
scrapy crawl jeju -o jeju.jl
scrapy crawl jejusori -o jeju.jl
scrapy crawl halla -o jeju.jl

python count_word2vec.py jeju.jl jeju

echo  =============================================================