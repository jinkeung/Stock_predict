import streamlit as st # GUI 라이브러리
# 다른 클래스를 접근하기 위함
import sub
import database_class as db
from crawling_class import stock_craw as craw

# main.py
import streamlit as st
from session_state import get_session
from sub import login_page, sign_up_page, main_page

# SessionState 로드
session_state = get_session()

def main():
    st.set_page_config(page_title='Stock Analysis App', layout='wide')
    st.sidebar.title('Navigation')

    if session_state.login:
        main_page(session_state)
    else:
        page = st.sidebar.selectbox("Choose a page", ["Login", "Sign Up"])

        if page == "Login":
            login_page(session_state)
        elif page == "Sign Up":
            sign_up_page(session_state)

if __name__ == "__main__":
    main()
