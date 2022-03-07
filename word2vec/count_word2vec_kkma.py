
#===============================================================================
#
#  실행방법 : python count_word2vec.py [input jl filename] [output model & csv filename]
#  
#  ex) python count_word2vec.py jeju.jl  jeju
#
#===============================================================================

from lib2to3.pgen2.tokenize import tokenize
import sys
import json
import os
import csv
import time
import timeit

from glob import glob
from collections import Counter
from gensim.models import word2vec
from konlpy.tag import Kkma
#from konlpy.tag import Twitter


import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

def main():
    """
    명령라인 매개변수로 지정한
    디렉터리 내부의 파일을 읽어 들이고
    빈출 단어를 출력합니다.
    """

    #start_time = time.process_time()
    start_time = timeit.default_timer()

    #twitter = Twitter()
    kkma = Kkma()
    count_proccessed = 0

    path = sys.argv[1]
    paper_name = sys.argv[2]
    print('Processing {0}...'.format(path), file=sys.stderr)
   
    input_model_name = sys.argv[2]

    tokens = []
    results = []

    # 단어의 빈도를 저장하기 위한 Counter 객체를 생성합니다.
    # Counter 클래스는 dict를 상속받는 클래스입니다.           
    frequency = Counter()
 
    # 파일을 엽니다.
    with open(path, 'r', encoding="utf-8") as file:
        #파일 내부의 모든 기사에 반복을 돌립니다.
        for line in file.readlines():
            
            json_object = json.loads(line)
            content = ''.join(json_object['body'])
           

            #print (content)
            node = kkma.pos(content)
            for (taeso, pumsa) in node:
                 # 고유 명사와 일반 명사만 추출합니다.
                 if pumsa in ('NNG', 'NNP'):
                    tokens.append(taeso)
    

            count_proccessed += 1

        rl = (" ".join(tokens)).strip()
        results.append(rl)



    #모든 기사의 처리가 끝나면 상위 0개의 단어를 출력합니다
    print("=========================================")
    print('{0} documents were processed.'
          .format(count_proccessed),file=sys.stderr)
    print("=========================================")

    print('Total token 개수 : {}'.format(len(tokens)))
    print("=========================================")
    #print(tokens)
    #print("=========================================")
    #print('Total result 개수 : {}'.format(len(results)))
    #print(results)


    # Word2Vec 모델 만들기 
    print("word2vec 모델 생성 중 ...")
    wakati_file = input_model_name +"_kkma.txt"
    #print(wakati_file)

    with open(wakati_file, 'w', encoding="utf-8") as f:
        f.write("\n".join(results))

    data = word2vec.LineSentence(wakati_file)
    model = word2vec.Word2Vec(data, vector_size=100, window=10, hs=1, min_count=2, sg=1)

    model_name = input_model_name + '_kkma_win10.model'
    model.save(model_name)

    # 실행 시간을 측정할 코드
    end_time = timeit.default_timer()
    print("%f초 걸렸습니다." % (end_time - start_time))

    #end_time = time.process_time()
    #print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")

    print(model_name + ' 모델 저장됨!')
    print('-finished-')

    # top20 키워드 산출 및 csv 저장
    frequency.update(tokens)

    wordInfo = dict()
    path = paper_name + "_top keywords_kkma.csv"

    with open(path, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'count'])
        
        
        for word, count in frequency.most_common(30):
            if (len(str(word)) > 1):
                wordInfo[word] = count
                writer.writerow([word, count])       
                #print ("%s : %d" % (word, count))

        f.close()

    print("프로그램 종료...!!!")
    print("=========================================")

    showGraph(wordInfo, paper_name)



def showGraph(word_info, paper_name):
    """
    다빈도 단어 중 top20의 단어와 단어별 빈도수를 
    히스토그램 그래프로 나타낸다.
    """
    #font_location = "c:\Windows\Fonts\malgun.ttf"
    #font_name = font_manager.FontProperties(fname=font_location).get_name()
    path_gothic = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    font_name = font_manager.FontProperties(fname=path_gothic).get_name()
    matplotlib.rc('font', family=font_name) 

    plt.xlabel('주요 단어')
    plt.ylabel('빈도수')
    plt.grid(True)  

    Sorted_Dict_Values = sorted(word_info.values(), reverse=True)
    Sorted_Dict_Keys = sorted(word_info, key=word_info.get, reverse=True)   
 
    plt.title(paper_name + "_Top 20 키워드! [v.kkma 형태소]")
    plt.bar(range(len(word_info)), Sorted_Dict_Values, align='center')
    plt.xticks(range(len(word_info)), list(Sorted_Dict_Keys), rotation='70')  
    plt.show()



def iter_docs(file):
    """
    파일 객체를 읽어 들이고
    기사의 내용(시작 태그 <doc>와 종료 태그 </doc> 사이의 텍스트)를 꺼내는
    제너레이터 함수
    """
    for line in file:
        if line.startswith('{'):
            # 시작 태그가 찾아지면 버퍼를 초기화합니다.
            buffer = []
        elif line.startswith('}'):
            # 종료 태그가 찾아지면 버퍼의 내용을 결합한 뒤 yield합니다.
            content = ''.join(buffer)
            yield content
        else:
            # 시작 태그/종료 태그 이외의 줄은 버퍼에 추가합니다.
            buffer.append(line)

if __name__ == '__main__':
    main()
