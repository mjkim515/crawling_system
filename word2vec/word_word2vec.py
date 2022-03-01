#===============================================================================
#
#  실행방법 : python word_word2vec.py [input jl filename] [output  model_name]
#  
#  ex) python word_word2vec.py donga.jl  donga
#
#===============================================================================


from lib2to3.pgen2.tokenize import tokenize
import sys
import json
import os
import csv
import codecs
from glob import glob
from tkinter import W
#from collections import Counter
#from konlpy.tag import Twitter
from konlpy.tag import Kkma
from gensim.models import word2vec

# showGraph를 위한 모듈 
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

def main():
    """
    명령라인 매개변수로 지정한
    디렉터리 내부의 파일을 읽어 들이고
    빈출 단어를 출력합니다.
    """
    #twitter = Twitter()
    kkma = Kkma()
    count_proccessed = 0

    path = sys.argv[1]
    print('Processing {0}...'.format(path), file=sys.stderr)

    input_model_name = sys.argv[2]
   
    tokens = []
    results = []

    # 파일을 엽니다.
    with open(path, 'r', encoding="utf-8") as file:
        #파일 내부의 모든 기사에 반복을 돌립니다.
        for line in file.readlines():
            
            json_object = json.loads(line)
            content = ''.join(json_object['body'])
            #twitter 형태소 분리기 사용
            #text_lines = content.split("\r\n")
            #word_dic = {}

            #for text in text_lines:
            #    malist = twitter.pos(text)
            #    #print(malist)
            #    for word in malist:
            #        if word[1] == "Noun":
            #            #print(word[0])
            #            if not (word[0] in word_dic):
            #                word_dic[word[0]] = 0

            #            word_dic[word[0]] += 1
            #            tokens.append(word[0])
            # twitter 형태소 분리기 사용 END

            node = kkma.pos(content)
            for (taeso, pumsa) in node:
                 # 고유 명사와 일반 명사만 추출합니다.
                 if pumsa in ('NNG', 'NNP'):
                    tokens.append(taeso)
    
            rl = (" ".join(tokens)).strip()
            results.append(rl)
            print(rl)

            count_proccessed += 1
     

    #모든 기사의 처리가 끝나면 상위 0개의 단어를 출력합니다
    print("=========================================")
    print('{0} documents were processed.'
          .format(count_proccessed),file=sys.stderr)
    print("=========================================")

    print('Total token 개수 : {}'.format(len(tokens)))

    wakati_file = input_model_name +".textpro"
    #print(wakati_file)

    with open(wakati_file, 'w', encoding="utf-8") as f:
        f.write("\n".join(results))

    # Word2Vec 모델 만들기 
    data = word2vec.LineSentence(wakati_file)
    model = word2vec.Word2Vec(data, vector_size=100, window=10, hs=1, min_count=2, sg=1)

    model_name = input_model_name + '.model'
    model.save(model_name)
    print(model_name + ' 모델 저장됨!')
    print('-finished-')



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
