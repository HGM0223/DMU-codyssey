import zipfile
import time

zip_path = 'codyssey_08/emergency_storage_key.zip'
output_file = 'codyssey_08/password.txt'

chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

# 3회 이상 반복되는 문자 포함 여부 확인 함수
def is_repeating(password):
    count = 1
    prev = '' # 직전 문자 저장장
    for c in password:
        if c == prev:
            count += 1
            if count >= 3:
                return True
        else:
            count = 1
            prev = c
    return False

def unlock_zip():
    total_attempts = 0
    start_time = time.time()
    repeating_queue = []

    print('암호 해제 시작 ------')
    print('시작 시간 :', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))

    # 1차: 반복되지 않는 비밀번호 먼저 검사
    for c1 in chars:
        for c2 in chars:
            for c3 in chars:
                for c4 in chars:
                    for c5 in chars:
                        for c6 in chars:
                            password = c1 + c2 + c3 + c4 + c5 + c6
                            if is_repeating(password):
                                repeating_queue.append(password) # 반복 큐(repeating_quese)에 비밀번호 임시저장
                                continue

                            total_attempts += 1
                            if try_extract_zip(zip_path, password):
                                duration_time = time.time() - start_time
                                print(f"\n성공! 암호: {password}")
                                print(f"총 시도 횟수: {total_attempts}")
                                print(f"총 소요 시간: {duration_time:.2f}초")
                                open_file_write(output_file, password)
                                return

                            if total_attempts % 1000 == 0:
                                duration_time = time.time() - start_time
                                print(f"1차 시도 (3개 이상 반복x): {total_attempts}, 경과: {duration_time:.2f}초, 현재 암호: {password}", end='\r')

    # 2차: 반복되는 비밀번호 검사
    for password in repeating_queue:
        total_attempts += 1
        if try_extract_zip(zip_path, password):
            duration_time = time.time() - start_time
            print(f"\n성공! 암호: {password}")
            print(f"총 시도 횟수: {total_attempts}")
            print(f"총 소요 시간: {duration_time:.2f}초")
            open_file_write(output_file, password)
            return

        if total_attempts % 1000 == 0:
            duration_time = time.time() - start_time
            print(f"2차 시도 (3개 이상 반복): {total_attempts}, 경과: {duration_time:.2f}초, 현재 암호: {password}")

    print('\n모든 조합을 시도했지만 암호를 찾지 못했습니다.')

def open_file_write(path, content):
    try:
        with open(path, 'a', encoding='utf-8') as f:
            return f.write(content)
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None

def try_extract_zip(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(pwd=password.encode('utf-8'))
        return True
    except:
        return False

if __name__ == '__main__':
    unlock_zip()
