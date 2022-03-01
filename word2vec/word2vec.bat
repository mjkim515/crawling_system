@echo off

echo ====================================================
echo    Count words and extract top20 word
echo ====================================================

echo python count_word2vec.py [input jl_filename] [output word2vec_model_name] 

python count_word2vec.py jeju_new.jl jeju
python count_word2vec.py chungcheong_new.jl chungcheong
python count_word2vec.py jeolla_new.jl jeolla
python count_word2vec.py gyeongsang_new.jl gyeongsang
python count_word2vec.py gangwon_new.jl gangwon
python count_word2vec.py gyeonggi_new.jl gyeonggi