from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests

from datetime import datetime


def read_html(url):
    '''
    인자로 뉴스 url을 받아서 해당하는 html문서를 읽고 리턴하는 함수
    '''

    headers = {
        # User Agent를 지정해서(브라우저 정보) 봇 차단을 회피
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        )
    }
    resp = requests.get(url, headers=headers)   # requests로 요청
    resp.raise_for_status()                                      # 예외 처리 
    return bs(resp.text, 'html.parser')    
    #soup = bs(kbs_url.read(), 'html.parser')  # html문서를 읽어 Beautiful 객체를 담은 객체 만듦

    #return soup


def return_headline_title(soup):
    '''
    html문서를 받아 헤드라인 제목만 리스트로 리턴하는 함수
    '''

    titles = soup.select('p[class="title"]')            # p.title 은 title이 포함되는 모든 클래스를 검색함 ex) <p class="title normal-weight">
    titles = [t.get_text(strip=True) for t in titles]   # 공백 제거 / 태그 제외한 text만 뽑아서 리스트에 넣음
    
    del titles[0]     # 첫번째는 '추천 인기 키워드' 들어감
    del titles[-1]    # 마지막은 '공유하기'

    headline_titles = []    # 빈리스트 만들어서 ''가 아닌 진짜 제목들만 넣어줌
    for i in range(len(titles)):
        if titles[i] != '':
            headline_titles.append(titles[i])

    return headline_titles



def print_list(list):
    '''
    list를 한 줄 씩 출력
    '''

    now = datetime.now()
    print(f'\nKBS 헤드라인 | {now}\n')
    for item in list:
        print(item)


if __name__ == "__main__":
    url = 'https://news.kbs.co.kr/news/pc/main/main.html'   # url 지정
    soup = read_html(url)                                   # 해당 html 문서 객체 soup에 저장
    headline_titles = return_headline_title(soup)           # soup에서 헤드라인 제목만 headline_titles에 저장
    print_list(headline_titles)                             # (KBS 헤드라인 | 현재시각 , 각 제목) 출력
    

    
    