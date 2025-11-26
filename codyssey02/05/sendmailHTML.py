import smtplib  # SMTP 사용을 위한 모듈
import re       # 정규표현식 사용을 위한 모듈
from email.mime.multipart import MIMEMultipart  # 메일의 Data(텍스트, 이미지 등)를 담는 컨테이너 모듈
from email.mime.text import MIMEText            # 메일의 텍스트 본문 내용을 넣기 위한 모듈
from email.mime.image import MIMEImage          # 메일의 이미지 파일을 base64 형식으로 변환하기 위한 모듈
import csv

def sendEmail(smtp, msg, send_account, recv_account):
    '''
    메일 주소 유효성 검사 후 메일 발송
    '''
    reg = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"  # 유효성 검사를 위한 정규표현식. r은 rqw string \. 같은 이스케이프 경고 피함. $는 끝을 의미
    if re.match(reg, recv_account): # 정규표현식과 매칭이 되면 (유효한 메일이면 실행)
        try: 
            smtp.sendmail(send_account, recv_account, msg.as_string()) 
            print("정상적으로 메일이 발송되었습니다.")
        except Exception as e:
            print("\n메일 발송에 실패하였습니다.", e)
    else:
        print("받으실 메일 주소를 정확히 입력하십시오.")
 

def sendEmailAll(smtp, msg, send_account, recv_list):
    '''
    여러명에게 동시에 메일 발송 (핵심은 smtp.sendmail의 두번째 인자에 리스트를 전달하는 것 msg에 지정한건 그냥 보여주기 용임)
    '''
    reg = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"  # 유효성 검사를 위한 정규표현식. r은 rqw string \. 같은 이스케이프 경고 피함. $는 끝을 의미
    vaild_list = []
    invalid_list = []

    for name, recv_account in recv_list:
        if re.match(reg, recv_account): # 정규표현식과 매칭이 되면 (유효한 메일이면 실행)
            vaild_list.append(recv_account)
        else:
            invalid_list.append(recv_account)
            print(f'다음 주소는 유효하지 않아 제외되었습니다 \n {name} : {recv_account}')
    
    if vaild_list:
        try:
            smtp.sendmail(send_account, vaild_list, msg.as_string())
            print(f'{len(vaild_list)}명에게 정상적으로 메일을 발송하였습니다.')

        except Exception as e:
           print("\n메일 발송에 실패하였습니다.", e)




# smpt 서버와 연결. 25번은 암호화x, 456은 ssl, 587은 tls
def connect_smtp_ssl(server, port):
    '''
    SSL 암호화로 smtp 서버와 연결
    '''
    try:
       smtp = smtplib.SMTP_SSL(server, port) # SSL 암호화로 즉시 연결
    except Exception as e:
       print("\n메일 서버 연결에 실패하였습니다.", e)
    return smtp

'''
# TLS 암호화로 연결 
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
'''

def login_smtp(smtp, sender_account, send_app_password):
    '''
    메일을 보내기 위한 로그인
    '''
    try:
       smtp.login(sender_account, send_app_password)
    except Exception as e:
       print("\n로그인에 실패하였습니다.", e)
 

def prepare_email(title, sender_account, receiver_accounts,  content, image_name):
    '''
    메일 기본 정보 설정 (헤더, 본문, 이미지 첨부)
    '''
    # 메일 기본 정보 설정(헤더 정보)
    msg = MIMEMultipart()           # 메일 컨테이너 생성
    msg["Subject"] = title          # 메일 제목
    msg["From"] = sender_account    # 보낸 사람
    #msg["To"] = receiver_account    # 받는 사람
    msg["To"] = ','.join(receiver_accounts)    # 받는 사람을 ,로 구분하여 여러명 설정

    
    # 메일 본문 내용
    content_part = MIMEText(content, "html") # html로 작성된 본문을 MIMEText 객체로 변환.
    msg.attach(content_part)

    # 이미지 파일 추가
    with open(image_name, 'rb') as file:  # 바이너리 읽기 모드로 파일 열기
        img = MIMEImage(file.read())      # 파일을 읽어 MIMEImage로 변환
        img.add_header('Content-Disposition', 'attachment', filename=image_name)
        msg.attach(img)

    return msg


def open_csv(filename):
    '''
    csv 파일 열기
    '''
    with open(filename, newline='', encoding='utf-8') as file:
        recv_list = []
        reader = csv.reader(file)
        next(reader) # 헤더 스킵 (이름, 이메일)
        for row in reader:
            recv_list.append((row[0], row[1])) # (이름, 이메일) 튜플로 리스트에 추가
    
    return recv_list


 

if __name__ == "__main__":
    # 메일 보내는 계정 (로그인)
    sender_account = "anniehamkm@gmail.com"
    sender_app_password = "cqjq xmjj wzzr hejv"  # 보안상 환경변수로 관리하는 게 좋음

    # smtp 서버와 연결
    gmail_smtp = "smtp.gmail.com"  # gmail smtp 주소
    gmail_port = 465  # gmail smtp 포트번호. ssl
    smtp = connect_smtp_ssl(gmail_smtp, gmail_port)

    # 로그인
    login_smtp(smtp, sender_account, sender_app_password)

    # 메일 내용
    title = f"파이썬으로 여러명에게 동시에 html gmail 보내기"
    content = "안녕하세요 <br> <h3> html로 작성된 본문입니다. </h3> <br> <p> 이미지도 보냅니다 <p> <br>"
    # 첨부 파일명
    image_name = "racon.jpg"

    # csv 파일 열기
    csv_file_name = 'codyssey02/05/mail_target_list.csv'
    recv_list = open_csv(csv_file_name)
    receiver_accounts = [email for name, email in recv_list]

    # 받는 사람이 있으면 메일 발송
    if not recv_list:
        print('받는 사람 목록이 없습니다.')
    else:

        # 반복적으로 한 명씩 메일 발송
        '''
        print(f'{len(recv_list)}명에게 메일을 보냅니다.')
        for name, recv_account in recv_list:
            print(f'{name}님({recv_account})에게 메일을 보냅니다.')
            
            msg = prepare_email(title, sender_account, recv_account, content, image_name)
            sendEmail(smtp, msg, sender_account, recv_account)
        '''

        # 여러명에게 동시에 메일 발송
        msg = prepare_email(title, sender_account, receiver_accounts, content, image_name)
        sendEmailAll(smtp, msg, sender_account, recv_list)
    
 
    # smtp 서버 연결 해제
    smtp.quit()