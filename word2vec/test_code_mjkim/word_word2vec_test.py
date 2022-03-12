#-*- coding:utf-8 -*-

#===============================================================================
#
#  실행방법 : python word_word2vec_test.py [input modelname] [keword]
#  
#  ex) python word_word2vec.py donga.model  대선
#
#===============================================================================

import sys

import matplotlib.pyplot as plt

from gensim.models import word2vec

# Windows
plt.rc('font', family='Malgun Gothic')
# ubuntu
# plt.rc('font', family='/usr/share/fonts/truetype/nanum/NanumGothic.ttf')


# 바 그래프 그리기

def showGraph(bargraph, inputword):

     xtick = [item[0] for item in bargraph] # 단어

     ytick = [item[1] for item in bargraph] # 유사도

     plt.figure()

     mycolors = ['#06c2ac', '#06c2ac', '#c79fef','#c79fef', '#ff796c', '#ff796c', \
                 '#aaff32', '#aaff32', '#0485d1', '#0485d1', '#a5a502', '#a5a502']
                 
     title = model_filename + " [ " + inputword + " ] 연관어 검출 결과"
     plt.title(title)
     plt.bar(xtick, ytick, color=mycolors)


# 모델 불러오기

model_filename = sys.argv[1] # model name

model = word2vec.Word2Vec.load(model_filename)

inputword = sys.argv[2] # input keywords
print("Model Name : " + model_filename + "Input keyword : ", inputword)

# 유사도 구하기
# 유사도가 높은 단어 10개를 리스트로 반환
bargraph = model.wv.most_similar(positive=[inputword])

showGraph(bargraph, inputword)

# Similarity Test... 
#similarity_test = []
#similarity_test = model.wv.similarity('후보', '후보자')
#print ("사업 : " + str(similarity_test))

plt.show()

