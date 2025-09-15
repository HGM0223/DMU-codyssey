import socket
import threading

# 새로운 client를 받아들이고 현재 client의 수를 반환하는 함수
def client_accept():
    child_sock, child_addr = server_sock.accept()     # accept()는 (소켓 객체, (ip, port)) 튜플 반환. blocking call로 client가 server에 접속할 때까지 대기 상태가 됨
    client_sockets.append([child_sock, child_addr])   # client 정보를 client_sockets 리스트에 추가
    announce_join_msg((child_sock, child_addr))
    print(f'\n{child_addr}에서 접속')
    print(f'\n현재 접속자 수: {len(client_sockets)}')
    print('======================================')


    return [child_sock, child_addr]                   # 새로운 client를 받은 후 client 정보를 반환


# '~님이 접속하셧습니다' 전송 함수
def announce_join_msg(from_client):  
    sock, addr = from_client 
    msg = f'\n[입장] {addr}님이 입장하셨습니다'           # from_client : 메세지를 보내는 client
    for client_socket in client_sockets:
        if not client_socket[0] == sock:            # 메세지를 송신하는 client에겐 수신하지 않음 
            client_socket[0].sendall(msg.encode('utf-8'))   


# 모든 client에게 메세지를 보내는 함수
def send_msg_all(msg, from_sock):                     # msg : 보낼 메세지, from_sock : 메세지를 보내는 client
    for client_socket in client_sockets:
        if not client_socket == from_sock:            # 메세지를 송신하는 client에겐 수신하지 않음 
            client_socket[0].sendall(msg)             # client_socket[0]은 각 client의 소켓 객체 


# 접속 중인 클라이언트 포트 목록
def client_port_list():
    ports = [str(addr[1]) for (sock, addr) in client_sockets]  # client 리스트에서 포트 번호만 리스트로 만듦
    return ' / '.join(ports)                                    # port1 / port2 / .. 이런 형식으로 return 해줌


# client의 채팅을 받아 전달하는 함수
def recv_msg(from_sock):       
    sock, addr = from_sock 
    try:
        while True:
            data = from_sock[0].recv(1024)                                           # 최대 1024바이트까지 메세지를 읽음
            data_decoded = data.decode('utf-8', errors='ignore').strip()             # socket은 byte로 정보를 주고 받기 때문에 '/종료'문자열과 비교하기 위해 decode함
            
            if data_decoded == '/종료':                                            
                try: 
                    from_sock[0].sendall('\n[서버] 연결을 종료합니다.\n'.encode('utf-8')) # 사용자가 '/종료' 입력시 종료 메세지 보내고 break
                except: 
                    pass
                break

            mode = 'normal'

            # 기본 normal 모드일때 메세지 처리
            if mode == 'normal':
                # 귓속말 모드 신청
                if data_decoded == '1-1':
                    mode = 'wait_port' # 모드 변경
                    port_list = client_port_list()
                    reply = f'\n 현재 접속자 목록 : {port_list}' 
                    try:
                        from_sock[0].sendall(reply.encode('utf-8'))
                    except Exception as e:
                        print(f'[에러] 접속자 목록 전송 실패 : {e}')
                    continue
                # 일반 브로드캐스트
                message = f'{addr[1]}> {data_decoded}\n'                            # 포트번호> 메세지 형식으로 구성
                send_msg_all(message.encode('utf-8'), from_sock)                    # 메세지를 모든 client에 브로드 캐스팅
                print(f'\n[client 메세지] : {message}', end="")                      # 누가 어떤 메세지를 보냈는지 콘솔에 출력

            elif mode == 'wait_port' :
                receiver_port = int(data_decoded)
                mode = 'wait_msg'

            elif mode == 'wait_msg' :
                msg = data_decoded
                secret_msg(msg, receiver_port,from_sock)
                mode = 'normal'


    except Exception as e:
        print(f'\n[에러] {from_sock[1]}: {e}')
    finally:
        close_client(from_sock)

# 포트 번호로 소켓을 매칭해주는 함수
def find_sock_by_port(receiver_port):
    for sock, addr in client_sockets:
        if addr[1] == receiver_port:        # 귓속말을 받을 포트 번호와 일치하는 소켓을 반환
            return sock, addr
        

# 귓속말 전달하는 함수
def secret_msg(msg, receiver_port, from_sock):
    receiver_sock, receiver_addr = find_sock_by_port(receiver_port) 
    sender_sock, sender_addr = from_sock
    if not receiver_sock: 
        try:
            sender_sock.sendall(f'포트 {receiver_port} 사용자를 찾을 수 없습니다')
        except:
            pass
        return
    secret_message = f'\n{sender_addr[1]} > {msg}'
    try: 
        receiver_sock.sendall(secret_message.encode('utf-8'))
        sender_sock.sendall('귓속말 전달 완료'.encode('utf-8'))
    except Exception as e:
        print(f'귓속말 전송 중 실패 : {e}')
            

# client 접속 종료하는 함수
def close_client(client_sock):
    try:
        client_sock[0].close()
    except Exception as e:
        print(f'\n[에러] 소켓 닫기 중 에러 발생 {client_sock[1]}: {e}')
    finally:
        if client_sock in client_sockets:
            client_sockets.remove(client_sock)
            print(f'\n{client_sock[1]} 연결 종료')


threads = []          # 스레드 리스트
client_sockets = []   # 현재 접속중인 client 리스트

host = 'localhost'    # 서버 주소
port = 55555          # 서버 포트

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)   # AF_INET : IPv4(주소체계), SOCK_STREAM : 연결 지향형(TCP), socket.IPPROTO_TCP : TCP 프로토콜 지정(생략 가능)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                     # 옵션 설정. 로컬 주소(ip,port) 재사용 허용 -> 서버 재시작을 빠르게 해줌
server_sock.bind((host, port))   # 서버 소켓에 주소 연결
server_sock.listen(5)            # accept를 받기위해 대기 시작, 최대 5개 연결까지 대기시킬 수 있음
print(f'\n채팅 서버 open\nhost: {host},\tport : {port}\n-------------------------------------------')

while True:
    client_info = client_accept()  # 새로 등록한 client의 [소켓, 주소]
    recv_thread = threading.Thread(target=recv_msg, args=(client_info,))  # 새로 들어온 client에 thread 부여
    recv_thread.start()            # thread 시작
    threads.append(recv_thread)    # thread 리스트에 방금 만든 스레드 넣음
