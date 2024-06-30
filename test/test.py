import streamlit as st

# 기본 로깅 설정
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)
        
# Streamlit 애플리케이션 코드
st.title('Streamlit 애플리케이션 with 로깅')

def main():
    st.write("이것은 Streamlit 애플리케이션입니다.")
    logger.info("Streamlit 애플리케이션이 시작되었습니다.")

    user_input = st.text_input("여기에 텍스트를 입력하세요:")
    if user_input:
        st.write(f"입력한 텍스트: {user_input}")
        logger.debug(f"사용자 입력: {user_input}")

    if st.button("오류 발생시키기"):
        try:
            raise ValueError("이것은 테스트 오류입니다.")
        except Exception as e:
            logger.error(f"오류 발생: {e}")

if __name__ == '__main__':
    main()
