# 주 기능 데이터베이스 라이브러리
import pymysql

# 외부 라이브러리
import logging
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import bcrypt

import streamlit as st

from session_state import get_session

Log = logging.getLogger()

# 데이터베이스 연결
def connect_db():
    try:
        host = st.secrets["database"]["host"]
        port = st.secrets["database"]["port"]
        username = st.secrets["database"]["username"]
        password = st.secrets["database"]["password"]
        database = st.secrets["database"]["database"]
        connection = pymysql.connect(host=host,port=port,user=username,password=password,database=database)
        return connection
    except Exception as e:
        Log.error(f"데이터베이스 연결 중 예외가 발생했습니다 : {e}")



# 회원정보 데이터베이스 적재 함수
def set_user_data(join_id, join_pwd, join_name):
    u_salt = bcrypt.gensalt()
    pepper = st.secrets["database"]["pepper"]
    hash_pwd = bcrypt.hashpw((join_pwd + pepper).encode(), salt=u_salt)

    cursor = None
    con = None

    try:
        con = connect_db()
        cursor = con.cursor()
        query = '''INSERT INTO USER_DATA (U_ID, U_PWD, U_NAME, U_SALT) VALUES (%s, %s, %s, %s)'''
        cursor.execute(query, (join_id, hash_pwd, join_name, u_salt))  # 튜플 형태로 파라미터 전달
        con.commit()
        join_success = True
        return join_success
    except Exception as e:
        Log.error(f"회원가입 중 예외가 발생했습니다: {e}")
        join_success = False
        return join_success
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()




# 전체 데이터베이스 적재
def set_all_data(stock_code, stock_name):
    try:
        con=connect_db()
        end_date = date.today()
        start_date = end_date - timedelta(days=1825)

        try:
            stock_data = yf.download(stock_code, start=start_date, end=end_date)
            if stock_data.empty:
                raise ValueError("5년치 데이터가 존재하지 않습니다.")
        except Exception as e:
            Log.error(f"5년치 데이터가 없어 전체 데이터를 불러옵니다 : {e}")
            stock_data = yf.download(stock_code)

        # 테이블 생성 (이미 존재할 경우 무시)
        with con.cursor() as cursor:
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {stock_name} (
                Date DATE PRIMARY KEY, Open int, High int, Low int,
                Close int, Adj_Close int, Volume INT); """
            cursor.execute(create_table_query)

        # 데이터프레임을 MySQL 테이블에 삽입
        with con.cursor() as cursor:
            truncate_table_query = f"TRUNCATE TABLE {stock_name};"
            cursor.execute(truncate_table_query)
            for index, row in stock_data.iterrows():
                sql = f"""
                INSERT INTO {stock_name} (Date, Open, High, Low, Close, Adj_Close, Volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s) """
                cursor.execute(sql, (index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))
        con.commit()
    except Exception as e:
        Log.error(f"데이터베이스에 데이터 적재중 예외가 발생했습니다 : {e}")
        pass


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
        pepper = st.secrets["database"]["pepper"]
        login_success = bcrypt.checkpw((login_pwd + pepper).encode(), u_pwd.encode())
        if login_success:
            session=get_session()
            session.login=True
            session.u_name=u_name
            return True
        else:
            pass
    except Exception as e:
        Log.error(f"로그인 도중 예외가 발생했습니다 : {e}")
        pass

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
        return graph_data
    except Exception as e:
        Log.error(f'그래프 데이터 반환도중 예외가 발생했습니다 : {e}')
        graph_data=pd.DataFrame(None)
        return graph_data


# 40일치 데이터 반환
def return_show_data(stock_name):
    try:
        con=connect_db()
        cursor=con.cursor()
        end_date=date.today()
        start_date=end_date-timedelta(40)
        end_date = end_date.strftime('%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')
        query = f"""SELECT * FROM {stock_name} WHERE date BETWEEN '{start_date}' AND '{end_date}'ORDER BY date DESC"""
        cursor.execute(query)
        data=cursor.fetchall()
        field=["날짜", "시가", "고가","저가","종가","수정 종가","거래량"]
        show_data=pd.DataFrame(data=data,columns=field)
        return show_data
    except Exception as e:
        Log.error(f"주식 데이터 반환도중 예외가 발생했습니다 : {e}")
        pass


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

        if len(train_data)<250:
            train_data=pd.DataFrame(None)
            print(train_data.empty)
            return train_data
        return train_data
    except Exception as e:
        Log.error(f"머신러닝 데이터 반환도중 예외가 발생했습니다 : {e}")
        train_data=pd.DataFrame(None)
        pass
        return train_data

