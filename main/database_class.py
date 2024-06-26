from session_state import get_session

# 외부 라이브러리 함수
import pymysql
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import bcrypt




# 데이터베이스 연결
def connect_db():
    host = '127.0.0.1'
    port = 3306
    username = 'root'
    password = '1234'
    database = 'stock_predict'
    # MySQL 연결
    connection = pymysql.connect(host=host,port=port,user=username,password=password,database=database)
    return connection

# 회원정보 데이터베이스 적재
def set_user_data(join_id, join_pwd, join_name):

    #회원가입시 필요한 salt 만들기
    u_salt=bcrypt.gensalt()
    pepper="HELLO"
    hash_pwd=bcrypt.hashpw((join_pwd+pepper).encode(),salt=u_salt)


    try:
        con = connect_db()
        cursor = con.cursor()
        query = '''INSERT INTO USER_DATA (U_ID, U_PWD, U_NAME, U_SALT) VALUES (%s, %s, %s, %s)'''
        cursor.execute(query, (join_id,hash_pwd , join_name, u_salt))  # 튜플 형태로 파라미터 전달
        con.commit()
        join_success = True
        return join_success
    except Exception as e:
        print(f"회원가입 에러: {e}")
        join_success = False
        return(join_success)
    finally:
        cursor.close()
        con.close()

# 전체(5년치) 데이터베이스 적재
def set_all_data(stock_code, stock_name):


    try:

        # MySQL 연결 설정
        con=connect_db()
        # 날짜 설정
        end_date = date.today()
        start_date = end_date - timedelta(days=1825)

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
        cursor.close()
        con.close()

# 로그인 데이터베이스 비교
def return_user_data(login_id, login_pwd):
    try:
        con=connect_db()
        cursor=con.cursor()
        query='''select * from user_data where u_id= %s'''
        cursor.execute(query,login_id)
        user_data=cursor.fetchall()
        u_pwd=user_data[0][1]
        u_name=user_data[0][2]


        #로그인시 입력한 pwd를 암호화 해서 db에서 추출해온 pwd와 비교
        pepper="HELLO"
        login_success = bcrypt.checkpw((login_pwd + pepper).encode(), u_pwd.encode())
        if login_success:
            session=get_session()
            session.login=True
            session.u_name=u_name

            print(session.login)
            print(session.u_name)
            return True
        else:
            pass

    except Exception as e:
        pass
    finally:
        cursor.close()
        con.close()

    return False





# 그래프 데이터베이스 가져오기
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
    finally:
        cursor.close()
        con.close()


# 40일치 데이터 반환
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
    finally:
        cursor.close()
        con.close()

# 머신러닝 데이터 반환
def return_train_data(stock_name):
    try:
        con=connect_db()
        cursor=con.cursor()
        query=f'''select date,Close from {stock_name}'''
        cursor.execute(query)
        data=cursor.fetchall()
        field=["Date","Close"]
        train_data=pd.DataFrame(data=data,columns=field)
        return train_data
    except Exception as e:
        print(e)
        pass
    finally:
        cursor.close()
        con.close()