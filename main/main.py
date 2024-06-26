# GUI 라이브러리
import streamlit as st
import database_class as db
from session_state import get_session

# 페이지 설정
st.set_page_config(page_title='Stock Analysis App', layout='wide')


# 메인 애플리케이션 함수
def main():
    st.title("주식 예측 플랫폼에 오신걸 환영합니다!")
    st.write("로그인을 진행해주세요!")
    login_container = st.container()
    with login_container:
        gap1, gap2 = st.columns([1,1])
        gap1.empty()
        gap2.empty()
        ext1, ext2, ext3 = st.columns([2,1,1])
        login = ext1
        ext2.empty()
        ext3.empty()
        with login:
            login_id = st.text_input("아이디")
            login_pwd = st.text_input("비밀번호", type='password')
            gap3, gap4 = st.columns([1,1])
            gap3.empty()
            gap4.empty()
            button = st.button("로그인")
            if button:
                login_success=db.return_user_data(login_id,login_pwd)
                if login_success:
                    session=get_session()
                    st.write(f"""{session.u_name}님 환영합니다""")
                    st.success("로그인 성공!")
                else:
                    st.error("로그인 실패. 아이디와 비밀번호를 확인하세요. 또는 회원가입을 진행해주세요")


if __name__ == "__main__":
    main()