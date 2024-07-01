import logging 

logging.basicConfig(
    # 로그 파일 이름 설정
    filename='Stock_Analysis_Log.log', 
    # 기록될 메세지 최소 수준 설정
    level=logging.DEBUG,
    # time 발생시간, name 로거 이름, level 로그 수준, message 오류 메세지
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
# 로그 인스턴스 생성
# logger = logging.getLogger(__name__)
# 로그 파일 정보
# logger.info("Streamlit 애플리케이션이 시작되었습니다.") 
# debug 수준의 로그 메세지 기록
# logger.debug(f"사용자 입력: {user_input}")
# 강제 예외 처리 발생
# raise ValueError("이것은 테스트 오류입니다.") 
# 예외 처리 발생 시 실행
# except Exception as e:
# error 수준의 로그 메세지 기록
# logger.error(f"오류 발생: {e}")
