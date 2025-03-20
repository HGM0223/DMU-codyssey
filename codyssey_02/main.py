

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


    try:
        print('\n인화성 지수가 0.7 이상인 물질--------------------------------\n')
        with open('codyssey_02/Mars_Base_Inventory_danger.csv', mode='w', encoding='utf-8') as danger_file:
            danger_file.write(Inventory_Lists_header)

            for f_list in Inventory_Lists_data:
                if float(f_list.split(',')[4]) >= 0.7:
                    print(f_list.strip())
                    danger_file.write(f_list)

        print('인화성 지수가 0.7 이상되는 목록을 csv로 저장 완료')
    
    except Exception as e:
        print('Mars_Base_Inventory_danger 파일 처리 중 오류 발생:', e)
        return
    
           

    try:
        with open('codyssey_02/Mars_Base_Inventory_List.bin', 'wb') as binary_file:
            for line in Inventory_Lists_data:
                binary_file.write(line.encode('utf-8'))
                binary_file.write(b'\n')
        
        with open('codyssey_02/Mars_Base_Inventory_List.bin', 'rb') as binary_file:
            load_binary_file = binary_file.readlines()
        
        print('\n이진 파일로 저장된 내용 출력----------------------------------')
        for line in load_binary_file:
            print(line.decode('utf-8').strip())
    
    except Exception as e:
        print('Mars_Base_Inventory_List.bin 파일 처리 중 오류 발생:', e)
        return



if __name__ == "__main__" :
    process_flammable_csv()