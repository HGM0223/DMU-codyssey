from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from datetime import datetime
import requests

def read_html(url):
    '''
    인자로 뉴스 url을 받아서 해당하는 html문서를 읽고 리턴하는 함수
    '''

    dallor_url = urlopen(url)
    soup = bs(dallor_url.read(), 'html.parser')  # html문서를 읽어 Beautiful 객체를 담은 객체 만듦

    return soup


def return_headline_title(soup):
    '''
    html문서를 받아 헤드라인 제목만 리스트로 리턴하는 함수
    '''

    titles = soup.select('p[class="_midMarketRateAmount_14arr_13"]')            # p.title 은 title이 포함되는 모든 클래스를 검색함 ex) <p class="title normal-weight">
    titles = [t.get_text(strip=True) for t in titles]   # 태그 제외한 text만 뽑아서 리스트에 넣음
    


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
    url = 'https://wise.com/kr/currency-converter/usd-to-krw-rate'   # url 지정
    headers = {"User-Agent": "Mozilla/5.0"}
    data = requests.get(url, headers=headers).json()
    rate = data["rate"]
    print(rate)

    #soup = read_html(url)                                   # 해당 html 문서 객체 soup에 저장
    #headline_titles = return_headline_title(soup)           # soup에서 헤드라인 제목만 headline_titles에 저장
    #print_list(headline_titles)                             # (KBS 헤드라인 | 현재시각 , 각 제목) 출력
    

    
    