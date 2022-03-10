@echo off

echo ==============================================================================================
echo    Related word search and extraction !!!
echo 
echo    setting : max_related_words = 10
echo    python word_word2vec_extracion.py jeju_%date%
echo ==============================================================================================


python word_word2vec_extracion.py  jeju_%date%
python word_word2vec_extracion.py  chungcheong_%date%
python word_word2vec_extracion.py  jeolla_%date%
python word_word2vec_extracion.py  gyeongsang_%date%
python word_word2vec_extracion.py  gangwon_%date%
python word_word2vec_extracion.py  gyeonggi_%date%