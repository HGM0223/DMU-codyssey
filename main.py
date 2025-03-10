print('Hello Mars')

#readlines 사용
from os import path
from numpy import sort

print('\n\nreadelines 사용')

try :
    f = open("mission_computer_main.log", 'r')
    lines = f.readlines()     #모든 줄을 요소로 하는 리스트 반환
    for line in lines:
        print(line)
        
        #출력 결과 중 문제가 되는 부분을 log_matter.txt에 저장함
        if('explosion' in line or 'Rocket' in line) :
            #print(line)
            if(path.exists('log_matter.txt')):
                matters_File = open('log_matter.txt', 'a')
            else :
                matters_File = open('log_matter.txt', 'w')

            matters_File.write(line)
            matters_File.close()

except FileNotFoundError :                        #파일이 없을때
    print('파일이 존재하지 않습니다.')
except PermissionError :                          #권한 오류
    print('파일을 읽을 수 있는 권한이 없습니다.')
except Exception as e:                            #그 외 오류
    print('파일을 처리하는데 오류가 발생했습니다!!')
    print(e)
else :                                            #정상 처리
    print('파일 내용 출력을 완료했습니다.')

finally :
    if 'f' in locals():  #로컬 변수에 f가 정의되어 있을 때 실행(파일이 open 상태일 때)
        f.close()
        print('열린 파일 닫음')


# 시간 역순으로 출력력
print('\n\n시간 역순으로 출력')
lines.sort(reverse=True)  #시간 역순으로 정렬 및 출력
for line in lines:
    print(line)











'''
#readeline 사용
print('\n\nreadeline 사용')
try :
    f = open("mission_computer_main.log", 'r')
    while True:
        line = f.readline()   #더 읽을 내용이 없을 때까지 읽어들임, line의 type은 <class 'str'> 
        if not line: 
            break
        print(line)

except FileNotFoundError :                        #파일이 없을때
    print('파일이 존재하지 않습니다.')
except PermissionError :                          #권한 오류
    print('파일을 읽을 수 있는 권한이 없습니다.')
except Exception as e:                            #그 외 오류
    print('파일을 처리하는데 오류가 발생했습니다!!')
    print(e)
else :                                            #정상 처리
    print('파일 내용 출력을 완료했습니다.')

finally :
    if 'f' in locals():  #로컬 변수에 f가 정의되어 있을 때 실행(파일이 open 상태일 때)
        f.close()
        print('열린 파일 닫음')
'''


