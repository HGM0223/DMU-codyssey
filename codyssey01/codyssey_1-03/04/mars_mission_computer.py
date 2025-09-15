import time
import random
from datetime import datetime 

import platform
import psutil

sensor_values_log_file_path = 'codyssey_03_04/env_sensor.csv'
stop_file_path = 'codyssey_03_04/stop_signal.txt'
sys_set_file_path = 'codyssey_03_04/setting.txt'


class DummySensor :
    def __init__(self) :  
        # __init__의 첫 번째 변수인 self는 DummySensor클래스 자체를 의미함.
        # self.env_values 처럼 init함수 안에서 클래스를 사용하고 클래스에 정의된 다른 함수와도 변수를 공유하기 위함.
        
        self.env_values = { # 인스턴스 변수로 딕셔너리 정의
            'mars_base_internal_temperature' : None,
            'mars_base_external_temperature' : None,
            'mars_base_internal_humidity' : None,
            'mars_base_external_illuminance' : None,
            'mars_base_internal_co2' : None,
            'mars_base_internal_oxygen' : None
        }

    def set_env(self) :
        # 랜덤 값이 변수에 찍히는 시간 저장 -> 한국 표준 시간을 세계시간 사이트에서 받아오는 방법도 있음.(인터넷이 안되면 사용할 수 없음)
        #user_time = input("날짜와 시간을 입력하세요 (예: 2025-03-27 14:30): ")
        #self.current_time = f"[{user_time}]"

        # 외부 라이브러리 datetime 사용
        self.current_time_datetime = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]") # 현재 시간 저장. 시간날짜를 문자열로 반환할 때 strftime, 문자열을 datetime으로 반환할 때 strptime


        self.env_values['mars_base_internal_temperature'] = random.randint(18,30) #randint는 정수, uniform은 실수
        self.env_values['mars_base_external_temperature'] = random.randint(0,21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50,60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500,715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02,0.1)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4,7)

    def get_env(self) :
        #now = self.current_time
        now = self.current_time_datetime
        log_content = ''
        log_content += '\n'
        log_content += str(now)

        for i, value in enumerate(self.env_values.values()) : # log 저장하는 부분은 따로 함수로 만들면 좋을듯
            log_content += ','
            log_content += str(value)

            # 아래처럼 하면 나중에 csv파일을 읽어올 때 귀찮아짐짐
            #if i < len(self.env_values) -1 :
            #    log_content += str(',')
        
        # 컴프리헨션
        # log_content = f"\n{now}," + ",".join(str(v) for v in self.env_values.values())

        open_file_write(sensor_values_log_file_path, log_content) # 요구사항에 맞게 log함수를 get_env에서 쓰면 값을 읽어올 때마다 log에 같은 값이 찍히는 문제 발생, set_env에 넣는게 더 적합함.
        print('\n센서값을 로그에 저장했습니다.')

        return self.env_values



def print_DummySensor(env_value) :
    for key, value in env_value.items() : # 센서값 키 : 값 형태로 출력
        print(key, ':', value)
    

def open_file_write(path, content) :
    try:
        with open(path, 'a', encoding='utf-8') as f :
            return f.write(content)
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None

def open_file_write_w(path, content) :
    try:
        with open(path, 'w', encoding='utf-8') as f :
            return f.write(content)
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None
    
def open_file_read(path) :
    try:
        with open(path, 'r', encoding='utf-8') as f :
            return f.read()
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None


def write_header_if_needed(path, header) :
    try: 
        with open(path, 'r', encoding='utf-8') as f :
            contents = f.read()
            if contents.strip() == '': # 공백 제거하고 내용이 없으면
                raise FileNotFoundError
    except FileNotFoundError : # 실제로 파일이 없거나, 내용이 없을 때
        with open(path, 'w', encoding='utf-8') as f :
            f.write(header + '\n')

