from lib2to3.pgen2.tokenize import tokenize
import sys
import json
import os
import csv
from glob import glob
from collections import Counter
from konlpy.tag import Kkma

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

def main():
    """
    명령라인 매개변수로 지정한
    디렉터리 내부의 파일을 읽어 들이고
    빈출 단어를 출력합니다.
    """
    kkma = Kkma()
    count_proccessed = 0

    path = sys.argv[1]
    print('Processing {0}...'.format(path), file=sys.stderr)
   
    token = []
    
    # 단어의 빈도를 저장하기 위한 Counter 객체를 생성합니다.
    # Counter 클래스는 dict를 상속받는 클래스입니다.           
    frequency = Counter()

    # 파일을 엽니다.
    with open(path, 'r', encoding="utf-8") as file:
        #파일 내부의 모든 기사에 반복을 돌립니다.
        for line in file.readlines():
            
            json_object = json.loads(line)
            content = ''.join(json_object['body'])

            node = kkma.pos(content)
            for (taeso, pumsa) in node:
                 # 고유 명사와 일반 명사만 추출합니다.
                 if pumsa in ('NNG', 'NNP'):
                    token.append(taeso)
    
            count_proccessed += 1

    frequency.update(token)

    #모든 기사의 처리가 끝나면 상위 0개의 단어를 출력합니다
    print("=========================================")
    print('{0} documents were processed.'
          .format(count_proccessed),file=sys.stderr)
    print("=========================================")

    wordInfo = dict()
    path = "word_count5.csv"

    with open(path, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'count'])
        #row = [json_object['word'], json_object['count']]

        for word, count in frequency.most_common(30):
            if (len(str(word)) > 1):
                wordInfo[word] = count
                writer.writerow([word, count])       
                print ("%s : %d" % (word, count))

        f.close()

    showGraph(wordInfo)



def showGraph(word_info):
    """
    다빈도 단어 중 top20의 단어와 단어별 빈도수를 
    히스토그램 그래프로 나타낸다.
    """
    font_location = "c:\Windows\Fonts\malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    matplotlib.rc('font', family=font_name) 

    plt.xlabel('주요 단어')
    plt.ylabel('빈도수')
    plt.grid(True)  

    Sorted_Dict_Values = sorted(word_info.values(), reverse=True)
    Sorted_Dict_Keys = sorted(word_info, key=word_info.get, reverse=True)   
 
    plt.title("제주일보(jejunews.com) Top 20 키워드")
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
