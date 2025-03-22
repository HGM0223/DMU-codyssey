
import csv
import pickle


def process_flammable_csv() :
    try :
        with open('codyssey_02/Mars_Base_Inventory_List.csv', 'r', encoding='utf-8') as file:
            # 1.readlines()를 통해 리스트로 반환 -> 각 줄을 요소로 하는 리스트. print(I_list)하면 Alcohol,0.789,0.79,Very weak,0.85
            Inventory_Lists = file.readlines()

            # 2.csv.reader() -> 각 줄을 리스트로 하는 리스트가 만들어짐. print(I_list)하면 ['Alcohol', '0.789', '0.79', 'Very weak', '0.85']
            #reader = csv.reader(file)
            #Inventory_Lists = list(reader)

            #csv내용 출력
            print('\nMars_Base_Inventory_List 내용 출력---------------------\n')
            for I_list in Inventory_Lists :
                print(I_list)

        #sort()를 통해 인화성이 높은 순서대로 정렬
        Inventory_Lists_header = Inventory_Lists[0]
        Inventory_Lists_data = Inventory_Lists[1:] #헤더 제거 
        Inventory_Lists_data.sort(key=lambda x: float(x.split(',')[4]), reverse=True) # ',' 기준 5번째 요소를 내림차순 정렬

    except Exception as e :
        print('Mars_Base_Inventory_List파일 처리중 오류 발생 : ',e)


    try :  
        print('\n인화성 지수가 0.7이상인 물질--------------------------------\n')
        with open('codyssey_02/Mars_Base_Inventory_danger.csv', mode='w', encoding='utf-8') as danger_file :

            header = Inventory_Lists_header.strip().split(',') #기존 csv파일의 header를 가져오는 과정
            writer = csv.writer(danger_file)
            writer.writerow(header)

            for f_list in Inventory_Lists_data :
                if float(f_list.split(',')[4]) >= 0.7 :
                    print(f_list)  #인화성 지수가 0.7이상인 물질 출력
                    data = f_list.strip().split(',') 
                    writer.writerow(data) #리스트로 바꾼후 csv파일에 입력

            print('인화성 지수가 0.7이상되는 목록을 csv로 저장 완료')

    except Exception as e :
        print('Mars_Base_Inventory_danger파일 처리중 오류 발생 : ',e)
           

    try :   
        with open('codyssey_02/Mars_Base_Inventory_List.bin', 'wb') as binary_file :
            pickle.dump(Inventory_Lists_data, binary_file)

        with open('codyssey_02/Mars_Base_Inventory_List.bin', 'rb') as binary_file :
            load_binary_file = pickle.load(binary_file)
            
            # 이진수로 파일 내용 출력하는 방법
            #binary_data = binary_file.read() #바이트 형태로 읽어오기
            #binary_string = ' '.join(format(byte, '08b') for byte in binary_data)
            #print(binary_string)
        
        #원래 내용 그래로 출력하는 방법
        print('\n이진파일로 저장된 내용 출력----------------------------------')
        print("".join(load_binary_file))

    except Exception as e :
        print('Mars_Base_Inventory_List.bin파일 처리중 오류 발생 : ',e)



if __name__ == "__main__" :
    process_flammable_csv()