# codyssey_04 내용
class MissionComputer :
    def __init__(self) :  
         # 사전객체를 env_values 속성으로 정의
        self.env_values = {
            'mars_base_internal_temperature' : None,
            'mars_base_external_temperature' : None,
            'mars_base_internal_humidity' : None,
            'mars_base_external_illuminance' : None,
            'mars_base_internal_co2' : None,
            'mars_base_internal_oxygen' : None
        }

    
    def get_sensor_data(self, dummy_sensor_instance) :
        # 5분마다 센서값의 평균값을 출력하기 위한 초기값 설정
        count = 0
        start_time = time.time()
        sum_env_values = {   # 데이터 불변성 중요.
            'mars_base_internal_temperature' : 0,
            'mars_base_external_temperature' : 0,
            'mars_base_internal_humidity' : 0,
            'mars_base_external_illuminance' : 0,
            'mars_base_internal_co2' : 0,
            'mars_base_internal_oxygen' : 0
        }

        while True :
            current_time = time.time()
            if current_time - start_time >= 15 : # 5분은 300초
                print('\n센서 평균값 출력-------------------------------------')
                for key, value in sum_env_values.items() :
                    print(f'{key} : {value/count:.3f}')
                    # 환경값의 총합 변수 초기화
                    sum_env_values[key] = 0
                count = 0
                start_time = start_time + 15 

            # 엔터키 입력시 환경 출력 중지 -> ctrlC 누르면 예외처리 할 수 있음.
            if open_file_read(stop_file_path).strip() == 'STOP' :
                open_file_write_w(stop_file_path,'None')
                print('System stoped...')
                break
            else : 
                print('\n센서값 출력')
                dummy_sensor_instance.set_env()
                json_data = '\n{'
                for i, (key, value) in enumerate(dummy_sensor_instance.get_env().items()):
                    self.env_values[key] = value
                    sum_env_values[key] += value
                    json_data += '\n "' + f'{key}' + '" : ' + f'{value}' + ''
                    if(i < 5) :
                        json_data +=','
                json_data += '\n}'
                print(json_data)
                count += 1
                
                # sleep 중에도 정확한 간격을 맞추기 위한 시간 조절. time.sleep(5)대신 아래처럼럼
                time_to_next_check = max(0, 5 - (time.time() - current_time))
                time.sleep(time_to_next_check)

    def get_mission_computer_info(self, system_values) :
        # 미션 컴퓨터의 시스템 정보를 저장하는 변수
        '''
        try :
            sys_values = {
                '운영체계' : platform.system(),
                '운영체계_버전' : platform.version(),
                'CPU_타입' : platform.processor(),
                'CPU_코어수' : psutil.cpu_count(),
                'memory_크기' : psutil.virtual_memory().total # virtual에는 총 메모리 total과 사용 가능한 avaliable 정보가 포함됨.
            }
            
        except Exception as e :
            print('시스템 정보를 가져오는 중 오류 발생 : ',e)
            sys_values = {}
        '''
        sys_values = {}
        sys_values['운영체계'] = system_values[0]
        sys_values['운영체계 버전'] = system_values[1]
        sys_values['CPU 타입'] = system_values[2]
        sys_values['CPU 코어수'] = system_values[3]
        sys_values['memory 크기'] = system_values[4]


        # 시스템 정보를 JSON형식으로 출력
        print('\n시스템 정보')
        json_data = '\n{'

        for i, (key, value) in enumerate(sys_values.items()):
            # 문자열 value는 ""를 붙이고 숫자엔 안붙임
            if(i<3) :
                json_data += f'\n    "{key}" : "{value}",'
            else :
                json_data += f'\n    "{key}" : {value},'

        json_data = json_data.rstrip('\n,') + '\n}'   

        print(json_data)


    def get_mission_computer_load(self, system_values) :
        '''
        try : 
            p = psutil.Process()
            cpu_usage = p.cpu_percent()
            memory_usage = p.memory_info().rss/2**20 #RSS는 물리 메모리에서 차지하는 크기기. bytes to MB

        except Exception as e :
            print('cpu및 메모리 사용량을 체크하는 중 오류발생 : ',e)
            cpu_usage 
            memory_usage 
        '''

        cpu_usage = system_values[5]
        memory_usage = system_values[6]
        

        # JSON형식으로 출력
        print('\nCPU와 메모리 사용량')
        print('\n{')
        print(f'    "CPU 사용량" : {cpu_usage},\n    "메모리 사용량" : {memory_usage}')
        print('}')


    def parse_settings(path):
        raw = open_file_read(path)
        settings = {}
        for line in raw.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':')
                settings[key.strip()] = value.strip().lower() == 'true'
        return settings



        

if __name__ == "__main__" :
    #log_header =  str('시간,화성 기지 내부 온도,화성 기지 외부 온도,화성 기지 내부 습도,화성 기지 외부 광량,화성 기지 내부 이산화탄소 농도,화성 기지 내부 산소 농도')
    #write_header_if_needed(sensor_values_log_file_path, log_header) # 파일이 제대로 만들어져 있으면 헤더는 다시 안써도 됨

    #ds = DummySensor()
    #RunComputer = MissionComputer()
    #RunComputer.get_sensor_data(ds)

    runComputer = MissionComputer()

    system_values = []
    system_values = open_file_read(sys_set_file_path).split('\n')
    
    runComputer.get_mission_computer_info(system_values)
    runComputer.get_mission_computer_load(system_values)














    '''
if __name__ == "__main__" :
    log_header =  str('시간,화성 기지 내부 온도,화성 기지 외부 온도,화성 기지 내부 습도,화성 기지 외부 광량,화성 기지 내부 이산화탄소 농도,화성 기지 내부 산소 농도')
    write_header_if_needed(sensor_values_log_file_path, log_header) # 파일이 제대로 만들어져 있으면 헤더는 다시 안써도 됨

    ds = DummySensor() # 인스턴스 생성
    ds.set_env() # 랜덤값 set
    sensor_values = ds.get_env() # 센서값 리턴 받기
    print_DummySensor(sensor_values)
    print('센서값 측정 및 출력을 완료했습니다.\n')

    '''



'''
    # ds값 반복해서 바꾸며 로그 남기기
    while True :
        prompt = input('\n\n엔터시 환경값 측정(종료시 q) : ')
        if prompt == '':
            ds.set_env() # 랜덤값 set
            sensor_values = ds.get_env() # 센서값 리턴 받기
            print_DummySensor(sensor_values)
            print('\n환경값을 측정하고 로그를 저장했습니다')
        elif prompt =='q' :  
            print('\n측정 종료합니다.')
            break
'''    
