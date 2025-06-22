import csv
import os
import datetime
import sounddevice as sd
import wave
import speech_recognition as sr
import whisper


def ensure_record_folder_exists():
    if not os.path.exists('records'):
        os.makedirs('records')

def ensure_recordSTT_folder_exists():
    if not os.path.exists('records_stt'):
        os.makedirs('records_stt')


def get_filename_by_datetime():
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    return os.path.join('records', filename)

# sample_rate는 헤르츠값. 인간이 들을 수 있는 소리를 담기위해 40,000hz이상이 필요하고, 너무 크게 설정하면 파일 용량이 커짐.
# channels는 오디오 채널. 1은 모노, 2는 스테레오
# dtype으로 소리의 해상도 값. 고품질은 float32 등으로 처리할 수 있음
def record_voice(duration = 5, sample_rate = 44100):
    print('녹음을 시작합니다. {}초 동안 기다려주세요...'.format(duration))
    recording = sd.rec(int(duration * sample_rate), samplerate = sample_rate, channels = 1, dtype = 'int16')
    sd.wait()
    filename = get_filename_by_datetime()

    try:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16bit = 2bytes
            wf.setframerate(sample_rate)
            wf.writeframes(recording.tobytes())
    
    except Exception as e:
        print(f'오류발생 : {e}\n')
        return None

    print('녹음 완료: {}'.format(filename))



def list_files_in_date_range(start_date, end_date):
    matched_files = []

    print('\n녹음 파일을 날짜 범위로 검색합니다: {} ~ {}'.format(start_date, end_date))
    for filename in os.listdir('records'):
        if filename.endswith('.wav'):
            try:
                file_date = datetime.datetime.strptime(filename[:-4], '%Y%m%d-%H%M%S').date() # 연월일만 추출
                if start_date <= file_date <= end_date:
                    matched_files.append(filename)
            except ValueError:
                continue

    if matched_files:
       print('\n검색된 오디오 파일 목록')
       for index, file in enumerate(matched_files, start = 1):
           print('{}. {}'.format(index, file))
    else:
        print('\n해당 날짜 범위에는 오디오 파일이 없습니다.')



def stt_all_whisper():
    print('\n[STT 실행] records 폴더 내 .wav 파일을 불러옵니다.')

    files = [f for f in os.listdir('records') if f.endswith('.wav')]
    if not files:
        print('records 폴더에 .wav 파일이 없습니다.')
        return

    model = whisper.load_model('base') 

    for wav_file in files:
        csv_file = wav_file.replace('.wav', '.csv')
        csv_path = os.path.join('records', csv_file)
        wav_path = os.path.join('records', wav_file)

        if os.path.exists(csv_path):
            print('이미 처리된 파일입니다: {}'.format(csv_file))
            continue

        print('{} 변환 중...'.format(wav_file))
        result = model.transcribe(wav_path)

        segments = result.get('segments', [])
        if not segments:
            print('인식 결과 없음')
            continue

        with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['시작', '끝', '인식된 텍스트'])

            for seg in segments:
                start = '{:.2f}'.format(seg['start'])
                end = '{:.2f}'.format(seg['end'])
                text = seg['text'].strip()
                writer.writerow([start, end, text])
                print(f'{start}~{end}초: {text}')


def stt_some_whisper(wav_file_name):
    print('\n[{}.wav 파일 STT 실행]'.format(wav_file_name))
    wav_file = wav_file_name + '.wav'
    wav_path = os.path.join('records', wav_file_name)
    csv_file = wav_file.replace('.wav', '.csv')
    csv_path = os.path.join('records', csv_file)


    





def main():
    ensure_record_folder_exists()
    ensure_recordSTT_folder_exists()

    
    while True:
        print('\n원하는 작업을 선택하세요===============')
        print('1. 끝내기')
        print('2. 녹음하기')
        print('3. 녹음 파일 검색')
        print('4. 모든 파일 STT 수행')
        print('5. 지정 파일 STT 수행')


        choice = input('선택 (1/2/3/4): ')

        if choice == '1':
            print('프로그램을 종료합니다.')
            break

        elif choice == '2':
            try:
                duration = int(input('녹음할 시간(초)을 입력하세요: '))
                record_voice(duration = duration)
            except ValueError:
                print('잘못된 입력입니다. 숫자를 입력해주세요.')

        elif choice == '3':
            start_str = input('\n시작 날짜를 입력하세요 (20250101): ')
            end_str = input('마지막 날짜를 입력하세요(20250102): ')

            try:
                start_date = datetime.datetime.strptime(start_str, '%Y%m%d').date()
                end_date = datetime.datetime.strptime(end_str, '%Y%m%d').date()

                # 시작 날짜가 끝 날짜보다 크면 바꿔서 검색
                if end_date < start_date :
                    temp = start_date
                    start_date = end_date
                    end_date = temp               


                list_files_in_date_range(start_date, end_date)
            except ValueError:
                print('잘못된 날짜 형식입니다. 20250101처럼 입력해주세요.')

        elif choice == '4':
            stt_all_whisper()

        elif choice == '5':
            wav_file_name = input('stt를 수행할 파일명을 입력하세요(예시 20250605-120101) : ')
            stt_some_whisper(wav_file_name)

        else:
            print('잘못된 입력력입니다. 1, 2, 3, 4 중 하나를 입력해주세요.')


if __name__ == '__main__':
    main()


