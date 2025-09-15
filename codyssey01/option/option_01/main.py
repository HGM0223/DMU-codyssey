log_path = 'option/option_01/mission_computer_main.log'
json_path = 'option/option_01/mission_computer_main.json'

def mk_log_list(log_path) :
    log_list = []
    log_lines = open_file_read(log_path) #로그 파일을 읽어들여 리스트로 저장

    if log_lines : #리스트로 저장된 내용이 있으면면
        log_lines = log_lines[1:] #헤더 제거
        for line in log_lines :
            parts = line.split(",",2) # "," 를 기준으로 3개 파트로 나눔. timestamp, event, message
            if len(parts) == 3 : #part 리스트의 요소 개수가 3일 때
                timestamp, event, message = parts 
                log_list.append([timestamp.strip(), message.strip()]) #strip()으로 앞뒤 공백 제거

        return log_list
    
    else : return log_list


def print_list(log_list) :
    print('\n\n 리스트 내용을 출력합니다.\n')
    print(log_list)


def reverse_sort_list(log_list) :
    log_list.sort(key=lambda x: x[0], reverse=True )
    print('\n\n 리스트를 시간 역순으로 정렬했습니다. \n')


def mk_log_dict(log_list) :
    #timestamp, message룰 키값으로 하는 딕셔너리를 요소로 갖는 리스트 
    log_dict = [{'timestamp':t, 'message':m }for [t,m] in log_list]
    print('\n\n 딕셔너리 내용을 출력합니다. \n')
    print(log_dict)

    return log_dict


def mk_log_json(log_dict) :
    #import json
    #json 형태로 출력
    #print(json.dumps(dict_lines, indent=4)) -> 형식에 맞게 알아서 처리 해주는 라이브러리

    #json 파일로 저장 -> 추가 라이브러리 없이 파이썬 명령만으로 작성
    #2.직접 형식대로 작성하기기
    JSON_data ='[\n\n'
    
    for i, line in enumerate(log_dict) :  #i는 인덱스 line은 딕셔너리가 들어감
        timestamp = line['timestamp']
        message = line['message']
        
        JSON_data += ' {'+ ' "timestamp" : "'+ timestamp + '",\n'+ '   "message" : "' + message + '" }'
        if i < len(log_dict)-1 :
            JSON_data += ','
        JSON_data += '\n\n'

    JSON_data += ']'
    open_file_write(json_path, JSON_data)
        
    print('\n\n 딕셔너리 내용을 JSON파일에 저장했습니다. \n')


def fine_string_and_print(dict) :
    while True :
        search_word = input("\n\n찾고 싶은 단어를 입력하세요(종료시 엔터) : ")
        if search_word == "":
            print("\n검색어가 입력되지 않아 종료합니다.")
            break
    
        found = False #검색어가 딕셔너리 message에 포함이 되는지 확인하는 변수수
        for line in dict :
            timestamp = line['timestamp']
            message = line['message']


            if search_word in message :
                print(f'\n{timestamp} : {message}')
                found = True

        if not found : 
            print(f'{search_word}가 포함된 로그를 찾을 수 없습니다.')


def open_file_read(path) :
    try:
        with open(path, 'r') as f :
            return f.readlines()
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None

    
def open_file_write(path, content) :
    try:
        with open(path, 'w') as f :
            return f.write(content)
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None
    



if __name__ == "__main__" :
    log_list = mk_log_list(log_path) #로그파일을 읽어 리스트로 전환
    print_list(log_list) #리스트 내용 출력
    reverse_sort_list(log_list) #시간 역순
    
    log_dict = mk_log_dict(log_list) #딕셔너리로 전환
    mk_log_json(log_dict) #JSON포멧으로 딕셔너리 내용 저장

    fine_string_and_print(log_dict)