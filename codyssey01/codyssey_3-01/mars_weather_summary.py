import mysql.connector

csv_path = 'mars_weathers_data.CSV'


class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def insert_data_from_csv(filepath):
    db_helper = MySQLHelper(
        host='localhost',
        user='root',
        password='hamkm',
        database='mars'
    )

    with open(filepath, 'r', encoding='utf-8') as file:
        next(file)  # 헤더 줄 건너뜀
        for line in file:
            line = line.strip()
            if not line:
                continue

            columns = line.split(',')
            if len(columns) < 4:
                continue  # 잘못된 줄 무시

            # 첫 번째 컬럼은 weather_id → 생략하고 나머지 3개 사용
            _, date_str, temp_str, storm_str = columns

            # 데이터 출력
            print(f"[{line_num}번째 줄] 날짜: {date_str}, 온도: {temp_str}, 폭풍: {storm_str}")

            query = (
                'INSERT INTO mars_weather (mars_date, temp, storm) '
                'VALUES (%s, %s, %s)'
            )
            db_helper.execute_query(query, (date_str, float(temp_str), int(storm_str)))

    db_helper.commit()
    db_helper.close()


insert_data_from_csv(csv_path)
