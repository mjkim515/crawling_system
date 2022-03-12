
#===============================================================================
#
#  실행방법 : python word_extraction.py [input jl filename] [output 사업 jl filename]
#  
#  ex) python word_count.py donga.jl  동아일보
#
#===============================================================================

from lib2to3.pgen2.tokenize import tokenize
from pickle import TRUE
import sys
import json
import os
import csv
from glob import glob
from collections import Counter
from types import coroutine
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
    #twitter = Twitter()
    kkma = Kkma()
    count_proccessed = 0
    count_extracted = 0

    path = sys.argv[1]

    print('Processing {0}...'.format(path), file=sys.stderr)

    tokens = []

    # 파일을 엽니다.
    extracted_path = sys.argv[2] 

    with open(extracted_path, 'w', newline='', encoding="utf-8") as f:

        with open(path, 'r', encoding="utf-8") as file:
            #파일 내부의 모든 기사에 반복을 돌립니다.
            for line in file.readlines():          

                first = True 
                
                json_object = json.loads(line)
                title = ''.join(json_object['title'])
                content = ''.join(json_object['body'])
                
                # 명사를 저장할 리스트입니다.

                node = kkma.pos(content)
                for (taeso, pumsa) in node:
                    # 고유 명사와 일반 명사만 추출합니다.
                    if pumsa in ('NNG', 'NNP'):
                        if ( taeso == '사업' and first ):   
                            first = False 
                            count_extracted += 1
                            #_business.jl
                            # f.write(line)
                            f.write(str(count_extracted) + ". " + title + "\n")

                        tokens.append(taeso)

                count_proccessed += 1
            

    #모든 기사의 처리가 끝나면 상위 0개의 단어를 출력합니다
    print("=========================================")
    print('{0} documents were processed.'
          .format(count_proccessed),file=sys.stderr)
    print("=========================================")

   #모든 기사의 처리가 끝나면 상위 0개의 단어를 출력합니다
    print("=========================================")
    print('{0} business documents were processed.'
          .format(count_extracted),file=sys.stderr)
    print("=========================================")

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
