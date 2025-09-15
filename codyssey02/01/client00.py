import socket
import threading
import sys

def recv_msg():
    while True:
        msg = client_sock.recv(1024)
        if not msg:                     # 서버가 닫힐 경우
            print('[서버 연결 종료]')
            break
        sys.stdout.write('\r'+ ' '*80+ '\r')
        print(f'\n{msg.decode("utf-8")}\n')
        sys.stdout.write('\n메세지 입력 > ')
        sys.stdout.flush()

def send_msg(msg):
    client_sock.sendall(msg.encode('utf-8'))

#def recv_client_list():




server_host = 'localhost'
server_port = 55555

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # IPv4로 TCP 프로토콜 사용

client_sock.connect((server_host,server_port))                    # 접속 시도
print(f'[서버] {server_host}, {server_port}에 정상적으로 연결')

recv_thread = threading.Thread(target=recv_msg)
recv_thread.start()

while True:
    msg = input('메세지 입력 > ')
    if msg == '/종료':
        client_sock.sendall(msg.encode('utf-8'))
        client_sock.close()
        break
    if msg == '1-1':
        input('귓속말 할 유저의 포트 번호 입력 : ')
        input('귓속말 멜세지 입력 : ')
    send_msg(msg)
