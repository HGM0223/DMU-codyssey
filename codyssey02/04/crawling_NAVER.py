from selenium import webdriver                                     # 웹드라이버
from selenium.webdriver.common.by import By                        # html 요소를 찾을 때 사용
from selenium.webdriver.support.ui import WebDriverWait            # 특정 조건이 충족될 때까지 대기
from selenium.webdriver.support import expected_conditions as EC   # 대기 조건 설정용
from selenium.webdriver import ActionChains, Keys                  # 액션체인(복사 붙여넣기용)
from selenium.webdriver.chrome.service import Service              # 크롬 서비스
from webdriver_manager.chrome import ChromeDriverManager           
import pyperclip                                                   # 클립보드 복붙용

from datetime import datetime


class NaverLogin():
    def __init__(self, id, pw):         
        ''' 생성자: 아이디/비번을 인스턴스 변수로 저장하는 함수 '''
        self.id = id
        self.pw = pw
        self.driver = None

    def login(self, timeout=30):
        '''
        네이버 로그인 실행 함수 (크롬 버전에 맞는 드라이버를 설치하고 실행)
        '''
        # ChromeDriverManager를 사용하여 ChromeDriver 설치 및 경로 설정
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)         # 크롬 드라이버 객체 생성

        self.driver.get('https://nid.naver.com/nidlogin.login') # 네이버 로그인 페이지로 이동
        wait = WebDriverWait(self.driver, timeout)              # 최대 timeout초 만큼 대기

        try:
            # 아이디와 비밀번호 입력창이 로드될 때까지 대기
            id_input = wait.until(EC.presence_of_element_located((By.ID, 'id')))
            pw_input = wait.until(EC.presence_of_element_located((By.ID, 'pw')))

            id_input.click()         # 아이디 입력창 클릭
            pyperclip.copy(self.id)  # 클립보트에 아이디를 복사한 후 붙여넣기 함
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

            pw_input.click()         # 위와 같은 방식으로 비밀번호 입력
            pyperclip.copy(self.pw)
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()


            login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn_login')))
            login_button.click()
            print('login successful')

        except Exception as e:
            print(f'Error during login: {e}')
        finally:
            pass


    
    def return_nickname(self, timeout=30):
        '''
        네이버 메인 페이지에서 닉네임을 리턴하는 함수
        '''
        wait = WebDriverWait(self.driver, timeout)
        try:
            # 새로운 닉네임 span 선택자 사용
            nickname_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.MyView-module__nickname___fcxwI'))
            )
            nickname = nickname_element.text
            return nickname
        except Exception as e:
            print(f'Error retrieving nickname: {e}')
            return None
        

    def open(self, url):
        '''
        크롬 브라우저를 열고 url 페이지로 이동 (크롬 버전에 맞는 드라이버를 매번 설치하고 실행)
        '''
        if not self.driver:
            print('새로운 브라우저를 엽니다.')
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            self.driver.get(url)

        self.driver.get(url)
        

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
        



def print_list(list):
    '''
    list를 한 줄 씩 출력
    '''

    now = datetime.now()
    print(f'\f로그인 정보 | {now}\n')
    for items in list:
        print(items)
    




if __name__ == "__main__":
    naver_service = NaverLogin('annie5648', 'gkarudals1094')  # 네이버 아이디, 비밀번호 입력
    naver_service.login()  # 로그인
    nickname = naver_service.return_nickname()  # 닉네임 가져오기
    print(nickname)