import pymysql
import pandas as pd
from datetime import date, timedelta
import yfinance as yf
from crawling_class import stock_craw

#주식 리스트 가져오기
def get_stock_list():
    # StockCrawler 클래스의 인스턴스 생성
    crawler = stock_craw()
    # 종목 이름과 URL 추출 메서드 호출
    crawler.name_craw()
    # 종목 코드 추출 메서드 호출
    crawler.url_craw()
    try: # MySQL 데이터베이스 연결
        con = pymysql.connect(host='localhost',
                              user='root',
                              password='1234',
                              db='Stock_predict')
        cursor = con.cursor()
        for name, code in zip(crawler.stock_name,crawler.stock_code):
            sql = "INSERT INTO stock_list (stock_name, stock_code) VALUES (%s, %s)"
            cursor.execute(sql, (name, code))
        con.commit()
        con.close()
    except Exception as e:
        print(e)


# 전체(2년치) 데이터 가져오는 함수
def get_all_data(stock_code, stock_name):
    # MySQL 연결 설정
    host = '127.0.0.1'
    port = 3306
    username = 'root'
    password = '1234'
    database = 'stock_predict'

    # MySQL 연결
    connection = pymysql.connect(host=host,port=port,user=username,password=password,database=database)

    # 날짜 설정
    end_date = date.today()
    start_date = end_date - timedelta(days=730)

    try:
        # 각 종목별로 데이터 다운로드 및 MySQL에 저장

        stock_data = yf.download(stock_code, start=start_date, end=end_date)


        # 테이블 생성 (이미 존재할 경우 무시)
        with connection.cursor() as cursor:

            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {stock_name} (
                Date DATE PRIMARY KEY,
                Open FLOAT,
                High FLOAT,
                Low FLOAT,
                Close FLOAT,
                Adj_Close FLOAT,
                Volume INT
            );
            """

            cursor.execute(create_table_query)

        # 데이터프레임을 MySQL 테이블에 삽입
        with connection.cursor() as cursor:
            truncate_table_query = f"TRUNCATE TABLE {stock_name};"
            cursor.execute(truncate_table_query)
            for index, row in stock_data.iterrows():
                sql = f"""
                INSERT INTO {stock_name} (Date, Open, High, Low, Close, Adj_Close, Volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))
        # 변경 사항 커밋
        connection.commit()
        print("주식 데이터가 MySQL 데이터베이스에 저장되었습니다.")
    except Exception as e:
        print(e)
        pass
    finally:
        # 연결 종료
        connection.close()




if __name__=="__main__":
    get_stock_list()


