import socket
import threading

'''전역 변수 설정'''
client_sockets = []
lock = threading.Lock()                                        # 멀티스레드에서 공유 자원 접근 시 충돌 막음

def broadcast_all(msg, sender_sock):
    '''
    메세지를 모든 client에게 보내는 함수(브로드캐스팅)
    '''
    data = msg.encode('utf-8')
    with lock :
        for client_socket in client_sockets:
            if not client_socket[0] is sender_sock:             # 메세지를 송신하는 client에겐 수신하지 않음 
                try:
                    client_socket[0].sendall(data)              # 메세지 송신
                except:
                    pass                                        # 전송 실패는 무시


def client_port_list():
    '''
    현재 접속 중인 클라이언트들의 포트 번호를 문자열로 반환
    '''
    ports = [str(addr[1]) for (sock, addr) in client_sockets]  # client 리스트에서 포트 번호만 리스트로 만듦
    return ' / '.join(ports)                                   # port1 / port2 / .. 이런 형식으로 return 해줌


def find_sock_by_port(target_port):
    '''
    포트 번호로 소켓을 매칭해주는 함수
    '''
    try:
        for sock, addr in client_sockets:
            if addr[1] == int(target_port):                    # 귓속말을 받을 포트 번호와 일치하는 소켓을 반환
                return sock, addr
    except:
        pass
            

def recv_msg(client_sock, client_addr):
    '''
    클라이언트의 메세지를 받아 처리하는 함수
    기본 채팅 기능 | 귓속말 기능
    '''
    try:
        while True:
            data = client_sock.recv(1024)    # 최대 1024byte까지 수신받기
            if not data:
                break                        # 정상 종료 or 연결 끊김
            
            text = data.decode('utf-8', errors='ignore').strip()  # 문자열로 디코드
            if not text:
                continue

            # 1) 종료
            if text == '/종료':
                try:
                    client_sock.sendall('\n[서버] 연결을 종료합니다.'.encode('utf-8'))
                    print(f'\n[퇴장] {client_addr}님이 퇴장하였습니다')
                except:
                    pass
                break
                

            # 2) 접속자 명단
            if text == '/접속자':
                port_list_msg = f'\n현재 접속자 포트 : {client_port_list()}\n'  # port_list_msg = '\n현재 접속자 포트 : 11111 / 11112 / 11113'
                try:
                    client_sock.sendall(port_list_msg.encode('utf-8'))
                except:
                    pass
                continue

            # 3) 귓속말 요청
            if text.startswith('/귓속말'):          # (/귓속말 /포트번호 /메세지) 형식으로 입력 받을 예정
                txt = text.lstrip('/')             # 맨 앞의 '/'는 제거 (귓속말 /포트번호 /메세지)
                parts = txt.split('/', 2)          # 앞에서부터 '/' 기준으로 2번만 나누기

                _, target_port, secret_msg = parts # 귓속말을 전할 포트 번호와 메세지를 나눠 저장
                try:
                    target_sock, target_addr = find_sock_by_port(target_port)
                except:
                    try:
                        client_sock.sendall('\n[귓속말 전송 실패] 수신자를 찾을 수 없습니다'.encode('utf-8'))
                    except:
                        pass
                    continue

                if len(parts) < 3:
                    try:
                        client_sock.sendall('\n[귓속말 전송 실패] 잘못된 입력입니다.'.encode('utf-8'))
                    except:
                        pass
                    continue
                
                else:
                    try:
                        target_sock.sendall(f'\n[{client_addr[1]}의 귓속말] {secret_msg}'.encode('utf-8'))
                    except Exception as e:
                        client_sock.sendall(f'\n[귓속말 전송 실패] {e}'.encode('utf-8'))
                    
                    client_sock.sendall(f'\n[{target_port}에게 귓속말 전송 성공] {secret_msg}'.encode('utf-8'))
                    print(f'\n[{client_addr[1]}이 {target_port}에게 귓속말 전송] {secret_msg}')
                continue

            # 4) 일반 브로드캐스트
            broadcast_msg = f'{client_addr[1]}> {text}'                            # 포트번호> 메세지 형식으로 구성
            broadcast_all(broadcast_msg, client_sock)                              # 메세지를 모든 client에 브로드 캐스팅
            print(f'\n[{client_addr[1]} 메세지] : {broadcast_msg}', end="")  

    except Exception as e:
        print(f'\n[client 메세지 처리 에러] : {e}')
    finally:
        for i, (s,a) in enumerate(client_sockets):
            if s is client_sock:
                del client_sockets[i]  # 클라이언트 리스트에서 제거
                break
        try:
            client_sock.close()
        except:
            pass
        try:
            broadcast_all(f'\n[퇴장] {client_addr}님이 접속을 종료합니다', client_sock)
        except:
            pass


def client_accept_msg(client_sock, client_addr):
    '''
    새로운 클라이언트가 연결되면 [입장] 메세지를 보내고 현재 접속자 수를 알리는 함수
    '''
    broadcast_all(f'\n[입장] {client_addr}에서 입장하였습니다.', client_sock)
    print(f'\n{client_addr}에서 접속 | 현재 접속자 수: {len(client_sockets)}\n'
          f'======================================')
    
def main():
    host = 'localhost'    # 서버 주소
    port = 55555          # 서버 포트

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)   # AF_INET : IPv4(주소체계), SOCK_STREAM : 연결 지향형(TCP), socket.IPPROTO_TCP : TCP 프로토콜 지정(생략 가능)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                     # 옵션 설정. 로컬 주소(ip,port) 재사용 허용 -> 서버 재시작을 빠르게 해줌
    server_sock.bind((host, port))   # 서버 소켓에 주소 연결
    server_sock.listen(5)            # accept를 받기위해 대기 시작, 최대 5개 연결까지 대기시킬 수 있음
    print(f'\n채팅 서버 open\nhost: {host},\tport : {port}\n-------------------------------------------')

    try:
        while True:
            client_sock, client_addr = server_sock.accept()     # accept()는 (소켓 객체, (ip, port)) 튜플 반환. blocking call로 client가 server에 접속할 때까지 대기 상태가 됨
            client_sockets.append([client_sock, client_addr])   # client 정보를 client_sockets 리스트에 추가
            client_accept_msg(client_sock, client_addr)

            t = threading.Thread(target=recv_msg, args=(client_sock, client_addr)) # 새로 들어온 client에 thread 부여
            t.start()
    
    except KeyboardInterrupt:
        print('\n서버 종료')
    finally:
        server_sock.close()



if __name__ == '__main__':
    main()
