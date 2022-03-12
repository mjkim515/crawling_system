@echo off

echo =============================================================================
echo    Count words, extract top20 word, and generate word2vec model
echo =============================================================================

echo python count_word2vec.py [input jl_filename] [output word2vec_model_name] 

python count_word2vec.py jeju_%date%.jl jeju_%date%
python count_word2vec.py chungcheong_%date%.jl chungcheong_%date%
python count_word2vec.py jeolla_%date%.jl jeolla_%date%
python count_word2vec.py gyeongsang_%date%.jl gyeongsang_%date%
python count_word2vec.py gangwon_%date%.jl gangwon_%date%
python count_word2vec.py gyeonggi_%date%.jl gyeonggi_%date%