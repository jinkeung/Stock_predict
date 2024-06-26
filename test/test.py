import streamlit as st
import mysql.connector
from mysql.connector import Error
import bcrypt
from streamlit_cookies_manager import EncryptedCookieManager

# MySQL 연결 설정
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='user_auth'
        )
    except Error as e:
        st.error(f"Error: '{e}'")
    return connection

# 사용자 등록
def register_user(username, name, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, name, email, password) VALUES (%s, %s, %s, %s)",
                   (username, name, email, hashed_password))
    connection.commit()
    cursor.close()
    connection.close()

# 사용자 인증
def authenticate_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        hashed_password = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    else:
        return False

# 쿠키 관리 설정
cookies = EncryptedCookieManager(prefix='auth')

if not cookies.ready():
    st.stop()

# 로그인 폼
def login_form():
    st.sidebar.title("로그인")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.button("Login"):
        if authenticate_user(username, password):
            cookies['logged_in'] = 'True'
            cookies['username'] = username
            st.experimental_rerun()
        else:
            st.sidebar.error("로그인 실패. 아이디와 비밀번호를 확인하세요.")

# 로그아웃 기능
def logout():
    cookies['logged_in'] = 'False'
    cookies['username'] = ''
    st.experimental_rerun()

# 회원가입 폼
def signup_form():
    st.sidebar.title("회원가입")
    username = st.sidebar.text_input("Username")
    name = st.sidebar.text_input("Name")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type='password')
    password_repeat = st.sidebar.text_input("Repeat Password", type='password')
    if st.sidebar.button("Sign Up"):
        if password == password_repeat:
            register_user(username, name, email, password)
            st.sidebar.success("회원가입이 완료되었습니다!")
        else:
            st.sidebar.error("Passwords do not match")

# 메인 애플리케이션
def main():
    st.title("Streamlit 회원가입 및 로그인 예제")

    if cookies.get('logged_in') == 'True':
        st.write(f"Welcome, {cookies.get('username')}!")
        if st.button("Logout"):
            logout()
    else:
        login_form()
        signup_form()

if __name__ == "__main__":
    main()
