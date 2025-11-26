import smtplib  # SMTP 사용을 위한 모듈
import re       # 정규표현식 사용을 위한 모듈
from email.mime.multipart import MIMEMultipart  # 메일의 Data(텍스트, 이미지 등)를 담는 컨테이너 모듈
from email.mime.text import MIMEText            # 메일의 텍스트 본문 내용을 넣기 위한 모듈
from email.mime.image import MIMEImage          # 메일의 이미지 파일을 base64 형식으로 변환하기 위한 모듈
 
def sendEmail(addr):
    '''
    메일 주소 유효성 검사 후 메일 발송
    '''
    reg = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"  # 유효성 검사를 위한 정규표현식. r은 rqw string \. 같은 이스케이프 경고 피함. $는 끝을 의미
    if re.match(reg, addr): # 정규표현식과 매칭이 되면 (유효한 메일이면 실행)
        try: 
            smtp.sendmail(send_account, to_mail, msg.as_string()) 
            print("정상적으로 메일이 발송되었습니다.")
        except Exception as e:
            print("\n메일 발송에 실패하였습니다.", e)
    else:
        print("받으실 메일 주소를 정확히 입력하십시오.")
 

# smpt 서버와 연결. 25번은 암호화x, 456은 ssl, 587은 tls
gmail_smtp = "smtp.gmail.com"  # gmail smtp 주소
gmail_port = 465  # gmail smtp 포트번호. 고정(변경 불가)
try:
    smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port) # SSL 암호화로 즉시 연결
except Exception as e:
    print("\n메일 서버 연결에 실패하였습니다.", e)

'''
# TLS 암호화로 연결 
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
'''

# 메일 보내는 계정 (로그인)
send_account = "anniehamkm@gmail.com"
send_app_password = "cqjq xmjj wzzr hejv"  # 보안상 환경변수로 관리하는 게 좋음
try:
    smtp.login(send_account, send_app_password)
except Exception as e:
    print("\n로그인에 실패하였습니다.", e)
 
# 메일을 받을 계정
to_mail = "jwsh171210@naver.com"
 

# 메일 기본 정보 설정(헤더 정보)
msg = MIMEMultipart() # 메일 컨테이너 생성
msg["Subject"] = f"최서현에게 파이썬으로 gmail 보내기 - 사진 첨부v"  # 메일 제목
msg["From"] = send_account                            # 보낸 사람
msg["To"] = to_mail                                   # 받는 사람
 
# 메일 본문 내용
content = "smtp를 통해 메일보내기. \n\n\
첨부파일도 함께\n\n\
"
content_part = MIMEText(content, "plain") # 평문 텍스트로 작성된 본문을 MIMEText 객체로 변환.
msg.attach(content_part)
 
# 이미지 파일 추가
image_name = "racon.jpg"
with open(image_name, 'rb') as file:  # 바이너리 읽기 모드로 파일 열기
    img = MIMEImage(file.read())      # 파일을 읽어 MIMEImage로 변환
    img.add_header('Content-Disposition', 'attachment', filename=image_name)
    msg.attach(img)
 
# 받는 메일 유효성 검사 거친 후 메일 전송
sendEmail(to_mail)
 
# smtp 서버 연결 해제
smtp.quit()