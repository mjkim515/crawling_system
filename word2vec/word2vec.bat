@echo off

echo ====================================================
echo    Count words and extract top20 word
echo ====================================================

echo python count_word2vec.py [input jl_filename] [output word2vec_model_name] 

python count_word2vec.py jeju.jl jeju
python count_word2vec.py chungcheong.jl chungcheong
python count_word2vec.py jeolla.jl jeolla
python count_word2vec.py gyeongsang.jl gyeongsang
python count_word2vec.py gangwon.jl gangwon
python count_word2vec.py gyeonggi.jl gyeonggi