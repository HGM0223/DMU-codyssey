import zipfile
import time
import threading

zip_path = 'codyssey_08/emergency_storage_key.zip'
output_file = 'codyssey_08/password.txt'

chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
password_length = 6
num_threads = 10

found = False # 암호 발견 시 True
lock = threading.Lock() # 스레드 충돌 방지용용

# zip 파일 여는 함수수
def try_extract_zip(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(pwd=password.encode('utf-8'))
        return True
    except:
        return False

def open_file_write(path, content):
    try:
        with open(path, 'a', encoding='utf-8') as f:
            return f.write(content)
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None

# index에 따라 가능한 비밀번호 조합을 만들어 주는 함수
def index_to_password(index):
    chars_len = len(chars) # 36개
    password = ''
    for _ in range(password_length): # 0~5까지
        password = chars[index % chars_len] + password # index = 0 일땐 aaaaaa, 1 일땐 aaaaab 
        index //= chars_len
    return password

def worker(start_index, step, total_combinations, start_time):
    global found
    total_attempts = 0

    for i in range(start_index, total_combinations, step): # start_index = 1 이면 i = 1, 11, 21...
        if found:
            break

        password = index_to_password(i)
        total_attempts += 1

        if try_extract_zip(zip_path, password):
            with lock:
                if not found:
                    found = True
                    duration_time = time.time() - start_time
                    print(f'\n[스레드 {start_index}] 성공! 암호: {password}')
                    print(f'[스레드 {start_index}] 총 시도 횟수: {total_attempts}')
                    print(f'[스레드 {start_index}] 소요 시간: {duration_time:.2f}초')
                    open_file_write(output_file, password)
            break

        if total_attempts % 1000 == 0:
            duration_time = time.time() - start_time
            print(f'[스레드 {start_index}] 시도: {total_attempts}, 경과: {duration_time:.2f}초, 현재 암호: {password}', end='\r')

def unlock_zip():
    start_time = time.time()
    print('암호 해제 시작 ------')
    print('시작 시간 : ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))

    total_combinations = len(chars) ** password_length # 가능한 조합 약 21억 가지
    threads = []

    # 스레드 num_threads만큼 생성 및 실행
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i, num_threads, total_combinations, start_time))
        t.start()
        threads.append(t)

    # 스레드 끝날 때까지 대기 (모든 암호를 시도 후 다음 코드로 넘어감)
    for t in threads:
        t.join()

    if not found:
        print('\n모든 조합을 시도했지만 암호를 찾지 못했습니다.')

if __name__ == '__main__':
    unlock_zip()
