# session_state.py
import streamlit as st

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.login = False  # 로그인 상태 기본값 False
        self.username = ""  # 로그인 사용자명 초기화

def get_session() -> SessionState:
    global _session_state

    if "_session_state" not in st.session_state:
        st.session_state._session_state = SessionState()

    return st.session_state._session_state
