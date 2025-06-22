from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class MyApplication(QWidget):
    def __init__(self):
        super().__init__()

        self.calculator = Calculator(self)
        self.result_shown = False

        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('계산기')
        self.resize(350, 600)
        self.setStyleSheet("background-color: black;")


        # 레이아웃 생성
        main_layout = QVBoxLayout(self) # QVBoxLayout 윗줄부터 채워가는 레이아웃 종류

        # 식과 결과 입력창
        self.pre_equation = QLineEdit("") # 계산 전 식 저장
        self.equation = QLineEdit("") # 식, 결과 
        
        self.pre_equation.setAlignment(Qt.AlignRight)  # ReadOnly 하는 게 좋음음
        self.equation.setAlignment(Qt.AlignRight)
        self.pre_equation.setFixedHeight(40)
        self.equation.setFixedHeight(40)
        self.pre_equation.setStyleSheet("color: white; border: none; font-size: 20px;")
        #self.equation.setStyleSheet("color: white; border: none; font-size: 40px;")

        main_layout.addWidget(self.pre_equation)
        main_layout.addWidget(self.equation)

        # 버튼 배치용 그리드 레이아웃
        grid = QGridLayout()
        main_layout.addLayout(grid)

        # 버튼 텍스트와 위치 정의
        buttons = [
            ('AC', 0, 0, self.calculator.reset),
            ('+/-', 0, 1, self.calculator.negative_positive),
            ('%', 0, 2, self.calculator.percent),
            ('/', 0, 3, self.calculator.divide),

            ('7', 1, 0, lambda: self.btn_number_clicked('7')),
            ('8', 1, 1, lambda: self.btn_number_clicked('8')),
            ('9', 1, 2, lambda: self.btn_number_clicked('9')),
            ('x', 1, 3, self.calculator.multiply),

            ('4', 2, 0, lambda: self.btn_number_clicked('4')),
            ('5', 2, 1, lambda: self.btn_number_clicked('5')),
            ('6', 2, 2, lambda: self.btn_number_clicked('6')),
            ('-', 2, 3, self.calculator.subtract),

            ('1', 3, 0, lambda: self.btn_number_clicked('1')),
            ('2', 3, 1, lambda: self.btn_number_clicked('2')),
            ('3', 3, 2, lambda: self.btn_number_clicked('3')),
            ('+', 3, 3, self.calculator.add),

            ('0', 4, 0, lambda: self.btn_number_clicked('0')),
            ('.', 4, 2, self.calculator.decimal),
            ('=', 4, 3, self.calculator.equal)
        ]

        for text, row, col, callback in buttons:
            button = QPushButton(text)
            button.setFixedSize(70, 70)
            button.clicked.connect(callback)
            button.setStyleSheet("background-color: gray; color: white; border-radius: 35px; font-size: 25px;")
            if text == '0':
                grid.addWidget(button, row, col, 1, 2)  # 0번 버튼은 2칸
                button.setFixedSize(150, 70)
            else:
                grid.addWidget(button, row, col)


        self.setLayout(main_layout)
        self.show()

    
    # 숫자 입력 함수수
    def btn_number_clicked(self, num):
        # 현재 입력된 식 가져오기 (콤마 제거)
        text = self.equation.text().replace(',', '')
 
        # 새로 입력된 숫자 추가
        text += num

        # 다시 콤마를 붙여서 세팅
        formatted_text = add_commas(text)
        self.equation.setText(formatted_text)
        self.result_shown = False

        self.adjust_font_size()

    def adjust_font_size(self):
        text = self.equation.text().replace(',', '')
        length = len(text)

        if length >= 15:
            font_size = 20
        elif length >= 10:
            font_size = 30 
        elif length >= 5:
            font_size = 35
        else:
            font_size = 40

        self.equation.setStyleSheet(f"color: white; border: none; font-size: {font_size}px;")


