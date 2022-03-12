
#==========================================================================================
#
#  실행방법 : python count_word2vec.py [input jl filename] [output model & csv filename]
#
#  ex) python word_count_word2vec.py jeju.jl  jeju
# 
#  Twitter 형태소 분석기 사용
#===========================================================================================

from lib2to3.pgen2.tokenize import tokenize
import sys
import json
import os
import csv
import timeit
from glob import glob
from collections import Counter
from gensim.models import word2vec
from konlpy.tag import Twitter


import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

def main():
    """
    명령라인 매개변수로 지정한
    디렉터리 내부의 파일을 읽어 들이고
    빈출 단어를 출력합니다.
    """

    start_time = timeit.default_timer()

    twitter = Twitter()
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
            #명사를 저장할 리스트입니다.
            # twitter 형태소 분리기 사용
            word_dic = {}
            text_lines = content.split("\r\n")

            for text in text_lines:
                malist = twitter.pos(text)
                #print(malist)
                for word in malist:
                    if ( word[1] == "Noun" ) : # or word[1] == "Verb" ):
                        #print(word[0])
                        if not (word[0] in word_dic):
                            word_dic[word[0]] = 0

                        word_dic[word[0]] += 1
                        tokens.append(word[0])
            # twitter 형태소 분리기 사용 END

         
            count_proccessed += 1

        rl = (" ".join(tokens)).strip()
        results.append(rl)
        #print(rl)




    #모든 기사의 처리가 끝나면 상위 0개의 단어를 출력합니다
    print("=========================================")
    print('{0} documents were processed.'
          .format(count_proccessed),file=sys.stderr)
    print("=========================================")

    print('Total token 개수 : {}'.format(len(tokens)))
    print("=========================================")


    # Word2Vec 모델 만들기 
    print("word2vec 모델 생성 중 ...")
    wakati_file = input_model_name + ".morpho"
    #print(wakati_file)

    with open(wakati_file, 'w', encoding="utf-8") as f:
        f.write("\n".join(results))

    data = word2vec.LineSentence(wakati_file)
    model = word2vec.Word2Vec(data, vector_size=100, window=5, hs=1, min_count=2, sg=1)

    model_name = input_model_name + '.model'
    model.save(model_name)

    # 실행 시간을 측정할 코드
    end_time = timeit.default_timer()
    print("%f초 걸렸습니다." % (end_time - start_time))

    print(model_name + ' 모델 저장됨!')
    print('-finished-')

    # top20 키워드 산출 및 csv 저장
    frequency.update(tokens)

    wordInfo = dict()
    path = paper_name + "_top20.csv"

    with open(path, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'count'])
        
        
        for word, count in frequency.most_common(n=40):
            if (len(str(word)) > 1):
                wordInfo[word] = count
                writer.writerow([word, count])       
                #print ("%s : %d" % (word, count))

        f.close()

    print("=========================================")

    saveGraph(wordInfo, paper_name)



def saveGraph(word_info, paper_name):
    """
    다빈도 단어 중 top20의 단어와 단어별 빈도수를 
    히스토그램 그래프로 나타낸다.
    """
    save_path =  "./../data/" + paper_name + ".png"
    font_location = "c:\Windows\Fonts\malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    # path_gothic = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    # font_name = font_manager.FontProperties(fname=path_gothic).get_name()
    matplotlib.rc('font', family=font_name) 

    plt.xlabel('주요 단어')
    plt.ylabel('빈도수')
    plt.grid(True)  

    Sorted_Dict_Values = sorted(word_info.values(), reverse=True)
    Sorted_Dict_Keys = sorted(word_info, key=word_info.get, reverse=True)   
 
    plt.title(paper_name + "_Top 20 키워드!!! ")
    plt.bar(range(len(word_info)), Sorted_Dict_Values, align='center')
    plt.xticks(range(len(word_info)), list(Sorted_Dict_Keys), rotation='70')  
    plt.savefig(save_path)
    #plt.show()


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
