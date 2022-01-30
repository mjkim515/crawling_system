import sys
import json
import os
import csv
from glob import glob
from collections import Counter
from konlpy.tag import Kkma


def main():
    """
    명령라인 매개변수로 지정한
    디렉터리 내부의 파일을 읽어 들이고
    빈출 단어를 출력합니다.
    """
    # 명령어의 첫 번째 매개변수로
    # WikiExtractor의 출력 디렉터리를 지정합니다.
    # input_dir = sys.argv[1]
    kkma = Kkma()
    count_proccessed = 0
    # glob()으로 와일드카드 매치 파일 목록을 추출하고
    # 매치한 모든 파일을 처리합니다.

    path = sys.argv[1]

    print ("Input(sys.argv[1]) : " + sys.argv[0] + " Output(sys.argv[2]) : " + sys.argv[1])
    print ("path : "+ path)
    print('Processing {0}...'.format(path), file=sys.stderr)


    # 파일을 엽니다.
    with open(path, 'r', encoding="utf-8") as file:
        with open(sys.argv[2], 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'url', 'tokens'])
            # 파일 내부의 모든 기사에 반복을 돌립니다.
            for line in file.readlines():
                # 단어의 빈도를 저장하기 위한 Counter 객체를 생성합니다.
                # Counter 클래스는 dict를 상속받는 클래스입니다.
                frequency = Counter()
                json_object = json.loads(line)
                content = ''.join(json_object['body'])
                tokens = get_tokens(kkma, content)
                frequency.update(tokens)
                count_proccessed += 1
                row = [json_object['title'], json_object['url']]
                for token, count in frequency.most_common(20):
                    row.append(token)
                    row.append(count)
                writer.writerows([row])
                # print(json_object['title'], json_object['url'],
                #         end=',', sep=',')
                # for token, count in frequency.most_common(30):
                #     print(token, count, end=',', sep=',')
                # print('', end='\n')
    
    #모든 기사의 처리가 끝나면 상위 30개의 단어를 출력합니다
    #print('{0} documents were processed.'
    #      .format(count_proccessed),file=sys.stderr)
    #for token, count in frequency.most_common(20):
    #    print(token, count)

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

def get_tokens(kkma, content):
    """
    문장 내부에 출현한 명사 리스트를 추출하는 함수
    """
    # 명사를 저장할 리스트입니다.
    tokens = []
    node = kkma.pos(content)
    for (taeso, pumsa) in node:
        # 고유 명사와 일반 명사만 추출합니다.
        if pumsa in ('NNG', 'NNP'):
            tokens.append(taeso)
    return tokens

if __name__ == '__main__':
    main()