class Calculator():
    # Calculator에서 MyApplication의 변수에 접근하기 위한 초기화 메서드
    # self.app 이 MyApplication 클래스를 가리킴
    def __init__(self, app):
        self.app = app        
    
    # 사칙연산 함수
    def add(self):
        self.app.equation.setText(self.app.equation.text() + '+')
        self.app.adjust_font_size()

    def subtract(self):
        self.app.equation.setText(self.app.equation.text() + '-')
        self.app.adjust_font_size()

    def multiply(self):
        self.app.equation.setText(self.app.equation.text() + 'x')
        self.app.adjust_font_size()
        
    def divide(self):
        self.app.equation.setText(self.app.equation.text() + '/')
        self.app.adjust_font_size()

    def equal(self):
        try:
            # 둘째줄의 방정식을 계산하기 전 첫줄에 출력시킴킴
            self.app.pre_equation.setText(self.app.equation.text())
            
            expr = self.app.equation.text().replace(',', '').replace('x', '*') # , 안 바꾸면 오류남
            result = eval(expr)
            if result == int(result):
                result = f"{int(result):,}"
                self.app.equation.setText(str(result))
            else :
                self.app.equation.setText(str(f"{eval(expr): .6f}"))
            # 결과가 제대로 출력되면 result_shown = True
            self.app.result_shown = True
        except:
            self.app.equation.setText('error')
        
        self.app.adjust_font_size()

    def reset(self):
        eq = self.app.equation.text().replace(',', '')

        # 이전에 '='을 눌러서 결과가 표시된 상태였다면 전체 초기화
        if self.app.result_shown:
            self.app.pre_equation.clear()
            self.app.equation.clear()
            self.app.result_shown = False
            return

        # 새로운 입력이 들어온 상태라면 한 글자만 삭제
        else:
            new_text = eq[:-1]
            self.app.equation.setText(add_commas(new_text))
    
    def negative_positive(self):
        eq = self.app.equation.text()
        if not eq:
            return

        eq = eq.replace(',', '')  # 숫자 처리 위한 콤마 제거

        i = len(eq) - 1
        # 숫자, 소수점, 괄호까지 뒤에서부터 스캔
        while i >= 0 and eq[i] not in ['+', 'x', '/']:
            if eq[i] == '-' and eq[i-1] == '(':
                i -= 2
                break
            if eq[i] == '-' and eq[i-1] != '(':
                i -= 1
                break
            i -= 1
                

        before_target = eq[:i+1]
        target_expression = eq[i+1:]  # 바꿀 값, (-2) , -3 등등

        # 공백제거
        target_expression = target_expression.strip()
        if target_expression.startswith('(-') and target_expression.endswith(')'):
            # (-2) → 괄호 제거 2
            new_target_number = target_expression[2:-1]
        elif target_expression.startswith('-') and target_expression[1:].replace('.', '', 1).isdigit():
            # -3 → 양수 3
            new_target_number = f'+{target_expression[1:]}'
        elif target_expression.replace('.', '', 1).isdigit():
            # 3 → 음수 괄호로 감싸기 (-3)
            new_target_number = f'(-{target_expression})'


        new_eq = before_target + new_target_number
        self.app.equation.setText(add_commas(new_eq))

    
    def percent(self):
        self.app.equation.setText(self.app.equation.text() + '%')

    # 소수점
    def decimal(self):
        eq = self.app.equation.text()

        # 수식이 비어있다면 그냥 .을 추가해도 됨
        if not eq:
            self.app.equation.setText('0.')
            return

        # 수식 끝에서부터 숫자/소수점만 찾아서 현재 입력 중인 숫자 추출
        i = len(eq) - 1
        while i >= 0 and (eq[i].isdigit() or eq[i] == '.' or eq[i] == ','):
            i -= 1
        current_number = eq[i+1:]  # 끝부분 숫자만 추출

        if '.' in current_number:
            return  # 이미 소수점이 포함되어 있으면 무시

        # 소수점 추가
        self.app.equation.setText(eq + '.')


# ',' 붙여주는 함수
def add_commas(text):        
    # equation에 넣을 최종 문자열을 저장하는 변수
    result = '' 
    # temp는 text에서 숫자만 임시 저장하기 위한 변수
    num_buffer = ''

    for ch in text: # self.equation.text()에서 한 글자씩 ch에 넣어 검사 
        if ch.isdigit() or ch == '.': # 숫자이거나 '.'일 때 temp에 넣어둠
            num_buffer += ch
        else:
            if num_buffer: # temp가 비어있지 않을 때
                result += format_number(num_buffer)
                num_buffer = ''
            result += ch # 연산자 다시 넣어주기 
    if num_buffer: 
        result += format_number(num_buffer)

    return result

# 소수점이 있는 경우. 정수/실수 부분을 나눠서 처리
def format_number(num_buffer):
    if '.' in num_buffer:
        integer_part, decimal_part = num_buffer.split('.', 1)
        return f"{int(integer_part):,}.{decimal_part}"
    else:
        return f"{int(num_buffer):,}"# 1000 -> 1,000 으로 바꿔줌



if __name__ == '__main__':
    app = QApplication([])     # 어플리케이션 객체 생성
    window = MyApplication()       # MyApplication 클래스 생성(init의 show로 클래스를 만들면 즉시 화면창도 생성)
    app.exec_()                # 어플리케이션 실행(이벤트처리 가능 상태)



'''
# 처음 했던 방식
# move를 이용한 좌표 직접 지정

    def setup_ui(self, text, x, y, w, h, callback):
        btn = QPushButton(text, self)
        btn.move(x, y)
        btn.setFixedSize(w, h)
        btn.clicked.connect(callback)
        return btn
'''