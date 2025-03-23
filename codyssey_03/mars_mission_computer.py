import random
from datetime import datetime 
sensor_values_log_file_path = 'codyssey_03/env_sensor.csv'

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
        self.env_values['mars_base_internal_temperature'] = random.randint(18,30) #randint는 정수, uniform은 실수
        self.env_values['mars_base_external_temperature'] = random.randint(0,21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50,60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500,715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02,0.1)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4,7)

    def get_env(self) :
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]") # 현재 시간 저장
        log_content = ''
        log_content += '\n'
        log_content += str(now)

        for i, value in enumerate(self.env_values.values()) :
            log_content += ','
            log_content += str(value)

            # 아래처럼 하면 나중에 csv파일을 읽어올 때 귀찮아짐짐
            #if i < len(self.env_values) -1 :
            #    log_content += str(',')
        
        # 컴프리헨션
        # log_content = f"\n{now}," + ",".join(str(v) for v in self.env_values.values())

        open_file_write(sensor_values_log_file_path, log_content)
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

def write_header_if_needed(path, header) :
    try: 
        with open(path, 'r', encoding='utf-8') as f :
            contents = f.read()
            if contents.strip() == '': # 공백 제거하고 내용이 없으면
                raise FileNotFoundError
    except FileNotFoundError : # 실제로 파일이 없거나, 내용이 없을 때
        with open(path, 'w', encoding='utf-8') as f :
            f.write(header + '\n')



if __name__ == "__main__" :

    log_header =  str('시간,화성 기지 내부 온도,화성 기지 외부 온도,화성 기지 내부 습도,화성 기지 외부 광량,화성 기지 내부 이산화탄소 농도,화성 기지 내부 산소 농도')
    write_header_if_needed(sensor_values_log_file_path, log_header) # 파일이 제대로 만들어져 있으면 헤더는 다시 안써도 됨

    ds = DummySensor() # 인스턴스 생성
    ds.set_env() # 랜덤값 set
    sensor_values = ds.get_env() # 센서값 리턴 받기
    print_DummySensor(sensor_values)
    print('센서값 측정 및 출력을 완료했습니다.\n')

    



'''
    # ds값 반복해서 바꾸며 로그 남기기기
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
