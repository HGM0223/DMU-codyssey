# 카이사르 암호 (시저 암호)
# 알파벳을 일정 칸 수 만큼 밀어 암호화하는 방식

password_path = 'codyssey_2-04/password.txt'
result_path = 'codyssey_2-04/result.txt'

dictionary = ['cody', 'dongyang', 'mirae', 'mars', 'door', 'world', 'ftk']


def caesar_cipher_decode(target_text) :
    # 몇 칸 이동해야 하는지 하나씩 검사
    for shift in range(1,26): # shift는 1~25. 영문자는 26개 a~z
        decoded_text = ''
        
        # mars06을 한 문자씩 치환하는 과정
        for target_char in target_text : 
            if 'a' <= target_char <= 'z': # 소문자
                decoded_text += chr(( ord(target_char) - ord('a') - shift ) % 26 + ord('a'))
            elif 'A' <= target_char <= 'Z': # 대문자
                decoded_text += chr(( ord(target_char) - ord('A') - shift ) % 26 + ord('A'))
            else : # 숫자 등
                decoded_text += target_char

        print(f'shift : {shift} | 암호문 : {decoded_text}')

        #사전 속 키워드 검사
        if check_word_in_dict(decoded_text, dictionary) :
            break


# 사용자가 입력한 번호를 통해 복호화하고 result.txt에 저장
def decode_with_shift(target_text,shift):
        result_text = ''

        for target_char in target_text : 
            if 'a' <= target_char <= 'z': # 소문자
                result_text += chr(( ord(target_char) - ord('a') - shift ) % 26 + ord('a'))
            elif 'A' <= target_char <= 'Z': # 대문자
                result_text += chr(( ord(target_char) - ord('A') - shift ) % 26 + ord('A'))
            else : # 숫자 등
                result_text += target_char

        open_file_write(result_path, result_text)

        # if, elif로 소문자 대문자 구분하지 말고 isupper 함수를 써서 소문자이면 ord('a'), 대문자면 ord('A')를 받아올 수 있도록 하면 좋음
        '''
        if target_text.isalpha : # 알파벳이라면
            if target_text.isupper() :
                ord_Aa = ord('a')
            else :
                ord_Aa = ord('A')
            result_text += chr(( ord(target_char) - ord_Aa - shift ) % 26 + ord_Aa)
        else : # 숫자, 공백 등이라면
            result_text += target_text
        '''


# 사전에 있는 단어와 일치하는 키워드가 암호속에 있는지 검사
def check_word_in_dict(decoded_text, dictionary) :
    if any(word in decoded_text.lower() for word in dictionary):
        print(f'사전 속 단어와 일치하는 키워드 발견 !!')
        open_file_write(result_path, decoded_text)
        return True
    return False


# 파일 read
def open_file_read(path) :
    try:
        with open(path, 'r', encoding='utf-8') as f :
            return f.read()
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None

# 파일 write
def open_file_write(path, content) :
    try:
        with open(path, 'w', encoding='utf-8') as f :
            return f.write(content)
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None




if __name__ == '__main__':
    password = open_file_read(password_path)
    caesar_cipher_decode(password)

    #result_shift = int(input('복호화를 위한 번호(shift)를 입력하세요 : '))
    #decode_with_shift(password, result_shift)
