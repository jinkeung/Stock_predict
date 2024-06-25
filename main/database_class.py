import pymysql
import pandas as pd
from datetime import date, timedelta
import yfinance as yf
from crawling_class import stock_craw

#db 연결
def connect_db():
    host = '127.0.0.1'
    port = 3306
    username = 'root'
    password = '1234'
    database = 'stock_predict'
    # MySQL 연결
    connection = pymysql.connect(host=host,port=port,user=username,password=password,database=database)
    return connection

#주식 리스트 db적재
def set_stock_list():
    # StockCrawler 클래스의 인스턴스 생성
    crawler = stock_craw()
    # 종목 이름과 URL 추출 메서드 호출
    crawler.name_craw()
    # 종목 코드 추출 메서드 호출
    crawler.url_craw()
    try: # MySQL 데이터베이스 연결
        con = connect_db()
        cursor = con.cursor()
        for name, code in zip(crawler.stock_name,crawler.stock_code):
            sql = "INSERT INTO stock_list (stock_name, stock_code) VALUES (%s, %s)"
            cursor.execute(sql, (name, code))
        con.commit()
        con.close()
    except Exception as e:
        print(e)


# 전체(5년치) 데이터 db 적재
def set_all_data(stock_code, stock_name):
    # MySQL 연결 설정
    con=connect_db()
    # 날짜 설정
    end_date = date.today()
    start_date = end_date - timedelta(days=1825)

    try:
        # 각 종목별로 데이터 다운로드 및 MySQL에 저장
        stock_data = yf.download(stock_code, start=start_date, end=end_date)

        # 테이블 생성 (이미 존재할 경우 무시)
        with con.cursor() as cursor:

            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {stock_name} (
                Date DATE PRIMARY KEY,
                Open int,
                High int,
                Low int,
                Close int,
                Adj_Close int,
                Volume INT
            );
            """

            cursor.execute(create_table_query)

        # 데이터프레임을 MySQL 테이블에 삽입
        with con.cursor() as cursor:
            truncate_table_query = f"TRUNCATE TABLE {stock_name};"
            cursor.execute(truncate_table_query)
            for index, row in stock_data.iterrows():
                sql = f"""
                INSERT INTO {stock_name} (Date, Open, High, Low, Close, Adj_Close, Volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))
        # 변경 사항 커밋
        con.commit()
        print("주식 데이터가 MySQL 데이터베이스에 저장되었습니다.")
    except Exception as e:
        print(e)
        pass
    finally:
        # 연결 종료
        con.close()

#
def return_stock_code(stock_name):

    try:
        con=connect_db()
        cursor=con.cursor()
        query = "SELECT stock_code FROM stock_list WHERE stock_name = %s"
        cursor.execute(query, (stock_name,))
        stock_code=cursor.fetchone()[0]
        con.close()
        return stock_code
    except Exception as e:
        print(e)
        pass

#10개 종목 name 반환
def return_stock_name():
    try:
        con=connect_db()
        cursor=con.cursor()
        query='select stock_name from stock_list'
        cursor.execute(query)
        stock_name_list=[]
        for i in cursor.fetchall():
            stock_name_list.append(i[0])
        con.close()
        return stock_name_list
    except Exception as e:
        print(e)
        pass

def return_graph_data(stock_name):
    try:
        con=connect_db()
        cursor=con.cursor()
        query=f'''select date,open,high,low,close from {stock_name}'''
        cursor.execute(query)
        data=cursor.fetchall()
        field=["날짜","시가","고가","저가","종가"]
        graph_data=pd.DataFrame(data=data, columns=field)
        print(graph_data)
        return graph_data
    except Exception as e:
        print(e)
        pass


#40일치 데이터 반환
def return_show_data(stock_name):
    try:
        con=connect_db()
        cursor=con.cursor()
        today=date.today()
        day=today-timedelta(40)
        today_str = today.strftime('%Y-%m-%d')
        day_str = day.strftime('%Y-%m-%d')

        # SQL 쿼리 생성
        query = f"""SELECT * FROM {stock_name} WHERE date BETWEEN '{day_str}' AND '{today_str}'ORDER BY date DESC"""
        cursor.execute(query)

        data=cursor.fetchall()
        field=["날짜", "시가", "고가","저가","종가","수정 종가","거래량"]
        show_data=pd.DataFrame(data=data,columns=field)
        return show_data
    except Exception as e:
        print(e)
        pass

def return_train_data(stock_name):
    try:
        con=connect_db()
        cursor=con.cursor()
        query=f'''select date,Close from {stock_name}'''
        cursor.execute(query)
        data=cursor.fetchall()
        field=["Date","Close"]
        train_data=pd.DataFrame(data=data,columns=field)
        con.close()
        return train_data
    except Exception as e:
        print(e)
        pass


if __name__=="__main__":
    set_stock_list()


