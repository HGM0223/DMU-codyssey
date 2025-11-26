
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler  # BaseHTTPRequestHandler 요청 처리용 핸들러

ROOT = Path(__file__).parent                                # 현재 파이썬 파일이 있는 경로
INDEX = ROOT / "index.html"                                 # 사용할 index.html 경로 설정

class myHandler(BaseHTTPRequestHandler):                    # http 서버가 실행할 함수. 매 요청마다 인스턴스가 생성되어 실행
    def set_Header(self, code):
        self.send_response(code)                            # 상태코드를 응답 헤더의 첫 줄에 전송

    def do_GET(self):
        print('get 요청이 들어옴')
        client_ip, client_port = self.client_address
        server_ip, server_port = server_address
        
        if self.path == "/" or self.path == "/index.html":  # 브라우저가 http://127.0.0.1:8080/ 또는 http://127.0.0.1:8080/index.html을 요청했을 때
            try:
                content = INDEX.read_bytes()                # byte로 읽어옴 
                    
            except FileNotFoundError:
                self.send_error(404)                        # 파일이 없으면 404 오류
                return
            
            self.set_Header(200)                                             # 접속 성공 코드 200 전송
            self.send_header('Content-Type', 'text/html; charset=utf-8')     # 본문 길이 
            self.send_header('Content-Length', str(len(content)))            # 본문 길이 
            self.end_headers()                                               # 헤더 끝 
            self.wfile.write(content)                                        # 본문 전송
            print(f'클라이언트 | {client_ip} : {client_port} -> 서버 | {server_ip} : {server_port}')

        else:
            self.send_error(404)

                    





    

if __name__ == '__main__':
    server_address = ('127.0.0.1', 8080)              # 서버가 바인딩할 주소와 포트. 0.0.0.0은 내가 가진 어떤 ip로 오는 요청도 받겠다는 의미(LAN이 여러개면 ip도 여러개인가봄)
    httpd = HTTPServer(server_address, myHandler)     # HTTP서버 생성
    print('서버 시작')
    try:
        httpd.serve_forever()                         # 서버 루프 시작
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()                          # 소켓, 서버 종료
        print('서버 끝')