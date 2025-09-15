from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("계산기")
        self.setFixedSize(400, 500)

        grid = QGridLayout()
        self.setLayout(grid)

        self.buttons = {}  # 버튼을 딕셔너리에 저장

        # 버튼 이름들 (이미지 순서대로)
        labels = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row, row_labels in enumerate(labels):
            for col, label in enumerate(row_labels):
                # "0"은 2칸 차지하게 하기
                if label == '0':
                    button = QPushButton(label)
                    button.setFixedSize(160, 80)
                    grid.addWidget(button, row, col, 1, 2)  # row, col, rowspan, colspan
                    continue
                if label == '=' and len(row_labels) == 3:
                    col += 1  # =는 오른쪽으로 밀기

                button = QPushButton(label)
                button.setFixedSize(80, 80)
                button.setStyleSheet(self.round_button_style())
                button.clicked.connect(self.make_handler(label))
                grid.addWidget(button, row, col)
                self.buttons[label] = button

        self.show()

    def round_button_style(self):
        return """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 40px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """

    def make_handler(self, label):
        return lambda: print(f"'{label}' 버튼이 눌렸습니다.")

if __name__ == '__main__':
    app = QApplication([])
    calc = Calculator()
    app.exec_()
