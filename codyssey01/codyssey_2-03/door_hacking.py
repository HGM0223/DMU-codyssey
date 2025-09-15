import zipfile
import time

zip_path = 'codyssey_08/emergency_storage_key.zip'
output_file = 'codyssey_08/password.txt'

def unlock_zip():

    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    total_attempts = 0
    start_time = time.time()

    print('암호 해제 시작 ------')
    print('시작 시간 : ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))

    for c1 in chars:
        for c2 in chars:
            for c3 in chars:
                for c4 in chars:
                    for c5 in chars:
                        for c6 in chars:
                            password = c1 + c2 + c3 + c4 + c5 + c6
                            total_attempts += 1

                            if try_extract_zip(zip_path,password):

                                duration_time = time.time() - start_time
                                print(f"\n성공! 암호: {password}")
                                print(f"총 시도 횟수: {total_attempts}")
                                print(f"총 소요 시간: {duration_time:.2f}초")

                                open_file_write(output_file, password)
                                return
                            
                            #zip이 열리지 않을 경우 (100번째마다 과정 출력)
                            if total_attempts % 1000 == 0:
                                duration_time = time.time() - start_time
                                print(f"시도: {total_attempts}, 경과: {duration_time:.2f}초, 현재 암호: {password}", end='\r')

    print('\n모든 조합을 시도했지만 암호를 찾지 못했습니다.')



def open_file_write(path, content) :
    try:
        with open(path, 'a', encoding='utf-8') as f :
            return f.write(content)
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None

# zip파일 압축을 푸는 함수 (성공하면 True, 실패하면 False)
def try_extract_zip(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(pwd=password.encode('utf-8'))
        return True
    except:
        return False
   


if __name__ == '__main__':
    unlock_zip()
