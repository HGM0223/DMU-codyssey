
import csv


def process_flammable_csv() :
    try :
        with open('codyssey_02/Mars_Base_Inventory_List.csv', 'r', encoding='utf-8') as file:
            #readlines()를 통해 리스트로 반환
            Inventory_Lists = file.readlines()

            #csv내용 출력
            print('\nMars_Base_Inventory_List 내용 출력------------\n')
            for I_list in Inventory_Lists :
                print(I_list)

        #sort()를 통해 인화성이 높은 순서대로 정렬
        Inventory_Lists_header = Inventory_Lists[0]
        Inventory_Lists_data = Inventory_Lists[1:] #헤더 제거 
        Inventory_Lists_data.sort(key=lambda x: float(x.split(',')[4]), reverse=True) # ',' 기준 5번째 요소를 내림차순 정렬
        


    except Exception as e :
        print('Mars_Base_Inventory_List파일 처리중 오류 발생 : ',e)


    try :  
        print('\n인화성 지수가 0.7이상인 물질-------------------\n')
        with open('codyssey_02/Mars_Base_Inventory_danger.csv', mode='w', encoding='utf-8') as danger_file :
            header = Inventory_Lists_header.split(',') #기존 csv파일의 header를 가져오는 과정
            writer = csv.writer(danger_file)
            writer.writerow(header)
            for f_list in Inventory_Lists_data :
                if float(f_list.split(',')[4]) >= 0.7 :
                    print(f_list)  #인화성 지수가 0.7이상인 물질 출력
                    data = f_list.split(',') 
                    writer.writerow(data) #리스트로 바꾼후 csv파일에 입력
            print('인화성 지수가 0.7이상되는 목록을 csv로 저장 완료')

    except Exception as e :
        print('Mars_Base_Inventory_danger파일 처리중 오류 발생 : ',e)
           



if __name__ == "__main__" :
    process_flammable_csv()