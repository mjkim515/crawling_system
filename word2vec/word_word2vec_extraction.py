#-*- coding:utf-8 -*-

#===============================================================================
#
#  실행방법 : python word_word2vec_extraction.py [input 지역_date]
#  
#  ex) python word_word2vec_extraction.py jeju_%date%
#
#===============================================================================

import sys
import csv
import matplotlib.pyplot as plt

from gensim.models import word2vec

max_save_count = 5 

# Windows
plt.rc('font', family='Malgun Gothic')
# ubuntu
# plt.rc('font', family='/usr/share/fonts/truetype/nanum/NanumGothic.ttf')


# 바 그래프 그리기
def saveGraph(bargraph, inputword):

    xtick = [item[0] for item in bargraph] # 단어

    ytick = [item[1] for item in bargraph] # 유사도

    plt.figure()
    mycolors = ['#06c2ac', '#06c2ac', '#c79fef','#c79fef', '#ff796c', '#ff796c', \
                '#aaff32', '#aaff32', '#0485d1', '#0485d1', '#a5a502', '#a5a502']
                
    title = model_filename + " [ " + inputword + " ] 연관어 검출 결과"
    plt.title(title)
    plt.bar(xtick, ytick, color=mycolors)


# 모델 불러오기

model_filename = sys.argv[1] + ".model" # model name
top20_filename = sys.argv[1] + "_top20.csv" #top20 keyworkd file

model = word2vec.Word2Vec.load(model_filename)
save_count = 0

# Read keywords from top20.csv and extract related words from word2vec model 
with open(top20_filename, 'r', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        #print(row['word'])
        if save_count > max_save_count :
            break

        inputword = row['word']
        bargraph = model.wv.most_similar(positive=[inputword])
       
        saveGraph(bargraph, inputword)
        #plt.show()
        save_path = "./../data/" + sys.argv[1] + "_"+ inputword + ".png"
        print("saved : " + save_path)
        plt.savefig(save_path)
        save_count += 1
