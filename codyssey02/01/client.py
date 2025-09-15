import socket
import threading
import sys

def close(client_sock):
    '''
    연결 종료 함수
    - [수신 에러] 서버가 사라졌을 때 실행
    '''
    try:
        client_sock.shutdown(socket.SHUT_RDWR)            # 소켓을 close하기 전 데이터 송수신부터 막아줌
    except:
        pass

    try:
        client_sock.close()
    except:
        pass


def recv_loop(client_sock, stop_event:threading.Event):
    '''
    서버에서 오는 데이터를 화면에 출력하는 함수
    - 메세지가 오면 현재 프롬프트를 지우고 다시 출력
    '''
    try:
        while not stop_event.is_set():                    # thread에 stop_event가 발생할 때까지
            data = client_sock.recv(1024)                 # 데이터 수신
            if not data:                                  # 서버가 닫힐 경우
                print('\n[서버 연결 종료]')
                break

            text = data.decode('utf-8', errors='ignore')  # utf-8로 디코딩
            if('연결을 종료' in  text):                     # /종료 를 입력해서 서버에서 '[서버]연결을 종료합니다'가 돌아오면
                sys.stdout.write('\r'+ ' '*80+ '\r')      # 메세지 입력> 을 지우고 커서를 앞으로 옮김
                sys.stdout.flush()
                print(text)     
                continue                      

            sys.stdout.write('\r'+ ' '*80+ '\r')          # 메세지 입력> 을 지우고 커서를 앞으로 옮김
            sys.stdout.flush()
            print(text)                                   # 수신받은 메세지 출력
            sys.stdout.write('\n메세지 입력 > ')

    except Exception as e:
        sys.stdout.write('\r'+ ' '*80+ '\r')          
        sys.stdout.flush()
        print(f'\n[수신 에러] {e}')
    
    finally:
        close(client_sock)
        stop_event.set()


def send_loop(client_sock, stop_event:threading.Event):
    '''
    클라이언트의 입력을 받아 서버에 넘기는 함수
    '''
    try:
        while not stop_event.is_set():
            msg = input('\n메세지 입력 >')
            if not msg :
                continue

            try:
                client_sock.sendall((msg+'\n').encode('utf-8'))
            except Exception as e:
                print(f'\n[전송 에러] {e}')
                close(client_sock)
                break

            if msg == '/종료':
                stop_event.wait(0.5)     # /종료 입력 후엔 recv_loop에서 처리를 받아올 것이기 때문에 send_loop는 잠시 대기시킴

    except:
        pass
    finally:
        close(client_sock)
        stop_event.set()




def main():
    server_host = 'localhost'
    server_port = 55555

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # IPv4로 TCP 프로토콜 사용
    client_sock.connect((server_host,server_port))                    # 접속 시도
    
    my_port = client_sock.getsockname()[1]
    print(f'\n[서버] {server_host}, {server_port}에 정상적으로 연결, (내 포트 : {my_port})\n')

    print('''
          
    [사용 가능한 명령] 
      /접속자                  : 현재 접속중인 클라이언트 목록 확인
      /귓속말/상대 번호/메세지  : 귓속말 보내기 (예: /귓속말/55122/안녕하세요)
      /종료                    : 연결 종료
          
    '''.strip())
    print('\n')
    
    stop_event = threading.Event() # 여러 thread에서 공유해서 사용할 수 있는 Event 객체

    recv_thread = threading.Thread(target=recv_loop, args=(client_sock, stop_event), daemon=True)
    recv_thread.start()

    send_thread = threading.Thread(target=send_loop, args=(client_sock, stop_event), daemon=True)
    send_thread.start()

    stop_event.wait()              # set()을 기다림. stop_event.is_set()이 되면 바로 종료, daemon도 함께 정리함.

    
    recv_thread.join(timeout=0.5)  # thread 끝날때까지 잠시 기다림
    send_thread.join(timeout=0.5)  

    print('\n클라이언트 종료')
        

if __name__ == '__main__':
    main()


        
