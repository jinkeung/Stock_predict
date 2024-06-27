# 외부 라이브러리
import streamlit as st

# 사용 할 세션 값 저장
class SessionState:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
        self.login = False
        self.u_name=""
        self.show_join_form = False
        self.search_button=False

# 세션 값 반환
def get_session() -> SessionState:
    global _session_state

    if "_session_state" not in st.session_state:
        st.session_state._session_state=SessionState()

    return st.session_state._session_state