stop_file_path = 'codyssey_03_04/stop_signal.txt'

while True :
    user_input = input('엔터를 누르면 센서 측정이 종료됩니다. : ')
    if user_input.strip() == '' :
        with open(stop_file_path, 'w') as f:
            f.write("STOP")
