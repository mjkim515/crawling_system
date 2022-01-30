import sys

import matplotlib.pyplot as plt

from gensim.models import word2vec

plt.rc('font', family='Malgun Gothic')

# 바 그래프 그리기

def showGraph(bargraph, inputword):

     xtick = [item[0] for item in bargraph] # 단어

     ytick = [item[1] for item in bargraph] # 유사도

     plt.figure()

     mycolors = ['#06c2ac', '#c79fef', '#ff796c', '#aaff32', '#0485d1', '#d648d7', '#a5a502', '#d8dcd6', '#5ca904', '#fffe7a' ]
     title = "[ " + inputword + " ] 유사단어 검출 결과"
     plt.title(title)
     plt.bar(xtick, ytick, color=mycolors)


# 모델 불러오기

model_filename = 'jeju.model'

model = word2vec.Word2Vec.load(model_filename)

inputword = sys.argv[1] 
print("Input keyword : ", inputword)

# 유사도 구하기

# 코로나 이라는 단어와 유사도가 높은 단어 10개를 리스트로 반환

bargraph = model.wv.most_similar(positive=[inputword])

showGraph(bargraph, inputword)

plt.show()

